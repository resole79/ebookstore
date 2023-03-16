# Note: If you don't have "Tabulate" install
# 1. Please download "module" folder with "database_manip.py"
# 2. Uncomment the following string "from module.tabulate import tabulate" and indent
# 3. Comment the following string "from tabulate import tabulate"

# from module.tabulate import tabulate

import sqlite3
from module.tabulate import tabulate
import os


# Function to check create db
def is_db_create(db_name):
    # Declare variable
    db_is_create = False

    # "if" condition to check path exists
    if os.path.exists(db_name):
        db_is_create = True

    return db_is_create


# Function to create and connect to database
def create_db(db_name):
    connect_to_database = ""

    # Clear db name from spaces
    db_name = db_name.strip()

    try:
        # Create and connect to database
        connect_to_database = sqlite3.connect(db_name)

    except Exception as error:
        print(error)

    if is_db_create(db_name):
        print(f"Your DatBase {db_name} is created!")

    return connect_to_database


# Function to check if table is create
def is_table_create(table_name):
    table_is_create = False
    cursor = using_db.cursor()

    cursor.execute(f''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name ='{table_name}' ''')

    # "if" condition to check "count(name)" is 1
    if cursor.fetchone() == 1:
        table_is_create = True

    using_db.commit()

    return table_is_create


# Function to create a table in database
def create_table(table_name, list_of_column):
    cursor = using_db.cursor()
    table_value = ""

    # "for" cycle to read "list_of_column"
    for i, row in enumerate(list_of_column):

        # "if" condition to insert comma after row
        if i == len(list_of_column)-1:
            table_value += f"{row}"
        else:
            table_value += f"{row},"
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS ''' + table_name + ''' (''' + table_value + ''')''')
        using_db.commit()

    except Exception as error:
        print(error)

    # "if" condition to check table is create
    if is_table_create(table_name):
        print(f"Your Table {table_name} is created!")


# Function to check if table is empty
def is_empty_table(table_name):
    # Declare variable
    table_is_empty = True
    rows = select_data(table_name)

    # "if" condition to check table is empty
    if (len(rows)) > 0:
        table_is_empty = False

    return table_is_empty


# Function to get name of column
def get_name_column(table_name, condition=""):
    # Declare variable
    select_column_result = ""
    column = []
    column_dict = {}
    cursor = using_db.cursor()

    try:
        cursor.execute('''SELECT name, type FROM PRAGMA_TABLE_INFO("''' + table_name + '''")''' + condition)
        select_column_result = cursor.fetchall()
        using_db.commit()
    except Exception as error:
        print(error)

    # Cycle "for" to read all column
    for column_and_type in select_column_result:
        column_dict[column_and_type[0]] = column_and_type[1]
        column.append(column_and_type[0])

    return column, column_dict


# Function to select data in table
def select_data(table_name, condition_select='', list_of_value=[]):
    # Declare variable
    rows = ""

    try:
        cursor = using_db.cursor()
    except AttributeError as attribute_error:
        print(attribute_error)

    try:
        cursor.execute('''SELECT * FROM ''' + table_name + condition_select, list_of_value)
        rows = cursor.fetchall()
        using_db.commit()
    except Exception as error:
        print(error)

    return rows


# Function to print data in table
def print_data(list_of_rows):
    print(tabulate(list_of_rows, header_table))


# Function to insert data in table
def insert_data(table_name, list_of_date, list_of_column=[]):
    # Declare variable
    column_name = ""


    try:
        cursor = using_db.cursor()
    except AttributeError as attribute_error:
        print(attribute_error)

    # Cycle "for" to read all column
    for count_column, column in enumerate(list_of_column):
        # "if" condition to insert comma after column
        if count_column == 0:
            column_name += f"( {column},  "
        elif count_column == len(list_of_column) - 1:
            column_name += f"{column} )"
        else:
            column_name += f"{column}, "

    # Cycle "for" to read all data
    for data_in_list in list_of_date:
        question_mark = ""
        # Cycle "for" to read all data
        for count_data_in_list, data in enumerate(data_in_list):

            # "if" condition to insert comma after question mark
            if count_data_in_list == len(data_in_list)-1:
                question_mark += "?"
            else:
                question_mark += "?,"
        try:
            cursor_execute = cursor.execute('''INSERT OR IGNORE INTO ''' + table_name + column_name + ''' VALUES (''' + question_mark + ''')''', data_in_list)
            using_db.commit()
        except Exception as error:
            print(error)

    # "if" condition to check execute query
    if cursor_execute.arraysize == 1:
        print(f"\n{green}{bold}Your rows is insert to {table_name} table!{end_code}\n")


