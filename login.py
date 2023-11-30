import tkinter as tk
from tkinter import messagebox
import mysql.connector

def check_login():
    student_id = entry_student_id.get()
    password = entry_password.get()

    # Replace the following with your MySQL connection details
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="records"
    )

    cursor = db_connection.cursor()

    # Replace "students" with your actual table name
    query = "SELECT * FROM students WHERE studentid = %s AND password = %s"
    cursor.execute(query, (student_id, password))
    result = cursor.fetchone()

    cursor.close()
    db_connection.close()

    if result:
        messagebox.showinfo("Login Successful", "Welcome, Student!")
        # Add logic to open the main application window or perform other actions
    else:
        messagebox.showerror("Login Failed", "Invalid Student ID or Password")

# Create the main window
window = tk.Tk()
window.attributes('-fullscreen', True)

#window.title("Login System")

# Create login widgets
label_student_id = tk.Label(window, text="Student ID:")
label_password = tk.Label(window, text="Password:")
entry_student_id = tk.Entry(window)
entry_password = tk.Entry(window, show="*")  # Show asterisks for password input
button_login = tk.Button(window, text="Login", command=check_login)

# Place login widgets on the window using the grid geometry manager
# Assign weight to rows and columns for centering
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

label_student_id.grid(row=0, column=0, padx=10, pady=10, sticky="e")
label_password.grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_student_id.grid(row=0, column=1, padx=10, pady=10, sticky="w")
entry_password.grid(row=1, column=1, padx=10, pady=10, sticky="w")
button_login.grid(row=2, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
window.mainloop()
