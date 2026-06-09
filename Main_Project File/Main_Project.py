from tkinter import Tk,Label,Frame, Entry, Button, simpledialog,messagebox,Image
from tkinter.ttk import Combobox # Dropdown Making library
import time # For Time Functions
import Random_Generator #User created Library for Captcha Generation
import tables # to the import library for the table database form the table.py file
 # The Library for Automating the Mail sending
import sqlite3  # For creatinga a connection between SQL database created in table.py file
tables.create_tables() #table function created in Random_generator file
from PIL import Image, ImageTk # For uploading Image in the Screen
import mailing #For mail sending


                    # ----- MAIN PAGE DETAILS -------#

#Background Colour and Adjustment
root=Tk()       
root.state('zoomed')
root.configure(bg="#0B192C") 


#Running Watch Function (Closing At 29th line)
def update_time():   #Running Watch Function (Closing At 29th line)
    datetime=time.strftime("📅 %d-%b-%y ⏰ %r")
    dt_lbl.configure(text=datetime)
    dt_lbl.after(1000,update_time)

#Title Name and Styling
title_lbl=Label(root,text="BANKING SIMULATOR",font=('Times New Rome',50,'bold','underline'),
                fg='#FFFFFF',bg='#0B192C')
title_lbl.pack() #packing the title label on the root window

#subtitle Name & Styling 
datetime=time.strftime("%d-%b-%y %r")

dt_lbl=Label(root,text=datetime,font=('times new rome',20,'bold'),
             fg='blue',bg='#0B192C')
dt_lbl.pack()
update_time() # Watch time Function calling (ref: 13th line)



#To attch Image logo in the Main screen
img=Image.open("logo.jpg")  #Image name with module+library+function
tkimg=ImageTk.PhotoImage(img,master=root) # The image will be active till the main screen (Root) is active

logo_lbl=Label(root,image=tkimg) #Image Placement on the Mainscreen
logo_lbl.place(relx=.05,rely=0,relwidth=0.15, relheight=0.15) # Positioning the Image


# Nested Function for Main Page (Login Page)
def main_screen():   #Main Frame size and background function (Closing at 104th line)
    
    # Main Frame Inputs and Desigining
    frm=Frame(root,highlightbackground='#FFFFFF',highlightthickness=2)
    frm.configure(bg='#1E3E62')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.72)
    
    def refresh():  #Refresh Button Function (Ref :90th line)
        gen_cap=Random_Generator.captcha()
        cap_im.configure(text=gen_cap)

#Navigator from Forgot Password Button(Main_Page) To forgot password Page
    def forgot():   #Command Usage 108th line
        frm.destroy() #Destroying Main Page Frame
        forgot_screen()
    
#Navigator from login Button(Main_Page) To User Page
    def login():   #Command Usage
        utype=user_combo.get()  #login with referenece to the dropdown(combobox)
        uacn=acn_entry.get()   #login with reference to the account no. entry
        upass=pass_entry.get()
        ucap=cap_entry.get()

# Error msg bos for not entering valid info in the entry boxes
        if len(uacn)==0: # error for the wrong AC no.
            messagebox.showerror("Login","Please Enter AC No.")
            return

        if len(upass)==0: # error for the wrong Password
            messagebox.showerror("Login","Please Enter Password")
            return

        if len(ucap)==0:    # error for the wrong Captcha
            messagebox.showerror("Login","Please Enter Captcha")
            return


        global gen_cap #globalizing the variable
       
        gen_cap=gen_cap.replace(" ","") #Getting the captcha from the entry and removing space for matching 
# Message will shown if the wrong captcha is entered
        if ucap!=gen_cap:
            messagebox.showerror("Login","Invalid Captch")
            return
        
    # function Condition for admin login     
        if utype=="Admin":
            
            if uacn=="0" and upass=="admin": # condition for admin login type = admin, Ac no. =0, Pass=admin
                frm.destroy() #Destroying Main Page Frame
                Admin_screen()
            
            else: #If conditions does not match, pop msg will appear
                messagebox.showerror("Login","Invalid Credentials")

    # function Condition for Customer login              
        elif utype=="Customer":
           
        # Connection B/W Database and Project to fetch customer details   
            conobj=sqlite3.connect(r"D:\CHITRA 8-3-2026\Data_Projects\Full Stack Project\Banking_Simulator_Project\bank.sqlite")
            curobj=conobj.cursor()
            query="select * from accounts where AC_No=? and Password=?" #Query to Fetch the Customer detail on the basis of Account No.
            curobj.execute(query,(uacn,upass)) #matching the Account no. and password from the above query
            tup=curobj.fetchone()
            conobj.close() 

            if tup!=None: # If condition is met
                frm.destroy()  # to destroy the current screen
                Customer_screen(uacn) # Navigated to the Customer Screen with Account No. Login
            else: # if condition is not met
                messagebox.showerror("Login","Invalid Credentials")
        else:
           # message warning pop box for not selecting any type of user
            messagebox.showerror("Login","Please Select User Type") 

