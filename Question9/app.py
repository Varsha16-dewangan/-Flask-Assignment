from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {'id':1, 'title':'Book 1', 'author':"Author 1"},
    {'id':2, 'title':'Book 2', 'author':"Author 2"},
    {'id':3, 'title':'Book 3', 'author':"Author 3"},
    ]

#Get all books
@app.route('/books', methods =["GET"])
def get_books():
    return jsonify(books)


# Get a specific book
@app.route('/books/<int:book_id>', methods = ['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is not None:
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

#Create a book
@app.route('/books', methods = ['POST'])
def create_book():
    if not request.json or not 'title' in request.json or not 'author' in request.json:
        return jsonify({'error': 'bad request'}), 400
    new_book = {
        'id': books[-1]['id']+1 if books else 1,
        'title': request.json['title'],
        'author': request.json['author']
    }
    books.append(new_book)
    return jsonify(new_book), 201


#Update a book
@app.route('/books/<int:book_id>', methods = ['PUT'])
def update_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    if not request.json:
        return jsonify({'error': 'bad request'}), 400
    book['title'] = request.json['title']
    book['author'] = request.json['author']
    return jsonify(book)


#Delete a book
@app.route('/books/<int:book_id>', methods = ['DELETE'])
def delete_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    books.remove(book)
    return jsonify({'message': 'Book deleted successfully'})


if __name__ == '__main__':
    app.run(debug =True, port = 8001)
