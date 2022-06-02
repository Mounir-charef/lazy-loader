from flask import Flask, render_template, request, jsonify, make_response
import random
import time

app = Flask(__name__)

heading = ' This heading looks epic ya zah'
content = """
Ywdi kol ma gole rah yakhlas el khadma
yzidolna fkin smana
w ana w delali fel jbel na7o f newwwaar
"""
db = list()

posts = 50
quantity = 10

for i in range(posts):
    heading_parts = heading.split()
    random.shuffle(heading_parts)

    content_parts = content.split()
    random.shuffle(content_parts)

    db.append([i,' '.join(heading_parts),' '.join(content_parts)])

@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

@app.route('/load')
def load():
    time.sleep(0.2)
    if request.args:
        counter = int(request.args.get('c'))
        if counter == 0:
            res = make_response(jsonify(db[0:quantity]),200)
        elif counter == posts:
            res = make_response(jsonify({}),200)
        else:
            res = make_response(jsonify(db[counter:counter+quantity]),200)
    return res

if __name__ == '__main__':
    app.run(debug=True)
