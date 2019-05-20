from flask import Flask
from bracket import get_blueprint

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(get_blueprint())
    app.run()
