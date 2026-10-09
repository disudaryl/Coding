# Activity: Weather Data Excel Reader (based on weather.xlsx)
# Raw columns in the file: "Days" (Excel auto-converted these to dates, so we
# ignore the actual values and just number the days 1, 2, 3...) and
# "Temperature" (stored as text with a degree symbol, e.g. "25°").
# Menu: 1) Load  2) View (Table / Summary / Graph)  3) Exit
# Requires: pip install pandas openpyxl matplotlib

import pandas as pd
import matplotlib.pyplot as plt


class WeatherData:

    def __init__(self, filename="weather.xlsx"):
        self.filename = filename
        self.data = None

    def load_file(self):
        try:
            raw = pd.read_excel(self.filename)

            # Clean the Temperature column: remove the degree symbol and
            # convert to numbers. Any row that fails to convert (like the
            # stray "HI" row) becomes NaN and gets dropped.
            temps = raw["Temperature"].astype(str).str.replace("°", "", regex=False)
            temps = pd.to_numeric(temps, errors="coerce")

            cleaned = pd.DataFrame({"Temperature": temps}).dropna()
            cleaned["Day"] = range(1, len(cleaned) + 1)

            self.data = cleaned[["Day", "Temperature"]]
            print(f"'{self.filename}' loaded successfully! ({len(self.data)} days found)\n")
        except FileNotFoundError:
            print(f"'{self.filename}' not found. Make sure it's in the same folder as this script.\n")
        except Exception as e:
            print(f"Something went wrong while loading the file: {e}\n")

    def view_table(self):
        if self.data is None:
            print("Please load the file first (option 1).\n")
            return

        print("\n--- Weather Data ---")
        print(self.data.to_string(index=False))
        print()

    def view_summary(self):
        if self.data is None:
            print("Please load the file first (option 1).\n")
            return

        temps = self.data["Temperature"]
        hottest = self.data.loc[temps.idxmax()]
        coldest = self.data.loc[temps.idxmin()]

        print("\n--- Weather Summary ---")
        print(f"Average Temperature : {temps.mean():.2f}°C")
        print(f"Highest Temperature  : {hottest['Temperature']:.0f}°C on Day {int(hottest['Day'])}")
        print(f"Lowest Temperature   : {coldest['Temperature']:.0f}°C on Day {int(coldest['Day'])}")
        print()

    def view_graph(self):
        if self.data is None:
            print("Please load the file first (option 1).\n")
            return

        plt.figure(figsize=(10, 5))
        plt.plot(self.data["Day"], self.data["Temperature"], marker="o", color="#4C9BE8")
        plt.title("Weather Data Over Time")
        plt.xlabel("Day")
        plt.ylabel("Temperature (°C)")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()

    def show_menu(self):
        print("=== WEATHER DATA VIEWER ===")
        print("1. Load")
        print("2. View")
        print("3. Exit")


weather = WeatherData()

while True:
    weather.show_menu()
    choice = input("Select an option (1-3): ")

    if choice == "1":
        weather.load_file()

    elif choice == "2":
        print("a. View Table")
        print("b. View Summary")
        print("c. View Graph")
        sub_choice = input("Choose an option: ")

        if sub_choice == "a":
            weather.view_table()
        elif sub_choice == "b":
            weather.view_summary()
        elif sub_choice == "c":
            weather.view_graph()
        else:
            print("Invalid option.\n")

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice! Select 1 - 3 only.\n")
