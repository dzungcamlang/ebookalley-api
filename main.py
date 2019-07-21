from pdfapi import *
from flask import *
#initializing flask app
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hit the /api to search for books and /download to download a book'

@app.route('/api', methods=['GET'])
def api():
    book_name = request.args.get('q')
    return jsonify(get_books_arr(book_name))


@app.route('/download', methods=['GET'])
def download():
    book_url = request.args.get('d')
    return jsonify(get_book_url(book_url))

app.run(debug=True)
