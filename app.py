from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route('/')
def home():
    return "<h1>Hello I'am Krishna nayak</h1>"


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/success/<int:a>')
def success(a):
    return "The person is pass and the score is " + str(a)


@app.route('/Fail/<int:a>')
def Fail(a):
    return "The person is Fail and the score is " + str(a)


@app.route('/Welcome')
def welcome():
    return "<h1>Welcome to Flask Training class</h1>"


@app.route('/calculate', methods=['POST', 'GET'])
def calculate():

    if request.method == 'GET':
        return render_template('calculate.html')

    else:
        maths = float(request.form['maths'])
        science = float(request.form['science'])
        history = float(request.form['History'])

        avg = (maths + science + history) / 3

        if avg >= 80:
            return redirect(url_for('success', a=int(avg)))
        else:
            return redirect(url_for('Fail', a=int(avg)))


if __name__ == '__main__':
    app.run(debug=True)