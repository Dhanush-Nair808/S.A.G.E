from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

vectorstore = Chroma(
    persist_directory=r"C:\Users\Dhanush Nair\OneDrive\Desktop\S.A.G.E\backend\chroma_db",
    embedding_function=embedding
        )


def retrieve_context(query, k=3):

    docs = vectorstore.similarity_search(
        query,
        k=k
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return context