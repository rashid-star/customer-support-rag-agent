# agent/retriever.py

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# same embedding model used during ingestion
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# load saved faiss vector database
vector_store = FAISS.load_local(

    "faiss_index",

    embeddings,

    allow_dangerous_deserialization=True
)


def clean_content(text: str):

    """
    Remove noisy dataset text.
    """

    # remove empty placeholders
    text = text.replace("{}", "")

    text = text.replace("  ", " ")

    text = text.strip()

    return text


def search_documents(query: str, k: int = 3):

    """
    Retrieve relevant documents from FAISS.
    """

    # similarity search
    results = vector_store.similarity_search_with_score(
        query,
        k=k
    )


    documents = []


    for doc, score in results:

        content = clean_content(
            doc.page_content
        )


        # skip weak retrievals
        # lower score = better match
        if score > 1.2:
            continue


        documents.append({

            "content": content,

            "metadata": doc.metadata,

            "score": float(score)
        })


    return documents


# local testing
if __name__ == "__main__":

    query = input("Enter your question: ")


    results = search_documents(query)


    print("\n" + "=" * 50)
    print("RETRIEVED DOCUMENTS")
    print("=" * 50)


    # show retrieved docs
    for i, result in enumerate(results, start=1):

        print(f"\nDOCUMENT {i}")
        print("-" * 50)

        print(result["content"])

        print("\nMetadata:")
        print(result["metadata"])

        print("\nScore:")
        print(result["score"])