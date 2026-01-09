import sys
import math


def create_process_position(start: tuple[int, int, int]):
    """Create a fixed 3D position
    and print its distance from the given start position."""

    position = (10, 20, 5)
    print("Position created:", position)
    x1, y1, z1 = start
    x2, y2, z2 = position
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    print(f"Distance between {start} and {position}: {distance: .2f}")


def parse_process_position(start: tuple[int, int, int]):
    """Parse a 3D position from command-line input,
    compute its distance from given start, and demonstrate tuple unpacking."""

    try:
        position = sys.argv[1].split(",")
        position = (int(position[0]), int(position[1]), int(position[2]))
        print(f"Parsing coordinates: \"{sys.argv[1]}\"")
        print("Parsed position:", position)
        i = 0
        distance = 0
        while i < 3:
            distance += (position[i] - start[i]) ** 2
            i += 1
        distance = math.sqrt(distance)
        print(f"Distance between {start} and {position}: {distance: .2f}")
        print()
        demostrate_unpack(position)
    except ValueError as error:
        print(f"Parsing invalid coordinates: \"{sys.argv[1]}\"")
        print("Error parsing coordinates:", error)
        print(f"Error details - Type: {type(error).__name__}, "
              f"Args: {error.args}")
        return
    except Exception as error:
        print("Error parsing: Please check if the input is valid!\n"
              "3D position should look like \"x, y, z\"\n"
              "Error details:", error)
        return


def demostrate_unpack(position: tuple[int, int, int]):
    """Demonstrate accessing and unpacking a 3D position tuple."""

    print("Unpacking demonstration:")
    print(f"Player at x={position[0]}, y={position[1]}, z={position[2]}")
    x, y, z = position
    print(f"Coordinates: X={x}, Y={y}, Z={z}")


def main():
    """Run a demo of creating, parsing, and analyzing 3D game coordinates."""

    print("=== Game Coordinate System ===")
    print()
    start = (0, 0, 0)
    create_process_position(start)
    print()
    parse_process_position(start)


if __name__ == "__main__":
    main()
