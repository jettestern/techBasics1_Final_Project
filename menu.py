def __str__(self):
    return f"{self.menu_name} x{self.quantity} - ${self.total_price():.2f}"
