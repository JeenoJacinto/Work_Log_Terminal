import csv
import datetime
import re

from time_handler import TimeHandler
from functions import clear, get_date, perdelta, get_row_list, edit_delete
from functions import get_options_to_edit


class LogHandler:
    def __init__(self, spreadsheet):
        self.spreadsheet = spreadsheet

    def __str__(self):
        """String version of class instance"""
        with open(self.spreadsheet, 'r') as csvfile:
            string = ""
            spread_sheet_reader = csv.reader(csvfile)
            for row in spread_sheet_reader:
                string += ', '.join(row) + "\n"
            return string

    def write_to_log(self):
        task_date = get_date("Task Date")
        while True:
            clear()
            print("Task Date: {}\n".format(task_date))
            tester = []
            task_name = input("Please enter the name of your task: ")
            # Task name
            if len(task_name) > 0:
                for i in task_name:
                    if i != " ":
                        tester.append(1)
            if len(tester) > 0:
                break
            else:
                print("Invalid Task Name")
                input("Press Enter")
        while True:
            clear()
            print("Task Date: {}".format(task_date))
            print("Task Name: {}\n".format(task_name))
            print("Enter the amount of time spent")
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
                task_duration = TimeHandler(int(hours), int(minutes))
                hours_fmt, minutes_fmt = task_duration.get_hours_minutes()
                time_spent = "Hours:{} Minutes:{}".format(
                    hours_fmt, minutes_fmt)
                # Time spent
                break
        clear()
        print("Task Date: {}".format(task_date))
        print("Task Name: {}".format(task_name))
        print("Time Spent: {}\n".format(time_spent))
        notes = input("Enter additional notes (Optional): ")
        # Notes
        tester2 = []
        if len(notes) > 0:
            for i in task_name:
                if i != " ":
                    tester2.append(1)
        if len(tester2) < 1:
            notes = 'N/A'
        with open(self.spreadsheet, 'a') as csvfile:
            fieldnames = ['Date', 'Task Name', 'Time Spent', 'Notes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                    lineterminator='\n')
            writer.writerow({
                'Date': task_date,
                'Task Name': task_name,
                'Time Spent': time_spent,
                'Notes': notes
            })

    def reset_log(self):
        with open(self.spreadsheet, 'w') as csvfile:
            fieldnames = ['Date', 'Task Name', 'Time Spent', 'Notes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                    lineterminator='\n')
            writer.writerow({
                'Date': 'Date',
                'Task Name': 'Task Name',
                'Time Spent': 'Time Spent',
                'Notes': 'Notes'
            })

    def search_log(self):
        row_list = get_row_list(self.spreadsheet)
        fmt = '%m/%d/%Y'
        while True:
            clear()
            print("Log Search Menu\n")
            print("1. Search by date")
            print("2. Search by time spent")
            print("3. Search by exact match or pattern")
            print("4. Page through individual entries")
            print("5. Previous menu\n")
            print("Please enter the number of the option you wish to choose.")
            user_choice = input("> ")
            if user_choice == '1':
                search_by_date = True
                while search_by_date:
                    clear()
                    print("Search an entry by date\n")
                    print("Would you like to enter a specific date range?")
                    user_choice2 = input("Y/N ")
                    if user_choice2.upper() == 'Y':
                        fmt_date_list = []
                        search_list = []
                        start_date = get_date("Starting Date")
                        end_date = get_date("Ending Date")
                        start_date_fmt = datetime.datetime.strptime(start_date,
                                                                    fmt)
                        end_date_fmt = datetime.datetime.strptime(end_date,
                                                                  fmt)
                        for result in perdelta(
                                start_date_fmt, end_date_fmt
                                + datetime.timedelta(days=1),
                                datetime.timedelta(days=1)):
                            fmt_date_list.append(datetime.datetime.strftime(
                                result, fmt))
                        for i in row_list:
                            if i[0] in fmt_date_list:
                                search_list.append(i)
                        get_options_to_edit(search_list, row_list,
                                            self.spreadsheet)
                        search_by_date = False
                    else:
                        selected_dates = []
                        task_date = get_date("Chosen date will list all entrie"
                                             + "s with matching Task Date")
                        for i in row_list:
                            if i[0] == task_date:
                                selected_dates.append(i)
                        get_options_to_edit(selected_dates, row_list,
                                            self.spreadsheet)
                        search_by_date = False
            elif user_choice == '2':
                selected_entries = []
                while True:
                    clear()
                    print("Seach an entry by time\n")
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
                        task_duration = TimeHandler(int(hours), int(minutes))
                        h_fmt, m_fmt = task_duration.get_hours_minutes()
                        time_spent = "Hours:{} Minutes:{}".format(
                            h_fmt, m_fmt)
                        # Time spent
                        break
                for row in row_list:
                    if row[2] == time_spent:
                        selected_entries.append(row)
                get_options_to_edit(selected_entries, row_list,
                                    self.spreadsheet)
            elif user_choice == '3':
                clear()
                selected_entries = []
                while True:
                    clear()
                    print("Search an entry by exact match or regular expression\n")
                    print("Please enter text or regular expression"
                          + " to match entries")
                    print("Do not add spaces after commas.")
                    string = input("> ")
                    if len(string) < 1:
                        print("Invalid Input")
                        input("Press Enter")
                    else:
                        break
                search_string = '(?P<results>%s)' % string
                for row in row_list:
                    row_string = ",".join(row)
                    parse = re.search(r'%s' % search_string, row_string, re.I)
                    if parse is not None:
                        selected_entries.append(row)
                get_options_to_edit(selected_entries, row_list,
                                    self.spreadsheet)
            elif user_choice == '4':
                page_range = list(range(0, len(row_list)))
                page = 0
                while True:
                    clear()
                    if len(row_list) == 0:
                        print("You don't have any entries to view.")
                        input("Press enter")
                        break
                    else:
                        current_row = row_list[page]
                        print("Entry #: {}\n".format(page + 1))
                        print("Date {}".format(current_row[0]))
                        print("Task Name: {}".format(current_row[1]))
                        print("Time Spent: {}".format(current_row[2]))
                        print("Notes: {}\n".format(current_row[3]))
                        print("1. Next Entry")
                        print("2. Previous Entry")
                        print("3. Edit Entry")
                        print("4. Back to previous menu\n")
                        print("Please enter the number of the option"
                              + " you wish to choose.")
                        user_choice = input("> ")
                        if user_choice == '1':
                            if page + 1 in page_range:
                                page = page + 1
                            else:
                                print("There are no more further entries.")
                                input("Press Enter")
                        elif user_choice == '2':
                            if page - 1 in page_range:
                                page = page - 1
                            else:
                                print("There are no more previous entries.")
                                input("Press Enter")
                        elif user_choice == '3':
                            edit_delete(row_list[page], row_list,
                                        self.spreadsheet)
                            break
                        elif user_choice == '4':
                            break
                        else:
                            print("Invalid Input")
                            input("Press Enter")
            elif user_choice == '5':
                break
            else:
                print("Invalid Input")
                input("Press Enter")
