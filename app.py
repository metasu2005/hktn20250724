from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# RDS接続設定（必要に応じて変更）
conn = pymysql.connect(
    host='your-rds-endpoint',
    user='admin',
    password='your-password',
    db='memoapp',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/memos', methods=['GET'])
def get_memos():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM memos")
        memos = cursor.fetchall()
    return jsonify(memos)

@app.route('/memos', methods=['POST'])
def create_memo():
    data = request.get_json()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO memos (content) VALUES (%s)", (data['content'],))
        conn.commit()
    return jsonify({'message': 'created'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
