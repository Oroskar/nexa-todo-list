#Or Oskar 325256162, Bar Reznik 209147792
#import Tkinter for GUI
from tkinter import Tk, Frame, Label, Button, Entry, StringVar, Spinbox, Toplevel, messagebox

#create the main window
root = Tk()
root.title("Nexa Todo List")
root.geometry("900x700")
root.configure(bg="lightblue")

#color and fonts at the top of the code so we could get easy access to them
bg_color = "lightblue"
btn_color = "white"
btn_fg = "darkblue"
font_style = ("Assistant",16)

#task and category classes
class Task:  # class that represents a task
    def __init__(self, title, notes, priority, date):
        self.title = title
        self.notes = notes
        self.priority = priority
        self.date = date

    def __str__(self):
        return f"{self.title} - {self.notes} (Priority {self.priority},Date {self.date})"

class Category:  #class that represents a category
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def clear_tasks(self):
        self.tasks = []

    def get_sorted_tasks(self): #sort tasks by priority (1-5), high to low
        sorted_tasks = []
        current_priority = 5
        while current_priority >= 1:
            for task in self.tasks:
                if task.priority == current_priority:
                    sorted_tasks.append(task)
            current_priority = current_priority - 1
        return sorted_tasks

    def __str__(self):
        return f"Category: {self.name}, Tasks: {len(self.tasks)}"

#storage
categories = {}
predefined_categories = ["Studies","Work","Home","Personal","Other"]
for name in predefined_categories:
    categories[name] = Category(name)

#general variables that will be used by the functions
current_category_name = None
current_window = None
title_var = None
notes_var = None
priority_var = None
day_var = None
month_var = None
year_var = None
rows = []
rows_has_task = []
rows_task_indices = []
max_rows = 10  #we decided to limitt the tasks for 10

def refresh_view():
    if current_category_name is None:
        return

    category = categories[current_category_name]
    tasks_list = category.tasks
    tasks_sorted = category.get_sorted_tasks()

    #reset all rows
    i = 0
    while i < max_rows:
        if i < len(tasks_sorted):
            t = tasks_sorted[i]
            rows[i][0].config(text=str(t))
            if i % 2 == 0:
                rows[i][1].config(text="delete")
            else:
                rows[i][1].config(text="Delete")
            rows_has_task[i] = True

            #save the index of this task in the original list
            index_in_list = 0
            found = False
            while index_in_list < len(tasks_list) and not found:
                if tasks_list[index_in_list] is t:
                    found = True
                else:
                    index_in_list = index_in_list + 1
            if found:
                rows_task_indices[i] = index_in_list
            else:
                rows_task_indices[i] = -1
        else:
            rows[i][0].config(text="")
            rows[i][1].config(text="")
            rows_has_task[i] = False
            rows_task_indices[i] = -1
        i = i + 1

#this function add task
def add_task():
    if current_category_name is None:
        return

    title = title_var.get()  #here we are using get() to read the user inputs ans saving them into a variable
    notes = notes_var.get()
    priority_text = priority_var.get()
    day_text = day_var.get()
    month_text = month_var.get()
    year_text = year_var.get()

    if title == "":  #we can't make a task without a title, so if a user try to do that we will show them a warning
        messagebox.showwarning("Error", "Enter task title")
        return

    priority = int(priority_text)
    day = int(day_text)
    month = int(month_text)
    year = int(year_text)

    date = f"{day:02d}/{month:02d}/{year}"
    task = Task(title, notes, priority, date)
    categories[current_category_name].add_task(task)

    #clear entries
    title_var.set("")
    notes_var.set("")
    day_var.set("1")
    month_var.set("1")
    year_var.set("2025")

    refresh_view()  #finally, were calling to this function so the user will see his new task

#this func is if the user already have tasks and he wants to delete all of them
def reset_tasks():
    if current_category_name is None:
        return
    answer = messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all tasks?")
    if answer:
        categories[current_category_name].clear_tasks()
        refresh_view()

#this func delete the task the user want, by index
def delete_task_at_index(row_index):
    if current_category_name is None:
        return
    if not rows_has_task[row_index]:
        return
    index_in_list = rows_task_indices[row_index]
    if index_in_list == -1:
        return
    tasks_list = categories[current_category_name].tasks
    if index_in_list >= 0 and index_in_list < len(tasks_list):
        removed = tasks_list.pop(index_in_list)
        print("Task deleted:",removed)
    refresh_view() #update the screen

#helpers functions that deletes the task in a specific row (0–9) they are connected
#to the delete buttons in rows 282-301 in this code
def delete_row_0():
    delete_task_at_index(0)