# Function for Resenting the entry, Reset Button    
    def reset():
        user_combo.current(0)
        acn_entry.delete(0,"end")
        pass_entry.delete(0,"end")
        cap_entry.delete(0,"end")

        user_combo.focus() #Position of the Curser after the reseting at User




# USER LABEL & DropDown Style & Placement
    user_lbl=Label(frm,text="USER",font=('arial',20,'bold'),fg="#FFFFFF",bg='#1E3E62')
    user_lbl.place(relx=.35,rely=.1)

#Combobox - Making Dropdown
    user_combo=Combobox(frm,values=['-----Select-----','Admin','Customer'],state="readonly",
                        font=('arial',20,'bold'))
    user_combo.place(relx=.42,rely=.1)
    user_combo.current(0)
    

# ACN LABEL & Entry STYLE & PLACEMENT
    acn_lbl=Label(frm,text="A/C No.",font=('arial',20,'bold'),fg="#FFFFFF",bg='#1E3E62')
    acn_lbl.place(relx=.35,rely=.2)

    acn_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    acn_entry.place(relx=.42,rely=.2,width=320)
    acn_entry.focus() #cursor focus on the enty

#Password Label & Entry style & Placement
    pass_lbl=Label(frm,text="Enter Password :",font=('arial',20,'bold'),fg="#FFFFFF",bg='#1E3E62')
    pass_lbl.place(relx=.35,rely=.3)

    pass_entry=Entry(frm,font=('arial',20,'bold'),bd=5,show="*")
    pass_entry.place(relx=.42,rely=.4,width=320)

#Captcha Label & Entry style & Placement
    global gen_cap #Making the variable global so that ti can be used throughout the project
    gen_cap=Random_Generator.captcha() #calling & Storing function in variable
    
    cap_lbl=Label(frm,text="Enter Captcha :",font=('arial',20,'bold'),fg="#FFFFFF",bg='#1E3E62')
    cap_lbl.place(relx=.35,rely=.5)

    cap_im=Label(frm,text=gen_cap,font=('Roboto Black',20,'bold'),fg="Grey")
    cap_im.place(relx=.51,rely=.5)

# Refresh Button Style & Placement
    refresh_btn=Button(frm,text="🔄",font=('Roboto Black',20,'bold'),
                       bg='#008DDA',command=refresh) #Command Ref 40th line function
    refresh_btn.place(relx=.6,rely=.5,width=40,height=40)
    
    cap_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    cap_entry.place(relx=.42,rely=.6,width=320)

#Login Button ---
    login_btn=Button(frm,text="Login",font=('arial',20,'bold'),
                    bg='#008DDA',bd=5,command=login)
    login_btn.place(relx=.44,rely=.7, height=45)

#Reset Button ---
    Reset_btn=Button(frm,text="Reset",font=('arial',20,'bold'),
                       bg='#008DDA',bd=5,command=reset)
    Reset_btn.place(relx=.54,rely=.7,height=45)

# ForgotPassword Button ---
    forgot_btn=Button(frm,text="Forgot Password",font=('arial',20,'bold'),
                       bg='#008DDA',bd=5,command=forgot) # Command Ref: 44th line
    forgot_btn.place(relx=.44,rely=.82, height=45)


main_screen() #main frame function calling



            #----- FORGOT PASSWORD PAGE-----#


# Forgot password Screen design & Srtructure 
def forgot_screen():

    def back():     #Navigator from Back Button(FG_Page) To Main Page
        frm.destroy()
        main_screen()
    
    # Function for Resenting the entry, Reset Button    
    def reset():
    
        acn_entry.delete(0,"end")
        email_entry.delete(0,"end")

    #function to get 
    def send_forgot_otp():
        acn=acn_entry.get()
        email=email_entry.get()

 #Connection object to fetch the above data and match it with the data in the database
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
     #Selecting name and password with reference to the Ac no and Email ID fetched for the function
        query="select Name,PAssword from accounts where AC_no=? and Email=?"
        curobj.execute(query,(acn,email))
        tup=curobj.fetchone()
        conobj.close()  # connection closing


#Condition for if the ac no and email are  matched and if details are not matched
        if tup!=None: # if details are matched OTP will be sent in mail
            otp=Random_Generator.forgototp
