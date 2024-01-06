import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime, timedelta

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
#Allow any pc to connect to the database use this statement to the main pc where database is located
#     GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'your_password' WITH GRANT OPTION;
#     FLUSH PRIVILEGES;


    cursor = db_connection.cursor()

    # Replace "students" with your actual table name
    query = "SELECT * FROM students WHERE studentid = %s AND password = %s"
    cursor.execute(query, (student_id, password))
    result = cursor.fetchone()


    if result:
        login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        #check if login exists
        existing_session_query = "SELECT * FROM login_sessions WHERE studentid = %s AND login_time = %s"
        cursor.execute(existing_session_query, (student_id, login_time))
        existing_session = cursor.fetchone()
        
        if existing_session:
            #update record
            update_query = "UPDATE login_sessions SET logout_time = NULL WHERE studentid = %s AND login_time = %s"
            cursor.execute(update_query, (student_id, login_time))
        
        else:
            #insert new record
            insert_query = "INSERT INTO login_sessions (studentid, login_time) VALUES (%s, %s)"
            cursor.execute(insert_query, (student_id, login_time))

        db_connection.commit()
        cursor.close()
        db_connection.close()

        window.destroy()
        show_menu(student_id, login_time)
        # Add logic to open the main application window or perform other actions
    else:
        messagebox.showerror("Login Failed", "Invalid Student ID or Password")

    db_connection.commit()
    cursor.close()
    db_connection.close()
    
def on_close_menu(menu_window):
    # Display a message asking the user to log out first
    messagebox.showinfo("Logout Required", "Please log out before closing the menu.")

def logout(menu_window, student_id, login_time):
    # Record the logout time in the database when clicking the Logout button
    logout_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="records"
    )

    cursor = db_connection.cursor()

    update_query = "UPDATE login_sessions SET logout_time = %s WHERE studentid = %s AND login_time = %s"
    cursor.execute(update_query, (logout_time, student_id, login_time))
    db_connection.commit()

    cursor.close()
    db_connection.close()

    menu_window.destroy()

# Function to show the menu window
def show_menu(student_id, login_time):
    menu_window = tk.Tk()
    menu_window.title("Menu")

    # Override the close button behavior
  #  menu_window.protocol("WM_DELETE_WINDOW", lambda: on_close_menu(menu_window))
    
    # Create menu widgets
    label_menu = tk.Label(menu_window, text=f"Welcome {student_id} to the Menu!\nLogin Time: {login_time}")
    button_logout = tk.Button(menu_window, text="Logout", command=lambda: logout(menu_window, student_id, login_time))

    # Place menu widgets on the window
    label_menu.pack(padx=10, pady=10)
    button_logout.pack(pady=10)

    # Start the Tkinter event loop for the menu window
    menu_window.mainloop()

# Create the main window
window = tk.Tk()
window.attributes('-fullscreen', True)
# Set the background color
window.configure(bg="#F9F4D6")

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
