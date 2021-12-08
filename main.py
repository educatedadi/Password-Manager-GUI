from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]

    shuffle(password_list)
    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_btn_clicked():
    website_name = (website_entry.get()).title()
    user_email = email_entry.get()
    user_pass = password_entry.get()

    if website_name and user_pass:
        ok_to_save = True
    else:
        messagebox.showerror(title='Empty Fields', message='Please check all the fields are filled')
        ok_to_save = False

    if ok_to_save:
        is_ok = messagebox.askokcancel(title=website_name,
                                       message=f'These are the entered details : \nEmail: {user_email} '
                                               f'\nPassword: {user_pass} \nIs it okay to save?')

        if is_ok:
            new_data = {website_name:
                {
                    'email': user_email,
                    'password': user_pass,
                }
            }
            try:
                with open('data.json', 'r') as my_file:
                    data = json.load(my_file)
                    data.update(new_data)
            except FileNotFoundError:
                with open('data.json', 'w') as json_file:
                    json.dump(new_data, json_file, indent=4)
            else:
                with open('data.json', 'w') as json_file:
                    json.dump(data, json_file, indent=4)

            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #


def search_password():
    website = (website_entry.get()).title()
    try:
        with open('data.json', 'r') as my_file:
            data = json.load(my_file)
    except FileNotFoundError:
        messagebox.showerror(title='Oops', message='file not found')
    else:
        if website in data.keys():
            website_dict = data[website]
            messagebox.showinfo(website, f'Email : {website_dict["email"]} \nPassword : {website_dict["password"]}')
        else:
            messagebox.showerror('Oops', 'The website you entered is not found in data file')


# ---------------------------- UI SETUP ------------------------------- #

screen = Tk()
screen.title('Password Generator')
screen.config(padx=20, pady=20, bg='white')

canvas = Canvas(width=200, height=190, bg='white', highlightthickness=0)
lock_img = PhotoImage(file='logo.png')
canvas.create_image(100, 95, image=lock_img)
canvas.grid(row=0, column=1)

website_label = Label(text='Website :', bg='white')
website_label.grid(row=1, column=0, pady=5)

email_label = Label(text='Email/Username :', bg='white')
email_label.grid(row=2, column=0, pady=5)

password_label = Label(text='Password :', bg='white')
password_label.grid(row=3, column=0, pady=5)

# Entries
website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(row=1, column=1, pady=5, sticky="EW")

email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2, pady=5, sticky="EW")
email_entry.insert(0, 'your_mail@gmail.com')

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, pady=5, sticky="EW")

# Buttons
generate_pass_btn = Button(text='Generate Password', command=generate_password)
generate_pass_btn.grid(row=3, column=2, pady=5, sticky="EW")

add_btn = Button(text='Add', width=35, command=add_btn_clicked)
add_btn.grid(row=4, column=1, columnspan=2, pady=5, sticky="EW")

search_btn = Button(text='Search', width=15, command=search_password)
search_btn.grid(row=1, column=2)

screen.mainloop()
