import tkinter
#import python ,tkinter, mysql and other libraries
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error, IntegrityError
from PIL import Image, ImageTk
from tkinter import filedialog
import re
import tkinter as tk
from datetime import datetime
from tkinter import ttk
import webbrowser

#connecting to the database
voting_systemdb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Croatia@24",
    database="voting_system"
)

#create if not exists the database and the tables
cursor = voting_systemdb.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS voting_system")
cursor.execute("USE voting_system")
cursor.execute("CREATE TABLE IF NOT EXISTS voter (voter_id INT AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255), email VARCHAR(255), address VARCHAR(255), mobile INT, password VARCHAR(255))")
cursor.execute("CREATE TABLE IF NOT EXISTS election (election_id INT AUTO_INCREMENT PRIMARY KEY, election_name VARCHAR(255), start_date DATE, end_date DATE, description VARCHAR(255))")
cursor.execute("CREATE TABLE IF NOT EXISTS candidate (candidate_id INT AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255),gender VARCHAR(45),age INT, address VARCHAR(255), city VARCHAR(255), state VARCHAR(255), zipcode INT, phonenumber INT)")
cursor.execute("CREATE TABLE IF NOT EXISTS party (party_id INT AUTO_INCREMENT PRIMARY KEY, party_name VARCHAR(100), party_symbol VARCHAR(100), party_image VARCHAR(255))")
#for ballot box
cursor.execute("CREATE TABLE IF NOT EXISTS vote (vote_id INT AUTO_INCREMENT PRIMARY KEY,party_name VARCHAR(45), candidate_name VARCHAR(45), username VARCHAR(45), election_name VARCHAR(45))")
cursor.execute("CREATE TABLE IF NOT EXISTS ballot_box (candidate_id INT PRIMARY KEY, election_id INT , party_id INT , election_name VARCHAR(45), candidate_name VARCHAR(45), party_name VARCHAR(45))")

