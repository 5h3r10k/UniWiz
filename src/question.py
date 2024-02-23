import pandas as pd
import numpy as np
from ast import literal_eval
import openai
from openai.embeddings_utils import distances_from_embeddings

openai.api_key_path = "key.env"

embed_engine = "text-embedding-3-small"

df = pd.read_csv('processed/embeddings.csv', index_col=0)
df['embeddings'] = df['embeddings'].apply(literal_eval).apply(np.array)

def create_context(question, df, max_len=1800, size="ada"):
    q_embeddings = openai.Embedding.create(input=question, engine = embed_engine)['data'][0]['embedding']
    df['distances'] = distances_from_embeddings(q_embeddings, df['embeddings'].values, distance_metric='cosine')
    returns = []
    cur_len = 0
    for i, row in df.sort_values('distances', ascending=True).iterrows():
        cur_len += row['n_tokens'] + 4
        if cur_len > max_len:
            break
        returns.append(row["text"])
    return "\n\n###\n\n".join(returns)

def answer_question(df, model="gpt-3.5-turbo-instruct", question="Am I allowed to publish model outputs to Twitter, without a human review?", max_len=1800, size="ada", debug=False, max_tokens=150, stop_sequence=None):
    context = create_context(question, df, max_len=max_len, size=size)
    if debug:
        print("Context:\n" + context + "\n\n")
    try:
        response = openai.Completion.create(
            prompt=f"Answer the question based on the context below\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_sequence,
            model=model,
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        print(e)
        return ""

# print(answer_question(df, question="Tell me about the Intro classes in CS", debug=False))

def answer(question):
    return answer_question(df, question=question, debug=False)