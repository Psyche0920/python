import sys


def main():
    """Print the program name and list all command-line arguments
    passed to the script."""

    print("=== Command Quest ===")
    length = len(sys.argv)
    if length < 2:
        print("No arguments provided!")
        print("Program name:", sys.argv[0])
    else:
        i = 1
        print("Program name:", sys.argv[0])
        print("Arguments received:", length - 1)
        while i < length:
            print(f"Argument {i}: {sys.argv[i]}")
            i += 1
    print("Total arguments:", length)


if __name__ == "__main__":
    main()
