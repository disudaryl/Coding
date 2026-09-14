"""
Coded by: Daryl Disu
          BSIT
"""

class shopping:

    def __init__(self):
        self.cart_items = []
        self.cart_prices = []
        self.tax_rate = 0.07

    def menu(self):
        print("=" * 20 + "\n" + "        MENU         " + "\n" + "=" * 20)
        print("\n1. Add Item")
        print("2. Remove Item")
        print("3. View Cart & Total")
        print("4. Exit")

    def add_item(self):
        item = input("Enter an item: ")
        price_input = input(f"Enter price for {item}: $")

        while True:
            price = float(price_input)
            try:
                if price <0:
                    print("Invalid Price")
                    price_input = input(f"Enter price for {item}: $")
                    continue
                break
            except ValueError:
                print("Invalid Price.")
                price_input = input(f"Enter price for {item}: $")           

        items = {
            "item": item,
            "price": price
        }

        self.cart_items.append(items)
        self.cart_prices.append(price)
        print("Items and price added Successfully!\n")

    def remove_item(self):
        if len(self.cart_items) == 0:
            print("No recorded items and price found!\n")
        else:
            for i, (name, price) in enumerate(self.cart_items, start=1):
                print(f"  {i}. {name} - ${price:.2f}")

        choice = input("\nEnter the number of the item to remove (or 'c' to cancel): ").strip()
        if choice.lower() == 'c':
            print("Cancelled.\n")
            return

        try:
            index = int(choice) - 1
            if 0 <= index < len(self.cart_items):
                removed_name = self.cart_items.pop(index)
                removed_price = self.cart_prices.pop(index)
                print(f"Removed '{removed_name}' - ${removed_price:.2f}\n")
            else:
                print("Invalid item number.\n")
                
        except ValueError:
            print("Invalid input.\n")


    def view_cart(self):
        if len(self.cart_items) == 0:
            print("No recorded items and price found!\n")
        else:
            print("\n" + "=" * 5 + "List of items" + "=" * 5)
            for i, entry in enumerate(self.cart_items, start=1):
                print(f"{i}. {entry['item']} - ${entry['price']:.2f}")
            print()

    def total(self):
        subtotal = sum(self.cart_prices)
        tax = subtotal * self.tax_rate
        total = subtotal + tax

        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Tax ({self.tax_rate * 100:.0f}%): ${tax:.2f}")
        print(f"Total: ${total:.2f}\n")

        return total

purchase = shopping()
while True:
    purchase.menu()
    choice = input("\nEnter your Choice: ")

    if choice == "1":
        purchase.add_item()
    elif choice == "2":
        purchase.remove_item()
    elif choice == "3":
        print("a. View Cart")
        print("b. Total")
        subchoice = input("choose an option: ")

        if subchoice == "a":
            purchase.view_cart()
        elif subchoice == "b":
            purchase.total()
        else:
            print("Invalid Choice!\n")

    elif choice == "4":
        print("Thank you for Shopping!\n")
        break
    else: 
        print("Invalid Choice!\n")
    