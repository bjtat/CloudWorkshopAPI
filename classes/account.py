import random
import sys
sys.path.insert(0, '../data')
from data.accounts import accounts as da

class Account:

    currId = 3

    def __init__(self, balance):
        self.id = self.currId
        self.accountNumber = random.randint(3, 1000)
        self.balance = balance
        self.status = 1
        self.currId+=1

    def getAccountNumber(self):
        return self.accountNumber
    
    def getBalance(self):
        return self.balance

    def getStatus(self):
        return self.status

    def closeAccount(self):
        self.status = 0
    
    def openAccount(self):
        self.status = 1
    
    def updateBalance(self, add, amount):
        if add == 1:
            self.balance += amount
        else:
            if self.balance - amount < 0:
                print("Negative")
                return
            self.balance -= amount

    def getAccount(self, accNum):
        # assuming set of all acc is called accounts
        for i in da:
            if accNum == i['accountNumber']:
                return i['accountNumber']
            else:
                return -1 # some sort of error


acc = Account(2)
print(acc.getAccount(1))
