import pandas as pd
import matplotlib.pyplot as plt


class WeatherForecast:

    def __init__(self, filename="weather.xlsx"):
        self.filename = filename
        self.data = None

    def load_file(self):
        try:
            self.data = pd.read_excel(self.filename)
            self.data["Date"] = pd.to_datetime(self.data["Date"])
            print(f"'{self.filename}' loaded successfully! ({len(self.data)} days found)\n")
        except FileNotFoundError:
            print(f"'{self.filename}' not found. Make sure it's in the same folder as this script.\n")
        except Exception as e:
            print(f"Something went wrong while loading the file: {e}\n")

    def view_table(self):
        if self.data is None:
            print("Please load the file first (option 1).\n")
            return

        print("\n--- 30-Day Weather Forecast ---")
        sorted_data = self.data.sort_values("Date")
        printable = sorted_data.copy()
        printable["Date"] = printable["Date"].dt.strftime("%Y-%m-%d")
        print(printable[["Date", "Temperature"]].to_string(index=False))
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
        print(f"Highest Temperature  : {hottest['Temperature']}°C on {hottest['Date'].strftime('%Y-%m-%d')}")
        print(f"Lowest Temperature   : {coldest['Temperature']}°C on {coldest['Date'].strftime('%Y-%m-%d')}")
        print()

    def view_graph(self):
        if self.data is None:
            print("Please load the file first (option 1).\n")
            return

        sorted_data = self.data.sort_values("Date")

        plt.figure(figsize=(10, 5))
        plt.plot(sorted_data["Date"], sorted_data["Temperature"], marker="o", color="#4C9BE8")
        plt.title("30-Day Weather Forecast")
        plt.xlabel("Date")
        plt.ylabel("Temperature (°C)")
        plt.xticks(rotation=45)
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()

    def show_menu(self):
        print("=" * 5 + "30-DAY WEATHER FORECAST VIEWER" + "=" * 5)
        print("1. Load")
        print("2. View")
        print("3. Exit")


forecast = WeatherForecast()

while True:
    forecast.show_menu()
    choice = input("Select an option (1-3): ")

    if choice == "1":
        forecast.load_file()

    elif choice == "2":
        print("a. View Table")
        print("b. View Summary")
        print("c. View Graph")
        sub_choice = input("Choose an option: ")

        if sub_choice == "a":
            forecast.view_table()
        elif sub_choice == "b":
            forecast.view_summary()
        elif sub_choice == "c":
            forecast.view_graph()
        else:
            print("Invalid option.\n")

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice! Select 1 - 3 only.\n")
