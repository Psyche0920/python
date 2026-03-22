
class GardenError(Exception):
    pass


class PlantError(GardenError):
    pass


class WaterError(GardenError):
    pass


class GardenManager:
    def __init__(self):
        self.plants = {}

    def add_plant(self, name):
        if not name:
            raise ValueError("Plant name cannot be empty!")
        self.plants[name] = {"water": 5, "sun": 8}
        return True

    def water_plants(self, plant_list):
        print("Opening watering system")
        try:
            for plant in plant_list:
                if plant in self.plants:
                    print(f"Watering {plant} - success")
                else:
                    print(f"Error: {plant} not found")
        finally:
            print("Closing watering system (cleanup)")

    def check_plant(self, name, water=None, sun=None):
        if name not in self.plants:
            return f"Error: {name} not found"
        if water is not None:
            current_water = water
        else:
            current_water = self.plants[name]["water"]
        if current_water > 10:
            raise ValueError(f"Water level {current_water} "
                             f"is too high (max 10)")
        elif current_water < 1:
            raise ValueError(f"Water level {current_water} is too low (min 1)")
        if sun is not None:
            current_sun = sun
        else:
            current_sun = self.plants[name]["sun"]
        if current_sun > 12:
            raise ValueError(f"Error: Sunlight hours {current_sun} "
                             f"is too high (max 12)")
        elif current_sun < 2:
            raise ValueError(f"Error: Sunlight hours {current_sun} "
                             f"is too low (min 2)")
        return f"{name}: healthy (water: {current_water}, sun: {current_sun})"


def main():
    print("=== Garden Management System ===\n")
    gm = GardenManager()

    print("Adding plants to garden...")
    for name in ["tomato", "lettuce", ""]:
        try:
            gm.add_plant(name)
            print(f"Added {name} successfully")
        except ValueError as e:
            print(f"Error adding plant: {e}")

    print("\nWatering plants...")
    gm.water_plants(["tomato", "lettuce"])

    print("\nChecking plant health...")
    try:
        print(gm.check_plant("tomato"))
    except Exception as e:
        print(f"Error checking tomato: {e}")
    try:
        print(gm.check_plant("lettuce", water=15))
    except ValueError as e:
        print(f"Error checking lettuce: {e}")

    print("\nTesting error recovery...")
    try:
        raise WaterError("Not enough water in tank")
    except GardenError:
        print("Caught GardenError: Not enough water in tank")
        print("System recovered and continuing...")
    print("\nGarden management system test complete!")


if __name__ == "__main__":
    main()

# Q1: except WaterError vs GardenError:
# 方案1：except WaterError: → "我只处理浇水错误", only see detailed type Watererror
# 方案2：except GardenError: → "我处理所有花园错误（包括浇水错误）", see general type Gardenerror
# except means matching or checking, print is the actual execution
