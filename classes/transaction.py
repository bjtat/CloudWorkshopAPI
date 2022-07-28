import random
from data.transactions import transactions

class Transaction: 

    def __init__(self, transaction_type, amount, account):
        self.transaction_type = transaction_type
        self.id = random.randrange(1000,5000)
        self.account_id = account.id
        self.amount = amount
        self.applyTransaction(self, account)
        transactions.append({'id': self.id,
                            'amount': self.amount,
                            'account_id': self.account_id,
                            'transaction_type': self.transaction_type})

    def applyTransaction(self, account):
        if self.transactionType == "Debit":
            account.balance -= self.amount
        else:
            account.balance += self.amount 

    