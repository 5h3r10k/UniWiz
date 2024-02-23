import pandas as pd
import tiktoken
import openai
import os

openai.api_key_path = "key.env"
embed_engine = "text-embedding-3-small"

def remove_newlines(serie):
    serie = serie.str.replace('\n', ' ').str.replace('\\n', ' ').str.replace('  ', ' ').str.replace('  ', ' ')
    return serie

texts = []
for file in os.listdir("scraped/"):
    with open("scraped/" + file, "r", encoding="UTF-8") as f:
        text = f.read()
        texts.append((file[11:-4].replace('-',' ').replace('_', ' ').replace('#update',''), text))


# create processed folder if it doesn't exist
if not os.path.exists('processed'):
    os.makedirs('processed')

df = pd.DataFrame(texts, columns = ['fname', 'text'])
df['text'] = df.fname + ". " + remove_newlines(df.text)
df.to_csv('processed/scraped.csv')

tokenizer = tiktoken.get_encoding("cl100k_base")

df = pd.read_csv('processed/scraped.csv', index_col=0)
df.columns = ['title', 'text']
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

max_tokens = 500

def split_into_many(text, max_tokens = max_tokens):
    sentences = text.split('. ')
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]
    chunks = []
    tokens_so_far = 0
    chunk = []

    for sentence, token in zip(sentences, n_tokens):
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0
        if token > max_tokens:
            continue
        chunk.append(sentence)
        tokens_so_far += token + 1

    if chunk:
        chunks.append(". ".join(chunk) + ".")
    return chunks

shortened = []
for row in df.iterrows():
    if row[1]['text'] is None:
        continue
    if row[1]['n_tokens'] > max_tokens:
        shortened += split_into_many(row[1]['text'])
    else:
        shortened.append(row[1]['text'])

df = pd.DataFrame(shortened, columns = ['text'])
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))



df['embeddings'] = df.text.apply(lambda x: openai.Embedding.create(input=x, engine=embed_engine)['data'][0]['embedding'])
df.to_csv('processed/embeddings.csv')
