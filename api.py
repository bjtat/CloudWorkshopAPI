import flask
from flask import jsonify
import classes.data.customers as dc
import classes.data.accounts as da
import classes.data.transactions as dt


app = flask.Flask(__name__)
app.config["DEBUG"] = True

# GET homepage
@app.route('/', methods=['GET'])
def home():
    return "<h1>Test API Home Page</h1><p>Test API.</p>"

# GET all customers
@app.route('/data/customers', methods=['GET'])
def api_customers():
    return jsonify(dc.customers)

# GET all accounts
@app.route('/data/accounts', methods=['GET'])
def api_accounts():
    return jsonify(da.accounts)

# GET all transactions
@app.route('/data/transactions', methods=['GET'])
def api_transactions():
    return jsonify(dt.transactions)


app.run()