#Storing the Email Body into a Text variale
            Text=f"""Welcome {tup[0]},
OTP to Recover password is = {otp}"""

        #Calling the function from mailing module with variable for sending email to the user
            mailing.forgototp_mail(email,Text)
        # Message will be shown as soon as the user clicks the send otp Button    
            messagebox.showinfo("Forgot","Otp sent to registered email")
            
        #Then a message boc will ask for the new generated otp received in the mail
            uotp=simpledialog.askinteger("Forgot","Otp")

# Condition to match the OTP entered is same the OTp sent
            if otp==uotp: # ---- If OTp Matches
                messagebox.showinfo("Password",tup[1]) # Password will be shown in the msg box
            
            else: #---- If OTP Does not match Below msg will be shown
                messagebox.showerror("Forgot","Invalid OTP")
# If Email and AC no does not match with the database, then bellow error will be shown        
        else:
            messagebox.showerror("Forgot","Invalid Details,Try Again")



    frm=Frame(root,highlightbackground='#FFFFFF',highlightthickness=2)
    frm.configure(bg='#1E3E62')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.72)

#Back Button on Forgot Password Screen
    back_btn=Button(frm,text="Back",font=('Roboto Black',20,'bold'),
                       bg='#008DDA',command=back)
    back_btn.place(relx=.01,rely=.01,width=100,height=40)

#A/C No. Label and Entry on forgot password screen

    acn_lbl=Label(frm,text="A/C No :",font=('arial',20,'bold'),fg="#FFFFFF",bg='#1E3E62')
    acn_lbl.place(relx=.3,rely=.1)

    acn_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    acn_entry.place(relx=.4,rely=.1,width=320)
    acn_entry.focus() #cursor focus on the enty

#Email ID Label and Entry on forgot password screen

    email_lbl=Label(frm,text="Email ID :",font=('arial',20,'bold'),fg="#FFFFFF",bg='#1E3E62')
    email_lbl.place(relx=.3,rely=.2)

    email_entry=Entry(frm,font=('arial',20,'bold'),bd=5)
    email_entry.place(relx=.4,rely=.2,width=320)
    email_entry.focus() #cursor focus on the enty

#otp Button on forgot password screen

    otp_btn=Button(frm,text="Send OTP",font=('arial',20,'bold'),
                       bg='#008DDA',bd=5,command=send_forgot_otp)
    otp_btn.place(relx=.33,rely=.4, width=250, height=45)

#Reset Button on forgot password screen

    Reset_btn=Button(frm,text="Reset",font=('arial',20,'bold'),
                       bg='#008DDA',bd=5)
    Reset_btn.place(relx=.53,rely=.4,width=230, height=45)


    
        #------ Login Page Design & Structure ---------#

def Admin_screen(): #Screen frame & Design

    frm=Frame(root,highlightbackground='#FFFFFF',highlightthickness=2)
    frm.configure(bg='#1E3E62')
    frm.place(relx=0,rely=.17,relwidth=1,relheight=.72)

    Wel_lbl=Label(frm,text="Welcome Admin!! Enter Your Details Carfully",font=('arial',15,'bold')
                        ,bg='#FFFFFF',fg='#1E3E62')
    Wel_lbl.place(relx=.4,rely=.9)

    def logout(): # Function for Logout Button - Admin Screen to Main screen
        frm.destroy()
        main_screen()

# Logout button design & Style
    Logout_btn=Button(frm,text="Logout",font=('arial',20,'bold'),fg='#FFFFFF',
                       bg='Blue',bd=5,command=logout)
    Logout_btn.place(relx=.92,rely=.92, width=120, height=45)

# Navigation from New Account Button to Overlapping New Frame with User Entry for name,MoB, Aadhar,Email ID  
    def new():
    
        ifrm=Frame(frm,highlightbackground='#008DDA',highlightthickness=2)
        ifrm.configure(bg='#FFFFFF')
        ifrm.place(relx=.1,rely=.17,relwidth=.8,relheight=.7)

    # Frame Heading 
        title_lbl=Label(ifrm,text="Fill Details For New Account",font=('arial',20,'bold')
                        ,bg='#FFFFFF',fg='#1E3E62')
        title_lbl.pack()
    
    # Name Label & Entry
        Name_lbl=Label(ifrm,text="Name:",font=('arial',15,'bold'),fg='#1E3E62',bg='#FFFFFF')
        Name_lbl.place(relx=.2,rely=.2)

        Name_entry=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        Name_entry.place(relx=.2,rely=.3,width=320)
        Name_entry.focus() #cursor focus on the enty

    # Email Label & Entry
        email_lbl=Label(ifrm,text="Email ID :",font=('arial',15,'bold'),fg='#1E3E62',bg='#FFFFFF')
        email_lbl.place(relx=.55,rely=.2)

        email_entry=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        email_entry.place(relx=.55,rely=.3,width=320)
        email_entry.focus() #cursor focus on the enty 

    # Mob Label & Entry
        Mob_lbl=Label(ifrm,text="Mob :",font=('arial',15,'bold'),fg='#1E3E62',bg='#FFFFFF')
        Mob_lbl.place(relx=.2,rely=.4)

        Mob_entry=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        Mob_entry.place(relx=.2,rely=.5,width=320)
        Mob_entry.focus() #cursor focus on the enty 
    
    # Aadhar Label & Entry
        Aadhar_lbl=Label(ifrm,text="Aadhar No. :",font=('arial',15,'bold'),fg='#1E3E62',bg='#FFFFFF')
        Aadhar_lbl.place(relx=.55,rely=.4)

        Aadhar_entry=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        Aadhar_entry.place(relx=.55,rely=.5,width=320)
        Aadhar_entry.focus() #cursor focus on the enty 


