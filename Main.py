def main():
    if not start_menu():
        return  # Exit if user chooses 2

    print("Loading Green Bowls Restaurant...")
    time.sleep(1.5)
    print_bowl()
    time.sleep(0.5)

    bases = [
        FoodMenu(name="Quinoa", price=3.00, category="Base"),
        FoodMenu(name="Rice", price=2.50, category="Base"),
        FoodMenu(name="Leafy Greens", price=2.00, category="Base")
    ]

    proteins = [
        FoodMenu(name="Chicken", price=2.50, category="Protein"),
        FoodMenu(name="Tofu", price=2.00, category="Protein"),
        FoodMenu(name="Salmon", price=3.50, category="Protein")
    ]

    toppings = [
        FoodMenu(name="Avocado", price=1.00, category="Topping"),
        FoodMenu(name="Chickpeas", price=0.80, category="Topping"),
        FoodMenu(name="Nuts", price=0.70, category="Topping"),
        FoodMenu(name="Cucumber", price=0.60, category="Topping"),
        FoodMenu(name="Cherry Tomatoes", price=0.90, category="Topping"),
        FoodMenu(name="Red Onion", price=0.50, category="Topping"),
        FoodMenu(name="Carrots", price=0.65, category="Topping"),
        FoodMenu(name="Corn", price=0.75, category="Topping")
    ]

    drinks = [
        DrinkMenu(name="Lemonade", price=3.00, size="Large", alcoholic=False),
        DrinkMenu(name="Beer", price=4.50, size="Medium", alcoholic=True),
        DrinkMenu(name="Water", price=1.50, size="Small", alcoholic=False),
        DrinkMenu(name="None", price=0.00, size="-", alcoholic=False)
    ]

    desserts = [
        DessertMenu(name="Chocolate Cake", price=4.50),
        DessertMenu(name="Fruit Salad", price=3.00),
        DessertMenu(name="Ice Cream", price=3.50),
        DessertMenu(name="None", price=0.00)
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

    # --- Show Pygame receipt ---
    pygame.init()
    screen = pygame.display.set_mode((400, 600))
    pygame.display.set_caption("Green Bowls Receipt")
    font = pygame.font.SysFont("Arial", 20)

    draw_receipt(screen, font, bowls, customer_name)

    # Event loop for the Pygame window
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()
