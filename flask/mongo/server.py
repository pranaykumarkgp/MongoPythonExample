import time
from flask import Flask, json, request, jsonify
from flask.wrappers import Response
import pymongo

app = Flask(__name__)

mongo = pymongo.MongoClient(host = "localhost", port = 27017,
serverSelectionTimeoutMS = 1000)
db = mongo['bookDetails']
collection = db['bookDetails']
collection_logs = db['logs']

########################################
@app.route("/users", methods=["POST"])
def create_user():
    return "Hello, You are in"

########################################

@app.route("/getBooksByGrade", methods = ["GET"])
def getBooks():

    subject = request.args.get('subject')
    print(subject)
    board = request.args.get('board')
    print(board)
    grade = request.args.get('grade')
    print(grade)


    filter_query = {"book_grade" : grade}
    if subject:
        filter_query["book_subject"] = subject
    if board:
        filter_query["book_board"] = board

    b = collection.find_one()
    print(b)

    books = collection.find(filter_query).sort('book_rank')
    books_list = []

    for book in books:
        book['_id'] = str(book['_id'])
        books_list.append(book)

    return jsonify(books_list)


@app.route("/getBooksByQuery")
def findBooks():

    subject = request.args.get('subject')
    grade = request.args['grade']
    board = request.args.get('board')
    query = request.args['query']

    filter_query = {'book_name': {'$regex' : query, '$options': 'i'}}
    if subject:
        filter_query["book_subject"] = subject
    if board:
        filter_query["book_board"] = board
    if grade:
        filter_query["book_grade"] = grade

    books = collection.find(filter_query)
    books_list = []

    for book in books:
        book['_id'] = str(book['_id'])
        books_list.append(book)
    
    return jsonify(books_list)

@app.before_request
def setStartTime():
    request.startTime = time.time()

@app.after_request
def logMessage(response):
    data = {
        'timestamp': int(time.time()),
        'method': request.method,
        'path': request.path,
        'query_params': dict(request.args),
        'response_body': response.json,
        'status_code': response.status_code,
        'response_time': time.time() - request.startTime
    }

    collection_logs.insert_one(data)
    print(data)
    return response



if __name__ == "__main__":
    app.run(port=80, debug=True)




