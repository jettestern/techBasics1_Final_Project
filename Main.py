import time
from datetime import datetime

# ---------- Klassen ----------

class Menu:
    def __init__(self, name, price, quantity=1):
        self.menu_name = name
        self.price = price
        self.quantity = quantity

    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.menu_name} x{self.quantity} - ${self.total_price():.2f}"

class FoodMenu(Menu):
    def __init__(self, name, price, quantity=1, category="General"):
        super().__init__(name, price, quantity)
        self.category = category

    def __str__(self):
        return f"{self.menu_name} ({self.category}) x{self.quantity} - ${self.total_price():.2f}"

class DrinkMenu(Menu):
    def __init__(self, name, price, size="Medium", alcoholic=False):
        super().__init__(name, price, quantity=1)
        self.size = size
        self.alcoholic = alcoholic

    def __str__(self):
        alc = "Alcoholic" if self.alcoholic else "Non-alcoholic"
        return f"{self.menu_name} ({self.size}, {alc}) - ${self.total_price():.2f}"

class DessertMenu(Menu):
    def __init__(self, name, price):
        super().__init__(name, price, quantity=1)

    def __str__(self):
        return f"{self.menu_name} - ${self.total_price():.2f}"

class ModeOfPayment:
    def __init__(self, customer_name: str, amount: float):
        self.customer_name = customer_name
        self.amount_due = round(float(amount), 2)
        self.timestamp = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S UTC")

    def get_receipt_header(self) -> str:
        return (
            "\n\n\t   Payment Receipt\n"
            " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            f" Name: {self.customer_name}\n"
            f" Total: €{self.amount_due:.2f}\n"
            f" Time: {self.timestamp}\n"
            " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        )

# ---------- Auswahlfunktion ----------

def choose_option_with_quantity(options, prompt, allow_quantity=True):
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(options):
                break
            else:
                print("Please choose a valid number.")
        except ValueError:
            print("Please enter a number.")

    selected = options[choice - 1]

    if allow_quantity:
        while True:
            try:
                quantity = int(input("Enter quantity: "))
                if quantity > 0:
                    break
                else:
                    print("Quantity must be at least 1.")
            except ValueError:
                print("Please enter a valid number.")
        selected_with_qty = type(selected)(selected.menu_name, selected.price, quantity)
        if hasattr(selected, "category"):
            selected_with_qty.category = selected.category
        return selected_with_qty
    else:
        return selected

def create_bowl(bases, proteins, toppings, drinks, desserts):
    print("\nChoose your base:")
    base = choose_option_with_quantity(bases, "Your choice: ")

    print("\nChoose your protein:")
    protein = choose_option_with_quantity(proteins, "Your choice: ")

    chosen_toppings = []
    while len(chosen_toppings) < 3:
        print(f"\nChoose topping {len(chosen_toppings)+1}:")
        available_toppings = [t for t in toppings if t.menu_name not in [ct.menu_name for ct in chosen_toppings]]
        topping = choose_option_with_quantity(available_toppings, "Your choice: ")
        chosen_toppings.append(topping)

    print("\nChoose your drink (or select 'None'):")
    drink = choose_option_with_quantity(drinks, "Your choice: ", allow_quantity=False)
    if drink.menu_name == "None":
        drink = None

    print("\nChoose your dessert (or select 'None'):")
    dessert = choose_option_with_quantity(desserts, "Your choice: ", allow_quantity=False)
    if dessert.menu_name == "None":
        dessert = None

    return {
        "base": base,
        "protein": protein,
        "toppings": chosen_toppings,
        "drink": drink,
        "dessert": dessert
    }

# ---------- Grafik ----------

def print_leaf():
    print(r"""
         _______
     .-        -.
    /            \
   |              |
   |,  .-.  .-.  ,|
   | )(_o/  \o_)( |
   |/     /\     \|
   (_     ^^     _)
    \__|IIIIII|__/
     | \IIIIII/ |
     \          /
      `--------`
    """)

def print_bowl():
    print(r"""
        .-----------------.
       /                   \
      /  🥑  🍅   🥕   🧅   \
     |   🥬   🍚   🧄   🧄    |
     |     🍗   🧄   🥦       |
      \                   /
       `-----------------'
    """)

# ---------- Main ----------

def main():
    print_leaf()
    print("Loading Green Bowls Restaurant...")
    time.sleep(1.5)
    print_bowl()
    time.sleep(1)
    print("Welcome to Green Bowls Restaurant!")
    time.sleep(0.8)
    print("Please choose the ingredients for your bowl!\n")
    time.sleep(0.5)

    bases = [
        FoodMenu("Quinoa", 3.00, category="Base"),
        FoodMenu("Rice", 2.50, category="Base"),
        FoodMenu("Leafy Greens", 2.00, category="Base")
    ]
    proteins = [
        FoodMenu("Chicken", 2.50, category="Protein"),
        FoodMenu("Tofu", 2.00, category="Protein"),
        FoodMenu("Salmon", 3.50, category="Protein")
    ]
    toppings = [
        FoodMenu("Avocado", 1.00, category="Topping"),
        FoodMenu("Chickpeas", 0.80, category="Topping"),
        FoodMenu("Nuts", 0.70, category="Topping"),
        FoodMenu("Cucumber", 0.60, category="Topping"),
        FoodMenu("Cherry Tomatoes", 0.90, category="Topping"),
        FoodMenu("Red Onion", 0.50, category="Topping"),
        FoodMenu("Carrots", 0.65, category="Topping"),
        FoodMenu("Corn", 0.75, category="Topping")
    ]
    drinks = [
        DrinkMenu("Lemonade", 3.00, size="Large", alcoholic=False),
        DrinkMenu("Beer", 4.50, size="Medium", alcoholic=True),
        DrinkMenu("Water", 1.50, size="Small", alcoholic=False),
        DrinkMenu("None", 0.00, size="-", alcoholic=False)
    ]
    desserts = [
        DessertMenu("Chocolate Cake", 4.50),
        DessertMenu("Fruit Salad", 3.00),
        DessertMenu("Ice Cream", 3.50),
        DessertMenu("None", 0.00)
    ]

    bowls = []
    while True:
        bowl = create_bowl(bases, proteins, toppings, drinks, desserts)
        bowls.append(bowl)
        more = input("\nDo you want to add another bowl? (y/n): ").strip().lower()
        if more != 'y':
            break

    print("\n--- Your full order ---")
    grand_total = 0
    for i, bowl in enumerate(bowls, start=1):
        print(f"\nBowl #{i}:")
        print(f" Base: {bowl['base']}")
        print(f" Protein: {bowl['protein']}")
        print(f" Toppings: {', '.join(str(t) for t in bowl['toppings'])}")
        if bowl["drink"]:
            print(f" Drink: {bowl['drink']}")
        if bowl["dessert"]:
            print(f" Dessert: {bowl['dessert']}")
        total = (
            bowl["base"].total_price() +
            bowl["protein"].total_price() +
            sum(t.total_price() for t in bowl["toppings"]) +
            (bowl["drink"].total_price() if bowl["drink"] else 0) +
            (bowl["dessert"].total_price() if bowl["dessert"] else 0)
        )
        print(f" Total price: ${total:.2f}")
        grand_total += total

    customer_name = input("\nPlease enter your name for the receipt: ")
    payment = ModeOfPayment(customer_name, grand_total)
    print(payment.get_receipt_header())
    print("Thank you for your order!")

# ---------- Start ----------

if __name__ == "__main__":
    main()
