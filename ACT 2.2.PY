class Profiling:

    def __init__(self, filename="output.txt"):
        self.filename = filename
        self.profiles = []
        

    def get_age_grp(self, age):
        if age <= 14:
            return "Minor"
        elif age <= 25:
            return "Youth"
        elif age <= 65:
            return "Adult"
        else:
            return "Senior"

    def add_record(self):
        name = input("Enter name: ")
        age = input("Enter age: ")

        while not age.isdigit():
            print("Invalid age!")
            age = input("Enter age: ")
        age = int(age)

        gender = input("Enter gender (M/F): ")

        while gender not in ("M", "m", "F", "f"):
            print("Invalid Gender!")
            gender = input("Enter gender (M/F): ")

        profile = {
            "name": name,
            "age": age,
            "gender": gender,
            "age_group": self.get_age_grp(age)
        }

        self.profiles.append(profile)
        print("Recorded added Successfully!\n")

    def view_records(self):
        if len(self.profiles) == 0:
            print("No records found. Add a record first.\n")
            return
        
        with open(self.filename, "w") as file:
            file.write("                    List of Records\n")
            file.write('-' * 60 + "\n")
            for i, profile in enumerate(self.profiles, start=1):
                file.write(f"{i:<4} | Name: {profile['name']:<15} | Age: {profile['age']:<8} | {profile['age_group']:<10}\n")

        print(f"All records written to {self.filename} (overwritten).\n")

    def appendFile(self):
        if len(self.profiles) == 0:
            print("No records found. Add a record first.\n")
            return

        profile = self.profiles[-1]
        with open(self.filename, "a") as file:
            file.write("\n" + "Not yet in the list. " + f"Name: {profile['name']:<15} | Age: {profile['age']:<8} | {profile['age_group']:<10}\n")
    
    def readFile(self):
        try:
            with open(self.filename, "r") as file:
                content = file.read()
                if content.strip() == "":
                    print("The file is empty.\n")
                else:
                    print("\n" + content)

        except FileNotFoundError:
            print(f"{self.filename} does not exist.\n")

    def readFilePerLine(self):
        try:
            with open(self.filename, "r") as file:
                lines = file.readlines()
                if len(lines) == 0:
                    print("The file is empty.\n")
                else:
                    print()
                    for line in lines:
                        print(line.rstrip())
                    print()

        except FileNotFoundError:
            print(f"{self.filename} does not exist.\n")

    def show_menu(self):
        print("=== RECORD MANAGEMENT SYSTEM ===")
        print("1. Add New Record")
        print("2. View Records")
        print("3. Write to the File (Create or Overwrite)")
        print("4. Exit")


track = Profiling()

while True:
    track.show_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
        track.add_record()
    elif choice == "2":
       print("a. Read whole file?")
       print("b. Read file line by line?")
       subChoice = input("Choose an option: ")

       if subChoice == "a":
           track.readFile()
       elif subChoice == "b":
           track.readFilePerLine()
       else:
           print("Invalid Option.\n")   

    elif choice == "3":
        print("a. Write")
        print("b. Append")
        subChoice = input("Choose an option: ")

        if subChoice == "a":
            track.view_records()
        elif subChoice == "b":
            track.appendFile()
        else:
            print("Invalid Option.\n")

    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid Choice! Select 1 - 4 only!")