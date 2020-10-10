#!/usr/bin/env python
import flask
import boto3
from boto3.dynamodb.conditions import Key
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True
dynamodb = boto3.resource('dynamodb')

@app.route('/')
def hello_world():
    return 'Hello, Emma!'

@app.route('/getUser',methods=['GET'])
def get_user():
    dynamoDB = boto3.resource('dynamodb')
    user_table = dynamoDB.Table('user_data')
    print(user_table.creation_date_time)
    print(user_table.key_schema)
    # print(type(request.form['id']))
    user_data  = user_table.get_item(Key={'username': request.form['username']})
    print(type(user_data))
    user_data = user_data[u'Item']
    user_items = dict([(str(k), str(v)) for k, v in user_data.items()])
    print(user_items)
    #jsonify(user_data)
    return jsonify(user_items)

@app.route('/test',methods= ['GET'])
def test():
    return '''<h1>Cultivida</h1>
<p>Emma and Ray is going to the Seven Walls</p>'''

if __name__ == "__main__":
    app.run(host="localhost", debug=True)