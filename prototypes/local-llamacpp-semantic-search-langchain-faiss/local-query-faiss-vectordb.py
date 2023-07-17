from langchain.vectorstores import FAISS
from langchain.llms import LlamaCpp
from langchain.embeddings import LlamaCppEmbeddings
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA

# Load DB from local file
embeddings = LlamaCppEmbeddings(model_path="./ggml-alpaca-7b-q4.bin")
new_db = FAISS.load_local("faiss_index", embeddings)

# Use llama-cpp as the LLM for langchain
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
llm = LlamaCpp(
    model_path="./ggml-alpaca-7b-q4.bin",
    n_ctx= 2048,
    callback_manager=callback_manager, 
    verbose=True,
    use_mlock=True
)

retriever = new_db.as_retriever()

# Conversational QA retrieval chain
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    response = qa.run(user_input)
    print(f"AI: {response}")