#------------ Below are the Actions that will take place after enterying the open account butten--------------#


# Function for user input after pressing the open account button
        def open_acn():
            name=Name_entry.get() # to get name
            email=email_entry.get() # to get email
            mob=Mob_entry.get()     # to get Mobile no.
            aadhar=Aadhar_entry.get() # to get aadhar No
            bal=0                       # given Initial Balance for New Account as 0
            opendate=time.strftime("%d-%b-%Y %r") # Account opening date & time
            # Password function Used
            pwd=Random_Generator.password() # Random password generated (Function Made in the Random_Generator file)

    # Connection object between the table.py database file and the project file
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
           #Insert Query for the tabel insertion table colum(8) schema wise entry.
            query="insert into accounts values(null,?,?,?,?,?,?,?)"
            curobj.execute(query,(name,pwd,bal,mob,aadhar,email,opendate)) #Account no.is auto incremented so Not added 
            conobj.commit() #connection object commited
            conobj.close()  # connection closing
    
    # Connection Object between the database table.py and the project file to fetch Account No.
        #Note: Autoincrement as been applied on the Account No. Colm
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            query="Select max(AC_No) from accounts" #Newly added Ac no. will be max of that colm(if only 1, then 1 is max)
            curobj.execute(query)
    #curser object stores the values in tuple and all the data will be stored
    # in the tuple single touple creating a table of nested staked tuples like a chocolate bar.
    # which will make Account Number in the 0 index (Acn,name...). we are using indexing to fetch the sigle no.
            acn=curobj.fetchone()[0] # using subscript as Zero Index Value will be shown
            conobj.close()


        #Creating default Input for the text variable created for the function openacn_mai(to,text)
            Text=f"""Welcome {name},
We have successfully opened your account in ABC Bank
This is your Credentials
ACN={acn}
Pass={pwd}"""
            
            # Passing name and email id details in Function from the mailing modul
            mailing.openacn_mail(email,Text)

    #popup Message box after pressing the open button that will display that all the above actions are completed
            messagebox.showinfo("Account Open","We have opened your accound successfully and mailed the credentials")
   
    #Open Account button for Submittion of the detail
        open_btn=Button(ifrm,text="Open Account",font=('arial',20,'bold'),
                       bg='green',bd=5,command=open_acn)
        open_btn.place(relx=.45,rely=.7, height=45)


# Navigation from View Account Button to Overlapping New Frame with User Entry for Popup Screen to see details

    def View():
    
        ifrm=Frame(frm,highlightbackground='#008DDA',highlightthickness=2)
        ifrm.configure(bg='#FFFFFF')
        ifrm.place(relx=.1,rely=.17,relwidth=.8,relheight=.7)

        title_lbl=Label(ifrm,text="View Account Details",font=('arial',20,'bold')
                        ,bg='#FFFFFF',fg='#1E3E62')
        title_lbl.pack()
    
    # Dialog bOx with User entry after pressing the View Account Button
        uacn=simpledialog.askinteger("View Account","Enter A/C No. :") #Simpledialog - Dialog box
#IF the User cancels the entry msg box, the command will not work futher
        if uacn==None: # if not this - The Balance will become Null or will show error
            return
         # Connection Object between the database table.py and the project file to 
         # fetch Account details with reference to the account no. provided by the user
        #Note: Autoincrement as been applied on the Account No. Colm
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        query="Select * from accounts where AC_No=?" #selecting the account details with reference to the ac no. provided(uacn)
        curobj.execute(query,(uacn,)) # Note: Sigle Values in Tuple is followed by a coma
        tup=curobj.fetchone() # fetching the details
        conobj.close()
        if tup!=None: # Logic function for existing account & Non Existing account
            messagebox.showinfo("Details",tup) # Message box with ac deatils for exiting account
        else: # Message box for account not exits
            messagebox.showerror("Details", "Account Doesn't exist")