# Function to update data
def update_data(table_name, is_update, condition_update, update_list_of_date):
    # Declare variable
    cursor = using_db.cursor()

    try:
        # check if the row to update exist
        rows_of_condition = select_data(table_name, condition_update, [update_list_of_date[-1]])

        if len(rows_of_condition) > 0:
            cursor_execute = cursor.execute('''UPDATE ''' + table_name + is_update + condition_update, update_list_of_date)
            using_db.commit()
        else:
            print(f"\n{red}{bold}Ⓔ Sorry, your research don't match any book{end_code}\n")

    except Exception as error:
        print(error)

    # "if" condition to check execute query
    if cursor_execute.arraysize == 1:
        print(f"\n{green}{bold}Your rows are update to {table_name} table!{end_code}\n")


# Function to delete data
def delete_data(table_name, condition_delete="", delete_list_of_date=""):
    cursor = using_db.cursor()

    try:

        for id_to_delete in delete_list_of_date:
            # check if the row to update exist
            rows_of_condition = select_data(table_name, condition_delete, [id_to_delete])

            if len(rows_of_condition) > 0:
                cursor_execute = cursor.execute('''DELETE FROM ''' + table_name + condition_delete, [id_to_delete])
                using_db.commit()

        # "if" condition to check execute query
        if cursor_execute.arraysize == 1:
            print(f"\n{green}{bold}Your rows are delete from {table_name} table!{end_code}\n")

    except Exception as error:
        print(error)


# Color use for program
green = "\u001b[32m"
red = "\u001b[31m"
bold = "\033[1m"
italic = "\033[3m"
revers = "\u001b[7m"
end_code = '\033[0m'


# Declare Variable
name_db = "./ebookstore.db"
name_table = "books"
table_list = ["id INTEGER PRIMARY KEY AUTOINCREMENT", "title TEXT", "author TEXT", "qty INTEGER"]

book_list = [[3001, "A Tale of Two Cities", "Charles Dickens", 30],
             [3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40],
             [3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25],
             [3004, "The Lord of the Rings", "J.R.R Tolkien", 37],
             [3005, "Alice in Wonderland", "Lewis Carroll", 12],
             [3006, "Nineteen Eighty-Four", "George Orwell", 20],
             [3007, "1Q84", "Haruki Murakami", 84],
             [3008, "The Man in the High Castle", "Philip K. Dick", 50],
             [3009, "Fatherland", "Robert Harris", 64]]             

# Create a db and connection
# "if" condition to check id db is created
if not is_db_create(name_db):
    using_db = create_db(name_db)

    # if db is created, create a table
    if is_db_create(name_db):
        create_table(name_table, table_list)
    else:
        print(f"Sorry, your table {name_table} can't be create. DB {name_db} missing! ")

    # if db and table is create insert data inside a table
    if is_db_create(name_db) and is_empty_table(name_table):
        insert_data(name_table, book_list)
else:
    using_db = sqlite3.connect(name_db)

    # if db is created, create the table
    if not is_table_create(name_table):
        create_table(name_table, table_list)

    # insert data inside a table if is empty
    if is_empty_table(name_table):
        insert_data(name_table, book_list)

# Call "get_name_column" function
header_table, header_table_dict = get_name_column(name_table)
is_searchable, is_searchable_dict = get_name_column(name_table, " WHERE type='TEXT' ")
is_writeable_updatable, is_writeable_updatable_dict = get_name_column(name_table, " WHERE pk != 1 ")

# Call "print_data" and s"elect_data" functions
print_data(select_data(name_table))

if is_db_create(name_db):
    menu = f"\n({green}1{end_code}).Enter book "
    menu += f"({green}2{end_code}).Update book "
    menu += f"({green}3{end_code}).Delete books "
    menu += f"({green}4{end_code}).Search books "
    menu += f"({green}5{end_code}).View all books "
    menu += f"({green}0{end_code}).exit\n"
    menu += "Please, choice a number : "
else:
    menu = ""

