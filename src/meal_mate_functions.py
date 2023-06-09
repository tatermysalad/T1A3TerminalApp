import csv
import time
from colored import fg, bg, attr


def view_ingr(file_name):
    print(f"\n{bg(28)}View pantry items{attr(0)}") 
    with open(file_name, "r") as f:
        reader = csv.reader(f)
        reader.__next__()
        for row in reader:
            print(f"{row[0]}")


def add_ingr(file_name):
    print(f"\n{bg(2)}Add pantry item{attr(0)}")
    ingr_title = input("Enter your ingredient: ")
    with open(file_name, "a") as ingr_file:
        writer = csv.writer(ingr_file)
        writer.writerow([ingr_title])


def remove_ingr(file_name):
    print(f"\n{bg(1)}Remove pantry item{attr(0)}")
    view_ingr(file_name)
    ingr_title = input("Enter the ingredient that you want to remove: ")
    ingr_lists = []
    with open(file_name, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if (ingr_title != row[0]):
                ingr_lists.append(row)
    with open(file_name, "w") as f:
        writer = csv.writer(f)
        writer.writerows(ingr_lists)
    view_ingr(file_name)


def staple_view_ingr(staple_file_name):
    print(f"\n{bg(90)}View staple items{attr(0)}")
    with open(staple_file_name, "r") as f:
        reader = csv.reader(f)
        reader.__next__()
        for row in reader:
            if row[1] == "True":
                print(f"{fg(2)}{row[0]} (in stock){attr(0)}")
            else:
                print(f"{fg(1)}{row[0]} (out of stock){attr(0)}")


def staple_edit_ingr(staple_file_name):
    print(f"\n{bg(90)}Modify staple item{attr(0)}")
    staple_view_ingr(staple_file_name)
    ingr_title = input("Enter the item that you want to check/uncheck: ")
    staple_lists = []
    with open(staple_file_name, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if (ingr_title == row[0]):
                if row[1] == "False":
                    staple_lists.append([row[0], "True"])
                else:
                    staple_lists.append([row[0], "False"])
            else:
                staple_lists.append(row)
    with open(staple_file_name, "w") as f:
        writer = csv.writer(f)
        writer.writerows(staple_lists)
    staple_view_ingr(staple_file_name)

def staple_ignore(staple_ignore_response):
    match staple_ignore_response:
        case 'y':
            return True
        case 'n':
            return False
        case _:
            print(f"\n{bg(1)}Please enter y (for yes) or n (for no){attr(0)}")
            time.sleep(1)
    