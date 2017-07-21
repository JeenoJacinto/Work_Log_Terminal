import csv
import datetime
import os
from time_handler import TimeHandler


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def get_date(custom_text):
    fmt = '%m/%d/%Y'
    while True:
        clear()
        print("Date Format: --/--/----\n")
        print("{}\n".format(custom_text))
        task_date = input("Please input a date: ")
        try:
            datetime.datetime.strptime(task_date, fmt)
        except ValueError:
            print("'{}' doesn't seem to be a valid date.".format(task_date))
            input("Press Enter")
        except AttributeError:
            print("'{}' doesn't seem to be a valid date.".format(task_date))
            input("Press Enter")
        else:
            return task_date
            break


def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta


def get_row_list(csv_file):
    row_list = []
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row_list.append([
                row['Date'],
                row['Task Name'],
                row['Time Spent'],
                row['Notes']
            ])
    return row_list


def edit_delete(selected_row, row_list, csv_file):
    task = True
    while task:
        clear()
        print("Selected Row: {}".format(", ".join(selected_row)))
        print("Edit or Delete\n")
        print("1. Edit")
        print("2. Delete\n")
        print("Please enter the number of the option you wish to choose.")
        choice = input("> ")
        if choice == '1':
            index_tracker = 0
            for key, value in enumerate(row_list):
                if value == selected_row:
                    del row_list[key]
                    index_tracker += key
                    break
            while True:
                clear()
                print("Selected Row: {}".format(", ".join(selected_row)))
                print("Choose which detail you wish to edit\n")
                print("1. Date")
                print("2. Task Name")
                print("3. Time Spent")
                print("4. Notes")
                print("5. Done\n")
                print("Please enter the number of the option you wish"
                      + " to choose.")
                print("Selecting 'Done' will updated the log file and will")
                print("return you to the previous menu.")
                choice = input("> ")
                if choice == '1':
                    del selected_row[0]
                    new_date = get_date("Date Editing")
                    selected_row.insert(0, new_date)
                elif choice == '2':
                    del selected_row[1]
                    while True:
                        clear()
                        tester = []
                        task_name = input("Enter new task name: ")
                        if len(task_name) > 0:
                            for i in task_name:
                                if i != " ":
                                    tester.append(1)
                        if len(tester) > 0:
                            break
                        else:
                            print("Invalid Task Name")
                            input("Press Enter")
                    selected_row.insert(1, task_name)
                elif choice == '3':
                    del selected_row[2]
                    while True:
                        clear()
                        print("Edit the amount of time spent")
                        hours = input("Hours: ")
                        minutes = input("Minutes: ")
                        if hours == '':
                            hours = '0'
                        if minutes == '':
                            minutes = '0'
                        try:
                            int(hours)
                            int(minutes)
                        except ValueError:
                            print("Invalid Entry")
                            input("Press Enter")
                        else:
                            task_duration = TimeHandler(
                                int(hours), int(minutes))
                            h_fmt, m_fmt = task_duration.get_hours_minutes()
                            time_spent = "Hours:{} Minutes:{}".format(
                                h_fmt, m_fmt)
                            break
                    selected_row.insert(2, time_spent)
                elif choice == '4':
                    clear()
                    del selected_row[3]
                    notes = input("Enter New notes or press enter to"
                                  + "leave notes blank: ")
                    tester2 = []
                    if len(notes) > 0:
                        for i in notes:
                            if i != " ":
                                tester2.append(1)
                    if len(tester2) < 1:
                        notes = 'N/A'
                    selected_row.insert(3, notes)
                elif choice == '5':
                    row_list.insert(index_tracker, selected_row)
                    with open(csv_file, 'w') as csvfile:
                        fieldnames = ['Date', 'Task Name',
                                      'Time Spent', 'Notes']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                                lineterminator='\n')
                        writer.writerow({
                            'Date': 'Date',
                            'Task Name': 'Task Name',
                            'Time Spent': 'Time Spent',
                            'Notes': 'Notes'
                        })
                        for row in row_list:
                            writer.writerow({
                                'Date': row[0],
                                'Task Name': row[1],
                                'Time Spent': row[2],
                                'Notes': row[3]
                            })
                    task = False
                    break
                else:
                    print("Invalid Input")
                    input("Press Enter")

        elif choice == '2':
            row_list.remove(selected_row)
            with open(csv_file, 'w') as csvfile:
                fieldnames = ['Date', 'Task Name', 'Time Spent', 'Notes']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                        lineterminator='\n')
                writer.writerow({
                    'Date': 'Date',
                    'Task Name': 'Task Name',
                    'Time Spent': 'Time Spent',
                    'Notes': 'Notes'
                })
                for row in row_list:
                    writer.writerow({
                        'Date': row[0],
                        'Task Name': row[1],
                        'Time Spent': row[2],
                        'Notes': row[3]
                    })
            task = False
            break
        else:
            print("Invalid Input")
            input("Press Enter")


def get_options_to_edit(selected_entries, row_list, csv_file):
    while True:
        clear()
        choice_dict = {}
        counter = 1
        for key, value in enumerate(selected_entries):
            print("{}. {}".format(key+1, ", ".join(value)))
            choice_dict[key + 1] = value
            counter += 1
        print("{}. Previous Menu".format(str(counter)))
        print("\nPlease enter the number of the"
              + " entry you wish to edit or delete.")
        print("If you do not wish to change the log,"
              + " return to the previous menu")
        choice = input("> ")
        try:
            int(choice)
        except ValueError:
            print("Invalid Input")
            input("Press Enter")
        else:
            if int(choice) in list(range(1, counter+1)):
                if int(choice) == counter:
                    break
                else:
                    chosen_entry = choice_dict[int(choice)]
                    edit_delete(chosen_entry, row_list,
                                csv_file)
                    break
            else:
                print("Chosen number is out of range.")
                print("Invalid Input")
                input("Press Enter")
