from mode_of_payment import ModeOfPayment

class CardPayment(ModeOfPayment):
    def __init__(self, customer_name: str, amount: float, card_number: str):
        super().__init__(customer_name, amount)
        self.card_number = str(card_number).strip()[-4:]

    def print_receipt(self):
        print(self.get_receipt_header())
        print(f" Paid with Card ending in ****{self.card_number}")
        print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

