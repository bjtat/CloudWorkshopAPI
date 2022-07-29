import random

class Transaction: 

    def __init__(self, transaction_type, amount, account):
        self.transaction_type = transaction_type
        self.id = random.randrange(1000,5000)
        self.account_id = account.id
        self.amount = amount
        self.applyTransaction(self, account)

    def getId(self):
        return self.id

    # Apply the transaction to the account balance
    def applyTransaction(self, account):
        if self.transactionType == "Debit":
            account.balance -= self.amount
        elif self.transactionType == "Credit":
            account.balance += self.amount 

    