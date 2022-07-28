import flask
from flask import jsonify, request
import classes.data.customers as dc
import classes.data.accounts as da
import classes.data.transactions as dt
from classes.account import Account
from classes.customer import Customer
from classes.transaction import Transaction


app = flask.Flask(__name__)
app.config["DEBUG"] = True

# GET homepage
@app.route('/', methods=['GET'])
def home():
    return "<h1>Test API Home Page</h1><p>Test API.</p>"

# GET all customers
@app.route('/api/Customers/all', methods=['GET'])
def api_customers():
    return jsonify(dc.customers)

# GET all accounts
@app.route('/api/CustomerAccounts/all', methods=['GET'])
def api_accounts():
    return jsonify(da.accounts)

# GET all transactions
@app.route('/api/Transactions/all', methods=['GET'])
def api_transactions():
    return jsonify(dt.transactions)

# GET account info by ID
@app.route('/api/CustomerAccounts/GetCustomerAccountByNumber', methods=['GET'])
def api_get_account_by_number():
    query_parameters = request.args
    account_id = int(query_parameters.get('account_id'))
    status = Account.getAccountByNumber(account_id)
    if status == -1:
        return f"<h1>Error: Customer account {account_id} not found</h1>"
    else:
        return jsonify(status)

# GET customer info by ID
@app.route('/api/Customers/GetCustomerByNumber', methods=['GET'])
def api_get_customer_by_number():
    query_parameters = request.args
    customer_id = int(query_parameters.get('customer_id'))
    status = Customer.getCustomerByNumber(customer_id)
    if status == -1:
        return f"<h1>Error: Customer ID {customer_id} not found</h1>"
    else:
        return jsonify(status)

# POST new customer account
@app.route('/api/CustomerAccounts/NewCustomer', methods = ['POST'])
def api_post_new_customer():
    query_parameters = request.args
    fname = query_parameters.get('first_name')
    lname = query_parameters.get('last_name')
    accountId = query_parameters.get('accountId')
    newCustomer = Customer(fname, lname, accountId)
    dc.append(newCustomer)
    
# PUT close customer account
@app.route('/api/CustomerAccounts/CloseAccount', methods = ['POST'])
def api_close_account():
    query_parameters = request.args
    account_number = query_parameters.get('account_number')
    return Account.getAccountByNumber(account_number).closeAccount()

# POST apply transaction
@app.route('/api/CustomerAccounts/ApplyTransactionToCustomerAccountAsync', methods=['POST'])
def api_apply_transaction():
    query_parameters = request.args
    transaction_type = query_parameters.get('transaction_type')
    amount = query_parameters.get('amount')
    account_id = query_parameters.get('account_id')
    newTransaction = Transaction(transaction_type, amount, Customer.getCustomer(account_id))
    dt.append(newTransaction)
    
app.run()