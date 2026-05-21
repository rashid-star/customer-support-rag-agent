# ingestion/ingest.py

"""
RAG INGESTION PIPELINE

This script:

1. Loads customer support dataset
2. Cleans bad text
3. Creates structured documents
4. Splits documents into chunks
5. Converts text → embeddings
6. Stores embeddings in FAISS vector DB

FAISS becomes the chatbot knowledge base.
"""

import pandas as pd
import numpy as np

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
    # limit dataset during testing
    # remove later for full production
    df = df.head(5000)

    print(f"Dataset loaded: {len(df)} rows")

    return df


# =========================================
# CLEAN DATA
# =========================================

def clean_data(df):

    """
    Clean dataset text.

    Removes:
    - placeholders
    - null values
    - duplicate rows
    """

    print("\nCleaning dataset...")


    # remove placeholder patterns
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


    # remove empty rows
    df = df.dropna(
        subset=["instruction", "response"]
    )


    # remove duplicates
    df = df.drop_duplicates(
        subset=["instruction", "response"]
    )


    print(f"Clean dataset rows: {len(df)}")

    return df


# =========================================
# CREATE DOCUMENTS
# =========================================

def create_documents(df):

    """
    Convert rows into LangChain Documents.

    Documents contain:
    - content
    - metadata
    """

    print("\nCreating documents...")

    documents = []


    for _, row in df.iterrows():

        # IMPORTANT:
        # structured formatting improves retrieval
        content = f"""

Category: {row['category']}

Intent: {row['intent']}

Customer Question:
{row['instruction']}

Support Answer:
{row['response']}
"""


        # metadata helps filtering/routing later
        metadata = {

            "category": row["category"],

            "intent": row["intent"]
        }


        # create LangChain document
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
    Split large documents into smaller chunks.

    Why chunking matters:
    - improves retrieval accuracy
    - better embeddings
    - better context matching
    """

    print("\nSplitting documents...")


    # recursive splitter keeps semantic structure
    text_splitter = RecursiveCharacterTextSplitter(

        # max characters per chunk
        chunk_size=400,

        # overlap preserves context continuity
        chunk_overlap=50,

        # preferred split order
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
# CREATE EMBEDDINGS + FAISS
# =========================================

def create_faiss_index(split_docs):

    """
    Convert chunks into vector embeddings.

    Embeddings:
    text → numerical vector representation

    FAISS stores vectors for semantic search.
    """

    print("\nLoading embedding model...")


    # lightweight fast embedding model
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
    Save FAISS index locally.
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

    # load env variables
    load_dotenv()


    # step 1
    df = load_dataset()


    # step 2
    df = clean_data(df)


    # step 3
    documents = create_documents(df)


    # step 4
    split_docs = split_documents(documents)


    # step 5
    vector_store = create_faiss_index(
        split_docs
    )


    # step 6
    save_faiss_index(vector_store)


    print("\nIngestion completed successfully!")


# entry point
if __name__ == "__main__":

    main()