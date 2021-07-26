# flask_web/app.py

from flask import Flask, jsonify
from sqlalchemy import create_engine, MetaData
from flask_sqlalchemy import SQLAlchemy

from models import practice

app = Flask(__name__)

# 'mysql+mysqldb://root:test@db:3306/ny_data'
user='root'
password='root'
host='db'
connection_string = f'mysql://{user}:{password}@{host}:3306/ny_data'

app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
db = SQLAlchemy(app)
print(db)
print('db initiated')
# engine = create_engine(connection_string)
# connection = engine.connect()
# metadata = MetaData(bind=engine)
# metadata.create_all(engine)


@app.route('/')
def hello_world():
    return jsonify('Hey, we have Flask in a Docker container!')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
