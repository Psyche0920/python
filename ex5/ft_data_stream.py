def get_event(count: int):
    """Generate a sequence of mock game events with player name,
    level, and event type."""

    player_names = ["Alice", "Bob", "Charlie", "Irek", "Erik"]
    event_names = ["killed monster", "found treasure",
                   "leveled up", "saved the world"]

    for i in range(count):
        yield dict(player=player_names[i % 5],
                   level=i * len(player_names[i % 5]) + 1,
                   event_name=event_names[i % 4])


def fibonacci():
    """Yield an infinite Fibonacci number sequence."""

    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def prime_num(count: int):
    """Generate the first `count` prime numbers."""

    num = 2
    i = 0
    while i < count:
        j = 2
        while j < num:
            if num % j == 0:
                num += 1
                continue
            j += 1
        yield num
        num += 1
        i += 1


def main():
    """Process streamed game events
    and demonstrate generator-based sequences."""

    print("=== Game Data Stream Processor ===")
    events_cnt = 1000
    print(f"\nProcessing {events_cnt} game events...\n")

    total_events = 0
    high_lev_players = 0
    tres_events = 0
    lv_up_events = 0

    events = get_event(events_cnt)
    for event in events:
        if event["level"] > 9:
            high_lev_players += 1
        if event["event_name"] == "found treasure":
            tres_events += 1
        elif event["event_name"] == "leveled up":
            lv_up_events += 1
        if total_events < 3:
            print(f"Event {total_events + 1}: Player {event['player']} "
                  f"(level {event['level']}) {event['event_name']}")
        total_events += 1

    print("...\n")
    print("=== Stream Analytics ===")
    print("Total events processed:", total_events)
    print("High-level players (10+):", high_lev_players)
    print("Treasure events:", tres_events)
    print("Level-up events:", lv_up_events)
    print()

    print("\n=== Generator Demonstration ===")
    fib_cnt = 10
    fib_gen = fibonacci()
    print(f"Fibonacci sequence (first {fib_cnt}):", end=" ")
    for _ in range(fib_cnt):
        print(next(fib_gen), end=" ")

    print()
    prime_cnt = 5
    print(f"Prime numbers (first {prime_cnt}):", end=" ")
    for num in prime_num(prime_cnt):
        print(num, end=" ")


if __name__ == "__main__":
    main()
