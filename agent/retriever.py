# agent/retriever.py

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# IMPORTANT:
# same embedding model used during ingestion
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# load saved FAISS vector database
vector_store = FAISS.load_local(

    "faiss_index",

    embeddings,

    allow_dangerous_deserialization=True
)


def search_documents(query: str, k: int = 3):

    """
    Search relevant documents with similarity scores.

    Returns:
    [
        {
            "content": ...,
            "metadata": ...,
            "score": ...
        }
    ]
    """

    # retrieve docs WITH similarity scores
    results = vector_store.similarity_search_with_score(
        query,
        k=k
    )


    formatted_results = []


    # format results cleanly
    for doc, score in results:

        formatted_results.append({

            "content": doc.page_content,

            "metadata": doc.metadata,

            # convert numpy float to normal float
            "score": float(score)
        })


    return formatted_results


# local testing
if __name__ == "__main__":

    query = input("Enter your question: ")


    results = search_documents(query)


    print("\n" + "=" * 50)
    print("RETRIEVED DOCUMENTS")
    print("=" * 50)


    for i, result in enumerate(results, start=1):

        print(f"\nDOCUMENT {i}")
        print("-" * 50)

        print(result["content"])

        print("\nMetadata:")
        print(result["metadata"])

        print("\nSimilarity Score:")
        print(result["score"])