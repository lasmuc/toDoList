from tkinter import *
from tkinter.font import Font
from tkinter import filedialog
import os
import pickle

root = Tk()
root.title('ToDo List')
root.geometry("515x515")

# Create font
my_font = Font(
    family="Comic Sans MS",
    size=30,
    weight="bold"
)

# Create frame
my_frame = Frame(root)
my_frame.pack(pady=10)

# Create listbox
my_list = Listbox(my_frame,
                  font=my_font,
                  width=20,
                  height=5,
                  bg="SystemButtonFace",
                  bd=0,
                  fg="#464646",
                  highlightthickness=0,
                  selectbackground="#a6a6a6",
                  activestyle="none"
                  )

my_list.pack(side=LEFT, padx=10, fill=BOTH)

# Create dummy list
# dummy_list = ["Walk The Dog", "Buy Groceries", "Take A Nap", "Learn Tkinter", "Rule The World"]
# Add dummy list to list box
# for item in dummy_list:
#     my_list.insert(END, item)

# Create scrollbar
my_scrollbar = Scrollbar(my_frame)
my_scrollbar.pack(side=RIGHT, fill=BOTH)

# Add scrollbar
my_list.config(yscrollcommand=my_scrollbar.set)
my_scrollbar.config(command=my_list.yview)

# create entrybox to add items to the list

my_entry = Entry(root, font=("Helvetica", 24))
my_entry.pack(pady=20, padx=10, anchor='w')

# Create a button frame
button_frame = Frame(root)
button_frame.pack(pady=20)

# Functions
def delete_item():
    my_list.delete(ANCHOR)

def add_item():
    my_list.insert(END, my_entry.get())
    my_entry.delete(0, END)

def cross_off_item():
    my_list.itemconfig(
        my_list.curselection(),
        fg="#dedede")
    # get rid of selection bar
    my_list.select_clear(0, END)

def uncross_item():
    my_list.itemconfig(
        my_list.curselection(),
        fg="#464646")
    # get rid of selection bar
    my_list.select_clear(0, END)

def delete_crossed():
    count = 0
    while count < my_list.size():
        if my_list.itemcget(count, "fg") == "#dedede":
            my_list.delete(my_list.index(count))
        else:
            count += 1

def save_list():
    file_name = filedialog.asksaveasfilename(
        initialdir=os.path.dirname(os.path.abspath(__file__)),
        title="Save File",
        filetypes=(("Dat Files", "*.dat"), ("All Files", "*.*"))
    )
    if file_name:
        if file_name.endswith(".dat"):
            pass
        else:
            file_name = f'{file_name}.dat'
        # delete crossed off items before saving
        count = 0
        while count < my_list.size():
            if my_list.itemcget(count, "fg") == "#dedede":
                my_list.delete(my_list.index(count))
            else:
                count += 1
        # all list items
        items = my_list.get(0, END)
        # open file
        output_file = open(file_name, 'wb')

        # Add the items to the file
        pickle.dump(items, output_file)

def open_list():
    file_name = filedialog.askopenfilename(
        initialdir=os.path.dirname(os.path.abspath(__file__)),
        title="Open File",
        filetypes=(("Dat Files", "*.dat"), ("All Files", "*.*"))
    )

    if file_name:
        # Delete currently open list
        my_list.delete(0, END)
        # Open the file
        input_file = open(file_name, 'rb')
        # Load data from file
        items = pickle.load(input_file)
        # Output to the screen
        for item in items:
            my_list.insert(END, item)

def clear_list():
    my_list.delete(0,END)


root.bind("<Return>", lambda event: add_item())

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add items to the menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
# Add dropdown items
file_menu.add_command(label="Save list", command=save_list)
file_menu.add_command(label="Open list", command=open_list)
file_menu.add_separator()
file_menu.add_command(label="Clear list", command=clear_list)


# Adding the buttons
delete_button = Button(button_frame, text="Delete Item", command=delete_item)
add_button = Button(button_frame, text="Add Item", command=add_item)
cross_off_button = Button(button_frame, text="Cross Off Item", command=cross_off_item)
uncross_button = Button(button_frame, text="Uncross Item", command=uncross_item)
delete_crossed_button = Button(button_frame, text="Delete Crossed", command=delete_crossed)

delete_button.grid(row=0, column=0)
add_button.grid(row=0, column=1, padx=20)
cross_off_button.grid(row=0, column=2)
uncross_button.grid(row=0, column=3, padx=20)
delete_crossed_button.grid(row=0, column=4)

root.mainloop()
