```bash, a script to run RAG locally
ollama instllation is required
conda installation is required

python -V # 3.12
conda create --name ollama-embedding python=3.12
conda activate ollama-embedding
python -V #3.12
pip install langchain langchain-community langchain-core

mkdir ollama-embedding
cd ollama-embedding
touch app.py # for command line script
touch ui.py  # for ui 

ollama pull nomic-embed-text
ollama pull mistral

pip install bs4 tiktoken chromadb
pip install -U langchain-ollama
python app.py # run command line

pip install gradio
python ui.py

