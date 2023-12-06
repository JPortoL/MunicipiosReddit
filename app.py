from flask import Flask, render_template

application = Flask(__name__)  # Cambia 'app' a 'application'

@application.route("/")
def raiz():
    return render_template("inicio.html")

if __name__ == "__main__":
    application.run(debug=False)
