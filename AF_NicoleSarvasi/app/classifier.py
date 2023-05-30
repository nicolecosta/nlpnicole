from sklearn.preprocessing import LabelEncoder
import tensorflow_hub as hub
import tensorflow as tf
from tensorflow_text import SentencepieceTokenizer
import joblib
import numpy

# Load the pre-trained model
model = joblib.load(r'C:\Users\nicol\OneDrive\Documentos\NLP\nlpnicole\AF_NicoleSarvasi\security_model.joblib')

# Create an instance of the LabelEncoder and fit it on training labels
label_encoder = LabelEncoder()
train_labels = ['malicious', 'non-malicious']
label_encoder.fit(train_labels)

# Load the Universal Sentence Encoder
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3")

def classify_prompt(prompt):
    # Preprocess the prompt and obtain the embedding
    prompt_embedding = embed(prompt).numpy()

    # Perform the classification using the loaded model
    prediction = model.predict(prompt_embedding)

    return prediction
#uvicorn main:app --reload   