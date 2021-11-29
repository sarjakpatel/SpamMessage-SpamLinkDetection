import streamlit as st
import pickle
import string
import re
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()


def Find(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
spamMessageModel = pickle.load(open('SpamMessageModel.pkl', 'rb'))

tfidf_url = pickle.load(open('vectorizer_url.pkl', 'rb'))
spamLinkModel = pickle.load(open('linkModel.pkl', 'rb'))

st.title("SMS/Link Spam Classifier")

input_sms = st.text_area("Enter the message/Link")

selectbox = st.selectbox(
    "Select any one ",
    ["Spam Messages", "Spam Link"]
)

if st.button('Predict'):

    if (selectbox == "Spam Messages"):

        transformed_sms = transform_text(input_sms)
        vector_input = tfidf.transform([transformed_sms])
        result = spamMessageModel.predict(vector_input)[0]
        if result == 1:
            st.error("This is a SPAM Message")
        else:
            st.success("This is  NOT a Spam Message")

    else:

        X_predict1 = Find(input_sms)
        X_predict1 = tfidf_url.transform(X_predict1)
        result_url = spamLinkModel.predict(X_predict1)
        if result_url[0] == "good":
            st.success("This is  NOT a Malicious URL")
        else:
            st.error("This is a Malicious URL  ")