# Navigation from Close Account Button to Overlapping New Frame with User Entry for Popup Screen to see details

    def Close():
    
        ifrm=Frame(frm,highlightbackground='#008DDA',highlightthickness=2)
        ifrm.configure(bg='#FFFFFF')
        ifrm.place(relx=.1,rely=.17,relwidth=.8,relheight=.7)

        title_lbl=Label(ifrm,text="Account Closing Screen",font=('arial',20,'bold')
                        ,bg='#FFFFFF',fg='#1E3E62')
        title_lbl.pack()
    
    # Dialog Box with user enty after pressing close account button
        uacn=simpledialog.askinteger("Close Account","Enter A/C No. :")
#IF the User cancels the entry msg box, the command will not work futher
        if uacn==None: # if not this - The Balance will become Null or will show error
            return
# Connection Object between the database table.py and the project file to 

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        query="Select Name,Email from accounts where AC_No=?" #selecting name and email with reference to user entered account no.
        curobj.execute(query,(uacn,)) # Note: Sigle Values in Tuple is followed by a coma
        tup=curobj.fetchone() # fetching the details
        conobj.close()
     # Logic function for existing account & Non Existing account
        if tup!=None:# Logic for Sending Otp to mail to verify existing the account holder
            otp=Random_Generator.closeotp() #Otp generation function created in random_generator module
            text=f"Hello {tup[0]},\nOTP to close your Account: {otp}" #The name is in the 0 index ot tuple fetched from above query
            mailing.closeotp_mail(tup[1],text)# mail is in 1 index in tuple fetched from the above query
            messagebox.showinfo("Close","OTP has been sent to your Email to close account") # Pop message when user press the ok after entering the account no.  
            uotp=simpledialog.askinteger("Close Otp","OTP") # User will enter the received OTP In the Dialogue box
       
        # Logic function for if the otp matches and if otp not matches entered by user    
            if otp==uotp: #if otp matches 
                conobj=sqlite3.connect(database="bank.sqlite") # connection B/w Database and logic function
                curobj=conobj.cursor()
                query="delete from accounts where AC_No=?" # Account no. given by user will be matched with the database & Delete
                curobj.execute(query,(uacn,)) # Note: Sigle Values in Tuple is followed by a coma
                conobj.commit() #DDL Queries needs to be commited
                conobj.close()
                messagebox.showinfo("Close Account","Account Closed") #pop msg after executing the above query
            
            else:   # if otp does not match then pop msg as below
                messagebox.showerror("Close Account","Invalid OTP")
       
        else: # Message box for account not exits
            messagebox.showerror("Details", "Account Doesn't exist")


# New Account Button Style & Design in Admin Screen
    Newac_btn=Button(frm,text="New Account",font=('Roboto Black',20,'bold'),
                     bg="green",command=new)
    Newac_btn.place(relx=.2,rely=.06,width=280,height=45)

# New Account Button Style & Design in Admin Screen
    Viewac_btn=Button(frm,text="View Account",font=('Roboto Black',20,'bold'),
                     bg="powder blue",command=View)
    Viewac_btn.place(relx=.4,rely=.06,width=280,height=45)


#Close Account Button Style & Desining In admin Screen
    closeac_btn=Button(frm,text="Closs Account",font=('Roboto Black',20,'bold'),
                     bg="red",command=Close)
    closeac_btn.place(relx=.6,rely=.06,width=280,height=45)

# Function for the Logout Button
    def logout(): # Function for Logout Button - Customer Screen to Main screen
        frm.destroy()
        main_screen()

# Logout button design & Style
    Logout_btn=Button(frm,text="Logout",font=('arial',20,'bold'),fg='#FFFFFF',
                       bg='Blue',bd=5,command=logout)
    Logout_btn.place(relx=.92,rely=.92, width=120, height=45)



#    ----------- Customer Screen ----------#

def Customer_screen(uacn): #Screen frame & Design

    frm=Frame(root,highlightbackground='#FFFFFF',highlightthickness=2)
    frm.configure(bg='#1E3E62')
    frm.place(relx=0,rely=.17,relwidth=1,relheight=.72)

# Created Connection b/W database the project to bring the name with reference to the account no.
# to show welcome with the dedicated name
    conobj=sqlite3.connect(database="bank.sqlite")
    curobj=conobj.cursor()
    query="select Name from accounts where AC_no=?"
    curobj.execute(query,(uacn,))
    name=curobj.fetchone()[0] # using subscript as Zero Index Value will be shown
    conobj.close()

