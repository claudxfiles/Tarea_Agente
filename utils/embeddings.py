from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

def get_embedding(text):
    """
    Generates embedding for a given text using OpenAI API.
    """
    cleaned_text = text.replace("\n", " ")
    try:
        response = client.embeddings.create(
            input=[cleaned_text],
            model=Config.EMBEDDING_MODEL
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []
