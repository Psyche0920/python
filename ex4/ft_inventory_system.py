def get_total_value(player: dict) -> int:
    """Calculate the total gold value of all items in a player's inventory."""

    total_value = 0
    for _, value in player["inventory"].items():
        try:
            total_value += value["quantity"] * value["value"]
        except Exception:
            continue
    return total_value


def get_item_count(player: dict) -> int:
    """Count the total number of items in a player's inventory."""

    item_cnt = 0
    for value in player["inventory"].values():
        try:
            item_cnt += value["quantity"]
        except Exception:
            continue
    return item_cnt


def inventory_report(player: dict):
    """Print a detailed report of a player's inventory
    and summary statistics."""

    print(f"=== {player['name']}'s Inventory ===")
    categories = dict()
    for key, value in player["inventory"].items():
        print(f"{key} ({value['category']}, {value['group']}): "
              f"{value['quantity']}x @ {value['value']} "
              f"gold each = {value['quantity'] * value['value']} gold")
        if value["category"] in categories:
            categories[value["category"]] += value["quantity"]
        else:
            categories[value["category"]] = value["quantity"]
    print()
    print(f"Inventory value: {get_total_value(player)} gold")
    print(f"Item count: {get_item_count(player)} items")
    categories_output = "Categories: "
    for key, value in categories.items():
        categories_output += f"{key}({value}), "
    if categories_output != "Categories: ":
        print(categories_output[:-2])


def transaction(giver: dict, recipient: dict, subject: str, quantity: int):
    """Transfer a quantity of an item
    from one player's inventory to another."""

    print(f"=== Transaction: {giver['name']} gives "
          f"{recipient['name']} {quantity} {subject}(s) ===")
    if (
        quantity > 0
        and subject in giver["inventory"]
        and giver["inventory"][subject]["quantity"] >= quantity
    ):
        giver["inventory"][subject]["quantity"] -= quantity
        if subject in recipient["inventory"]:
            recipient["inventory"][subject]["quantity"] += quantity
        else:
            recipient["inventory"][subject] = dict()
            recipient["inventory"].update(giver["inventory"][subject])
            recipient["inventory"][subject]["quantity"] = quantity
        print("Transaction successful!")
        print()
        print("=== Updated Inventories ===")
        print(f"{giver['name']} {subject} amount: "
              f"{giver['inventory'][subject]['quantity']}")
        print(f"{recipient['name']} {subject} amount: "
              f"{recipient['inventory'][subject]['quantity']}")
    else:
        print("Transaction failed. "
              "Not enough amount or wrong name of the stuff")


def report_analytics(players: list[dict]):
    """Identify and print players with the most valuable inventory
    and most items."""

    if not players:
        return
    print("=== Inventory Analytics ===")
    valuable_player = players[0]
    most_items_player = players[0]
    for player in players:
        if player is not valuable_player:
            if get_total_value(valuable_player) < get_total_value(player):
                valuable_player = player
        if player is not most_items_player:
            if get_item_count(most_items_player) < get_item_count(player):
                most_items_player = player
    print(f"Most valuable player: {valuable_player['name']} "
          f"({get_total_value(valuable_player)} gold)")
    print(f"Most items: {most_items_player['name']} "
          f"({get_item_count(most_items_player)} items)")


def main():
    """Demonstrate a simple player inventory system
    with reporting and transactions."""

    print("=== Player Inventory System ===")
    sword_dict = dict(category="weapon", group="rare", value=500, quantity=1)
    potion_dict = dict(category="consumable",
                       group="common", value=50, quantity=5)
    shield_dict = dict(category="armor", group="uncommon",
                       value=200, quantity=1)
    alice_inventory = dict(sword=sword_dict)
    alice_inventory.update(dict(potion=potion_dict))
    alice_inventory.update(dict(shield=shield_dict))
    alice = dict(name="Alice", inventory=alice_inventory)
    bob = dict(name="Bob", inventory=dict())
    print()
    inventory_report(alice)
    print()
    inventory_report(bob)
    print()
    transaction(alice, bob, "potion", 2)
    print()
    report_analytics([alice, bob])


if __name__ == "__main__":
    main()
