
import os

from log_handler import LogHandler

# relearn how to write and read from files

if __name__ == "__main__":
    def clear():
        """Clears the screen"""
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def menuloop(csv_file):
        while True:
            clear()
            print("Work Log Terminal: Main Menu\n")
            print("1. Add new entry")
            print("2. View and/or edit Data")
            print("3. Clear/Reset Work Log Data")
            print("4. Quit\n")
            print("Please enter the number of the option you wish to choose.")
            choice = input("> ")
            if choice == '1':
                csv_file.write_to_log()
            elif choice == '2':
                print(csv_file.search_log())
            elif choice == '3':
                csv_file.reset_log()
            elif choice == '4':
                clear()
                break
            else:
                print("Invalid Input")
                input("Press Enter")

    csv_file = LogHandler('log.csv')
    menuloop(csv_file)
