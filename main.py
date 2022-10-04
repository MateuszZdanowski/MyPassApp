from tkinter import *
from tkinter import messagebox
import random
import string
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def create_password():
    ascii_string = string.ascii_lowercase[:-1]
    ascii_string_upper = string.ascii_uppercase[:-1]
    all_ciphers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    symbols = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"]
    random_range = random.randint(2, 4)
    password = []
    for type_of_chars in [ascii_string, ascii_string_upper, all_ciphers, symbols]:
        for one_char in range(random_range):
            random_char = random.choice(type_of_chars)
            password.append(random_char)
    random.shuffle(password)
    ready_password = "".join(password)
    if len(password_entry.get()) == 0:
        password_entry.insert(0, ready_password)
        pyperclip.copy(ready_password)
    else:
        password_entry.delete(0, END)
        password_entry.insert(0, ready_password)
        pyperclip.copy(ready_password)


# ---------------------------- Search For Site ----------------------------- #


def search():
    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
            for key in data:
                if key == website_entry.get():
                    searched_site_name = key
        searched_site_dict = data[searched_site_name]
        searched_mail = searched_site_dict['email']
        searched_password = searched_site_dict['password']
        messagebox.showinfo(title=searched_site_name,
                            message=f"email: {searched_mail}\nPassword: {searched_password}", )
    except UnboundLocalError:
        messagebox.showwarning(title="Wrong Website!", message="Better check website spelling")
    except json.decoder.JSONDecodeError:
        messagebox.showwarning(title="Wrong Website!", message="Better check website spelling")


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            'email': email,
            'password': password,
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty")
    else:
        try:
            with open('data.json', 'r') as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        except json.decoder.JSONDecodeError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40, bg='white')

canvas = Canvas(width=200, height=200, bg='white', highlightthickness=0)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:", bg="white")
website_label.grid(column=0, row=1, sticky="nsew")
email_username_label = Label(text="Email/Username:", bg="white")
email_username_label.grid(column=0, row=2, sticky="nsew")
password_label = Label(text="Password:", bg="white")
password_label.grid(column=0, row=3, sticky="nsew")

# Entries
website_entry = Entry(width=35, bd=2)
website_entry.grid(column=1, row=1, columnspan=2, sticky="nsew")
website_entry.focus()
email_username_entry = Entry(width=35, bd=2)
email_username_entry.grid(column=1, row=2, columnspan=2, sticky="nsew")
email_username_entry.insert(0, "mateonez@gmail.com")
password_entry = Entry(width=21, bd=2)
password_entry.grid(column=1, row=3, sticky="nsew")

# Buttons
generate_password_button = Button(text="Generate Password", command=create_password)
generate_password_button.grid(column=2, row=3, sticky="nsew")
add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky="nsew")
search_button = Button(text="Search", command=search)
search_button.grid(column=2, row=1, sticky="nsew")

window.mainloop()
