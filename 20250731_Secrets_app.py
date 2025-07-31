from flask import Flask, request, jsonify, render_template
import pymysql
import boto3
import json

app = Flask(__name__)

def get_secret():
    secret_name = "prod/rds/credentials"  # あなたのSecret名
    region_name = "ap-northeast-1"  # 東京リージョンなど

    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

def get_connection():
    secret = get_secret()
    return pymysql.connect(
        host=secret['host'],
        user=secret['username'],
        password=secret['password'],
        db=secret['dbname'],
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/memos', methods=['GET'])
def get_memos():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM memos")
        memos = cursor.fetchall()
    conn.close()
    return jsonify(memos)

@app.route('/memos', methods=['POST'])
def create_memo():
    data = request.get_json()
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO memos (content) VALUES (%s)", (data['content'],))
        conn.commit()
    conn.close()
    return jsonify({'message': 'created'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
