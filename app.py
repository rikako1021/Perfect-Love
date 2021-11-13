from six import text_type
from voice2 import speek_to_text
from flask import Flask,render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import Float
from sqlalchemy.types import Integer
from sqlalchemy.types import String
from voice2 import speek_to_text
from face import Myself
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///result.db'
db = SQLAlchemy(app)

class Result(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer, primary_key = True)
    character = db.Column(db.String(10))
    point = db.Column(db.Integer)
    result_text = db.Column(db.String(100), nullable = False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        #  DB[Result]からすべての行を取り出し、それをトップページに渡す
        results = Result.query.all()
        return render_template('index.html', results = results)
    else:
        character = request.form.get('character')
        point = request.form.get('point')
        result_text = request.form.get('result_text')

        # due = datetime.strptime(due, '%Y-%m-%d')
        new_result = Result(point=point, result_text=result_text,)

        db.session.add(new_result)
        db.session.commit()
        return redirect('/')

@app.route('/select', methods=['GET'])
def select():
    return render_template('select.html')
   
# @app.route('/result/<int:id>')
# def read(id):
#     result = Result.query.get(id)
#     return render_template('result.html', result=result)

@app.route('/fem1', methods=['GET'])
def rec():
    return render_template('fem1.html')

@app.route('/recording')
def recording():
    voice = speek_to_text()
    face = Myself()
    text = voice.record()
    result = Result.query.get(voice.point())
    f_point = face.cap_face()
    return render_template('result.html', result=result, text=text, f_point=f_point)

@app.route('/result', methods=['GET'])
def result():
    return render_template('result.html')

if __name__ == "__main__":
    app.run(debug=True)