# Welcome Label on old screen placed below the new screen
    Wel_lbl=Label(frm,text=f"Welcome {name.capitalize()}!!",font=('arial',15,'bold')
                        ,bg='#FFFFFF',fg='#1E3E62')
    Wel_lbl.place(relx=.44,rely=.9)


# function for Navigating from Show Details Button to Overlapping New Frame with User Entry 
    def Show():
    
        ifrm=Frame(frm,highlightbackground='#008DDA',highlightthickness=2)
        ifrm.configure(bg='#FFFFFF')
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.69)
    
     # Frame Heading 
        title_lbl=Label(ifrm,text="Customer Account Details",font=('arial',20,'bold')
                        ,bg='#FFFFFF',fg='#1E3E62')
        title_lbl.pack()

    # Created Connection b/W database the project to bring the name with reference to the account no.
    # to show welcome with the dedicated name
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        query="select * from accounts where AC_no=?" # selecting all the colm from the tabel, to choose desired colm
        curobj.execute(query,(uacn,)) # Maintaining the connection between the Account Number for the referel
        tup=curobj.fetchone() 
        conobj.close()

# Details that is to be shown, saved in a Variable 
        text=f"""Account No         :   {tup[0]}

A/C Open Date    :   {tup[7]}

Aadhar No            :   {tup[5]}

Mob No.                :   {tup[4]}

A/N Balance         :   {tup[3]}"""
        
        info_lbl=Label(ifrm,text=text,font=("arial",17,"bold"),bg="white",fg="dark blue",justify='left')
        info_lbl.place(relx=.3,rely=.25)
 
 # function for Navigation from Customer Details Button to Overlapping New Frame with User Entry for name,MoB,Password,Email ID  
    def edit():
    
        ifrm=Frame(frm,highlightbackground='#008DDA',highlightthickness=2)
        ifrm.configure(bg='#FFFFFF')
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.69)

    # Frame Heading 
        title_lbl=Label(ifrm,text="Updated Account Detail",font=('arial',20,'bold')
                        ,bg='#FFFFFF',fg='#1E3E62')
        title_lbl.pack()

# Function for Update & Save Button to get the details entered and Update it in the DB Table
        def update():
            name=Name_entry.get() #To get New Entered Name
            pwd=Pass_entry.get()   #To get New Entered password
            mob=Mob_entry.get() #To get New Entered Mobile Number
            email=email_entry.get() #To get New Entered Email

    #Connection Object to Update the above entry into the database
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            query="update accounts set Name=?,Password=?,Mob_No=?,Email=? where AC_No=?" #this will get the details from the above functions and Update in DB
            curobj.execute(query,(name,pwd,mob,email,uacn))
            conobj.commit()
            conobj.close()

        #Update Successfull Msg after Cliking the Update & Save Button
            messagebox.showinfo("Update","Details Updated")
    
    # Name Label & Entry
        Name_lbl=Label(ifrm,text="Name:",font=('arial',15,'bold'),fg='#1E3E62',bg='#FFFFFF')
        Name_lbl.place(relx=.15,rely=.2)

        Name_entry=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        Name_entry.place(relx=.15,rely=.3,width=320)
        Name_entry.focus() #cursor focus on the enty

    # Email Label & Entry
        email_lbl=Label(ifrm,text="Email ID :",font=('arial',15,'bold'),fg='#1E3E62',bg='#FFFFFF')
        email_lbl.place(relx=.57,rely=.2)

        email_entry=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        email_entry.place(relx=.57,rely=.3,width=320)
        email_entry.focus() #cursor focus on the enty 

    # Mob Label & Entry
        Mob_lbl=Label(ifrm,text="Email ID :",font=('arial',15,'bold'),fg='#1E3E62',bg='#FFFFFF')
        Mob_lbl.place(relx=.15,rely=.4)

        Mob_entry=Entry(ifrm,font=('Mob No. :',15,'bold'),bd=5)
        Mob_entry.place(relx=.15,rely=.5,width=320)
        Mob_entry.focus() #cursor focus on the enty 
    
    # Aadhar Label & Entry
        Pass_lbl=Label(ifrm,text="Password :",font=('arial',15,'bold'),fg='#1E3E62',bg='#FFFFFF')
        Pass_lbl.place(relx=.57,rely=.4)

        Pass_entry=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        Pass_entry.place(relx=.57,rely=.5,width=320)
        Pass_entry.focus() #cursor focus on the enty 

    #Open button for Submittion of the detail
        Update_btn=Button(ifrm,text="Update & Save",font=('arial',15,'bold'),
                       bg='green',bd=5,command=update)
        Update_btn.place(relx=.43,rely=.8, height=45)

   # Created Connection b/W database the project to bring the name,pass,email,MOB with reference to the account no.
    # to edit the details of the customer
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        query="select Name,Mob,Email,Password from accounts where AC_no=?" # selecting all the colm from the tabel, to choose desired colm
        curobj.execute(query,(uacn,)) # Maintaining the connection between the Account Number for the referel
        tup=curobj.fetchone() 
        conobj.close()

    #to enter the details in the correct index 
        Name_entry.insert(0,tup[0])
        Pass_entry.insert(0,tup[3])
        Mob_entry.insert(0,tup[1])
        email_entry.insert(0,tup[2])