while True:

    # Ask user choice from menu
    choice_user = input(f"{menu}")

    if choice_user == "1":
        # Declare variable
        book = []
        insert_condition_list = []

        # Cycle "for" to read the column from dict
        for count_column_updatable, column_updatable in enumerate(is_writeable_updatable_dict):
            write = input(f"Please, insert the {column_updatable} of book : ")
            # "if" condition to check integer column
            if is_writeable_updatable_dict[column_updatable] == "INTEGER":
                # Cycle "while" condition to exit "write" is not empty
                while not write:
                    print(f"\n{red}{bold}Ⓔ Sorry, your {column_updatable} is empty.{end_code}\n")
                    write = input(f"Please, insert the {column_updatable} of book : ")
                else:
                    # Cycle "while" condition to exit "write" is empty
                    while write:
                        # "if" condition to check numeric item
                        if write.isnumeric():
                            book.append(write)
                            break
                        else:
                            # Cycle "while" condition to exit "write" is numeric
                            while not write.isnumeric():
                                print(f"\n{red}{bold}Ⓔ Invalid input. Please enter an integer.{end_code}\n")
                                write = input(f"Please, insert the {column_updatable} of book : ")
                            else:
                                book.append(write)
                                break
            else:
                # Cycle "while" condition to exit "write" is empty
                while not write:
                    print(f"\n{red}{bold}Ⓔ Sorry, your {column_updatable} is empty.{end_code}\n")
                    write = input(f"Please, insert the {column_updatable} of book : ")
                else:
                    book.append(write)

        insert_condition_list.append(book)

        # Call "select_data" function
        insert_data(name_table, insert_condition_list, is_writeable_updatable)
        print_data(select_data(name_table))

    elif choice_user == "2":
        # Variable Declare
        book_to_update = []
        column_to_update = {}
        update_condition = f" WHERE {header_table[0]} = ? "

        # Ask user to insert the id book to update
        id_book = input("Please, insert the id of the book : ")

        # Cycle "while" condition to exit item is not inside the table
        while not select_data(name_table, update_condition, [id_book]):
            try:
                print(f"\n{red}{bold}Ⓔ Sorry, your research don't match any book{end_code}\n")
                id_book = int(input("Please, insert the id of the book : "))
            except ValueError:
                print(f"\n{red}{bold} Ⓔ Invalid input. Please enter an integer.{end_code}\n")

        # "if" condition to check table is not empty
        if not is_empty_table(name_table):
            # Cycle "for" to read the column from dict
            for count_column_updatable, column_updatable in enumerate(is_writeable_updatable_dict):

                # Ask user to insert the title, author and quantity to uppdate
                update = input(f"Please, insert the {column_updatable} of book you want to update (otherwise leave empty) : ")
                # "if" condition to check integer item
                if is_writeable_updatable_dict[column_updatable] == "INTEGER":
                    # Cycle "while" condition to exit item is empty
                    while update:
                        # "if" condition to check item is not empty and numeric
                        if update and update.isnumeric():
                            book_to_update.append(update)
                            column_to_update[column_updatable] = update
                            break
                        elif update and not update.isnumeric():
                            # Cycle "while" condition to exit item is empty and numeric
                            while not update.isnumeric() and update:
                                update = input(f"Please, insert the {column_updatable} of book you want to update (otherwise leave empty) : ")
                else:
                    # "if" condition to check empty item
                    if update:
                        book_to_update.append(f"{update}")
                        column_to_update[column_updatable] = update
            # "if" condition to check "book_to_update" is empty
            if book_to_update:
                book_to_update.append(id_book)

                is_update_condition = " SET "
                update_range = len(column_to_update) - 1
                count = 0
                # Cycle "for" to read column name in dict
                for column_update in column_to_update.keys():

                    # "if" condition to insert comma after row
                    if count == update_range:
                        is_update_condition += f" {column_update} = ?"
                    else:
                        is_update_condition += f" {column_update} = ?, "
                    count += 1

                sure_update = input("Are you sure want update this books? (Y / N) : ").lower()

                # Block to ask user want really update the item
                while sure_update != "y" and sure_update != "n":
                    print(f"\n{red}{bold} Ⓔ Sorry your choice is uncorrected!{end_code}\n")
                    sure_update = input("Are you sure want update this books? (Y / N) : ").lower()

                if sure_update == "y":
                    # Call "update_data" function
                    update_data(name_table, is_update_condition, update_condition, book_to_update)
                    # Call "select_data" and "print_data" functions
                    print_data(select_data(name_table))

                elif sure_update == "n":
                    print(f"\n{red}{bold}Ⓔ Your books doesn't update!{end_code}\n")
                    # Call "select_data" and print_data functions
                    print_data(select_data(name_table))

            else:
                print(f"\n{red}{bold}Ⓔ Sorry, you didn't provide any update!{end_code}\n")
                # Call "select_data" and print_data functions
                print_data(select_data(name_table))
        else:
            print(f"\n{red}{bold} Ⓔ Sorry your table is empty!{end_code}\n")

    elif choice_user == "3":
        # Variable Declare
        book_to_delete = []
        delete_condition = f" WHERE {header_table[0]} = ? "
        row_in_table = int(len(select_data(name_table)))

        if not is_empty_table(name_table):
            # Ask user number of item to delete
            row_to_delete = int(input("Please, how many book do you want delete? : "))

            # Number of "row_in_table" is less than user want delete
            while row_to_delete > row_in_table:
                try:
                    print(f"\n{red}{bold}Ⓔ Invalid input. Please enter an integer less than {row_in_table}.{end_code}\n")
                    row_to_delete = int(input("Please, how many book do you want delete? : "))
                except ValueError:
                    print(f"\n{red}{bold} Ⓔ Invalid input. Please enter an integer.{end_code}\n")

            # Cycle "for" to count number of item delete
            for count_id in range(row_to_delete):
                id_book = int(input("Please, insert the id of the book : "))

                # Cycle "while" condition to exit id is inside table
                while not select_data(name_table, delete_condition, [id_book]):
                    try:
                        print(f"\n{red}{bold}Ⓔ Sorry, your research don't match any book{end_code}\n")
                        id_book = int(input("Please, insert the id of the book : "))
                    except ValueError:
                        print(f"\n{red}{bold} Ⓔ Invalid input. Please enter an integer.{end_code}\n")

                book_to_delete.append(id_book)

            if book_to_delete:

                # Block to ask user want really delete the item
                sure_delete = input("Are you sure want delete this books? (Y / N) : ").lower()

                while sure_delete != "y" and sure_delete != "n":
                    print(f"\n{red}{bold} Ⓔ Sorry your choice is uncorrected!{end_code}\n")
                    sure_delete = input("Are you sure want delete this books? (Y / N) : ").lower()

                if sure_delete == "y":
                    # Call "delete_data" function
                    delete_data(name_table, delete_condition, book_to_delete)
                    # Call "select_data" and "print_data" functions
                    print_data(select_data(name_table))

                elif sure_delete == "n":
                    print(f"\n{red}{bold}Ⓔ Your books doesn't delete!{end_code}\n")
                    # Call "select_data" and "print_data" functions
                    print_data(select_data(name_table))
        else:
            print(f"\n{red}{bold} Ⓔ Sorry your table is empty!{end_code}\n")

    elif choice_user == "4":
        # Variable Declare
        book_to_search = []
        column_to_search = {}

        if not is_empty_table(name_table):
            for count_column_searchable, column_searchable in enumerate(is_searchable):
                search = input(f"Please, insert the {column_searchable} of book you want to research (otherwise leave empty) : ")
                if search:
                    book_to_search.append(f"%{search}%")
                    column_to_search[column_searchable] = search

            if book_to_search:
                search_condition = " WHERE "
                search_range = len(column_to_search) - 1
                count = 0

                # Cycle "for" to read column name in dict
                for column_search in column_to_search.keys():
                    # "if" condition to insert "AND" after row
                    if count == search_range:
                        search_condition += f"{column_search} LIKE ?"
                    else:
                        search_condition += f"{column_search} LIKE ? AND "
                    count += 1

                # Check if search match books
                search_result = select_data(name_table, search_condition, book_to_search)
                if len(search_result) > 0:
                    print(f"\n{'-' * 30} {green}{bold}I found {len(search_result)} rows{end_code} {'-' * 30}")
                    # Call "print_data" function
                    print_data(search_result)
                else:
                    print(f"\n{red}{bold}Ⓔ Sorry, your research don't match any book{end_code}\n")
            else:
                print(f"\n{red}{bold}Ⓔ Sorry, your research don't match any book{end_code}\n")
                # Call "select_data" and "print_data" functions
                print_data(select_data(name_table))
        else:
            print(f"\n{red}{bold}Ⓔ Sorry your table is empty!{end_code}\n")

    elif choice_user == "5":
        # Call "select_data" and "print_data" functions
        print_data(select_data(name_table))

    elif choice_user == "0":
        using_db.close()
        print("Goodbye!")
        break

    else:
        print(f"\n{red}{bold}Ⓔ Sorry your choice is uncorrected!!{end_code}\n")
