import pandas as pd
from datasets import load_dataset

df = pd.read_csv("hf://datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset/Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv")

print(df.shape)
print(df.columns.tolist())
print(df.head())