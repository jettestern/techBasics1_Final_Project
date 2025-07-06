import time
from datetime import datetime
import pygame
import sys

# ---------- Klassen ----------

class Menu:
    def __init__(self, name, price, quantity=1):
        self.menu_name = name
        self.price = price
        self.quantity = quantity

    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.menu_name} x{self.quantity} - €{self.total_price():.2f}"

class FoodMenu(Menu):
    def __init__(self, name, price, quantity=1, category="General"):
        super().__init__(name, price, quantity)
        self.category = category

    def __str__(self):
        return f"{self.menu_name} ({self.category}) x{self.quantity} - €{self.total_price():.2f}"

class DrinkMenu(Menu):
    def __init__(self, name, price, size="Medium", alcoholic=False):
        super().__init__(name, price, quantity=1)
        self.size = size
        self.alcoholic = alcoholic

    def __str__(self):
        alc = "Alcoholic" if self.alcoholic else "Non-alcoholic"
        return f"{self.menu_name} ({self.size}, {alc}) - €{self.total_price():.2f}"

class DessertMenu(Menu):
    def __init__(self, name, price):
        super().__init__(name, price, quantity=1)

    def __str__(self):
        return f"{self.menu_name} - €{self.total_price():.2f}"

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

def print_bowl():
    print(r"""
        .-----------------.
       /                   \
      /   🥗    🥕    🍅    🥒   \
     |   🥬   🍚   🧄   🧅    |
     |      🥦    🥑           |
      \                   /
       `-----------------'
    """)

# ---------- Pygame Bon-Funktion ----------

def zeichne_bon(screen, font, bowls, customer_name):
    screen.fill((255, 255, 255))
    y = 20

    title = font.render("BON - Green Bowls Restaurant", True, (0, 128, 0))
    screen.blit(title, (20, y))
    y += 40

    # Zeige Kundenname und Zeit
    zeit_text = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S UTC")
    name_text = font.render(f"Kunde: {customer_name}", True, (0, 0, 0))
    zeit_text_surface = font.render(f"Zeit: {zeit_text}", True, (0, 0, 0))
    screen.blit(name_text, (20, y))
    y += 30
    screen.blit(zeit_text_surface, (20, y))
    y += 40

    gesamt = 0
    for i, bowl in enumerate(bowls, start=1):
        header = font.render(f"Schüssel #{i}:", True, (0, 0, 0))
        screen.blit(header, (20, y))
        y += 30

        text_base = font.render(f"Base: {bowl['base'].menu_name} x{bowl['base'].quantity} - €{bowl['base'].total_price():.2f}", True, (0, 0, 0))
        screen.blit(text_base, (40, y))
        y += 25

        text_protein = font.render(f"Protein: {bowl['protein'].menu_name} x{bowl['protein'].quantity} - €{bowl['protein'].total_price():.2f}", True, (0, 0, 0))
        screen.blit(text_protein, (40, y))
        y += 25

        text_toppings = font.render("Toppings:", True, (0, 0, 0))
        screen.blit(text_toppings, (40, y))
        y += 25
        for topping in bowl["toppings"]:
            topping_text = font.render(f"{topping.menu_name} x{topping.quantity} - €{topping.total_price():.2f}", True, (0, 0, 0))
            screen.blit(topping_text, (60, y))
            y += 20

        if bowl["drink"]:
            text_drink = font.render(f"Drink: {bowl['drink'].menu_name} x{bowl['drink'].quantity} - €{bowl['drink'].total_price():.2f}", True, (0, 0, 0))
            screen.blit(text_drink, (40, y))
            y += 25

        if bowl["dessert"]:
            text_dessert = font.render(f"Dessert: {bowl['dessert'].menu_name} x{bowl['dessert'].quantity} - €{bowl['dessert'].total_price():.2f}", True, (0, 0, 0))
            screen.blit(text_dessert, (40, y))
            y += 25

        subtotal = (
            bowl["base"].total_price() +
            bowl["protein"].total_price() +
            sum(t.total_price() for t in bowl["toppings"]) +
            (bowl["drink"].total_price() if bowl["drink"] else 0) +
            (bowl["dessert"].total_price() if bowl["dessert"] else 0)
        )
        subtotal_text = font.render(f"Subtotal: €{subtotal:.2f}", True, (0, 0, 0))
        screen.blit(subtotal_text, (40, y))
        y += 30

        gesamt += subtotal

    pygame.draw.line(screen, (0, 128, 0), (20, y), (380, y), 2)
    y += 10

    total_text = font.render(f"Gesamt: €{gesamt:.2f}", True, (0, 128, 0))
    screen.blit(total_text, (20, y))

    y += 50
    info_text = font.render("Fenster schließen zum Beenden.", True, (100, 100, 100))
    screen.blit(info_text, (20, y))

    pygame.display.flip()

# ---------- Startmenü ----------

def start_menu():
    print("Willkommen bei Green Bowls Restaurant!")
    print("1. Menü starten")
    print("2. Exit")
    while True:
        choice = input("Bitte wählen Sie eine Option (1 oder 2): ").strip()
        if choice == '1':
            return True
        elif choice == '2':
            print("Programm wird beendet. Auf Wiedersehen!")
            return False
        else:
            print("Ungültige Eingabe. Bitte 1 oder 2 eingeben.")

# ---------- Main ----------

def main():
    if not start_menu():
        return  # Exit

    print("Loading Green Bowls Restaurant...")
    time.sleep(1.5)
    print_bowl()
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
        print(f" Total price: €{total:.2f}")
        grand_total += total

    customer_name = input("\nPlease enter your name for the receipt: ")
    payment = ModeOfPayment(customer_name, grand_total)
    print(payment.get_receipt_header())
    print("Thank you for your order!")

    # --- Pygame Bon anzeigen ---
    pygame.init()
    screen = pygame.display.set_mode((400, 600))
    pygame.display.set_caption("Green Bowls Bon")
    font = pygame.font.SysFont("Arial", 20)

    zeichne_bon(screen, font, bowls, customer_name)

    # Eventloop fürs Pygame-Fenster
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()

# ---------- Start ----------

if __name__ == "__main__":
    main()




