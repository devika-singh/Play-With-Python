from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

IDE_window = Tk()
IDE_window.title("Python IDE 101")
IDE_window.geometry('1250x700')

upper_frame = Frame(IDE_window,width=1250,height=500)
upper_frame.pack(side=TOP)

lower_frame = Frame(IDE_window,width=1250,height=300,bd=2)
lower_frame.pack(side=BOTTOM)

IDE_editor = Text(upper_frame,width=1200,bg="white",foreground="black", undo=True)
IDE_editor.pack(side=RIGHT)

IDE_terminal = Text(lower_frame,width=1250,height=300,bg="gainsboro",foreground="black")
IDE_terminal.pack()


#global variables
is_dark = False
open_file_path = ""
is_terminal_open = True
entry = Entry()


#function

def switch_mode():
    global is_dark
    if is_dark == False:
        IDE_editor.configure(bg="grey5",foreground="thistle3")
        IDE_terminal.configure(bg="black",foreground="lime green")
        is_dark = True
    else:
        IDE_editor.configure(bg="white",foreground="black")
        IDE_terminal.configure(bg="gainsboro",foreground="black")
        is_dark = False

def set_open_file_path(path):
    global open_file_path
    open_file_path = path

def open_file():
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        code = file.read()
        IDE_editor.delete("1.0",END)
        IDE_editor.insert("1.0",code)
        set_open_file_path(path)

def save_as():
    path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'w') as file:
        code = IDE_editor.get("1.0",END)
        file.write(code)
        set_open_file_path(path)
        
def save():
    global open_file_path
    if open_file_path == "":
        save_as()
    else:
        path = open_file_path
    with open(path, 'w') as file:
        code = IDE_editor.get("1.0",END)
        file.write(code)
        set_open_file_path(path)

def unsaved_changes_window():
    prompt = Toplevel()
    text = Label(prompt, text="Unsaved Changes",height=5,width=50)
    save_button = Button(prompt, text="Save", command=save)
    cancel_button = Button(prompt, text="Cancel",command=prompt.destroy)
    save_button.pack()
    cancel_button.pack()
    text.pack()

def open_recent_file():
    global open_file_path
    if open_file_path == "":
        prompt = Toplevel()
        text = Label(prompt, text="No Recent File Found!",height=5,width=50)
        text.pack()
    else:
        save()
        path = open_file_path
        with open(path, 'r') as file:
            code = file.read()
            IDE_editor.delete("1.0",END)
            IDE_editor.insert("1.0",code)
            set_open_file_path(path)

def new_file():
    global IDE_editor
    global open_file_path
    if open_file_path == "":
        save_as()
    else:
        path = open_file_path
        with open(path, 'r') as file:
            code = file.read()
            if IDE_editor.get("1.0",END) != code:
                unsaved_changes_window()
    IDE_editor.delete("1.0",END)
    IDE_editor.insert("1.0","")

def close():
    save()
    IDE_window.quit

def intro():
    save_prompt = Toplevel()
    text = Label(save_prompt, text="Python IDE \nmade by\nhttps://github.com/devika-singh \nfor \nCodePeak 2022\nGithub of Project \nhttps://github.com/World-of-ML/Play-With-Python")
    text.pack(padx=5,pady=5)


def run():
    global open_file_path
    if open_file_path == "":
        unsaved_changes_window()
    command = f'python {open_file_path}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    IDE_terminal.insert(END, output)
    IDE_terminal.insert(END, error)

#menu
menu = Menu(IDE_window)
IDE_window.config(menu=menu)


filemenu = Menu(menu, tearoff= False)
menu.add_cascade(label="File",menu=filemenu)
filemenu.add_command(label="New File", command=new_file)
filemenu.add_command(label="Open..", command=open_file)
filemenu.add_command(label="Open Recent File",command=open_recent_file)
filemenu.add_separator()
filemenu.add_command(label="Save             ",command=save)
filemenu.add_command(label="Save As...       ",command=save_as)
filemenu.add_separator()
filemenu.add_command(label="Close            ",command=close)
filemenu.add_command(label="Exit without Saving            ",command=IDE_window.quit)

editmenu = Menu(menu, tearoff= False)
menu.add_cascade(label="Edit",menu=editmenu)
editmenu.add_command(label="Undo",command=IDE_editor.edit_undo)
editmenu.add_command(label="Redo",command=IDE_editor.edit_redo)
editmenu.add_command(label="Reset",command=IDE_editor.edit_reset)

run_menu = Menu(menu, tearoff= False)
menu.add_cascade(label="Run",menu=run_menu)
run_menu.add_command(label="Run Module",command=run)

optionsmenu = Menu(menu, tearoff= False)
menu.add_cascade(label="Options",menu=optionsmenu)
optionsmenu.add_command(label="Change Mode", command=switch_mode)

helpmenu = Menu(menu, tearoff= False)
menu.add_cascade(label="Help",menu=helpmenu)
helpmenu.add_command(label="About IDE",command=intro)


IDE_window.mainloop()