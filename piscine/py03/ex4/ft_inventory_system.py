# 1. dict.update(dict2) 执行的是合并/更新操作, dict2 会作为同级元素合并到 dict 中，而不是嵌套字典。update+{}
# 2. dict_items() 返回的是一个 视图对象，不是真正的列表：
# 3. 当 'RUNOOB' 不存在时，[tinydict.get('RUNOOB')] 返回 None
# [tinydict.get('RUNOOB', {})] - 从 tinydict 中获取键为 'RUNOOB' 的值。
# 如果这个键不存在，返回一个空字典 {}，而不是抛出 KeyError。
# 使用 .get(key, default) 的好处： 避免 KeyError 异常
# {}.get('url') 的结果是 None

def get_total_value(player: dict) -> int:
    """Calculate the total gold value of all items in a player's inventory."""
    total_value = 0
    for value in player["inventory"].values():
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
    # 检查交易条件：数量>0，物品存在，数量足够
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
            recipient["inventory"][subject].update(giver["inventory"][subject])
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

    for player in players[1:]:
        if get_total_value(valuable_player) < get_total_value(player):
            valuable_player = player
        if get_item_count(most_items_player) < get_item_count(player):
            most_items_player = player
    print(f"Most valuable player: {valuable_player['name']} "
          f"({get_total_value(valuable_player)} gold)")
    print(f"Most items: {most_items_player['name']} "
          f"({get_item_count(most_items_player)} items)")
    rarest_items = []
    highest_rarity = 0
    rarity_map = {"common": 1, "uncommon": 2, "rare": 3}

    for player in players:
        for item_name, item_info in player["inventory"].items():
            group = item_info.get("group", "common")
            rarity = rarity_map.get(group, 0)
            if rarity > highest_rarity:
                highest_rarity = rarity
                rarest_items = [item_name]
            elif rarity == highest_rarity and highest_rarity > 0:
                if item_name not in rarest_items:
                    rarest_items.append(item_name)
    if rarest_items:
        print(f"Rarest items: {', '.join(sorted(rarest_items))}")


def main():
    """Demonstrate a simple player inventory system
    with reporting and transactions."""
    print("=== Player Inventory System ===")
    sword_dict = dict(category="weapon", group="rare", value=500, quantity=1)
    potion_dict = dict(category="consumable",
                       group="common", value=50, quantity=5)
    shield_dict = dict(category="armor",
                       group="uncommon", value=200, quantity=1)
    alice_inventory = dict(sword=sword_dict)
    alice_inventory.update(dict(potion=potion_dict))
    alice_inventory.update(dict(shield=shield_dict))
    alice = dict(name="Alice", inventory=alice_inventory)
    magic_ring_dict = dict(category="accessory",
                           group="rare", value=0, quantity=1)
    bob_inventory = dict(magic_ring=magic_ring_dict)
    bob = dict(name="Bob", inventory=bob_inventory)
    print()
    inventory_report(alice)
    print()
    transaction(alice, bob, "potion", 2)
    print()
    report_analytics([alice, bob])


if __name__ == "__main__":
    main()

# Q1: 字典对游戏数据至关重要的原因：
# 快速访问：通过键立即找到数据
# 灵活结构：每个对象可以有不同属性
# 自然映射：符合游戏中的各种关系
# 易于扩展：运行时动态添加数据
# Q2: 嵌套字典建模复杂关系：
# 层次清晰：数据按逻辑分组
# 深度访问：直接访问任意层级
# 易于维护：修改不影响其他部分
# 内存高效：只存储实际需要的数据
# Q3
# 特性   	列表 (List)	 元组 (Tuple)	集合 (Set)	字典 (Dict)
# 可变性	✅ 可变	    ❌ 不可变	   ✅ 可变	  ✅ 可变
# 有序性	✅ 有序	    ✅ 有序	       ❌ 无序	   ✅ 有序(3.7+)
# 重复元素	✅ 允许	    ✅ 允许	       ❌ 不允许  	键❌不允许，值✅允许
# 语法	    []	        ()	           {}	        {key: value}
# 查找速度	O(n)	     O(n)	        O(1)	     O(1)
# 主要用途	顺序数据       固定数据	       唯一性检查    键值映射
