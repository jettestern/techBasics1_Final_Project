class FoodMenu(Menu):
    def __init__(self, name, price, quantity=1, category="General"):
        super().__init__(name, price, quantity)
        self.category = category

    def __str__(self):
        return f"{self.menu_name} ({self.category}) x{self.quantity} - ${self.total_price():.2f}"