class votingsystem:
        #initializing the class
    def __init__(self, root):
        self.root = root
        self.root.title("Democracy Solutions, Inc")
        self.root.geometry("1200x750")
        self.root.config(bg="white")
        
        self.loginscreen()
    
    #function to destroy all the widgets on the screen
    def loginscreen(self):
        for i in self.root.winfo_children():
            i.destroy()
            
        self.login_frame = Frame(self.root, bg="white")
        self.login_frame.place(x=0, y=0, width=1200, height=750)
        
        self.show_pass_var = tk.IntVar()
        self.password_visible = False
        # adding Logindogpage1 image
        self.bg = Image.open("login screen image.png")
        self.bg = self.bg.resize((1200, 750), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.login_frame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        #adding Welcome text on the top
        self.welcome_label = Label(self.login_frame, text="Empower Your Voice. Vote with Ease", font=("calibri", 20,"bold"), bg="white", fg="grey")
        self.welcome_label.place(x=30, y=40)
        self.welcome_label = Label(self.login_frame, text="Anytime, Anywhere.", font=("calibri", 20,"bold"), bg="white", fg="black")
        self.welcome_label.place(x=30, y=80)
        self.welcome_label = Label(self.login_frame, text="With Democracy Solutions, Inc", font=("calibri", 30,"bold"), bg="white", fg="grey")
        self.welcome_label.place(x=30, y=120)
        
        #adding login text to the login page right side
        self.login_label = Label(self.login_frame, text="Login", font=("calibri", 20,"bold"), bg="white", fg="black")
        self.login_label.place(x=900, y=150)
        
        # adding username labels and entry boxes
        self.username_label = Label(self.login_frame, text="Username", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.username_label.place(x=850, y=200)
        self.username_entry = Entry(self.login_frame, font=("calibri", 15), bg="white", fg="black")
        self.username_entry.place(x=850, y=230)
        
        # adding password labels and entry boxes
        self.password_label = Label(self.login_frame, text="Password", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.password_label.place(x=850, y=270)
        self.password_entry = Entry(self.login_frame, font=("calibri", 15), bg="white", fg="black", show="*")
        self.password_entry.place(x=850, y=300)
        
        # adding show password check button
        self.show_pass = Checkbutton(self.login_frame, text="Show Password", variable=self.show_pass_var, onvalue=1, offvalue=0,bg="white", fg="black")#command=self.show_password
        self.show_pass.place(x=850, y=330)
        
        # adding forgot password button
        self.forgot_pass = Button(self.login_frame, text="Forgot Password?", font=("calibri", 10), bg="white", fg="black", bd=0, cursor="hand2") #command=self.forgot_password
        self.forgot_pass.place(x=860, y=360)
        
        # adding login button
        self.login_button = Button(self.login_frame, text="Login", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.login_authentication)
        self.login_button.place(x=880, y=390)
        
        # adding register button
        self.register_button = Button(self.login_frame, text="Register", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.signupscreen)
        self.register_button.place(x=960, y=390)
        
    def signupscreen(self):
        for i in self.root.winfo_children():
            i.destroy()
            
        self.signup_frame = Frame(self.root, bg="white")
        self.signup_frame.place(x=0, y=0, width=1200, height=750)
        
        self.show_pass_var = tk.IntVar()
        self.password_visible = False
        # adding Logindogpage1 image
        self.bg = Image.open("register.png")
        self.bg = self.bg.resize((1200, 750), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.signup_frame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
    
        # adding register text to the signup page right side
        self.register_label = Label(self.signup_frame, text="Register to Vote", font=("calibri", 20,"bold"), bg="#fffcf5", fg="black")
        self.register_label.place(x=800, y=100)
        
        # add first name label and entry box a bit left to the register text
        self.first_name_label = Label(self.signup_frame, text="First Name", font=("calibri", 15,"bold"), bg="#fffcf5", fg="black")
        self.first_name_label.place(x=650, y=150)
        self.first_name_entry = Entry(self.signup_frame, font=("calibri", 15), bg="#fffcf5", fg="black")
        self.first_name_entry.place(x=650, y=180)
        
        # add last name label and entry box next to the first name entry box
        self.last_name_label = Label(self.signup_frame, text="Last Name", font=("calibri", 15,"bold"), bg="#fffcf5", fg="black")
        self.last_name_label.place(x=870, y=150)
        self.last_name_entry = Entry(self.signup_frame, font=("calibri", 15), bg="#fffcf5", fg="black")
        self.last_name_entry.place(x=870, y=180)
        
        # add email label and entry box below the first name entry box
        self.email_label = Label(self.signup_frame, text="Email", font=("calibri", 15,"bold"), bg="#fffcf5", fg="black")
        self.email_label.place(x=650, y=210)
        self.email_entry = Entry(self.signup_frame, font=("calibri", 15), bg="#fffcf5", fg="black")
        self.email_entry.place(x=650, y=240)
        
        # add home address label and entry box below rhe email entry box
        self.home_address_label = Label(self.signup_frame, text="Home Address", font=("calibri", 15,"bold"), bg="#fffcf5", fg="black")
        self.home_address_label.place(x=650, y=270)
        self.home_address_entry = Entry(self.signup_frame, font=("calibri", 15), bg="#fffcf5", fg="black")
        self.home_address_entry.place(x=650, y=300)
        
        # add phone number label and entry box below the home address entry box
        self.phone_number_label = Label(self.signup_frame, text="Phone Number", font=("calibri", 15,"bold"), bg="#fffcf5", fg="black")
        self.phone_number_label.place(x=650, y=330)
        self.phone_number_entry = Entry(self.signup_frame, font=("calibri", 15), bg="#fffcf5", fg="black")
        self.phone_number_entry.place(x=650, y=360)
        
        # add password label and entry box below the phone number entry box
        self.password_label = Label(self.signup_frame, text="Password", font=("calibri", 15,"bold"), bg="#fffcf5", fg="black")
        self.password_label.place(x=650, y=390)
        self.password_entry = Entry(self.signup_frame, font=("calibri", 15), bg="#fffcf5", fg="black", show="*")
        self.password_entry.place(x=650, y=420)
        
        # add confirm password label and entry box below the password entry box
        self.confirm_password_label = Label(self.signup_frame, text="Confirm Password", font=("calibri", 15,"bold"), bg="#fffcf5", fg="black")
        self.confirm_password_label.place(x=650, y=450)
        self.confirm_password_entry = Entry(self.signup_frame, font=("calibri", 15), bg="#fffcf5", fg="black", show="*")
        self.confirm_password_entry.place(x=650, y=480)
        
        # add register button
        self.register_button = Button(self.signup_frame, text="Register", font=("calibri", 15,"bold"), bg="#fffcf5", fg="black", bd=1, cursor="hand2", command=self.registration_data)
        self.register_button.place(x=770, y=520)
        
        # add back to login button
        self.login_button = Button(self.signup_frame, text="Back", font=("calibri", 15,"bold"), bg="#fffcf5", fg="black", bd=1, cursor="hand2", command=self.loginscreen)
        self.login_button.place(x=870, y=520)
        
    def registration_data(self):
        # get the data from the entry boxes
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        address = self.home_address_entry.get()
        mobile = self.phone_number_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # check if the data is empty
        if first_name == "" or last_name == "" or email == "" or mobile == "" or password == "" or confirm_password == "":
            messagebox.showerror("Error", "All fields are required")
            return
        # email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid Email")
            return
        # mobile validation
        if not re.fullmatch(r"^[0-9]{10}$", mobile):
            messagebox.showerror("Error", "Invalid Mobile Number")
            return
        # password validation
        if len(password) < 8 or not re.search("[a-z]", password) or not re.search("[A-Z]", password) or not re.search("[0-9]", password):
            messagebox.showerror("Error", "Password must contain at least 8 characters, including letters and numbers")
            return
        # check if the password and confirm password are the same
        if password != confirm_password:
            messagebox.showerror("Error", "Password and Confirm Password should be the same")
            return
        # inserting the data to the database
        try:
                cursor = voting_systemdb.cursor()
                
                # Check for duplicate email or mobile
                cursor.execute("SELECT * FROM voter WHERE email = %s OR mobile = %s", (email, mobile))
                existing_user = cursor.fetchone()

                if existing_user:
                    messagebox.showerror("Error", "An account with this email or mobile number already exists.")
                    return

                # inserting the data to the database
                insert_data = "INSERT INTO voter (first_name, last_name, email, address, mobile, password) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_data, (first_name, last_name, email, address, mobile, password))
                voting_systemdb.commit()
                
                messagebox.showinfo("Success", "You have successfully registered")
                self.loginscreen()

        except IntegrityError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

        finally:
            cursor.close()
        
    # login page validation with the database
    def login_authentication(self):
        # get the data from the entry boxes
        self.email = self.username_entry.get()
        password = self.password_entry.get()
        
        # checking the email and password with the database
        cursor = voting_systemdb.cursor()
        select_data = f"SELECT * FROM voter WHERE email = '{self.email}' AND password = '{password}'"
        cursor.execute(select_data)
        user = cursor.fetchone()

        if user:
            self.voter_id = user[0]
            self.first_name = user[1]
            self.last_name = user[2]
            self.email = user[3]
            self.address = user[4]
            self.mobile = user[5]
            self.current_password = user[6]
            self.voter_screen()
        elif self.email == "admin" and password == "admin":
            self.admin_screen()
        else:
            messagebox.showerror("Error", "Invalid Email or Password")
            return

    # add voter screen function
    def voter_screen(self):
        for i in self.root.winfo_children():
            i.destroy()
            
        self.voter_frame = Frame(self.root, bg="white")
        self.voter_frame.place(x=0, y=0, width=1200, height=750)
        
        #add voter image
        # self.bg = Image.open("download.jpg")
        # self.bg = self.bg.resize((1200, 750), Image.LANCZOS)
        # self.bg = ImageTk.PhotoImage(self.bg)
        # self.bg_image = Label(self.voter_frame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        
        # add voter text to the voter page center
        self.voter_label = Label(self.voter_frame, text="Welcome Voter", font=("calibri", 20,"bold"), bg="white", fg="black")
        self.voter_label.place(x=550, y=100)
        
        # add vote button to the left side of the page
        self.vote_button = Button(self.voter_frame, text="Vote", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.vote_screen)
        self.vote_button.place(x=500, y=250)
        
        # add view result button to the left side of the page
        self.view_result_button = Button(self.voter_frame, text="View Result", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.view_result_screen)
        self.view_result_button.place(x=500, y=300)
        
        # add logout button to the right side of the page
        self.logout_button = Button(self.voter_frame, text="Logout", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.loginscreen)
        self.logout_button.place(x=500, y=550)
    
    # admin screen function
    def admin_screen(self):
        for i in self.root.winfo_children():
            i.destroy()
            
        self.admin_frame = Frame(self.root, bg="white")
        self.admin_frame.place(x=0, y=0, width=1200, height=750)
        #add admin image
        self.bg = Image.open("admin.png")
        self.bg = self.bg.resize((1200, 750), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.admin_frame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        
        # add admin text to the admin page center
        self.admin_label = Label(self.admin_frame, text="Welcome Admin", font=("calibri", 20,"bold"), bg="white", fg="black")
        self.admin_label.place(x=550, y=60)
        
        # add create an image as button to the left side of the page
        self.create_elction = Image.open("create_election.png")
        self.create_elction = self.create_elction.resize((80, 80), Image.LANCZOS)
        self.create_elction = ImageTk.PhotoImage(self.create_elction)
        self.create_election_button = Button(self.admin_frame, image=self.create_elction,bg= "white",bd=0, cursor="hand2",command=self.create_election)
        self.create_election_button.place(x=170, y=200)
        self.create_election_lable = Label(self.admin_frame, text="Create Election", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.create_election_lable.place(x=150, y=280)
        
        
        # self.create_election_button = Button(self.admin_frame, text="Create Election", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.create_election)
        # self.create_election_button.place(x=200, y=250)
        
        # add create election candiate image as button to the right side of the page
        self.create_candidate = Image.open("create_candidate.png")
        self.create_candidate = self.create_candidate.resize((70, 70), Image.LANCZOS)
        self.create_candidate = ImageTk.PhotoImage(self.create_candidate)
        self.create_candidate_button = Button(self.admin_frame, image=self.create_candidate,bg= "white",bd=0, cursor="hand2",command=self.create_candidate_screen)
        self.create_candidate_button.place(x=670, y=200)
        # add text to the create candidate button
        self.create_candidate_label = Label(self.admin_frame, text="Create Candidate", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.create_candidate_label.place(x=635, y=270)
        
        # add create party image as button next to the create candidate button
        self.create_party = Image.open("party.png")
        self.create_party = self.create_party.resize((80, 80), Image.LANCZOS)
        self.create_party = ImageTk.PhotoImage(self.create_party)
        self.create_party_button = Button(self.admin_frame, image=self.create_party,bg= "white",bd=0, cursor="hand2",command=self.register_party)
        self.create_party_button.place(x=890, y=190)
        self.create_party_label = Label(self.admin_frame, text="Create Party", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.create_party_label.place(x=880, y=270)
        
        
        # self.delete_election_button = Button(self.admin_frame, text="Delete Election", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.delete_election)
        # self.delete_election_button.place(x=500, y=250)
        
        # add view election image as button below the create election button
        self.view_election = Image.open("view_elections.png")
        self.view_election = self.view_election.resize((80, 80), Image.LANCZOS)
        self.view_election = ImageTk.PhotoImage(self.view_election)
        self.view_election_button = Button(self.admin_frame, image=self.view_election,bg= "white",bd=0, cursor="hand2",command=self.view_election_screen)
        self.view_election_button.place(x=170, y=400)
        self.view_election_lable = Label(self.admin_frame, text="View Elections", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.view_election_lable.place(x=150, y=480)
        
        # self.view_election_button = Button(self.admin_frame, text="View Elections", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2",command=self.view_election_screen)
        # self.view_election_button.place(x=210, y=350)
        # add view result image as button below the view election button
        self.view_result = Image.open("view_results.png")
        self.view_result = self.view_result.resize((80, 80), Image.LANCZOS)
        self.view_result = ImageTk.PhotoImage(self.view_result)
        self.view_result_button = Button(self.admin_frame, image=self.view_result,bg= "white",bd=0, cursor="hand2",command=self.admin_view_result)
        self.view_result_button.place(x=470, y=400)
        self.view_result_lable = Label(self.admin_frame, text="View Results", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.view_result_lable.place(x=450, y=480)
        
        #add ballot image as button below the view result button
        self.ballot = Image.open("ballo-box.png")
        self.ballot = self.ballot.resize((80, 80), Image.LANCZOS)
        self.ballot = ImageTk.PhotoImage(self.ballot)
        self.ballot_button = Button(self.admin_frame, image=self.ballot,bg= "white",bd=0, cursor="hand2",command=self.ballot_box)
        self.ballot_button.place(x=170, y=550)
        self.ballot_lable = Label(self.admin_frame, text="Ballot-Box", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.ballot_lable.place(x=160, y=640)
        
        
        # self.view_result_button = Button(self.admin_frame, text="View Result", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2")
        # self.view_result_button.place(x=510, y=350)
        
        # add create candidate button to the left side of the page
        
        self.delete_elction = Image.open("delete_election.png")
        self.delete_elction = self.delete_elction.resize((70, 70), Image.LANCZOS)
        self.delete_elction = ImageTk.PhotoImage(self.delete_elction)
        self.delete_election_button = Button(self.admin_frame, image=self.delete_elction,bg= "white",bd=0, cursor="hand2",command=self.delete_election)
        self.delete_election_button.place(x=440, y=200)
        self.delete_election_label = Label(self.admin_frame, text="Delete Election", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.delete_election_label.place(x=410, y=270)
        
        # self.create_candidate_button = Button(self.admin_frame, text="Create Candidate", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.create_candidate_screen)
        # self.create_candidate_button.place(x=200, y=450)
        
        # add logout button image as button to the top right side of the page
        self.logout = Image.open("logout.jpeg")
        self.logout = self.logout.resize((50, 30), Image.LANCZOS)
        self.logout = ImageTk.PhotoImage(self.logout)
        self.logout_button = Button(self.admin_frame, image=self.logout,bg= "white",bd=0, cursor="hand2")
        self.logout_button.place(x=1120, y=40)
        self.logout_button.config(command=self.loginscreen)
        
        
        
        # self.logout_button = Button(self.admin_frame, text="Logout", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.loginscreen)
        # self.logout_button.place(x=200, y=600)
        
    def create_election(self):
        for i in self.root.winfo_children():
            i.destroy()
            
        self.create_election_frame = Frame(self.root, bg="white")
        self.create_election_frame.place(x=0, y=0, width=1200, height=750)
        
        #add image to the create election page
        self.bg = Image.open("election.png")
        self.bg = self.bg.resize((1200, 750), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.create_election_frame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        
        
        # add create election text to the create election page right side
        self.create_election_label = Label(self.create_election_frame, text="Create Election", font=("calibri", 20,"bold"), bg="#003d60", fg="white")
        self.create_election_label.place(x=700, y=100)
        

        
        # add election name label and entry box to the left side of the page
        self.election_name_label = Label(self.create_election_frame, text="Election Name", font=("calibri", 15,"bold"), bg="#003d60", fg="white")
        self.election_name_label.place(x=650, y=200)
        self.election_name_entry = Entry(self.create_election_frame, font=("calibri", 15), bg="#003d60", fg="white")
        self.election_name_entry.place(x=650, y=230)
        
        # add Election start date label and entry box to the left side of the page
        self.election_start_date_label = Label(self.create_election_frame, text="Election Start Date", font=("calibri", 15,"bold"), bg="#003d60", fg="white")
        self.election_start_date_label.place(x=650, y=260)
        self.election_start_date_entry = Entry(self.create_election_frame, font=("calibri", 15), bg="#003d60", fg="white")
        self.election_start_date_entry.place(x=650, y=290)
        self.election_start_date_entry.insert(0, "YYYY-MM-DD")
        self.election_start_date_entry.bind('<FocusIn>', self.startdateremove)
        self.election_start_date_entry.bind('<FocusOut>', self.startdateremove)
        
        # add Election end date label and entry box to the right side of the election start date entry box
        self.election_end_date_label = Label(self.create_election_frame, text="Election End Date", font=("calibri", 15,"bold"), bg="#003d60", fg="white")
        self.election_end_date_label.place(x=880, y=260)
        self.election_end_date_entry = Entry(self.create_election_frame, font=("calibri", 15), bg="#003d60", fg="white")
        self.election_end_date_entry.place(x=880, y=290)
        self.election_end_date_entry.insert(0, "YYYY-MM-DD")
        self.election_end_date_entry.bind('<FocusIn>', self.enddateremove)
        self.election_end_date_entry.bind('<FocusOut>', self.enddateremove)
        
        # add election description label and entry box to the left side of the page
        self.election_description_label = Label(self.create_election_frame, text="Election Description", font=("calibri", 15,"bold"), bg="#003d60", fg="white")
        self.election_description_label.place(x=650, y=320)
        self.election_description_entry = Entry(self.create_election_frame, font=("calibri", 15), bg="#003d60", fg="white",width=30)
        self.election_description_entry.place(x=650, y=350)
        
        # add create election button
        self.create_election_button = Button(self.create_election_frame, text="Register Election", font=("calibri", 15,"bold"), bg="#003d60", fg="white", bd=1, cursor="hand2", command=self.register_election)
        self.create_election_button.place(x=650, y=460)
        
        # add back to admin button to the right side bottom of the page
        self.back_button = Button(self.create_election_frame, text="Back to Admin Page", font=("calibri", 15,"bold"), bg="#003d60", fg="white", bd=1, cursor="hand2", command=self.admin_screen)
        self.back_button.place(x=920, y=600)
        
    
    
        #creating entry lable inside the start date and end date entry boxes
    def startdateremove(self, event):
        if self.election_start_date_entry.get() == "YYYY-MM-DD":
            self.election_start_date_entry.delete(0, "end")
            self.election_start_date_entry.config(fg="white")
        elif self.election_start_date_entry.get() == "":
            self.election_start_date_entry.insert(0, "YYYY-MM-DD")
            self.election_start_date_entry.config(fg="white") 
    
    def enddateremove(self, event):
        if self.election_end_date_entry.get() == "YYYY-MM-DD":
            self.election_end_date_entry.delete(0, "end")
            self.election_end_date_entry.config(fg="white")
            
        elif self.election_end_date_entry.get() == "":
            self.election_end_date_entry.insert(0, "YYYY-MM-DD")
            self.election_end_date_entry.config(show="")
            self.election_end_date_entry.config(fg="white") 
    
    
    def register_election(self):
        # get the data from the entry boxes
        election_name = self.election_name_entry.get()
        start_date = self.election_start_date_entry.get()
        end_date = self.election_end_date_entry.get()
        description = self.election_description_entry.get()
        
        # check if the data is empty
        if election_name == "" or start_date == "" or end_date == "" or description == "":
            messagebox.showerror("Error", "All fields are required")
            return
        
        # inserting the data to the database
        try:
            cursor = voting_systemdb.cursor()

            # inserting the data to the database
            insert_data = "INSERT INTO election (election_name, start_date, end_date, description) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_data, (election_name, start_date, end_date, description))
            voting_systemdb.commit()
            
            messagebox.showinfo("Success", "Election created successfully")
        
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        
        finally:
            cursor.close()
    
    def create_candidate_screen(self):
        for i in self.root.winfo_children():
            i.destroy()
            
        self.create_candidate_frame = Frame(self.root, bg="white")
        self.create_candidate_frame.place(x=0, y=0, width=1200, height=750)
        
        #add image to the create candidate page
        self.bg = Image.open("candidate.png")
        self.bg = self.bg.resize((1200, 750), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.create_candidate_frame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        
        # add create candidate text to the create candidate page right side
        self.create_candidate_label = Label(self.create_candidate_frame, text="Create Candidate", font=("calibri", 20,"bold"), bg="white", fg="black")
        self.create_candidate_label.place(x=750, y=100)
        
        #add candidate first name label and entry box to the left side of the page
        self.candidate_first_name_label = Label(self.create_candidate_frame, text="First Name", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.candidate_first_name_label.place(x=650, y=200)
        self.candidate_first_name_entry = Entry(self.create_candidate_frame, font=("calibri", 15), bg="white", fg="black")
        self.candidate_first_name_entry.place(x=650, y=230)
        
        #add candidate last name label and entry box to the right side of the page
        self.candidate_last_name_label = Label(self.create_candidate_frame, text="Last Name", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.candidate_last_name_label.place(x=850, y=200)
        self.candidate_last_name_entry = Entry(self.create_candidate_frame, font=("calibri", 15), bg="white", fg="black")
        self.candidate_last_name_entry.place(x=850, y=230)
        
        # add candidate gender radio buttons 
       # Variable to store the selected gender
        self.gender_var = StringVar()
        

        # Add candidate gender label
        self.candidate_gender_label = Label(self.create_candidate_frame, text="Gender", font=("calibri", 15, "bold"), bg="white", fg="black")
        self.candidate_gender_label.place(x=650, y=300)

        # Add male gender radio button (with circular indicator)
        self.male_radio = Radiobutton(self.create_candidate_frame, text="Male", variable=self.gender_var, value="Male", font=("calibri", 15), bg="white", fg="black")
        self.male_radio.place(x=650, y=330)

        # Add female gender radio button (with circular indicator)
        self.female_radio = Radiobutton(self.create_candidate_frame, text="Female", variable=self.gender_var, value="Female", font=("calibri", 15), bg="white", fg="black")
        self.female_radio.place(x=750, y=330)

        # Add other gender radio button (with circular indicator)
        self.other_radio = Radiobutton(self.create_candidate_frame, text="Other", variable=self.gender_var, value="Other", font=("calibri", 15), bg="white", fg="black")
        self.other_radio.place(x=850, y=330)
        
        # Set default value
        self.gender_var.set(" ")
        
       

        # candidate age label and entry box
        self.candidate_age_label = Label(self.create_candidate_frame, text="Age", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.candidate_age_label.place(x=650, y=360)
        self.candidate_age_entry = Entry(self.create_candidate_frame, font=("calibri", 15), bg="white", fg="black")
        self.candidate_age_entry.place(x=650, y=390)
        
        #candidate address label and entry box
        self.candidate_address_label = Label(self.create_candidate_frame, text="Address", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.candidate_address_label.place(x=650, y=420)
        self.candidate_address_entry = Entry(self.create_candidate_frame, font=("calibri", 15), bg="white", fg="black")
        self.candidate_address_entry.place(x=650, y=450)
        
        #city label and entry box
        self.candidate_city_label = Label(self.create_candidate_frame, text="City", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.candidate_city_label.place(x=650, y=480)
        self.candidate_city_entry = Entry(self.create_candidate_frame, font=("calibri", 15), bg="white", fg="black")
        self.candidate_city_entry.place(x=650, y=510)
        
        #state label and entry box
        self.candidate_state_label = Label(self.create_candidate_frame, text="State", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.candidate_state_label.place(x=850, y=480)
        self.candidate_state_entry = Entry(self.create_candidate_frame, font=("calibri", 15), bg="white", fg="black")
        self.candidate_state_entry.place(x=850, y=510)
        
        #zip code label and entry box
        self.candidate_zip_code_label = Label(self.create_candidate_frame, text="Zip Code", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.candidate_zip_code_label.place(x=650, y=540)
        self.candidate_zip_code_entry = Entry(self.create_candidate_frame, font=("calibri", 15), bg="white", fg="black")
        self.candidate_zip_code_entry.place(x=650, y=570)
        
        #phone number label and entry box in next line
        self.candidate_phone_number_label = Label(self.create_candidate_frame, text="Phone Number", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.candidate_phone_number_label.place(x=650, y=600)
        self.candidate_phone_number_entry = Entry(self.create_candidate_frame, font=("calibri", 15), bg="white", fg="black")
        self.candidate_phone_number_entry.place(x=650, y=630)
        
        #create candidate button
        self.create_candidate_button = Button(self.create_candidate_frame, text="Register Candidate", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.register_candidate)
        self.create_candidate_button.place(x=650, y=680)
        
        #back to admin button
        self.back_button = Button(self.create_candidate_frame, text="Back to Admin Page", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.admin_screen)
        self.back_button.place(x=850, y=680)
        
        
        
    def register_candidate(self):
        # get the data from the entry boxes
        first_name = self.candidate_first_name_entry.get()
        last_name = self.candidate_last_name_entry.get()
        gender = self.gender_var.get()
        age = self.candidate_age_entry.get()
        address = self.candidate_address_entry.get()
        city = self.candidate_city_entry.get()
        state = self.candidate_state_entry.get()
        zip_code = self.candidate_zip_code_entry.get()
        phone_number = self.candidate_phone_number_entry.get()
        
        
        #check if the data is empty
        if first_name == "" or last_name == "" or age == "" or address == "" or city == "" or state == "" or zip_code == "" or phone_number == "":
            messagebox.showerror("Error", "All fields are required")
            return
        #inserting the data to the database
        try:
            cursor = voting_systemdb.cursor()
            # inserting the data to the database
            insert_data = "INSERT INTO candidate (first_name, last_name,gender, age, address, city, state, zipcode, phonenumber) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_data, (first_name, last_name,gender, age, address, city, state, zip_code, phone_number))
            voting_systemdb.commit()
            
            messagebox.showinfo("Success", "Candidate created successfully")
        
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        
        finally:
            cursor.close()
    
    def view_election_screen(self):
        for i in self.root.winfo_children():
            i.destroy()
            
        self.view_election_frame = Frame(self.root, bg="white")
        self.view_election_frame.place(x=0, y=0, width=1200, height=750)
        
        #add image to the view election page
        self.bg = Image.open("viewelections.png")
        self.bg = self.bg.resize((1200, 750), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.view_election_frame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        
        # add view election text to the view election page right side
        self.view_election_label = Label(self.view_election_frame, text="View Elections", font=("calibri", 20,"bold"), bg="#15196e", fg="white")
        self.view_election_label.place(x=550, y=50)
        
        #show the election details
        cursor = voting_systemdb.cursor()
        select_data = "SELECT election_name,start_date,end_date,description FROM election"
        cursor.execute(select_data)
        elections = cursor.fetchall()
        
        #display the election details from the database not as a treeview with heading
        
        for i, election in enumerate(elections):
            #heading for the election details
            
            
            election_name_heading = Label(self.view_election_frame, text="Election Name", font=("calibri", 15,"bold"), bg="#15196e", fg="white")
            election_name_heading.place(x=50, y=120)
            
            election_start_date_heading = Label(self.view_election_frame, text="Start Date", font=("calibri", 15,"bold"), bg="#15196e", fg="white")
            election_start_date_heading.place(x=250, y=120)
            
            election_end_date_heading = Label(self.view_election_frame, text="End Date", font=("calibri", 15,"bold"), bg="#15196e", fg="white")
            election_end_date_heading.place(x=450, y=120)
            
            election_description_heading = Label(self.view_election_frame, text="Description", font=("calibri", 15,"bold"), bg="#15196e", fg="white")
            election_description_heading.place(x=650, y=120)
            
            election_name = Label(self.view_election_frame, text=election[0], font=("calibri", 15,"bold"), bg="#15196e", fg="white")
            election_name.place(x=50, y=150+(i*30))
            
            start_date = Label(self.view_election_frame, text=election[1], font=("calibri", 15,"bold"), bg="#15196e", fg="white")
            start_date.place(x=250, y=150+(i*30))
            
            end_date = Label(self.view_election_frame, text=election[2], font=("calibri", 15,"bold"), bg="#15196e", fg="white")
            end_date.place(x=450, y=150+(i*30))
            
            description = Label(self.view_election_frame, text=election[3], font=("calibri", 15,"bold"), bg="#15196e", fg="white")
            description.place(x=650, y=150+(i*30))
            
            
            
            
            #add delete election button for each election entry
            # delete_election_button = Button(self.view_election_frame, text="Delete", font=("calibri", 15,"bold"), bg="#15196e", fg="white", bd=1, cursor="hand2", command=self.delete_election)
            # delete_election_button.place(x=850, y=y_position)
            # y_position += 30
            
        
        
        # # add treeview to show the election details
        # self.election_tree = ttk.Treeview(self.view_election_frame, columns=("Election Name", "Start Date", "End Date", "Description"), height=15)
        # style = ttk.Style()
        # style.configure("Treeview", background="#black", foreground="black", fieldbackground="#15196e")
        # style.configure("Treeview.Heading", background="#15196e", foreground="#15196e",fieldbackground="#15196e")
        # self.election_tree.heading("#1", text="Election Name")
        # self.election_tree.heading("#2", text="Start Date")
        # self.election_tree.heading("#3", text="End Date")
        # self.election_tree.heading("#4", text="Description")
        # self.election_tree["show"] = "headings"
        # self.election_tree.place(x=50, y=150)
        
        # for election in elections:
        #     self.election_tree.insert("", "end", values=election)
            
        
        # add back to admin button to the left side bottom of the page
        self.back_button = Button(self.view_election_frame, text="Back to Admin Page", font=("calibri", 15,"bold"), bg="#15196e", fg="white", bd=1, cursor="hand2", command=self.admin_screen)
        self.back_button.place(x=100, y=600)
    
    # def delete_election(self):
        
    #     for i in self.root.winfo_children():
    #         i.destroy()
            
    #     self.delete_election_frame = Frame(self.root, bg="white")
    #     self.delete_election_frame.place(x=0, y=0, width=1200, height=750)
        
    #     #add image to the view election page
    #     self.bg = Image.open("viewelections.png")
    #     self.bg = self.bg.resize((1200, 750), Image.LANCZOS)
    #     self.bg = ImageTk.PhotoImage(self.bg)
    #     self.bg_image = Label(self.delete_election_frame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        
    #     # add view election text to the view election page right side
    #     self.view_election_label = Label(self.delete_election_frame, text="delete Elections", font=("calibri", 20,"bold"), bg="#15196e", fg="white")
    #     self.view_election_label.place(x=550, y=50)
        
    #     #show the election details
    #     cursor = voting_systemdb.cursor()
    #     select_data = "SELECT election_name,start_date,end_date,description FROM election"
    #     cursor.execute(select_data)
    #     elections = cursor.fetchall()
        
    #     #display the election details from the database not as a treeview with heading
        
    #     for i, election in enumerate(elections):
            
    #         #heading for the election details
    #         election_name_heading = Label(self.view_election_frame, text="Election Name", font=("calibri", 15,"bold"), bg="#15196e", fg="white")
    #         election_name_heading.place(x=50, y=120)
            
    #         election_start_date_heading = Label(self.view_election_frame, text="Start Date", font=("calibri", 15,"bold"), bg="#15196e", fg="white")
    #         election_start_date_heading.place(x=250, y=120)
            
    #         election_end_date_heading = Label(self.view_election_frame, text="End Date", font=("calibri", 15,"bold"), bg="#15196e", fg="white")
    #         election_end_date_heading.place(x=450, y=120)
            
    #         election_description_heading = Label(self.view_election_frame, text="Description", font=("calibri", 15,"bold"), bg="#15196e", fg="white")
    #         election_description_heading.place(x=650, y=120)
            
    #         election_name = Label(self.view_election_frame, text=election[0], font=("calibri", 15,"bold"), bg="#15196e", fg="white")
    #         election_name.place(x=50, y=150+(i*30))
            
    #         start_date = Label(self.view_election_frame, text=election[1], font=("calibri", 15,"bold"), bg="#15196e", fg="white")
    #         start_date.place(x=250, y=150+(i*30))
            
    #         end_date = Label(self.view_election_frame, text=election[2], font=("calibri", 15,"bold"), bg="#15196e", fg="white")
    #         end_date.place(x=450, y=150+(i*30))
            
    #         description = Label(self.view_election_frame, text=election[3], font=("calibri", 15,"bold"), bg="#15196e", fg="white")
    #         description.place(x=650, y=150+(i*30))
            
            
        
        
        
        
    #     # add back to admin button to the left side bottom of the page
    #     self.back_button = Button(self.view_election_frame, text="Back to Admin Page", font=("calibri", 15,"bold"), bg="#15196e", fg="white", bd=1, cursor="hand2", command=self.admin_screen)
    #     self.back_button.place(x=100, y=600)
    
    def delete_election(self):
        
        for i in self.root.winfo_children():
            i.destroy()
            
        self.delete_election_frame = Frame(self.root, bg="white")
        self.delete_election_frame.place(x=0, y=0, width=1200, height=750)
        
        #add image to the view election page
        self.bg = Image.open("viewelections.png")
        self.bg = self.bg.resize((1200, 750), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.delete_election_frame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        
        # add delete election text to the view election page center
        
        self.delete_election_label = Label(self.delete_election_frame, text="Delete Election", font=("calibri", 20,"bold"), bg="#15196e", fg="white")
        self.delete_election_label.place(x=550, y=50)
        
        
        #create a dropdown to select the election to delete
        #show the election details
        cursor = voting_systemdb.cursor()
        select_data = "SELECT election_name FROM election"
        cursor.execute(select_data)
        elections = cursor.fetchall()
        
        election_list = []
        
        for election in elections:
            election_list.append(election[0])
            
        self.election_var = StringVar()
        self.election_var.set("Select Election")
        self.election_entry = ttk.Combobox(self.root, textvariable=self.election_var, values=election_list, state="readonly")
        self.election_entry.place(x=500, y=200)
        
        #add delete button
        self.delete_button = Button(self.root, text="Delete", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.delete_election_data)
        self.delete_button.place(x=500, y=250)
        
        #add back to admin button
        self.back_button = Button(self.root, text="Back to Admin Page", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.admin_screen)
        self.back_button.place(x=500, y=300)
        
    def delete_election_data(self):
        election_name = self.election_var.get()
        
        if election_name == "Select Election":
            messagebox.showerror("Error", "Select an Election")
            return
        
        # delete election row from the database and show the remaining election
        cursor = voting_systemdb.cursor()
        delete_data = "DELETE FROM election WHERE election_name = %s"
        cursor.execute(delete_data, (election_name,))
        voting_systemdb.commit()
        messagebox.showinfo("Success", "Election deleted successfully")
        self.view_election_screen()
        
        
        # # delete election row from the database and show the remaining election
        # cursor = voting_systemdb.cursor()
        # delete_data = "DELETE FROM election WHERE election_name = %s"
        # cursor.execute(delete_data, (election_name,))
        # voting_systemdb.commit()
        # messagebox.showinfo("Success", "Election deleted successfully")
        # self.view_election_screen()
        
    def vote_screen(self):
        for i in self.root.winfo_children():
            i.destroy()
            
        self.vote_frame = Frame(self.root, bg="white")
        self.vote_frame.place(x=0, y=0, width=1200, height=750)
        
        #add image to the vote page
        # self.bg = Image.open("vote.png")
        # self.bg = self.bg.resize((1200, 750), Image.LANCZOS)
        # self.bg = ImageTk.PhotoImage(self.bg)
        # self.bg_image = Label(self.vote_frame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        
        # add vote text to the vote page center
        self.vote_label = Label(self.vote_frame, text="Choose your election", font=("calibri", 20,"bold"), bg="white", fg="black")
        self.vote_label.place(x=550, y=100)
        
        #show the avaliable elections in the dropdown from ballot box
        cursor = voting_systemdb.cursor()
        select_data = "SELECT DISTINCT election_name FROM ballot_box"
        cursor.execute(select_data)
        elections = cursor.fetchall()
        
        election_list = []
        
        for election in elections:
            election_list.append(election[0])
            
        self.election_var = StringVar()
        self.election_var.set("Select Election")
        self.election_entry = ttk.Combobox(self.vote_frame, textvariable=self.election_var, values=election_list, state="readonly")
        self.election_entry.place(x=500, y=200)
        
        #next button to show the candidates with party name and image
        self.next_button = Button(self.vote_frame, text="Next", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.show_candidates)
        self.next_button.place(x=500, y=250)
        
        #add back to home button
        self.back_button = Button(self.vote_frame, text="Back to Home", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.home_screen)
        self.back_button.place(x=500, y=300)
        
    def show_candidates(self):
        for i in self.vote_frame.winfo_children():
            i.destroy()
        
        #create a frame to show the candidates
        self.vote_frame = Frame(self.root, bg="white")
        self.vote_frame.place(x=0, y=0, width=1200, height=750)
        
        self.vote_label = Label(self.vote_frame, text="Choose your candidate", font=("calibri", 20,"bold"), bg="white", fg="black")
        self.vote_label.place(x=550, y=50)
        
        #validate if the user has already voted in this election
        cursor = voting_systemdb.cursor()
        select_data = "SELECT * FROM vote WHERE username = %s"
        cursor.execute(select_data, (self.email,))
        votes = cursor.fetchall()
        
        for vote in votes:
            if vote[4] == self.election_var.get():
                messagebox.showerror("Error", "You have already voted in this election")
                self.vote_screen()
                return
       
        
        
        
        
        
        
        election_name = self.election_var.get()
        
        if election_name == "Select Election":
            messagebox.showerror("Error", "Select an Election")
            return
        
        # Add headings
        candidate_name_heading = Label(self.vote_frame, text="Candidate Name", font=("calibri", 15,"bold"), bg="white", fg="black")
        candidate_name_heading.place(x=50, y=100)
        
        party_name_heading = Label(self.vote_frame, text="Party Name", font=("calibri", 15,"bold"), bg="white", fg="black")
        party_name_heading.place(x=250, y=100)
        
        party_symbol_heading = Label(self.vote_frame, text="Party Symbol", font=("calibri", 15,"bold"), bg="white", fg="black")
        party_symbol_heading.place(x=450, y=100)
        
        # Fetch candidates in the election from the database
        cursor = voting_systemdb.cursor()
        select_data = """
            SELECT bb.candidate_name, bb.party_name, p.party_image 
            FROM ballot_box as bb 
            LEFT JOIN party as p ON p.party_id = bb.party_id  
            WHERE bb.election_name = %s
        """
        cursor.execute(select_data, (election_name,))
        candidates = cursor.fetchall()
        
        self.candidate_var = StringVar()  # To store the selected candidate name
        self.candidate_var.set(None)  # Set the default value to None
        self.party_var = StringVar()  # To store the selected party name
        
        for i, candidate in enumerate(candidates):
            candidate_name = Label(self.vote_frame, text=candidate[0], font=("calibri", 15,"bold"), bg="white", fg="black")
            candidate_name.place(x=50, y=150+(i*150))
            
            party_name = Label(self.vote_frame, text=candidate[1], font=("calibri", 15,"bold"), bg="white", fg="black")
            party_name.place(x=250, y=150+(i*150))
            
            party_image = Image.open(candidate[2])
            party_image = party_image.resize((100, 100), Image.LANCZOS)
            party_image = ImageTk.PhotoImage(party_image)
            party_image_label = Label(self.vote_frame, image=party_image)
            party_image_label.image = party_image
            party_image_label.place(x=450, y=150+(i*150))
            
            # Store both candidate name and party name in the value of the radio button
            candidate_radio = Radiobutton(self.vote_frame, text=candidate[0], variable=self.candidate_var, value=candidate[0], font=("calibri", 15), bg="white", fg="black", command=lambda c=candidate[0], p=candidate[1]: self.update_party(c, p))
            candidate_radio.place(x=650, y=150+(i*150))
        
        # Add vote button
        self.vote_button = Button(self.vote_frame, text="Vote", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.vote_capture)
        self.vote_button.place(x=500, y=600)
        
        # Add back to home button
        self.back_button = Button(self.vote_frame, text="Back to Home", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.home_screen)
        self.back_button.place(x=500, y=650)

    def update_party(self, candidate_name, party_name):
        self.candidate_var.set(candidate_name)
        self.party_var.set(party_name)

    def vote_capture(self):
        candidate_name = self.candidate_var.get()
        party_name = self.party_var.get()
        
        #get election name from the election dropdown
        election_name = self.election_var.get()
        
        # Get the user's first name and last name from the login page
        username= self.email
        
        if candidate_name == "":
            messagebox.showerror("Error", "Select a Candidate")
            return
        
        # Insert the party name, candidate name, and user first and last name into the vote table
        cursor = voting_systemdb.cursor()
        insert_data = "INSERT INTO vote (party_name, candidate_name, username,election_name) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_data, (party_name, candidate_name, username,election_name))
        voting_systemdb.commit()  # Commit the transaction
        
        messagebox.showinfo("Success", "Vote casted successfully")
            
    def view_result_screen(self):
        for i in self.root.winfo_children():
            i.destroy()
            
        self.view_result_frame = Frame(self.root, bg="white")
        self.view_result_frame.place(x=0, y=0, width=1200, height=750)
        
        #add image to the view result page
        # self.bg = Image.open("viewresult.png")
        # self.bg = self.bg.resize((1200, 750), Image.LANCZOS)
        # self.bg = ImageTk.PhotoImage(self.bg)
        # self.bg_image = Label(self.view_result_frame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        
        # add view result text to the view result page center
        self.view_result_label = Label(self.view_result_frame, text="View Results", font=("calibri", 20,"bold"), bg="#15196e", fg="white")
        self.view_result_label.place(x=550, y=50)
        
        #select the election name from the dropdown
        cursor = voting_systemdb.cursor()
        select_data = "SELECT DISTINCT election_name FROM vote"
        cursor.execute(select_data)
        elections = cursor.fetchall()
        
        election_list = []
        
        for election in elections:
            election_list.append(election[0])
            
        self.election_var = StringVar()
        self.election_var.set("Select Election")
        self.election_entry = ttk.Combobox(self.view_result_frame, textvariable=self.election_var, values=election_list, state="readonly")
        self.election_entry.place(x=500, y=100)
        
        #show the result button
        self.show_result_button = Button(self.view_result_frame, text="Show Result", font=("calibri", 15,"bold"), bg="#15196e", fg="white", bd=1, cursor="hand2", command=self.show_result)
        self.show_result_button.place(x=500, y=150)
        
        #add back to admin button
        self.back_button = Button(self.view_result_frame, text="Back to Admin Page", font=("calibri", 15,"bold"), bg="#15196e", fg="white", bd=1, cursor="hand2", command=self.admin_screen)
        self.back_button.place(x=500, y=200)
        


    def show_result(self):
        for i in self.view_result_frame.winfo_children():
            i.destroy()
        
        self.view_result_frame = Frame(self.root, bg="white")
        self.view_result_frame.place(x=0, y=0, width=1200, height=750)
        
        self.view_result_label = Label(self.view_result_frame, text="View Results", font=("calibri", 20,"bold"), bg="#15196e", fg="white")
        self.view_result_label.place(x=550, y=50)
        
        election_name = self.election_var.get().strip()  # Make sure to strip any extra spaces
        
        if election_name == "Select Election":
            messagebox.showerror("Error", "Select an Election")
            return
        
        # Fetch the end date of the selected election
        cursor = voting_systemdb.cursor()
        select_end_date_query = "SELECT end_date FROM election WHERE election_name = %s"
        cursor.execute(select_end_date_query, (election_name,))
        election_data = cursor.fetchone()
        
        if not election_data:
            messagebox.showerror("Error", f"Election '{election_name}' not found.")
            return
        
        end_date = election_data[0]
        current_date = datetime.now().date()
        
        # Check if the current date is after the election's end date
        if current_date < end_date:
            messagebox.showinfo("Info", f"Results are not available until the election ends on {end_date.strftime('%Y-%m-%d')}")
            return
        
        # Calculate the total number of votes and show the winner for the selected election
        select_data = """
            SELECT candidate_name, COUNT(username) AS total_votes 
            FROM vote 
            WHERE election_name = %s 
            GROUP BY candidate_name 
            ORDER BY total_votes DESC
        """
        cursor.execute(select_data, (election_name,))
        votes = cursor.fetchall()
        
        if not votes:
            messagebox.showinfo("Info", "No votes have been cast for this election.")
            return
        
        # Show the winner
        winner = votes[0][0]
        total_votes = votes[0][1]
        
        winner_label = Label(self.view_result_frame, text=f"Winner: {winner}", font=("calibri", 15,"bold"), bg="#15196e", fg="white")
        winner_label.place(x=550, y=100)
        
        total_votes_label = Label(self.view_result_frame, text=f"Total Votes: {total_votes}", font=("calibri", 15,"bold"), bg="#15196e", fg="white")
        total_votes_label.place(x=550, y=150)
        
        # Show the candidate name and total votes
        candidate_name_label = Label(self.view_result_frame, text="Candidate Name", font=("calibri", 15,"bold"), bg="#15196e", fg="white")
        candidate_name_label.place(x=50, y=200)
        
        total_votes_label = Label(self.view_result_frame, text="Total Votes", font=("calibri", 15,"bold"), bg="#15196e", fg="white")
        total_votes_label.place(x=250, y=200)
        
        for i, vote in enumerate(votes):
            candidate_name = Label(self.view_result_frame, text=vote[0], font=("calibri", 15,"bold"), bg="#15196e", fg="white")
            candidate_name.place(x=50, y=230+(i*30))
            
            total_votes = Label(self.view_result_frame, text=vote[1], font=("calibri", 15,"bold"), bg="#15196e", fg="white")
            total_votes.place(x=250, y=230+(i*30))
        
        # Add back to admin button
        self.back_button = Button(self.view_result_frame, text="Back to Admin Page", font=("calibri", 15,"bold"), bg="#15196e", fg="white", bd=1, cursor="hand2", command=self.admin_screen)
        self.back_button.place(x=100, y=600)
 
    def register_party(self):
        for i in self.root.winfo_children():
            i.destroy()
        
        self.create_party_frame = Frame(self.root, bg="white")
        self.create_party_frame.place(x=0, y=0, width=1200, height=750)
        
        
        # party name lqbel and entry box
        self.party_name_label = Label(self.create_party_frame, text="Party Name", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.party_name_label.place(x=650, y=200)
        self.party_name_entry = Entry(self.create_party_frame, font=("calibri", 15), bg="white", fg="black")
        self.party_name_entry.place(x=650, y=230)
        
        # party symbol label and choose image button
        self.party_symbol_label = Label(self.create_party_frame, text="Party Symbol", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.party_symbol_label.place(x=650, y=260)
        self.party_symbol_entry = Entry(self.create_party_frame, font=("calibri", 15), bg="white", fg="black")
        self.party_symbol_entry.place(x=650, y=290)
        
        self.choose_image_button = Button(self.create_party_frame, text="Choose Image", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.choose_image)
        self.choose_image_button.place(x=850, y=290)
        
        # create party button
        self.create_party_button = Button(self.create_party_frame, text="Register Party", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.register_party_data)
        self.create_party_button.place(x=650, y=350)
        
        # back to admin button
        self.back_button = Button(self.create_party_frame, text="Back to Admin Page", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.admin_screen)
        self.back_button.place(x=850, y=350)
        
    def choose_image(self):
        #CHOOSE IMAGE FUNCTION from the file dialog
        #def upload_image(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetypes=(("JPEG files", "*.jpeg"),("JPG files", "*.jpg"), ("PNG files", "*.png"),("all files", "*.*")))
        print(self.filename)

        #messagebox.showinfo("Success", "Image Uploaded")
        if self.filename:

            messagebox.showinfo("Success", "Image Uploaded")
            self.admin_shoe_image_button.config(text="Image Uploaded")
        else:
            messagebox.showinfo("Error", "No Image Selected")

        
    def register_party_data(self):
        party_name = self.party_name_entry.get()
        party_symbol = self.party_symbol_entry.get()
        party_image = self.filename
        
        if party_name == "" or party_symbol == "":
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            cursor = voting_systemdb.cursor()
            insert_data = "INSERT INTO party (party_name, party_symbol,party_image) VALUES (%s, %s,%s)"
            cursor.execute(insert_data, (party_name, party_symbol,party_image))
            voting_systemdb.commit()
            messagebox.showinfo("Success", "Party created successfully")
        
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        
        finally:
            cursor.close()
    
    def ballot_box(self):
        for i in self.root.winfo_children():
            i.destroy()
        
        self.ballot_box_frame = Frame(self.root, bg="white")
        self.ballot_box_frame.place(x=0, y=0, width=1200, height=750)
        
        # #add image to the ballot box page
        # self.bg = Image.open("ballotbox.png")
        # self.bg = self.bg.resize((1200, 750), Image.LANCZOS)
        # self.bg = ImageTk.PhotoImage(self.bg)
        # self.bg_image = Label(self.ballot_box_frame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        
        # add ballot box text to the ballot box page center
        self.ballot_box_label = Label(self.ballot_box_frame, text="Ballot Box", font=("calibri", 20,"bold"), bg="#15196e", fg="white")
        self.ballot_box_label.place(x=550, y=50)
        
        #show selected election
        cursor = voting_systemdb.cursor()
        select_data = "SELECT CONCAT(election_id, ' - ', election_name) AS election_info FROM election WHERE start_date >= CURDATE()"
        cursor.execute(select_data)
        elections = cursor.fetchall()
        
        election_list = []
        
        for election in elections:
            election_list.append(election[0])
            
        self.election_var = StringVar()
        self.election_var.set("Select Election")
        self.election_entry = ttk.Combobox(self.ballot_box_frame, textvariable=self.election_var, values=election_list, state="readonly")
        self.election_entry.place(x=500, y=200)
        
        #after selection assign it's respective id to election_id and candidate_id variable by using the selected election name
        election_id = 0
        candidate_id = 0
        
        
        #show the candidates from the candidate table 
        # Fetch candidates from the 'candidate' table, including both first and last names
        cursor = voting_systemdb.cursor()

        # SQL query to concatenate first and last name, and fetch the candidate ID as well
        select_data = "SELECT CONCAT(candidate_id,'-',first_name, ' ', last_name) AS full_name FROM candidate"

        # Execute the query
        cursor.execute(select_data)
        candidates = cursor.fetchall()

        # Create a list to store formatted strings with candidate ID and full name
        candidate_list = []

        # Format each entry as "ID - Full Name"
        for candidate in candidates:
            candidate_list.append(candidate[0])

        # Set up the combobox with formatted candidate entries
        self.candidate_var = StringVar()
        self.candidate_var.set("Select Candidate")
        self.candidate_entry = ttk.Combobox(self.ballot_box_frame, textvariable=self.candidate_var, values=candidate_list, state="readonly")
        self.candidate_entry.place(x=500, y=300)

        
        #select party
        cursor = voting_systemdb.cursor()
        select_data = "SELECT CONCAT(party_id, '-', party_name) AS party_info FROM party"
        cursor.execute(select_data)
        parties = cursor.fetchall()
        
        party_list = []
        
        for party in parties:
            party_list.append(party[0])
            
        self.party_var = StringVar()
        self.party_var.set("Select Party")
        self.party_entry = ttk.Combobox(self.ballot_box_frame, textvariable=self.party_var, values=party_list, state="readonly")
        self.party_entry.place(x=500, y=350)
        
        #add to ballot box button
        self.add_to_ballot_box_button = Button(self.ballot_box_frame, text="Add to Ballot Box", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.add_to_ballot_box)
        self.add_to_ballot_box_button.place(x=500, y=400)
        
        #back to admin button
        self.back_button = Button(self.ballot_box_frame, text="Back to Admin Page", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.admin_screen)
        self.back_button.place(x=500, y=500)
        
    def add_to_ballot_box(self):
        election_id = self.election_var.get().split("-")[0]
        candidate_id = self.candidate_var.get().split("-")[0]
        election_name = self.election_var.get().split("-")[1]
        candidate_name = self.candidate_var.get().split("-")[1]
        party_id = self.party_var.get().split("-")[0]
        party_name = self.party_var.get().split("-")[1]
        
        if election_id == "Select Election" or candidate_id == "Select Candidate" or party_name == "Select Party":
            messagebox.showerror("Error", "Select Election, Candidate and Party")
            return
        
        try:
            cursor = voting_systemdb.cursor()
            # Insert the selected candidate into the 'ballot_box' table into election_id, candidate_id, election_name ,candidate_name, party_name
            insert_data = "INSERT INTO ballot_box (election_id, candidate_id, party_id, election_name, candidate_name,  party_name) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_data, (election_id, candidate_id, party_id, election_name, candidate_name, party_name))
            voting_systemdb.commit()
            messagebox.showinfo("Success", "Candidate added to Ballot Box successfully")
        
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        
        finally:
            cursor.close()
        
    def admin_view_result(self):
        #admin needs to select the election to view the result
        for i in self.root.winfo_children():
            i.destroy()
            
        self.admin_view_result_frame = Frame(self.root, bg="white")
        self.admin_view_result_frame.place(x=0, y=0, width=1200, height=750)
        
        #add image to the view result page
        # self.bg = Image.open("viewresult.png")
        # self.bg = self.bg.resize((1200, 750), Image.LANCZOS)
        # self.bg = ImageTk.PhotoImage(self.bg)
        # self.bg_image = Label(self.admin_view_result_frame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        
        # add view result text to the view result page center
        self.view_result_label = Label(self.admin_view_result_frame, text="View Results", font=("calibri", 20,"bold"), bg="#15196e", fg="white")
        self.view_result_label.place(x=550, y=50)
        
        #select the election name from the dropdown
        cursor = voting_systemdb.cursor()
        select_data = "SELECT DISTINCT election_name FROM vote"
        cursor.execute(select_data)
        elections = cursor.fetchall()
        
        election_list = []
        
        for election in elections:
            election_list.append(election[0])

        self.election_var = StringVar()
        
        self.election_var.set("Select Election")
        self.election_entry = ttk.Combobox(self.admin_view_result_frame, textvariable=self.election_var, values=election_list, state="readonly")
        self.election_entry.place(x=500, y=100)
        
        #show the result button
        self.show_result_button = Button(self.admin_view_result_frame, text="Show Result", font=("calibri", 15,"bold"), bg="#15196e", fg="white", bd=1, cursor="hand2", command=self.admin_show_result)
        self.show_result_button.place(x=500, y=150)
        
        #add back to admin button
        self.back_button = Button(self.admin_view_result_frame, text="Back to Admin Page", font=("calibri", 15,"bold"), bg="#15196e", fg="white", bd=1, cursor="hand2", command=self.admin_screen)
        self.back_button.place(x=500, y=200)
        
    def admin_show_result(self):
        for i in self.admin_view_result_frame.winfo_children():
            i.destroy()
        
        self.admin_view_result_frame = Frame(self.root, bg="white")
        self.admin_view_result_frame.place(x=0, y=0, width=1200, height=750)
        
        self.view_result_label = Label(self.admin_view_result_frame, text="View Results", font=("calibri", 20,"bold"), bg="#15196e", fg="white")
        self.view_result_label.place(x=550, y=50)
        
        election_name = self.election_var.get().strip()  # Make sure to strip any extra spaces
        
        if election_name == "Select Election":
            messagebox.showerror("Error", "Select an Election")
            return
        
        # siply show the result of the selected election
        select_data = """
            SELECT candidate_name, COUNT(username) AS total_votes 
            FROM vote 
            WHERE election_name = %s 
            GROUP BY candidate_name 
            ORDER BY total_votes DESC
        """
        cursor = voting_systemdb.cursor()
        cursor.execute(select_data, (election_name,))
        votes = cursor.fetchall()
        
        if not votes:
            messagebox.showinfo("Info", "No votes have been cast for this election.")
            return
        
        # Show the candidate name and total votes
        candidate_name_label = Label(self.admin_view_result_frame, text="Candidate Name", font=("calibri", 15,"bold"), bg="#15196e", fg="white")
        candidate_name_label.place(x=50, y=100)
        
        total_votes_label = Label(self.admin_view_result_frame, text="Total Votes", font=("calibri", 15,"bold"), bg="#15196e", fg="white")
        total_votes_label.place(x=250, y=100)
        
        for i, vote in enumerate(votes):
            candidate_name = Label(self.admin_view_result_frame, text=vote[0], font=("calibri", 15,"bold"), bg="#15196e", fg="white")
            candidate_name.place(x=50, y=130+(i*30))
            
            total_votes = Label(self.admin_view_result_frame, text=vote[1], font=("calibri", 15,"bold"), bg="#15196e", fg="white")
            total_votes.place(x=250, y=130+(i*30))
            
        # Add back to admin button
        self.back_button = Button(self.admin_view_result_frame, text="Back to Admin Page", font=("calibri", 15,"bold"), bg="#15196e", fg="white", bd=1, cursor="hand2", command=self.admin_screen)
        self.back_button.place(x=100, y=600)
        
    

        
        
            
        
        
        
    
      
            
    
        
        
        
        
        
        
        
#starter code
if __name__ == "__main__":
    root = Tk()
    app = votingsystem(root)
    root.mainloop()