# function for Navigating from Deposite Button to Overlapping New Frame with User Entry 
    def Deposite():
    
        ifrm=Frame(frm,highlightbackground='#008DDA',highlightthickness=2)
        ifrm.configure(bg='#FFFFFF')
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.69)
    
    # Frame Heading 
        title_lbl=Label(ifrm,text="Customer Deposite details",font=('arial',20,'bold')
                        ,bg='#FFFFFF',fg='#1E3E62')
        title_lbl.pack()
    
    # Dialog Box with user enty after pressing close account button
        depamt=simpledialog.askfloat("Deposite","Enter Amount :")   # Deposite amount Entery

# IF the User cancels the entry msg box, the command will not work futher
        if depamt==None: # if not this - The Balance will become Null or will show error
            return

# Created Connection b/W database the project update total amount with reference to the account no.
# Amount will be updated in database
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        query="Update accounts set Balance=Balance+? where AC_no=?" # Current balance + New amount entry will be total balance that will shown
        curobj.execute(query,(depamt,uacn)) 
        conobj.commit()
        conobj.close()

# Message will be visibale after the amount is entered and ok is pressed
        messagebox.showinfo("Deposite",f"{depamt} deposited")

# function for Navigating from Withdraw Button to Overlapping New Frame with User Entry 
    def Withdraw():
    
        ifrm=Frame(frm,highlightbackground='#008DDA',highlightthickness=2)
        ifrm.configure(bg='#FFFFFF')
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.69)

    # Frame Heading 
        title_lbl=Label(ifrm,text="Customer Withdraw details",font=('arial',20,'bold')
                        ,bg='#FFFFFF',fg='#1E3E62')
        title_lbl.pack()
    
    # Dialog Box with user enty after pressing close account button
        wamt=simpledialog.askfloat("Withdraw","Enter Amount :") # Withdrawal amount Entery

# IF the User cancels the entry msg box, the command will not work futher
        if wamt is None: 
            return # Handle if user clicks Cancel

# Created Connection b/W database the project total Balance remaining for withdrawal with reference to the account no.
# Balance Amount will be shown in database
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        query="Select Balance from accounts where AC_no=?" # Current balance + New amount entry will be total balance that will shown
        curobj.execute(query,(uacn,)) 
        bal=curobj.fetchone()[0] #Fetching Balance amount at 0 index from the query
        conobj.close()

#Conditionto check the Sufficient Balance to withdraw amount
        if bal>=wamt:# Condition if the sufficient amount is present
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            query="Update accounts set Balance=Balance-? where AC_no=?" # Current balance -amount Withdrawed entry will be total balance that remain will be updated in the database
            curobj.execute(query,(wamt,uacn)) #withdrawn amount with reference to the account No. and the query executed
            conobj.commit()
            conobj.close()
            # Message will be visibale after the amount is withdrawed and the above conditions are met
            messagebox.showinfo("Withdraw",f"{wamt} Withdrawed")         
        else:# if insufficient amount
            messagebox.showinfo("Withdraw","Insufficient Balance")  # Message will be visibale if the amount is insufficient    


# function for Navigating from Show Details Button to Overlapping New Frame with User Entry 
    def Transfer():
    
        ifrm=Frame(frm,highlightbackground='#008DDA',highlightthickness=2)
        ifrm.configure(bg='#FFFFFF')
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.69)
    
    # Frame Heading 
        title_lbl=Label(ifrm,text="Customer Amount Transfer details",font=('arial',20,'bold')
                        ,bg='#FFFFFF',fg='#1E3E62')
        title_lbl.pack()
    
     # Update the window so Tkinter forces 'ifrm' to render before dialogs pop up
        ifrm.update_idletasks() 

 #-----    Syntex to check for the Correct account number in the DB-----#
# Dialog Box with user enty after pressing close account button
        toamt=simpledialog.askinteger("Transfer","Enter to Account No.") # Transfer amount Entery

# IF the User cancels the entry msg box, the command will not work futher
        if toamt is None: 
            return # Handle if user clicks Cancel
        
