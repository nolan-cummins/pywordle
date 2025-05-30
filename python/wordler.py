from flask import Flask, request, jsonify, make_response
from bs4 import BeautifulSoup
from helpers import extractWordle, extractWordly, generatePossibilites, findMatches
from urllib.parse import urlparse

# get OED-scraped dictionary with Google Ngram data
dictionary={}
all_words=[]
with open("/home/ncummins1/pycheater/dictionary.txt", "r") as file:
    for line in file:
        word, frequency = line.split(",")
        dictionary[word.lower()] = float(frequency.strip())
        all_words.append(word.lower())
all_words = set(all_words)

app = Flask(__name__)

@app.before_request
def handle_preflight():
    if request.method == 'OPTIONS':
        resp = make_response()
        resp.headers['Access-Control-Allow-Origin']  = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return resp, 200

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/save', methods=['POST'])
def save():
    # parse JSON request
    data = request.get_json(force=True)
    html = data.get('html', '')
    page_url = data.get('url', '')
    soup = BeautifulSoup(html, "html.parser")

    # extract domain
    parsed = urlparse(page_url)
    domain = parsed.netloc   # e.g. 'www.nytimes.com'
    key_states, rows = None, None

    if "nytimes" in domain:
        key_states, rows = extractWordle(soup)
    elif "wordly" in domain:
        key_states, rows = extractWordly(soup)
    if key_states is None or rows is None:
        best_matches = f"Error: Domain name {domain} not recognized!"
    elif len(key_states['absent']) == 0:
        best_matches = "roate"
    else:
        ch = generatePossibilites(key_states, rows)
        best_matches = findMatches(ch, key_states, all_words, dictionary)

    # now you have domain + letters
    result = {'best matches': best_matches}
    return jsonify(result), 200

if __name__ == '__main__':
    app.run()