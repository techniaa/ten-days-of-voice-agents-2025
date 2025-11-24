import json
from livekit.agents import Agent
import os

class CoffeeAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="""
            You are a friendly barista at  techniaa Coffee .
            Maintain an order object:
            {
              "drinkType": "",
              "size": "",
              "milk": "",
              "extras": [],
              "name": ""
            }
            Ask questions to fill all fields.
            Once the order is complete, save it to a JSON file.
            """
        )
        self.order = {
            "drinkType": "",
            "size": "",
            "milk": "",
            "extras": [],
            "name": ""
        }
        self.extras_collected = False

    def order_complete(self):
        return all([
            self.order["drinkType"],
            self.order["size"],
            self.order["milk"],
            self.order["name"]
        ])

    async def on_message(self, msg, ctx):
        user_input = msg.text.strip().lower()

        if not self.order['name']:
            self.order['name'] = msg.text
            await ctx.send_message(f"Hi {self.order['name']}! What drink would you like?")
            return

        if not self.order['drinkType']:
            self.order['drinkType'] = msg.text
            await ctx.send_message("What size would you like? Small, medium, or large?")
            return

        if not self.order['size']:
            self.order['size'] = msg.text
            await ctx.send_message("What milk would you like? Regular, oat, soy, almond, or none?")
            return

        if not self.order['milk']:
            self.order['milk'] = msg.text
            await ctx.send_message("Any extras? Say 'no' if none.")
            return

        # Handle extras
        if not self.extras_collected:
            if user_input != "no":
                self.order["extras"].append(msg.text)
            self.extras_collected = True
            await ctx.send_message("Anything else? Or say 'no' to finish.")
            return

        if self.order_complete():
            await self.finish_order(ctx)

    async def finish_order(self, ctx):
        summary = (
            f"Here's your order summary:\n"
            f"Name: {self.order['name']}\n"
            f"Drink: {self.order['drinkType']}\n"
            f"Size: {self.order['size']}\n"
            f"Milk: {self.order['milk']}\n"
            f"Extras: {', '.join(self.order['extras']) if self.order['extras'] else 'None'}"
        )
        await ctx.send_message(summary)

        os.makedirs("orders",exist_ok=True)
        filename = os.path.join("orders",f"{self.order['name']}_order.json")
        with open(filename, "w") as f:
            json.dump(self.order, f, indent=4)
        print(f"Order saved to {filename}:")
        print(json.dumps(self.order, indent=4))
        await ctx.send_message("Your order has been saved. Thanks for visiting  techniaa Coffee!")