# Created Connection b/W database & the project for Money transfer with reference to the account no.

        conobj=sqlite3.connect(database="bank.sqlite") # Connection object
        curobj=conobj.cursor()
     #Checks if the Account No. above entered Matches with the DB   
        query="Select * from accounts where AC_no=?" 
        curobj.execute(query,(toamt,)) # query executed with respect to the AC no. entered by the user
        tup=curobj.fetchone() # this will fetch the account details with respect to the entered AC no.
        conobj.close()

# Transfered amount will be deducted from the senders and added in the receivers
# Note: This is a interbank transaction system, only check for details in its own DB       
        # If condition for fetching the data and simulatneously updating the data in 
        # database with reference to the input received 


#------ Condition to Check Sufficiant Balance respect to amount entered --------#

# Condition to check wheather the user has enough Balance in Count with reference to the Transfer amount entered        
        if tup!=None: # 
            uamt=simpledialog.askfloat("Transfer","Enter Amount :") #Dialogue Box to get transfer Amount from the User
            # IF the User cancels the entry msg box, the command will not work futher
            if uamt is None: 
                return # Handle if user clicks Cancel
            
            # Created Connection b/W database the project total Balance remaining for withdrawal with reference to the account no.
    # Balance Amount will be shown in database
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            query="Select Balance from accounts where AC_no=?" # Current balance + New amount entry will be total balance that will shown
            curobj.execute(query,(uacn,)) 
            sender_bal=curobj.fetchone()[0] #Fetching Balance amount at 0 index from the query
            conobj.close()

#------- Fund Transfer Syntex deduction from one account to add in another --------#

#Conditionto check the Sufficient Balance to withdraw amount
            if sender_bal>=uamt:# Condition if the sufficient amount is present
                conobj=sqlite3.connect(r"D:\CHITRA 8-3-2026\Data_Projects\Full Stack Project\Banking_Simulator_Project\bank.sqlite") # Connection object
                curobj=conobj.cursor()
            # query for adding amount in the receivers account  
                query1="update accounts set Balance=Balance-? where AC_No=?"
                    
                # query for minusing amount from the senders account  
                query2="update accounts set Balance=Balance+? where AC_No=?"
                # Executing both the queries 
                curobj.execute(query1,(uamt,uacn)) # query executed to the amount deducted from the user with respect to ac no. from the main screen
                curobj.execute(query2,(uamt,toamt)) # query executed to the amount entered by the user and transfered with respect to ac no. from the main screen

                conobj.commit()
                
                conobj.close()
                #Dispaly msg on successful transaction
                messagebox.showinfo ("Transfer",f"{uamt} transfered to {toamt}")           
        
            else:# if insufficient amount
                messagebox.showinfo("Withdraw","Insufficient Balance")  # Message will be visibale if the amount is insufficient    
                                       
        else: # If account No. Does not exists
            messagebox.showerror("Transfer","Invalid Account No.")


 # --- Customer Screen Buttons ------#       
# Show Details Button    
    Show_btn=Button(frm,text="Show Details",font=('Roboto Black',20,'bold'),
                     bg="green",command=Show)
    Show_btn.place(relx=0,rely=.05,width=250,height=45)

# Update Details Button  
    Upacn_btn=Button(frm,text="Update Details",font=('Roboto Black',20,'bold'),
                     bg="green",command=edit)
    Upacn_btn.place(relx=0,rely=.2,width=250,height=45)

# Deposite Money Button 
    Deposite_btn=Button(frm,text="Deposite",font=('Roboto Black',20,'bold'),
                     bg="green",command=Deposite)
    Deposite_btn.place(relx=0,rely=.35,width=250,height=45)

# Money Withdraw Button
    Withdraw_btn=Button(frm,text="Withdraw",font=('Roboto Black',20,'bold'),
                     bg="green",command=Withdraw)
    Withdraw_btn.place(relx=0,rely=.5,width=250,height=45)

# Money Transfer Button 
    Transfer_btn=Button(frm,text="Transfer",font=('Roboto Black',20,'bold'),
                     bg="green",command=Transfer)
    Transfer_btn.place(relx=0,rely=.65,width=250,height=45)

# Function for the Logout Button
    def logout(): # Function for Logout Button - Customer Screen to Main screen
        frm.destroy()
        main_screen()

# Logout button design & Style
    Logout_btn=Button(frm,text="Logout",font=('arial',20,'bold'),fg='#FFFFFF',
                       bg='Blue',bd=5,command=logout)
    Logout_btn.place(relx=.92,rely=.92, width=120, height=45)




# Footer Label and Style
footer_lbl=Label(root,text="Chitra \n Demo Project",font=('Times New Rome',20,'bold'),
                fg='#FFFFFF',bg='#0B192C')

footer_lbl.pack(side='bottom',pady=10)



root.mainloop()

