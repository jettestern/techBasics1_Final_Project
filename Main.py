import time

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
    def __init__(self, name, price, quantity=1, size="Medium", alcoholic=False):
        super().__init__(name, price, quantity)
        self.size = size
        self.alcoholic = alcoholic

    def __str__(self):
        if self.menu_name.lower() == "no drink":
            return "No Drink"
        alc = "Alcoholic" if self.alcoholic else "Non-alcoholic"
        return f"{self.menu_name} ({self.size}, {alc}) - ${self.total_price():.2f}"

class DessertMenu(Menu):
    def __init__(self, name, price, quantity=1):
        super().__init__(name, price, quantity)

    def __str__(self):
        if self.menu_name.lower() == "no dessert":
            return "No Dessert"
        return f"{self.menu_name} - ${self.total_price():.2f}"

def choose_option_with_quantity(options, prompt):
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

    # For Base and Protein: ask quantity
    if isinstance(selected, FoodMenu) and selected.category in ["Base", "Protein"]:
        while True:
            try:
                quantity = int(input("Enter quantity: "))
                if quantity > 0:
                    break
                else:
                    print("Quantity must be at least 1.")
            except ValueError:
                print("Please enter a valid number.")
    else:
        quantity = 1

    selected_with_qty = type(selected)(selected.menu_name, selected.price, quantity)
    # Copy extra attributes
    for attr in ["category", "size", "alcoholic"]:
        if hasattr(selected, attr):
            setattr(selected_with_qty, attr, getattr(selected, attr))
    return selected_with_qty

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

    print("\nChoose your drink:")
    drink = choose_option_with_quantity(drinks, "Your choice: ")

    print("\nChoose your dessert:")
    dessert = choose_option_with_quantity(desserts, "Your choice: ")

    return {
        "base": base,
        "protein": protein,
        "toppings": chosen_toppings,
        "drink": drink,
        "dessert": dessert
    }

def main():
    print("Loading Green Bowls Restaurant...")
    time.sleep(1.5)
    print("Welcome to Green Bowls Restaurant!")
    time.sleep(1)
    print("Please choose the ingredients for your bowl!")
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
        DrinkMenu("No Drink", 0.00, size="None", alcoholic=False),
        DrinkMenu("Lemonade", 3.00, size="Large", alcoholic=False),
        DrinkMenu("Beer", 4.50, size="Medium", alcoholic=True),
        DrinkMenu("Water", 1.50, size="Small", alcoholic=False)
    ]
    desserts = [
        DessertMenu("No Dessert", 0.00),
        DessertMenu("Chocolate Cake", 4.50),
        DessertMenu("Fruit Salad", 3.00),
        DessertMenu("Ice Cream", 3.50)
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
        print(f" Drink: {bowl['drink']}")
        print(f" Dessert: {bowl['dessert']}")
        total = (
            bowl['base'].total_price()
            + bowl['protein'].total_price()
            + sum(t.total_price() for t in bowl['toppings'])
            + bowl['drink'].total_price()
            + bowl['dessert'].total_price()
        )
        print(f" Total price: ${total:.2f}")
        grand_total += total

    print(f"\nGrand total for all bowls: ${grand_total:.2f}")
    print("\nThank you for your order!")

if __name__ == "__main__":
    main()

