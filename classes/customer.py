import classes.data.customers as dc

class Customer:
    curr_id = 2
    def __init__(self, first_name, last_name, account_id):
        self.id = curr_id
        self.first_name = first_name
        self.last_name = last_name
        self.account_id = account_id
        curr_id += 1

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
        

    
