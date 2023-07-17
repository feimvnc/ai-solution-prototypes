from langchain.embeddings import LlamaCppEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader

embeddings = LlamaCppEmbeddings(model_path="./ggml-alpaca-7b-q4.bin", n_ctx= 2048)

from langchain.document_loaders import TextLoader
loader = TextLoader('./training.txt')
# loader = TextLoader('./training_full_clean.txt')
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000, 
    chunk_overlap = 50,
    length_function = len)
docs = text_splitter.split_documents(documents)

db = FAISS.from_documents(docs, embeddings)
db.save_local("faiss_index")

# Now let's test it out
query = "what is an four-door mid-size sedan?"
docs_q = db.similarity_search(query)
for doc in docs:
    print("docs>", doc.page_content)
