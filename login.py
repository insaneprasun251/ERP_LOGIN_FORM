import tkinter as tk

import mysql.connector

def initialize_connection():
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "12345"
    )

    cursor = conn.cursor()
    create_database(cursor)
    create_table(cursor)

    return conn, cursor

def create_database(cursor):
    cursor.execute("SHOW DATABASES")
    temp = cursor.fetchall()
    databases = [item[0] for item in temp]
     
    if "tutorial" not in databases:
        cursor.execute("CREATE DATABASE tutorial")
     
    cursor.execute("USE tutorial")

	
def create_table(cursor):  
    cursor.execute("SHOW TABLES")
    temp = cursor.fetchall()
    tables = [item[0] for item in temp]
     
    if "users" not in tables:
        cursor.execute("""CREATE TABLE users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            firstName VARCHAR(100),
            lastName VARCHAR(100),
            password VARCHAR(30),
            email VARCHAR(100) UNIQUE,
            gender VARCHAR(100),
            age INT,
            address VARCHAR(200)
        )""")

def login(cursor, data):
    cursor.execute(f"""SELECT * FROM users WHERE email = '{data["email"]}' 
                       AND password = '{data["password"]}' """)
     
    if cursor.fetchone() != None:
        return True
    return False

def register(cursor, conn, data):
    cursor.execute(f"""INSERT INTO users values( 
        NULL,
        '{data["firstName"]}', 
        '{data["lastName"]}', 
        '{data["password"]}', 
        '{data["email"]}', 
        '{data["gender"]}', 
        '{data["age"]}', 
        '{data["address"]}'
    )""")
 
    conn.commit()

def display(cursor, email):
    cursor.execute(f"""SELECT * FROM users WHERE email = '{email}' """)
    tup = cursor.fetchone()
    return tup
 
conn, cursor = initialize_connection()
email = ""
 