def delete_row_1():
    delete_task_at_index(1)

def delete_row_2():
    delete_task_at_index(2)

def delete_row_3():
    delete_task_at_index(3)

def delete_row_4():
    delete_task_at_index(4)

def delete_row_5():
    delete_task_at_index(5)

def delete_row_6():
    delete_task_at_index(6)

def delete_row_7():
    delete_task_at_index(7)

def delete_row_8():
    delete_task_at_index(8)

def delete_row_9():
    delete_task_at_index(9)

#this long func create a new window for the selected catgory and also builds the form for new tasks
def open_category_window(category_name):
    global current_category_name
    global current_window
    global title_var, notes_var, priority_var, day_var, month_var, year_var
    global rows, rows_has_task, rows_task_indices

    current_category_name = category_name
    current_window = Toplevel(root)
    current_window.title("Category: " + category_name)
    current_window.geometry("700x600")
    current_window.configure(bg=bg_color)
    current_window.grab_set()

    #title input
    lbl_title = Label(current_window, text="Task title", bg=bg_color, fg=btn_fg, font=font_style)
    lbl_title.grid(row=0, column=0, pady=5, padx=10, sticky="e")

    title_var = StringVar()
    title_widget = Entry(current_window, textvariable=title_var, font=font_style)
    title_widget.grid(row=0, column=1, pady=5, padx=10)

    #notes input
    lbl_notes = Label(current_window, text="Notes", bg=bg_color, fg=btn_fg, font=font_style)
    lbl_notes.grid(row=1, column=0, pady=5, padx=10, sticky="e")

    notes_var = StringVar()
    notes_widget = Entry(current_window, textvariable=notes_var, font=font_style)
    notes_widget.grid(row=1, column=1, pady=5, padx=10)

    #priority
    lbl_priority = Label(current_window, text="Priority (1-5)", bg=bg_color, fg=btn_fg, font=font_style)
    lbl_priority.grid(row=2, column=0, pady=5, padx=10, sticky="e")

    priority_var = StringVar(value="3")
    priority_widget = Spinbox(current_window, from_=1, to=5, textvariable=priority_var, font=font_style, width=5)
    priority_widget.grid(row=2, column=1, pady=5, padx=10, sticky="w")

    #date inputs
    lbl_day = Label(current_window, text="Day", bg=bg_color, fg=btn_fg, font=font_style)
    lbl_day.grid(row=3, column=0, pady=5, padx=10, sticky="e")

    day_var = StringVar(value="1")
    day_widget = Spinbox(current_window, from_=1, to=31, textvariable=day_var, font=font_style, width=5)
    day_widget.grid(row=3, column=1, pady=5, padx=10, sticky="w")

    lbl_month = Label(current_window, text="Month", bg=bg_color, fg=btn_fg, font=font_style)
    lbl_month.grid(row=4, column=0, pady=5, padx=10, sticky="e")

    month_var = StringVar(value="1")
    month_widget = Spinbox(current_window, from_=1, to=12, textvariable=month_var, font=font_style, width=5)
    month_widget.grid(row=4, column=1, pady=5, padx=10, sticky="w")

    lbl_year = Label(current_window, text="Year", bg=bg_color, fg=btn_fg, font=font_style)
    lbl_year.grid(row=5, column=0, pady=5, padx=10, sticky="e")

    year_var = StringVar(value="2025")
    year_widget = Spinbox(current_window, from_=2023, to=2030, textvariable=year_var, font=font_style, width=7)
    year_widget.grid(row=5, column=1, pady=5, padx=10, sticky="w")

    btn_add = Button(current_window, text="Add task", command=add_task,
                     bg=btn_color, fg=btn_fg, font=font_style)
    btn_add.grid(row=6, column=0, columnspan=2, pady=10, padx=6)

    btn_reset = Button(current_window, text="Reset category", command=reset_tasks,
                       bg=btn_color, fg=btn_fg, font=font_style)
    btn_reset.grid(row=7, column=0, columnspan=2, pady=10)

    # tasks table
    tasks_frame = Frame(current_window, bg=bg_color)
    tasks_frame.grid(row=8, column=0, columnspan=2, pady=20)

    rows = []
    rows_has_task = []
    rows_task_indices = []

    #This loop goes over the rows and creates the label and the matching delete button for each one
    i = 0
    while i < max_rows:
        lbl_task = Label(tasks_frame, text="", bg=bg_color, fg="black", font=font_style)
        lbl_task.grid(row=i, column=0, sticky="w", padx=5, pady=2)

        if i == 0:
            btn_delete = Button(tasks_frame, text="", bg=btn_color, fg=btn_fg, font=("Assistant", 12), command=delete_row_0)
        elif i == 1:
            btn_delete = Button(tasks_frame, text="", bg=btn_color, fg=btn_fg, font=("Assistant", 12), command=delete_row_1)
        elif i == 2:
            btn_delete = Button(tasks_frame, text="", bg=btn_color, fg=btn_fg, font=("Assistant", 12), command=delete_row_2)
        elif i == 3:
            btn_delete = Button(tasks_frame, text="", bg=btn_color, fg=btn_fg, font=("Assistant", 12), command=delete_row_3)
        elif i == 4:
            btn_delete = Button(tasks_frame, text="", bg=btn_color, fg=btn_fg, font=("Assistant", 12), command=delete_row_4)
        elif i == 5:
            btn_delete = Button(tasks_frame, text="", bg=btn_color, fg=btn_fg, font=("Assistant", 12), command=delete_row_5)
        elif i == 6:
            btn_delete = Button(tasks_frame, text="", bg=btn_color, fg=btn_fg, font=("Assistant", 12), command=delete_row_6)
        elif i == 7:
            btn_delete = Button(tasks_frame, text="", bg=btn_color, fg=btn_fg, font=("Assistant", 12), command=delete_row_7)
        elif i == 8:
            btn_delete = Button(tasks_frame, text="", bg=btn_color, fg=btn_fg, font=("Assistant", 12), command=delete_row_8)
        else:
            btn_delete = Button(tasks_frame, text="", bg=btn_color, fg=btn_fg, font=("Assistant", 12), command=delete_row_9)

        btn_delete.grid(row=i, column=1, padx=5)

        rows.append((lbl_task, btn_delete))
        rows_has_task.append(False)
        rows_task_indices.append(-1)
        i = i + 1
    refresh_view()

