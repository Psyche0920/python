def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda x: x["power"], reverse=True)
# key=sorting rules


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda m: m["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda s: "* " + s + " *", spells))


def mage_stats(mages: list[dict]) -> dict:
    max_power = max(mages, key=lambda m: m["power"])["power"]
    min_power = min(mages, key=lambda m: m["power"])["power"]
    avg_power = round(sum(map(lambda m: m["power"], mages)) / len(mages), 2)

    return {
        "max_power": max_power,
        "min_power": min_power,
        "avg_power": avg_power
    }


def main() -> None:
    artifacts = [
        {"name": "Fire Staff", "power": 92, "type": "staff"},
        {"name": "Crystal Orb", "power": 85, "type": "orb"}
    ]

    spells = ["fireball", "heal", "shield"]

    mages = [
        {"name": "A", "power": 10, "element": "fire"},
        {"name": "B", "power": 50, "element": "ice"},
        {"name": "C", "power": 30, "element": "wind"}
    ]
    print()
    print("Sorted artifacts:")
    print(artifact_sorter(artifacts))
    print()
    print("Filtered mages:")
    print(power_filter(mages, 20))
    print()
    print("Transformed spells:")
    print(spell_transformer(spells))
    print()
    print("Mage stats:")
    stats = mage_stats(mages)
    print({
        "max_power": stats["max_power"],
        "min_power": stats["min_power"],
        "avg_power": f"{stats['avg_power']:.2f}"
    })


if __name__ == "__main__":
    main()

# artifact = 神器
#
# 1. [map + lambda]
# 对列表中的每个元素做“转换”
# # return
# map object (iterator)
# 可以转成： list tuple set for loop
#
# 2. [for-loop fulfillment]
# def artifact_sorter(artifacts):
#     artifacts_copy = artifacts[:]
#     for i in range(len(artifacts_copy)):
#         for j in range(i + 1, len(artifacts_copy)):
#             if artifacts_copy[i]["power"] < artifacts_copy[j]["power"]:
#                 artifacts_copy[i], artifacts_copy[j] = artifacts_copy[j],
#                    artifacts_copy[i]
#     return artifacts_copy
#
#
# def power_filter(mages, min_power):
#     result = []
#     for mage in mages:
#         if mage["power"] >= min_power:
#             result.append(mage)
#     return result
#
#
# def spell_transformer(spells):
#     result = []
#     for spell in spells:
#         new_spell = "* " + spell + " *"
#         result.append(new_spell)
#     return result
#
#
# def mage_stats(mages):
#     max_power = mages[0]["power"]
#     min_power = mages[0]["power"]
#     total = 0
#     for mage in mages:
#         power = mage["power"]
#         if power > max_power:
#             max_power = power
#         if power < min_power:
#             min_power = power
#         total += power
#     avg_power = round(total / len(mages), 2)
#     return {
#         "max_power": max_power,
#         "min_power": min_power,
#         "avg_power": avg_power
#     }
#
#
# 1️⃣ How do lambda expressions make code more concise?
# Lambda expressions make code more concise
# because  define small, anonymous functions inline without using def.
# This reduces boilerplate code when the function is simple and used only once.

# 2️⃣ When should you use lambda vs regular function definitions?
# Lambda should be used for small, simple, one-line functions used only once.
# def should be used for complex logic, multiple statements, or reusable funcs