def center_window(width, height):
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
 
 
class WelcomeWindow(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Welcome")
        center_window(240, 120)
         
        login_button = tk.Button(self, text="Login", width=10,
                          command=self.open_login_window)
        login_button.pack(padx=20, pady=(20, 10))
         
        register_button = tk.Button(self, text="Register", width=10, 
                          command=self.open_register_window)
        register_button.pack(pady=10)
        self.pack()
         
    def open_login_window(self):
        for widget in self.winfo_children(): 
            widget.destroy()
        self.destroy()
        LoginWindow(self.master)
         
    def open_register_window(self):
        for widget in self.winfo_children(): 
            widget.destroy()
        self.destroy()
        RegisterWindow(self.master)
 
class PopUpWindow(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Pop Up")
        center_window(240, 120)
        tk.Label(self, text="Data Submitted Successfully!").grid(row=4, column=0, sticky="w", pady=20)
        submit_button = tk.Button(self, text="Back", width=8, command=self.back)
        submit_button.grid(row=7, column=0, sticky="w", padx=10, pady=(10, 10))
        self.pack()

    def back(self):
        for widget in self.winfo_children(): 
            widget.destroy()
        self.destroy()
        WelcomeWindow(self.master)
 
class LoginWindow(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Login")
        self.master.resizable(False, False)
        center_window(240, 150)
         
        tk.Label(self, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
         
        tk.Label(self, text="Password:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
         
        submit_button = tk.Button(self, text="Submit", width=8, command=self.submit)
        submit_button.grid(row=2, column=1, sticky="e", padx=10, pady=(10, 0))
 
        submit_button = tk.Button(self, text="Back", width=8, command=self.back)
        submit_button.grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
        self.pack()
             
    def submit(self):
        global email
        data = {}
        data["email"] = self.username_entry.get()
        data["password"] = self.password_entry.get()
        email = self.username_entry.get()
        
        if login(cursor, data) == True:
            print("successful login")
            for widget in self.winfo_children(): 
                widget.destroy()
            self.destroy()
            MainWindow(self.master)
        else:
            print("unsuccessful login")
 
    def back(self):
        for widget in self.winfo_children(): 
            widget.destroy()
        self.destroy()
        WelcomeWindow(self.master)
 
 
class RegisterWindow(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Register")
        self.master.resizable(False, False)
        center_window(320, 350)
         
        tk.Label(self, text="First Name:").grid(row=0, column=0, sticky="w")
        self.first_name_entry = tk.Entry(self, width=26)
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")
         
        tk.Label(self, text="Last Name:").grid(row=1, column=0, sticky="w")
        self.last_name_entry = tk.Entry(self, width=26)
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        tk.Label(self, text="Email:").grid(row=2, column=0, sticky="w")
        self.email_entry = tk.Entry(self, width=26)
        self.email_entry.grid(row=2, column=1, padx=10, pady=10, sticky="e")
         
        tk.Label(self, text="Password:").grid(row=3, column=0, sticky="w")
        self.password_entry = tk.Entry(self, show="*", width=26)
        self.password_entry.grid(row=3, column=1, padx=10, pady=10, sticky="e")
         
        tk.Label(self, text="Gender:").grid(row=4, column=0, sticky="w")
        # self.gender_entry = tk.Entry(self, width=10)
        # self.gender_entry.grid(row=4, column=1, padx=10, pady=10, sticky="e")
        v = tk.StringVar(self, "1") 
        values = {"Male" : "Male", "Female" : "Female"}
        for (text, value) in values.items(): 
            if(text == "Male"):
                tk.Radiobutton(self, text = text, variable = v, value = value).grid(row=4, column=1, padx=0, pady=0, sticky="s")
            else:
                tk.Radiobutton(self, text = text, variable = v, value = value).grid(row=4, column=1, padx=0, pady=0, sticky="e")
        
        self.gender_entry = v
                
         
        tk.Label(self, text="Age:").grid(row=5, column=0, sticky="w")
        self.age_entry = tk.Entry(self, width=10)
        self.age_entry.grid(row=5, column=1, padx=10, pady=10, sticky="e")
         
        tk.Label(self, text="Address:").grid(row=6, column=0, sticky="w")
        self.address_entry = tk.Text(self, width=20, height=3)
        self.address_entry.grid(row=6, column=1, padx=10, pady=10, sticky="e")
         
        submit_button = tk.Button(self, text="Submit", width=8, command=self.submit)
        submit_button.grid(row=7, column=1, padx=10, pady=10, sticky="e")
 
        submit_button = tk.Button(self, text="Back", width=8, command=self.back)
        submit_button.grid(row=7, column=0, sticky="w", padx=10, pady=(10, 10))
        self.pack()
         
    def submit(self):
        data = {}
        data["firstName"]= self.first_name_entry.get()
        data["lastName"]= self.last_name_entry.get()
        data["password"]= self.password_entry.get()
        data["email"]= self.email_entry.get()
        data["gender"]= self.gender_entry.get()
        data["age"]= self.age_entry.get()
        data["address"]= self.address_entry.get(1.0, tk.END)
 
        register(cursor, conn, data)

        for widget in self.winfo_children(): 
            widget.destroy()
        self.destroy()
        PopUpWindow(self.master)

    def back(self):
        for widget in self.winfo_children(): 
            widget.destroy()
        self.destroy()
        WelcomeWindow(self.master)
 
 
class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        center_window(600, 400)
        id = display(cursor, email)

        tk.Label(self, text="ID").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self, text=":").grid(row=1, column=1, padx=10, pady=10)
        tk.Label(self, text=id[0]).grid(row=1, column=2, padx=10, pady=10)

        tk.Label(self, text="First Name").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self, text=":").grid(row=2, column=1, padx=10, pady=10)
        tk.Label(self, text=id[1]).grid(row=2, column=2, padx=10, pady=10)

        tk.Label(self, text="Last Name").grid(row=3, column=0, padx=10, pady=10)
        tk.Label(self, text=":").grid(row=3, column=1, padx=10, pady=10)
        tk.Label(self, text=id[2]).grid(row=3, column=2, padx=10, pady=10)

        tk.Label(self, text="Email").grid(row=4, column=0, padx=10, pady=10)
        tk.Label(self, text=":").grid(row=4, column=1, padx=10, pady=10)
        tk.Label(self, text=id[4]).grid(row=4, column=2, padx=10, pady=10)

        tk.Label(self, text="Gender").grid(row=5, column=0, padx=10, pady=10)
        tk.Label(self, text=":").grid(row=5, column=1, padx=10, pady=10)
        tk.Label(self, text=id[5]).grid(row=5, column=2, padx=10, pady=10)

        tk.Label(self, text="Age").grid(row=6, column=0, padx=10, pady=10)
        tk.Label(self, text=":").grid(row=6, column=1, padx=10, pady=10)
        tk.Label(self, text=id[6]).grid(row=6, column=2, padx=10, pady=10)

        tk.Label(self, text="Address").grid(row=7, column=0, padx=10, pady=10)
        tk.Label(self, text=":").grid(row=7, column=1, padx=10, pady=10)
        tk.Label(self, text=id[7]).grid(row=7, column=2, padx=10, pady=10)
        self.pack()
 
 
root = tk.Tk()
root.eval('tk::PlaceWindow . center')
WelcomeWindow(root)
# lable = tk.Label(root, text="Hello, world!")
# lable.pack()
root.mainloop()