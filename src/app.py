# flask_web/app.py

from flask import Flask, jsonify
from sqlalchemy import create_engine, MetaData

app = Flask(__name__)

# 'mysql+mysqldb://root:test@db/ny_data'
user='root'
password='test'
host='db'
connection_string = f'mysql+mysqldb://{user}:{password}@{host}/ny_data'

print(connection_string)

engine = create_engine(connection_string)
metadata = MetaData(bind=engine)

print(metadata.tables.keys())

@app.route('/')
def hello_world():
    return jsonify('Hey, we have Flask in a Docker container!')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
