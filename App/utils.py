import os
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

# Suppress TensorFlow warnings and errors
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

def clean_up_sentence(sentence):
    ignore_symbols = ['?', '!', '.', ',']
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words if word not in ignore_symbols]
    return sentence_words

def bag_of_words(sentence):
    words = pickle.load(open('model/words.pkl', 'rb'))
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        if w in words:
            bag[words.index(w)] = 1
    return np.array(bag)

def predict_class(sentence):
    classes = pickle.load(open('model/classes.pkl', 'rb'))
    model = load_model('model/chatbot_model.keras')
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.1  # Adjusted threshold for testing
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return [{'intents': classes[r[0]], 'probability': str(r[1])} for r in results]

def get_response(intents_list):
    if not intents_list:
        return "Sorry, I didn't understand that."

    intents_json = json.load(open('model/intents.json'))
    tag = intents_list[0]['intents']
    list_of_intents = intents_json['intents']

    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    else:
        result = "Sorry, I didn't find a suitable response."

    return result