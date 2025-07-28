import gradio as gr
from langchain_community.chat_models import ChatOllama
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import CharacterTextSplitter


def process_input(urls, question):
    model_local = ChatOllama(model="mistral")

    # # 1. split data into chunks
    # urls = [
    #     "https://ollama.com",
    #     "https://ollama.com/blog/windoes-preview",
    #     "https://ollama.com/blog/openai-compatibility",
    # ]
    urls = urls.split("\n")
    print(urls)
    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=7500, chunk_overlap=100
    )
    doc_splits = text_splitter.split_documents(docs_list)

    # 2. Convert documents to embeddings and store them
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma",
        embedding=OllamaEmbeddings(model="nomic-embed-text"),
    )
    retriever = vectorstore.as_retriever()

    # # 3. Before RAG
    # print("Before RAG")
    # before_rag_template = "What is {topic}"
    # before_rag_prompt = ChatPromptTemplate.from_template(before_rag_template)
    # before_rag_chain = before_rag_prompt | model_local | StrOutputParser()
    # print(before_rag_chain.invoke({"topic": "Ollama"}))

    # 4. After RAG
    print("\n##\n After RAG")
    after_rag_template = """Answer the question based only on the following context {context}
    Question: {question}
    """
    after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
    after_rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | after_rag_prompt
        | model_local
        | StrOutputParser()
    )

    output = after_rag_chain.invoke("What is Ollama?")
    print(output)
    return output


# Define Gradio interface
iface = gr.Interface(
    fn=process_input,
    inputs=[
        gr.Textbox(label="Enter URLs separated by new lines"),
        gr.Textbox(label="Question"),
    ],
    outputs="text",
    title="Document query with RAG Ollama",
    description="Enter URLs and a question to query the document",
)
iface.launch()
