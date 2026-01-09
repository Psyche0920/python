def main():
    """Analyze and display player achievements using set operations."""

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
    unique_achievements = alice.union(bob, charlie)
    print("All unique achievements:", unique_achievements)
    print("Total unique achievements:", len(unique_achievements))
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
    common_achievements = set.intersection(alice, bob, charlie)
    print("Common to all players:", common_achievements)
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
