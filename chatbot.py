import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Load dataset
data = pd.read_csv("faq_dataset.csv")  # query,response columns
queries = data['query'].tolist()
responses = data['response'].tolist()

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')
query_embeddings = model.encode(queries, convert_to_tensor=True)

def get_response(user_input):
    # Encode user input
    user_embedding = model.encode(user_input, convert_to_tensor=True)
    
    # Find closest match
    scores = util.cos_sim(user_embedding, query_embeddings)[0]
    best_match_idx = scores.argmax().item()
    best_score = scores[best_match_idx].item()
    
    if best_score > 0.6:  # confidence threshold
        return responses[best_match_idx]
    else:
        return "I'm not sure, let me connect you to support."
