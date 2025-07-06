class DrinkMenu(Menu):
    def __init__(self, name, price, quantity=1, size="Medium", alcoholic=False):
        super().__init__(name, price, quantity)
        self.size = size
        self.alcoholic = alcoholic

    def __str__(self):
        alc = "Alcoholic" if self.alcoholic else "Non-alcoholic"
        return f"{self.menu_name} ({self.size}, {alc}) x{self.quantity} - ${self.total_price():.2f}"
