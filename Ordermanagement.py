class Order:
    """
    A simple class to represent a single customer order.
    """
    def __init__(self, order_id, customer_name, order_items=None):
        self.order_id = order_id
        self.customer_name = customer_name
        self.items = order_items if order_items is not None else []
        self.is_paid = False

    def add_item(self, item_name, quantity, unit_price):
        """Adds an item to the order list."""
        self.items.append({
            'name': item_name,
            'quantity': quantity,
            'price': unit_price
        })
        print(f"Added {quantity} x {item_name} to Order {self.order_id}")

    def calculate_total(self):
        """Calculates the total cost of all items in the order."""
        total = 0
        for item in self.items:
            total += item['quantity'] * item['price']
        return total

# Example usage (for demonstration, won't run when imported)
if __name__ == "__main__":
    order1 = Order(order_id="A001", customer_name="Alice Smith")

    order1.add_item("Laptop Charger", 1, 35.50)
    order1.add_item("Wireless Mouse", 2, 12.99)

    total_price = order1.calculate_total()
    print("-" * 25)
    print(f"Order ID: {order1.order_id}")
    print(f"Customer: {order1.customer_name}")
    print(f"Total Price: ${total_price:.2f}")
