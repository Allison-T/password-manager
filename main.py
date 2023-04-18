import tkinter as tk
from tkinter import messagebox
from random import choice, randint, shuffle
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 5))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)

    generated_password = "".join(password_list)

    password_input.insert(0, generated_password)
    window.clipboard_clear()
    window.clipboard_append(generated_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website: {
            'email': email,
            'password': password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops",
                            message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("my_password.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("my_password.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)
            with open("my_password.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            website_input.delete(0, "end")
            email_input.delete(0, "end")
            email_input.insert(0, "username@gmail.com")
            password_input.delete(0, "end")


# ---------------------------Search Password ----------------------------#
def search_password():
    website = website_input.get()
    try:
        with open("my_password.json") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title=website, message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website,
                                message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No detail for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Password Manager")
window.config(padx=20, pady=50)

canvas = tk.Canvas(width=200, height=200, highlightthickness=0)
logo_img = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Label
website_label = tk.Label(text="Website:")
website_label.grid(column=0, row=1, sticky="w")

email_label = tk.Label(text="Email/Username:")
email_label.grid(column=0, row=2, sticky="w")

password_label = tk.Label(text="Password:")
password_label.grid(column=0, row=3, sticky="w")

# Entry
website_input = tk.Entry(window, width=27)
website_input.grid(column=1, row=1, sticky="w")
website_input.focus()

email_input = tk.Entry(width=45)
email_input.grid(column=1, row=2, columnspan=2, sticky="w")
email_input.insert(0, "username@gmail.com")

password_input = tk.Entry(width=27)
password_input.grid(column=1, row=3, sticky="w")

# Button
search_button = tk.Button(text="Search", command=search_password, highlightthickness=0)
search_button.grid(column=2, row=1, sticky="ew")
generate_button = tk.Button(text="Generate Password", command=generate_password, highlightthickness=0)
generate_button.grid(column=2, row=3, sticky="ew")

add_button = tk.Button(text="Add", width=41, command=save, highlightthickness=0)
add_button.grid(column=1, row=4, columnspan=2, sticky="ew")

window.mainloop()
