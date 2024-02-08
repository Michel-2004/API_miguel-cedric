from flask import Flask


app = Flask(__name__)


@app.route("/")

@app.route('/venta')
def getVenta():
    return 