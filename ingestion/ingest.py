# ingestion/ingest.py
"""
RAG INGESTION PIPELINE

This script:

1. Loads customer support dataset
2. Cleans noisy text
3. Creates structured documents
4. Splits documents into chunks
5. Converts chunks into embeddings
6. Stores embeddings in FAISS vector DB

FAISS becomes the chatbot knowledge base.
"""

import pandas as pd

from dotenv import load_dotenv

# LangChain document format
from langchain_core.documents import Document

# text chunking
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

# embedding model
from langchain_huggingface import (
    HuggingFaceEmbeddings
)

# vector database
from langchain_community.vectorstores import FAISS


# =========================================
# DATASET LOCATION
# =========================================

DATASET_PATH = (

    "hf://datasets/bitext/"
    "Bitext-customer-support-llm-chatbot-training-dataset/"
    "Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv"
)


# =========================================
# LOAD DATASET
# =========================================

def load_dataset():

    """
    Load CSV dataset using pandas.
    """

    print("\nLoading dataset...")


    df = pd.read_csv(DATASET_PATH)


    # IMPORTANT:
    # smaller dataset gives cleaner retrieval
    # enough for project demo
    df = df.head(3000)


    print(f"Dataset loaded: {len(df)} rows")


    return df


# =========================================
# CLEAN DATA
# =========================================

def clean_data(df):

    """
    Clean dataset text.
    """

    print("\nCleaning dataset...")


    # remove placeholders
    df["instruction"] = (

        df["instruction"]

        .str.replace(
            r"\{\{.*?\}\}",
            "",
            regex=True
        )

        .str.strip()
    )


    df["response"] = (

        df["response"]

        .str.replace(
            r"\{\{.*?\}\}",
            "",
            regex=True
        )

        .str.strip()
    )


    # remove null rows
    df = df.dropna(
        subset=["instruction", "response"]
    )


    # remove duplicate rows
    df = df.drop_duplicates(
        subset=["instruction", "response"]
    )


    # remove weak/broken responses
    df = df[
        df["response"].str.len() > 20
    ]


    print(f"Clean dataset rows: {len(df)}")


    return df


# =========================================
# CREATE DOCUMENTS
# =========================================

def create_documents(df):

    """
    Convert dataset rows into LangChain documents.
    """

    print("\nCreating documents...")


    documents = []


    for _, row in df.iterrows():


        # clean structured content
        content = f"""
Customer Question:
{row['instruction']}

Support Answer:
{row['response']}
"""


        # metadata helps filtering later
        metadata = {

            "category": row["category"],

            "intent": row["intent"]
        }


        # create document
        doc = Document(

            page_content=content,

            metadata=metadata
        )


        documents.append(doc)


    print(f"Documents created: {len(documents)}")


    return documents


# =========================================
# SPLIT DOCUMENTS
# =========================================

def split_documents(documents):

    """
    Split documents into smaller chunks.

    Smaller chunks improve:
    - retrieval quality
    - semantic matching
    - response cleanliness
    """

    print("\nSplitting documents...")


    text_splitter = RecursiveCharacterTextSplitter(

        # smaller chunks = cleaner retrieval
        chunk_size=300,

        # overlap preserves context
        chunk_overlap=50,

        separators=[
            "\n\n",
            "\n",
            ". ",
            " "
        ]
    )


    split_docs = text_splitter.split_documents(
        documents
    )


    print(f"Chunks created: {len(split_docs)}")


    return split_docs


# =========================================
# CREATE FAISS VECTOR DB
# =========================================

def create_faiss_index(split_docs):

    """
    Convert chunks into embeddings
    and store them in FAISS.
    """

    print("\nLoading embedding model...")


    # lightweight embedding model
    embeddings = HuggingFaceEmbeddings(

        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


    print("Creating FAISS vector database...")


    # create vector store
    vector_store = FAISS.from_documents(

        split_docs,

        embeddings
    )


    print("FAISS index created successfully")


    return vector_store


# =========================================
# SAVE VECTOR DATABASE
# =========================================

def save_faiss_index(

    vector_store,

    path="faiss_index"
):

    """
    Save FAISS vector database locally.
    """

    print(f"\nSaving FAISS index to '{path}'...")


    vector_store.save_local(path)


    print("FAISS index saved successfully")


# =========================================
# MAIN PIPELINE
# =========================================

def main():

    """
    Complete ingestion workflow.
    """

    # load environment variables
    load_dotenv()


    # step 1 → load dataset
    df = load_dataset()


    # step 2 → clean data
    df = clean_data(df)


    # step 3 → create documents
    documents = create_documents(df)


    # step 4 → split documents
    split_docs = split_documents(documents)


    # step 5 → create vector database
    vector_store = create_faiss_index(
        split_docs
    )


    # step 6 → save faiss index
    save_faiss_index(vector_store)


    print("\nIngestion completed successfully!")


# entry point
if __name__ == "__main__":

    main()