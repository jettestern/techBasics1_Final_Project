from datetime import datetime

class ModeOfPayment:
    def __init__(self, customer_name:str, amount:float):
        self.customer_name = customer_name
        self.amount_due = round(float(amount), 2)
        self.timestamp = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S UTC")

    def set_customer_name(self, name:str):
        self.customer_name = name

    def set_amount(self, amount:float):
        self.amount_due = round(float(amount), 2)

    def get_receipt_header(self)-> str:
        return (
            "\n\n\t   Payment Receipt\n"
            " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            f" Name: {self.customer_name}\n"
            f" Total: €{self.amount_due:.2f}\n"
            f" Time: {self.timestamp}\n"
        )