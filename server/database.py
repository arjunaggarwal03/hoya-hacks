from pymongo import MongoClient
from transformers import BertModel, BertTokenizer
import torch

model_name = 'bert-base-uncased'  # Example model; choose the one appropriate for your task
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)


conn_str = 'mongodb+srv://anshviswanathan:CjB0XfBdxJ9jL70c@admitly.emkrmyt.mongodb.net/'
client = MongoClient(conn_str)
db = client['admitly']  # Replace 'database_name' with your database name
collection = db['Pages']


documents = [
    {
        "title": "Exploring the Solar System",
        "content": "The solar system consists of the sun and the objects that orbit it...",
        "tags": ["space", "planets", "science"]
    },
    {
        "title": "The Wonders of Nature",
        "content": "Nature offers an array of beautiful landscapes and phenomena...",
        "tags": ["nature", "earth", "environment"]
    },
    {
        "title": "Advancements in Artificial Intelligence",
        "content": "AI has been making significant strides in recent years, impacting various sectors...",
        "tags": ["technology", "AI", "future"]
    },
    {
        "title": "A Guide to Healthy Eating",
        "content": "Healthy eating involves a balanced and diverse diet...",
        "tags": ["health", "food", "nutrition"]
    },
    {
        "title": "Understanding Quantum Computing",
        "content": "Quantum computing operates on the principles of quantum mechanics...",
        "tags": ["computing", "quantum", "technology"]
    }
]


# Function to get BERT embeddings
def get_bert_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    # Using the mean pool of the last layer hidden states for embedding
    embeddings = outputs.last_hidden_state.mean(1).squeeze().tolist()
    return embeddings

# Iterate over the documents and add BERT embeddings
for doc in documents:
    # Generate BERT embeddings for the content field
    doc['vectorValue'] = get_bert_embeddings(doc['content'])
    # Insert the document into the MongoDB collection
    collection.insert_one(doc)

# Close the MongoDB connection
client.close()

