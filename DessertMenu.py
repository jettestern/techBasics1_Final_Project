class DessertMenu(Menu):
    def __init__(self, name, price, quantity=1):
        super().__init__(name, price, quantity)

    def __str__(self):
        return f"{self.menu_name} x{self.quantity} - ${self.total_price():.2f}"
