"""
StoreFlow - A simple Python "pick coach" designed for ALL retail environments.

Created for:
- Retail stores (Walmart, Target, Kroger, Publix, etc.)
- Gig shoppers (Instacart, Shipt)
- Campus stores / campus markets
- Any team that uses pick lists to gather items for customer orders

What StoreFlow does:
- Asks for a customer name and order ID.
- Walks the worker through a pick list one item at a time.
- Lets the worker pick, skip, or quit.
- Warns about overpicking to reduce mistakes.
- Tracks short items and picked quantities.
- Shows an end-of-order summary with accuracy % and coaching tips.
- Can run multiple customer orders back-to-back in one session.

StoreFlow is designed to make picking:
- Faster
- More accurate
- Easier for new employees or gig shoppers

How to run:
    python storeflow.py
"""

# ------------------------
# 1. Sample pick list (you can change this)
# ------------------------

# Each item is a dictionary with simple info.
default_pick_list = [
    {
        "sku": "1001",
        "name": "1 Gallon Milk",
        "zone": "Dairy",
        "aisle": "Aisle 1",
        "location": "Cooler 2",
        "need": 2
    },
    {
        "sku": "2005",
        "name": "Bananas (each)",
        "zone": "Produce",
        "aisle": "Aisle 3",
        "location": "Table 1",
        "need": 6
    },
    {
        "sku": "3050",
        "name": "Chips 10oz",
        "zone": "Grocery",
        "aisle": "Aisle 7",
        "location": "Middle shelf",
        "need": 3
    },
    {
        "sku": "5010",
        "name": "Coke 12-pack",
        "zone": "Beverages",
        "aisle": "Aisle 9",
        "location": "Floor",
        "need": 1
    },
    {
        "sku": "8075",
        "name": "Toothpaste 4oz",
        "zone": "Health & Beauty",
        "aisle": "Aisle 15",
        "location": "Eye level",
        "need": 2
    },
]


# ------------------------
# 2. Helper functions
# ------------------------

def show_header():
    print("=" * 55)
    print("                StoreFlow – Pick Coach")
    print("=" * 55)
    print("This tool helps you pick items for each customer order.")
    print("Type numbers only. Type 'q' to quit during picking.")
    print()


def show_item(index, item, total_items):
    """Display one item in a friendly way."""
    print("-" * 55)
    print(f"Item {index + 1} of {total_items}")
    print(f"Name:   {item['name']}")
    print(f"SKU:    {item['sku']}")
    print(f"Zone:   {item['zone']}")
    print(f"Aisle:  {item['aisle']}")
    print(f"Where:  {item['location']}")
    print(f"Need:   {item['need']} unit(s)")


def ask_quantity(needed):
    """
    Ask how many units were picked.
    Returns:
        int  - quantity picked
        None - if user types 'q' to quit
    """
    while True:
        user_input = input(f"How many did you pick (need {needed})? ")

        # quit option
        if user_input.strip().lower() == "q":
            return None

        # check if it's a number
        if not user_input.isdigit():
            print("Please enter a whole number (0, 1, 2, ...) or 'q' to quit.")
            continue

        qty = int(user_input)

        # warn if they pick more than needed
        if qty > needed:
            print("⚠ You entered more than needed.")
            print("   Usually you should NOT overpick for online orders.")
            choice = input("Use the needed amount instead? (y/n): ").strip().lower()
            if choice == "y":
                return needed
            else:
                # let them enter again
                continue

        # quantity is okay
        return qty


def show_summary(customer_name, order_id, total_items,
                 total_needed_units, total_picked_units, total_short_items):
    """Print a simple summary for one customer/order."""
    print("=" * 55)
    print("                StoreFlow Summary")
    print("=" * 55)
    print(f"Customer:         {customer_name}")
    print(f"Order ID:         {order_id}")
    print("-" * 55)
    print(f"Total items:      {total_items}")
    print(f"Total units need: {total_needed_units}")
    print(f"Total units pick: {total_picked_units}")
    print(f"Items short/skip: {total_short_items}")

    # calculate accuracy %
    if total_needed_units > 0:
        accuracy = (total_picked_units / total_needed_units) * 100
    else:
        accuracy = 0.0

    print(f"Pick accuracy:    {accuracy:.1f}% (by units)")
    print()
    print("Tips from StoreFlow:")
    if accuracy < 90:
        print("- Try to double-check the shelf and SKU before moving on.")
        print("- If it's out of stock, make sure it's marked correctly.")
    else:
        print("- Great work! Your accuracy is high. Keep it up.")

    if total_short_items > 0:
        print("- If the same items are short a lot, that location may need checking.")
    print()
    print("End of summary for this customer.")
    print("=" * 55)
    print()


# ------------------------
# 3. One picking session (one customer)
# ------------------------

def run_storeflow_for_one_customer(pick_list):
    """Run StoreFlow once for a single customer/order."""
    show_header()

    # Ask basic info about this order
    customer_name = input("Enter customer name (or nickname): ").strip()
    if customer_name == "":
        customer_name = "Unknown Customer"

    order_id = input("Enter order ID (or number): ").strip()
    if order_id == "":
        order_id = "No ID"

    print("\nStarting StoreFlow for this customer...")
    print(f"Customer: {customer_name} | Order ID: {order_id}")
    print()

    total_items = len(pick_list)
    total_needed_units = 0
    total_picked_units = 0
    total_short_items = 0

    # go through each item in the list
    for index, item in enumerate(pick_list):
        total_needed_units += item["need"]

        show_item(index, item, total_items)

        # Ask what to do with this item
        while True:
            choice = input("Choose: [1] Pick now, [2] Skip, [q] Quit: ").strip().lower()

            if choice == "q":
                print("\nYou chose to quit early for this customer.")
                print("Ending StoreFlow session for this order...\n")
                show_summary(customer_name, order_id,
                             total_items, total_needed_units,
                             total_picked_units, total_short_items)
                return  # stop this session

            if choice == "2":
                print("✔ Item skipped (handle later in your system).")
                total_short_items += 1
                break  # go to next item

            if choice == "1":
                # pick now
                qty_picked = ask_quantity(item["need"])
                if qty_picked is None:
                    # user typed q during quantity input
                    print("\nYou chose to quit early for this customer.")
                    print("Ending StoreFlow session for this order...\n")
                    show_summary(customer_name, order_id,
                                 total_items, total_needed_units,
                                 total_picked_units, total_short_items)
                    return

                total_picked_units += qty_picked

                if qty_picked < item["need"]:
                    print(f"Short pick recorded. Needed {item['need']}, picked {qty_picked}.")
                    total_short_items += 1
                else:
                    print("✔ Item completed with full quantity.")

                break  # move to next item

            print("Please choose 1, 2, or q.")

    # Finished all items
    print("\nYou reached the end of the pick list for this customer!")
    print()
    show_summary(customer_name, order_id,
                 total_items, total_needed_units,
                 total_picked_units, total_short_items)


# ------------------------
# 4. Main loop – handle multiple customers one after another
# ------------------------

def main():
    while True:
        # Run StoreFlow for one customer/order
        run_storeflow_for_one_customer(default_pick_list)

        # Ask if user wants to process another customer
        again = input("Run StoreFlow for another customer? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("\nExiting StoreFlow. Goodbye!")
            break


# ------------------------
# 5. Run the program
# ------------------------

if __name__ == "__main__":
    main()
