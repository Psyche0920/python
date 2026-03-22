def main():
    """Demonstrate comprehensions"""

    print("=== Game Analytics Dashboard ===")

    players = [
        dict(name="alice",
             score=2300,
             is_active=True,
             region="north",
             achievements={
                 'first_kill',
                 'level_10',
                 'boss_slayer',
                 'perfectionist',
                 'treasure_hunter'
             }
             ),
        dict(name="bob",
             score=1800,
             is_active=True,
             region="east",
             achievements={
                 'treasure_hunter',
                 'speed_demon',
                 'collector'
             }
             ),
        dict(name="charlie",
             score=2150,
             is_active=True,
             region="west",
             achievements={
                 'first_kill',
                 'level_10',
                 'boss_slayer',
                 'perfectionist',
                 'treasure_hunter',
                 'speed_demon',
                 'collector'
             }
             ),
        dict(name="diana",
             score=2050,
             is_active=False,
             region="south",
             achievements={
                 'first_kill',
                 'collector'
             }
             )
    ]

    print("\n=== List Comprehension Examples ===")
    high_scorers = [player["name"] for player in players
                    if player["score"] > 2000]
    print("High scorers (>2000):", high_scorers)
    scores_dbl = [player["score"] * 2 for player in players]
    print("Scores doubled:", scores_dbl)
    active_players = [player["name"]
                      for player in players if player["is_active"]]
    print("Active players:", active_players)

    print("\n=== Dict Comprehension Examples ===")
    scores = {player["name"]: player["score"] for player in players}
    print("Player scores:", scores)
    score_cats = {
        'high': sum(player["score"] >= 2000 for player in players),
        'medium': sum(2000 > player["score"] >= 1500 for player in players),
        'low': sum(player["score"] <= 1500 for player in players),
    }
    print("Score categories:", score_cats)
    ach_cnt = {player["name"]: len(player["achievements"])
               for player in players}
    print("Achievement counts:", ach_cnt)

    print("\n=== Set Comprehension Examples ===")
    uniq_players = {player["name"] for player in players}
    print("Unique players:", uniq_players)
    uniq_achs = {
        achievement for player in players
        for achievement in player["achievements"]}
    print("Unique achievements:", uniq_achs)
    act_regs = {player["region"] for player in players if player["is_active"]}
    print("Active regions:", act_regs)

    print("\n=== Combined Analysis ===")
    print("Total players:", len(uniq_players))
    print("Total unique achievements:", len(uniq_achs))
    total_scr = sum(player["score"] for player in players)
    print("Average score:", total_scr / len(uniq_players))
    top_player = next(player for player in players if player["score"] == max(
        [player["score"] for player in players]))
    print(f'Top performer: {top_player["name"]} ({top_player["score"]} points,'
          f' {len(top_player["achievements"])} achievements)')


if __name__ == "__main__":
    main()

# Q1 How do comprehensions 推导式 make complex data transformations readable?
# 声明式风格，接近自然语言; 一行代码完成复杂转换; 纯函数式特性，无副作用
# Q2 What makes them essential for data engineering workflows?
# 代码更易维护，团队协作更顺畅; 减少bug，提高开发效率减少bug，提高开发效率; 易于并行化处理，适合分布式系统
# 1.  开始
#   ↓
# 需要保持顺序吗？
#   ├── 是 → 使用列表(List)
#   │       (聊天记录、任务队列、时间序列)
#   │
#   └── 否 → 需要通过"键"快速查找吗？
#            ├── 是 → 使用字典(Dict)
#            │       (玩家属性、物品价格、配置设置)
#            │
#            └── 否 → 需要去重或集合运算吗？
#                     ├── 是 → 使用集合(Set)
#                     │       (唯一用户、标签系统、权限检查)
#                     │
#                     └── 否 → 可能还是用列表
#                             (简单数据、临时存储)
#
# 2. Python 列表、字典、集合功能对比表
# 功能/特性	列表 (List)	   字典 (Dict)	        集合 (Set)
# 核心用途	有序数据序列	 键值对映射	          唯一元素集合
# 是否有序	✅ 保持插入顺序	✅ 保持插入顺序	     ❌ 无序（不保证顺序）
# 是否可变	✅ 可修改	   ✅ 可修改	           ✅ 可修改（元素必须是不可变的）
# 允许重复	✅ 允许	       ❌ 键不允许重复	    ❌ 元素不允许重复
# 访问方式	索引（数字）	 键（任何不可变类型）	只能遍历，不能索引
# 查找速度	O(n)（慢）	    O(1)（快）	         O(1)（快）
# 内存占用	较低	        较高（存储键值对）	      中等
#
# 3. 数据分析仪表板
# ├── 列表推导式（基础筛选和转换）
# │   ├── 筛选：高分玩家 (if score > 2000)
# │   ├── 转换：分数翻倍 (score * 2)
# │   └── 筛选：活跃玩家 (if is_active)
# │
# ├── 字典推导式（数据聚合和映射）
# │   ├── 映射：玩家→分数 (name: score)
# │   ├── 聚合：分数段统计 (category: count)
# │   └── 聚合：成就数量 (name: achievement_count)
# │
# └── 集合推导式（唯一值处理）
#     ├── 去重：唯一玩家
#     ├── 展平：所有唯一成就
#     └── 筛选：活跃区域
# 1)
# max_score = max(p["score"] for p in players)
# generator = (p for p in players if p["score"] == max_score)

# top_players = []
# try:
#     while True:
#         player = next(generator)
#         top_players.append(player)
#         print(f"找到最高分玩家: {player['name']}")
# except StopIteration:
#     print(f"共找到 {len(top_players)} 个最高分玩家")
# 2)
#
# generator = (p for p in players if p["score"] == max_score
# top_players = []
# for player in generator:  # for循环自动处理StopIteration
#     top_players.append(player)
#     print(f"找到最高分玩家: {player['name']}")
# print(f"共找到 {len(top_players)} 个最高分玩家")

# 2).2for 循环的内部实现：
# for item in generator:
#     print(item)
# # 实际上是这样工作的：
# iterator = iter(generator)
# while True:
#     try:
#         item = next(iterator)  # ← 这里调用了next()
#         print(item)
#     except StopIteration:      # ← 这里捕获了StopIteration
#         break
