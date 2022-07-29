import flask
from flask import jsonify, request
import classes.data.customers as dc
import classes.data.accounts as da
import classes.data.transactions as dt
from classes.account import Account
from classes.customer import Customer
from classes.transaction import Transaction
from flask_dynamo import Dynamo
from boto3.session import Session

session = Session(
    aws_access_key_id="AKIAWLU3NUWTHCSCSZUR",
    aws_secret_access_key="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",
    region_name="us-west-1"
)

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['DYNAMO_SESSION'] = session
app.config["DYNAMO_TABLES"] = [
    {
        "TableName":'accounts',
        "KeySchema": [
            { "AttributeName": "id", "KeyType": "HASH" }
        ],
        "AttributeDefinitions": [
            { "AttributeName": "id", "AttributeType": "N" }
        ]
    }, 
    {
        "TableName":'customers',
        "KeySchema": [
            { "AttributeName": "id", "KeyType": "HASH" }
        ],
        "AttributeDefinitions": [
            { "AttributeName": "id", "AttributeType": "N" }
        ]
    }, 
    {
        "TableName":'transactions',
        "KeySchema": [
            { "AttributeName": "id", "KeyType": "HASH" }
        ],
        "AttributeDefinitions": [
            { "AttributeName": "id", "AttributeType": "N" }
        ]
    }
]

dynamo = Dynamo()
dynamo.init_app(app)

# GET homepage
@app.route('/', methods=['GET'])
def home():
    return "<h1>Test API Home Page</h1><p>Test API.</p>"

# GET all customers
@app.route('/api/Customers/all', methods=['GET'])
def api_customers():
    customers_table = dynamo.tables['customers']
    return jsonify(customers_table.scan())

# GET all accounts
@app.route('/api/CustomerAccounts/all', methods=['GET'])
def api_accounts():
    accounts_table = dynamo.tables['accounts']
    return jsonify(accounts_table.scan())

# GET all transactions
@app.route('/api/Transactions/all', methods=['GET'])
def api_transactions():
    transactions_table = dynamo.tables['transactions']
    return jsonify(transactions_table.scan())

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

# POST new customer record and new account record
@app.route('/api/Customers/NewCustomer', methods = ['POST'])
def api_post_new_customer():
    query_parameters = request.args
    fname = query_parameters.get('first_name')
    lname = query_parameters.get('last_name')
    accountId = query_parameters.get('account_id')
    newCustomer = Customer(fname, lname, accountId)
    dynamo.tables['customers'].put_item(Item={
        'id': newCustomer.getId(),
        'first_name': fname,
        'last_name': lname,
        'account_id': accountId,
    })
    return "it works!"
    
# PUT close customer account record
@app.route('/api/CustomerAccounts/CloseAccount', methods = ['PUT'])
def api_close_account():
    query_parameters = request.args
    account_number = query_parameters.get('account_number')
    return Account.getAccountByNumber(account_number).closeAccount()

# POST create transaction record and apply it to the corresponding account
@app.route('/api/CustomerAccounts/ApplyTransactionToCustomerAccountAsync', methods=['POST'])
def api_apply_transaction():
    query_parameters = request.args
    transaction_type = query_parameters.get('transaction_type')
    amount = query_parameters.get('amount')
    account_id = query_parameters.get('account_id')
    newTransaction = Transaction(transaction_type, amount, Customer.getCustomer(account_id))
    dynamo.tables['transactions'].put_item(data={
        'id': newTransaction.getId(),
        'amount': amount,
        'transaction_type': transaction_type,
        'account_id': account_id
    })
    #dt.append(newTransaction)
    
app.run()