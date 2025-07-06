from mode_of_payment import ModeOfPayment

class CashPayment(ModeOfPayment):
    def __init__(self, customer_name:str, amount:float, amount_given: float):
        super().__init__(customer_name, amount)
        self.amount_given = float(amount_given)
        self.change = round(self.amount_given - self.amount_due, 2)

    def print_receipt(self):
        print(self.get_receipt())
        print(f" Amount Given: €{self.amount_given:.2f}")
        print(f" Change: {self.change:.2f}")
        print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

