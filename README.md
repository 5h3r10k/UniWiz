# UniWiz
A chatbot which focuses on removing the stress to navigate through multiple websites and provide solutions in a more user friendly and concise format!

## Description
The project includes two key components: a web scraper and a text chunker-embedder. The scraper, implemented in scraper.py, crawls specified URLs, extracts text content from web pages, and saves the data locally. The chunker-embedder.py script processes these texts, splitting them into manageable chunks based on token count, and generates embeddings using OpenAI's API. This setup allows for efficient text extraction, processing, and embedding generation for further analysis or application.

UniWiz is a web app for Computer Science advising, built using Flask for the backend. It represents our chosen use case, leveraging processed data and AI embeddings to deliver personalized student guidance.

## Installation

A few notes before starting installation: 
- This project requires an OpenAI API key which can be obtained from the OpenAI website.
- This project uses Python 3, so please ensure you have the correct version installed. Python 2 is not supported.

1. Clone the repository:
```bash
git clone https://github.com/5h3r10k/ScarletWiz.git
```
1. Install dependencies
```bash
pip3 install -r requirements.txt
```
1. Create 'key.env' and add your OpenAI API key

## Usage
1. Start the flask server
```bash
python src/chatbot.py
```
2. Run localhost 5000
```
http://localhost:5000/
```

### Demo
[![UniWiz YouTube Demo](https://i.ibb.co/Gsx8K0d/image.png)](https://youtu.be/oEq7eAFU0JA)

## Built with
* OpenAI: API for generating text embeddings and implementing RAG (Retrieval-Augmented Generation).
* BeautifulSoup: Library for web scraping and HTML parsing.
* Pandas: Data manipulation and analysis.
* tiktoken: Tokenization library for processing text.
* Flask: Web framework for creating the backend.
* HTML/CSS: For frontend design and styling.
* Requests: For making HTTP requests.
* Python: Programming language used for the project.


## Made with ❤️ by Team Uniwiz

- [Soham](https://github.com/soham-phargade) - Flask frontend and integration with backend
- [Ishaan](https://github.com/5h3r10k) - Backend data collection and RAG implementation