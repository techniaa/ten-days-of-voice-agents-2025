import json
import os
from datetime import datetime
from typing import List, Dict, Optional

CATALOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "grocery_catalog.json")
ORDERS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "orders.json")

def load_catalog() -> List[Dict]:
    if not os.path.exists(CATALOG_PATH):
        return []
    with open(CATALOG_PATH, "r") as f:
        return json.load(f)

class GroceryCart:
    def __init__(self):
        self.items: Dict[str, Dict] = {} # item_id -> {item_details, quantity}
        self.catalog = load_catalog()

    def _find_item_by_name(self, name: str) -> Optional[Dict]:
        name_lower = name.lower()
        # Exact match first
        for item in self.catalog:
            if item["name"].lower() == name_lower:
                return item
        # Partial match
        for item in self.catalog:
            if name_lower in item["name"].lower():
                return item
        return None

    def add_item(self, name: str, quantity: int = 1) -> str:
        item = self._find_item_by_name(name)
        if not item:
            return f"Sorry, I couldn't find {name} in our catalog."

        item_id = item["id"]
        if item_id in self.items:
            self.items[item_id]["quantity"] += quantity
        else:
            self.items[item_id] = {
                "item": item,
                "quantity": quantity
            }
        return f"Added {quantity} {item['name']} to your cart."

    def remove_item(self, name: str) -> str:
        item = self._find_item_by_name(name)
        if not item:
            return f"Could not find {name} to remove."

        item_id = item["id"]
        if item_id in self.items:
            del self.items[item_id]
            return f"Removed {item['name']} from your cart."
        return f"{item['name']} is not in your cart."

    def get_cart_details(self) -> str:
        if not self.items:
            return "Your cart is empty."

        details = "Here is what you have in your cart:\n"
        total = 0.0
        for entry in self.items.values():
            item = entry["item"]
            qty = entry["quantity"]
            subtotal = item["price"] * qty
            total += subtotal
            details += f"- {qty}x {item['name']} (${subtotal:.2f})\n"

        details += f"\nTotal: ${total:.2f}"
        return details

    def get_cart_items(self) -> List[Dict]:
        return list(self.items.values())

    def get_total(self) -> float:
        total = 0.0
        for entry in self.items.values():
            total += entry["item"]["price"] * entry["quantity"]
        return total

    def clear(self):
        self.items = {}

class OrderManager:
    def __init__(self):
        self._ensure_orders_file()

    def _ensure_orders_file(self):
        if not os.path.exists(ORDERS_PATH):
            with open(ORDERS_PATH, "w") as f:
                json.dump([], f)

    def place_order(self, cart: GroceryCart) -> str:
        if not cart.items:
            return "Cannot place an empty order."

        orders = []
        try:
            with open(ORDERS_PATH, "r") as f:
                orders = json.load(f)
        except json.JSONDecodeError:
            orders = []

        new_order = {
            "order_id": f"ord_{int(datetime.now().timestamp())}",
            "timestamp": datetime.now().isoformat(),
            "status": "received",
            "items": [
                {
                    "id": entry["item"]["id"],
                    "name": entry["item"]["name"],
                    "price": entry["item"]["price"],
                    "quantity": entry["quantity"]
                }
                for entry in cart.items.values()
            ],
            "total": cart.get_total()
        }

        orders.append(new_order)

        with open(ORDERS_PATH, "w") as f:
            json.dump(orders, f, indent=2)

        cart.clear()
        return f"Order placed successfully! Your order ID is {new_order['order_id']}."

    def get_order_status(self, order_id: str = None) -> str:
        try:
            with open(ORDERS_PATH, "r") as f:
                orders = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return "No orders found."

        if not orders:
            return "No orders found."

        # If no ID provided, get the latest one
        if not order_id:
            order = orders[-1]
            return f"Your latest order ({order['order_id']}) is currently: {order['status']}."

        for order in orders:
            if order["order_id"] == order_id:
                return f"Order {order_id} is currently: {order['status']}."

        return f"Order {order_id} not found."