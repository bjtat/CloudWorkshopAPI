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
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import random
import string

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
    return jsonify({'Customers': customers_table.scan().get('Items')})

# GET all accounts
@app.route('/api/CustomerAccounts/all', methods=['GET'])
def api_accounts():
    accounts_table = dynamo.tables['accounts']
    return jsonify({'Accounts': accounts_table.scan().get('Items')})

# GET all transactions
@app.route('/api/Transactions/all', methods=['GET'])
def api_transactions():
    transactions_table = dynamo.tables['transactions']
    return jsonify({'Transactions': transactions_table.scan().get('Items')})

# GET account info by Account Number
@app.route('/api/CustomerAccounts/GetCustomerByAccountNumber', methods=['GET'])
def api_get_customer_by_account():
    query_parameters = request.args
    account_id = query_parameters.get('account_id')
    customers_table = dynamo.tables['customers']
    accounts_table = dynamo.tables['accounts']
    try:
        customer_info = customers_table.query(
            KeyConditionExpression=Key('account_id').eq(account_id)
        )
        account_info = accounts_table.query(
            KeyConditionExpression=Key('account_id').eq(account_id)
        )
    except:
        return f"Error: Customer account {account_id} not found"
    else:
        return jsonify({'Customer': customer_info.get('Items')[0]}, {'Account': account_info.get('Items')[0]})

# POST new customer record and new account record
@app.route('/api/Customers/NewCustomer', methods = ['POST'])
def api_post_new_customer():
    query_parameters = request.args
    fname = query_parameters.get('first_name')
    lname = query_parameters.get('last_name')
    balance = query_parameters.get('balance')
    res = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=7))
    try:
        dynamo.tables['customers'].put_item(Item={
            'first_name': fname,
            'last_name': lname,
            'account_id': res
        })
        dynamo.tables['accounts'].put_item(Item={
            'account_status': 1,
            'balance': balance,
            'account_id': res
        })
        return f"Successfully created customer and account entry for {fname} {lname}"
    except:
        return "Error: Could not create database entry"
        
    
# POST close customer account record
@app.route('/api/CustomerAccounts/CloseAccount', methods = ['POST'])
def api_close_account():
    query_parameters = request.args
    account_id = query_parameters.get('account_id')
    try:
            
        dynamo.tables['accounts'].update_item(
            Key = {'account_id': account_id},
            UpdateExpression = "SET account_status = :s",
            ExpressionAttributeValues = {
                ":s" : 0
            }
        )
    except:
        return f"Error: Could not access account {account_id}"
    else:
        return f"Successfully closed account {account_id}"

# POST create transaction record and apply it to the corresponding account
@app.route('/api/CustomerAccounts/ApplyTransactionToCustomerAccountAsync', methods=['POST'])
def api_apply_transaction():
    query_parameters = request.args
    transaction_type = query_parameters.get('transaction_type')
    account_id = query_parameters.get('account_id')
    amount = query_parameters.get('amount')

    try:
        assert Decimal(amount) >= 0
    except AssertionError: 
        return "Error: Transaction amount must be at least 0"

    try:
        assert transaction_type == "Debit" or transaction_type == "Credit"
    except AssertionError: 
        return "Error: Transaction type must either be 'Debit' or 'Credit' (case-sensitive)"

    query = dynamo.tables['accounts'].query(
        KeyConditionExpression=Key('account_id').eq(account_id)
    )
    balance = Decimal(query["Items"][0]["balance"])
    if transaction_type == "Debit":
        balance -= Decimal(amount)
    elif transaction_type == "Credit": 
        balance += Decimal(amount)

    try:
        assert balance >= 0
    except AssertionError:
        return "Error: Transaction denied due to balance going below 0"

    # Post transaction to transactions table
    transaction_id = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=7))
    dynamo.tables['transactions'].put_item(Item={
        'id': transaction_id,
        'amount': amount,
        'transaction_type': transaction_type,
        'account_id': account_id
    })

    # Post update to balance in accounts table
    # Return relevant information
    return (
        "Account ID: " + str(account_id) + "\nOld balance: " 
        + str(query["Items"][0]["balance"]) + "\nNew balance: " 
        + str(dynamo.tables['accounts'].update_item(
            Key = {'account_id': account_id}, 
            UpdateExpression = "SET balance = :b",
            ExpressionAttributeValues = {
                ":b" : balance
            },
            ReturnValues = "UPDATED_NEW"
        )["Attributes"]["balance"])
    )
    
app.run()