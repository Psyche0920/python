import sys


def fill_in(scores: list[str]) -> list[int]:
    """Convert a list of score strings to integers,
    ignoring and reporting invalid values."""

    int_scores: list[int] = []
    for score in scores:
        try:
            int_scores.append(int(score))
        except ValueError:
            print(f"'{score}' is not a valid number")
    return int_scores


def main():
    """Process player scores and print summary statistics."""

    print("=== Player Score Analytics ===")
    scores = fill_in(sys.argv[1:])
    if not scores:
        print("No scores provided. "
              f"Usage: python3 {sys.argv[0]} <score1> <score2> ...")
        return
    print("Scores processed:", scores)
    print("Total players:", len(scores))
    print("Total score:", sum(scores))
    print(f"Average score: {sum(scores)/len(scores):.1f}")
    print("High score:", max(scores))
    print("Low score:", min(scores))
    print("Score range:", max(scores) - min(scores))


if __name__ == "__main__":
    main()
