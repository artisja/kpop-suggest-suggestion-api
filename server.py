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


def convert_byte_data(user_data):
    return dict([(str(k), str(v)) for k, v in user_data.items()])


@app.route('/getUser',methods=['GET'])
def get_user():
    # dynamoDB = boto3.resource('dynamodb')
    user_table = dynamodb.Table('user_data')
    print(user_table.creation_date_time)
    print(user_table.key_schema)
    # print(type(request.form['id']))
    user_data  = user_table.get_item(Key={'username': request.form['username']})
    print(type(user_data))
    user_data = user_data[u'Item']
    user_items = convert_byte_data(user_data)
    print(user_items)
    #jsonify(user_data)
    return jsonify(user_items)

@app.route('/updateEmail',methods=['POST'])
def update_email():
    print(request.form)
    user_table = dynamodb.Table('user_data')
    print(request.form['new_email'])
    new_email= request.form['new_email']
    response = user_table.update_item(Key={
            'username': request.form['username']
        },
        UpdateExpression="set email=:e",
        ExpressionAttributeValues={
            ':e': new_email
        },
        ReturnValues="UPDATED_NEW")
    return "200"

@app.route('/updatePassword',methods=['POST'])
def update_password():
    # print(request.form)
    user_table = dynamodb.Table('user_data')
    user_data = user_table.get_item(Key={'username': request.form['username']})
    user_data = user_data[u'Item']
    user_items = convert_byte_data(user_data)
    username = request.form['username']
    old_password = request.form['current_password']
    new_password = request.form['new_password']
    print(old_password)
    if old_password != user_items['password']:
        return "500"
    print(request.form['new_password'])
    response = user_table.update_item(Key={
        'username': username
    },
        UpdateExpression="set password=:p",
        ExpressionAttributeValues={
            ':p': new_password
        },
        ReturnValues="UPDATED_NEW")
    # response
    return response

@app.route('/test',methods=['GET'])
def test():
    return '''<h1>Cultivida</h1>
<p>Emma and Ray is going to the Seven Walls</p>'''

if __name__ == "__main__":
    app.run(host="localhost", debug=True)