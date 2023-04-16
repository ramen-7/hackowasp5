from flask import Flask, request, json
import requests
from flask_cors import CORS, cross_origin
import pickle
import nltk
import string

nltk.download('stopwords')
from nltk.corpus import stopwords
import pandas as pd
from nltk.stem.porter import PorterStemmer
import re
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from sklearn.model_selection import train_test_split

vectorization = TfidfVectorizer()
# port_stem = PorterStemmer()
# vector_form = pickle.load(open('vector.pkl', 'rb'))
# load_model = pickle.load(open('model.pkl', 'rb'))

LR = joblib.load('lr.pkl')
DT = joblib.load('dt.pkl')


# GBC= joblib.load(filename)
# RFC = joblib.load(filename)
def output_lable(n):
  if n == 0:
    return "Fake News"
  elif n == 1:
    return "Not A Fake News"


def wordopt(text):
  text = text.lower()
  text = re.sub(
    '\[.*?\]', '',
    text)  # removes occurences of text such as [abc], [123], [xyz123]
  text = re.sub(
    "\\W", " ", text
  )  # replaces all non-word characters (e.g. punctuation marks, special characters)
  text = re.sub(
    'https?://\S+|www\.\S+', '', text
  )  #  will match both URLs that start with "http://" or "https://" and URLs that start with "www"
  text = re.sub(
    '<.*?>+', '',
    text)  # the regular expression pattern <.*?>+ will match all HTML tags
  text = re.sub('[%s]' % re.escape(string.punctuation), '',
                text)  # removes punctuations
  text = re.sub('\n', '', text)  # removes next line
  text = re.sub('\w*\d\w*', '', text)  # removes any string containing digits
  return text


# df = pd.read_csv("final.csv")
# x = df["text"]
# y = df["class"]
# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
# xv_train = vectorization.fit_transform(x_train)


def manual_testing(news):
  testing_news = {"text": [news]}
  new_def_test = pd.DataFrame(testing_news)
  new_def_test["text"] = new_def_test["text"].apply(wordopt)
  new_x_test = new_def_test["text"]
  new_xv_test = vectorization.transform(new_x_test)
  pred_LR = LR.predict(new_xv_test)
  pred_DT = DT.predict(new_xv_test)
  # pred_GBC = GBC.predict(new_xv_test)
  # pred_RFC = RFC.predict(new_xv_test)
  # print(f"\n\nLR Prediction: {output_lable(pred_LR[0])} \nDT Prediction{output_lable(pred_DT[0])}\nGBC Prediction:{output_lable(pred_GBC[0])} \nRFC Prediction: {output_lable(pred_RFC[0])}")
  print(pred_LR)
  print(pred_DT)


def getPred(inp):
  url = "https://discriminate.grover.allenai.org/api/disc"

  payload = {
    "article": f"{inp}",
    "domain": "",
    "date": "",
    "authors": "",
    "title": "",
    "target": "discrimination"
  }
  headers = {
    "authority": "discriminate.grover.allenai.org",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json;charset=UTF-8",
    "dnt": "1",
    "origin": "https://grover.allenai.org",
    "referer": "https://grover.allenai.org/",
  }

  response = requests.request("POST", url, json=payload, headers=headers)

  return response.json()


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def index():
  return 'Hello from Flask!'


@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
  data = request.get_data(as_text=True)
  # # output = model.predict([input_string])[0]
  # # return output
  output = getPred(data)
  # manual_testing(data)
  final = {'value': float(output['groverprob']), 'value2': float(1)}
  return json.dumps(final, indent=1)

  # Do something with the string data

  # return "Received string data: " + data


app.run(host='0.0.0.0', port=81)
