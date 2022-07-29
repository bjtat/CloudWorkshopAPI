import classes.data.customers as dc
import random

class Customer:
    def __init__(self, first_name, last_name, account_id):
        self.id = random.randrange(1000,5000)
        self.first_name = first_name
        self.last_name = last_name
        self.account_id = account_id

    def getId(self):
        return self.id

    def getName(self):
        return (self.first_name + " " + self.last_name)

    def getAccountId(self):
        return self.account_id

    @staticmethod
    def getCustomerByNumber(customer_id):
        # assuming set of all acc is called accounts
        for i in dc.customers:
            if customer_id == i['id']:
                return i
        return -1
        

    
