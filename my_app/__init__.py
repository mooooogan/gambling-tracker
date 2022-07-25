from flask import Flask
from contextlib import closing

app = Flask(__name__)
app.config["SECRET_KEY"] = "f030eb082a15a4b232347ac4"

from my_app import routes