#start screen
start_frame = Frame(root, bg=bg_color)
start_frame.pack(expand=True, fill="both")

lbl_title = Label(start_frame, text="Nexa To-Do List",font=("Assistant", 28, "bold"), fg=btn_fg, bg=bg_color)
lbl_title.pack(pady=40)

def go_to_info():
    start_frame.destroy() #dear Dron: we know that we didnt learn destroy.we did asked ai for this row tbh
    info_frame.pack(expand=True, fill="both")

btn_start = Button(start_frame, text="Start", command=go_to_info,
                   bg=btn_color, fg=btn_fg, font=font_style)
btn_start.pack(pady=20)

#info screen
info_frame = Frame(root, bg=bg_color)
lbl_info = Label(info_frame, text=("Welcome to Nexa To-Do List\n"
          "organize your life in one simple place\n"
          "stay focused and reduce stress\n"
          "balance work, studies and your personal goals\n"
          "click continue to get started"),
    font=("Assistant", 20), fg=btn_fg, bg=bg_color, justify="center")
lbl_info.pack(pady=80)

def go_to_categories():
    info_frame.destroy()
    categories_frame.pack(expand=True, fill="both")

btn_continue = Button(info_frame, text="Continue", command=go_to_categories,
                      bg=btn_color, fg=btn_fg, font=font_style)
btn_continue.pack(pady=20)

#categories screen
categories_frame = Frame(root, bg=bg_color)

lbl_choose = Label(categories_frame, text="Choose a category:",
                   font=("Assistant", 24, "bold"), fg=btn_fg, bg=bg_color)
lbl_choose.pack(pady=40)

#functions to open each category,uses the func from row 201 in this code
def open_studies():
    open_category_window("Studies")

def open_work():
    open_category_window("Work")

def open_home():
    open_category_window("Home")

def open_personal():
    open_category_window("Personal")

def open_other():
    open_category_window("Other")

btn1 = Button(categories_frame, text="Studies", command=open_studies,
              bg=btn_color, fg=btn_fg, font=("Assistant", 20), width=20, height=2)
btn1.pack(pady=15)

btn2 = Button(categories_frame, text="Work", command=open_work,
              bg=btn_color, fg=btn_fg, font=("Assistant", 20), width=20, height=2)
btn2.pack(pady=15)

btn3 = Button(categories_frame, text="Home", command=open_home,
              bg=btn_color, fg=btn_fg, font=("Assistant", 20), width=20, height=2)
btn3.pack(pady=15)

btn4 = Button(categories_frame, text="Personal", command=open_personal,
              bg=btn_color, fg=btn_fg, font=("Assistant", 20), width=20, height=2)
btn4.pack(pady=15)

btn5 = Button(categories_frame, text="Other", command=open_other,
              bg=btn_color, fg=btn_fg, font=("Assistant", 20), width=20, height=2)
btn5.pack(pady=15)

#run everything
root.mainloop()
