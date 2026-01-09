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
    high_scorers = [player["name"] for player in players if player["score"] > 2000]
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
