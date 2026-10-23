from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index1.html")


@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    result = ""

    if request.method == "POST":
        a = float(request.form["a"])
        b = float(request.form["b"])
        operation = request.form["operation"]

        if operation == "+":
            result = a + b
        elif operation == "-":
            result = a - b
        elif operation == "*":
            result = a * b
        elif operation == "/":
            if b != 0:
                result = a / b
            else:
                result = "Cannot divide by zero"

    return render_template("calculator.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)