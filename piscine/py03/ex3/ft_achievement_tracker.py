def main():
    """Analyze and display player achievements using set operations."""
# 创建三个玩家的成就集合
    print("=== Achievement Tracker System ===")
    alice = {'first_kill', 'level_10', 'treasure_hunter', 'speed_demon'}
    bob = {'first_kill', 'level_10', 'boss_slayer', 'collector'}
    charlie = {'level_10', 'treasure_hunter',
               'boss_slayer', 'speed_demon', 'perfectionist'}
    print()
    print(f"Player Alice achievements: {alice}")
    print(f"Player Bob achievements: {bob}")
    print(f"Player Charlie achievements: {charlie}")
    print()

    print("=== Achievement Analytics ===")
    # 获取所有独特成就（并集操作）
    unique_achievements = alice.union(bob, charlie)
    print("All unique achievements:", unique_achievements)
    print("Total unique achievements:", len(unique_achievements))
    # 找出每个玩家缺少的成就
    alice_lack = unique_achievements.difference(alice)
    if alice_lack:
        print("Alice is missing following achievements", alice_lack)
    bob_lack = unique_achievements.difference(bob)
    if bob_lack:
        print("Bob is missing following achievements", bob_lack)
    charlie_lack = unique_achievements.difference(charlie)
    if charlie_lack:
        print("Charlie is missing following achievements", charlie_lack)
    print()
    # 所有玩家共同的成就（交集操作）
    common_achievements = set.intersection(alice, bob, charlie)
    print("Common to all players:", common_achievements)
    # 稀有成就（只有一个玩家拥有的）&&合并所有稀有成就
    rare_achievements = alice.difference(bob.union(charlie))
    rare_achievements = rare_achievements.union(
        bob.difference(alice.union(charlie)))
    rare_achievements = rare_achievements.union(
        charlie.difference(alice.union(bob)))
    print("Rare achievements (1 player):", rare_achievements)
    print()

    print("Players with the same achievement:")
    for achievement in unique_achievements:
        achievement_holders = set()
        if achievement in alice:
            achievement_holders = achievement_holders.union(set(["Alice"]))
        if achievement in bob:
            achievement_holders = achievement_holders.union(set(["Bob"]))
        if achievement in charlie:
            achievement_holders = achievement_holders.union(set(["Charlie"]))
        if len(achievement_holders) > 1:
            print(f"'{achievement}' community: {achievement_holders}")
    print()
    print("Alice vs Bob common:", alice.intersection(bob))
    print("Alice unique:", alice.difference(bob))
    print("Bob unique:", bob.difference(alice))


if __name__ == "__main__":
    main()

# 1. set {}
# 集合的特性
# 无序：没有索引，不能通过位置访问
# !!!唯一：自动去除重复元素
# 可变：可以添加/删除元素（但在这个练习中不需要）
# 让去重简单：因为设计就是"唯一元素的集合"。
# 集合操作完美用于分析：因为数据分析的本质就是集合运算（找共同、找不同、合并数据）。
# 一句话：集合的数学特性正好匹配数据分析的需求，性能又好。
# 2.
# s.union(other)           # 并集
# s.intersection(other)    # 交集
# s.difference(other)      # 差集 返回集合s有但集合other没有的元素
# 3.
# union vs add union() 不修改原集合，更安全; 项目限制
# 4.
# 你的观察完全正确：set(["Alice"]) 中的列表包装确实you必要
# union() 接受的是"可迭代对象":  # 列表, 元组, 字符串, 集合...
#  finally incorporated as element in set
# set("Alice")   # 把字符串拆成字符：{'A', 'l', 'i', 'c', 'e'}
# set(["Alice"]) # 列表中的元素：{'Alice'}
# achievement_holders.union({"Alice"})
