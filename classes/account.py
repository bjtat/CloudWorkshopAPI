import random
# import data.accounts as da
import classes.data.accounts as da
class Account:

    currId = 3

    def __init__(self, balance, accountnum):
        self.id = self.currId
        self.accountNumber = accountnum
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


# acc = Account(2)
# print(acc.getAccountByNumber(1))
