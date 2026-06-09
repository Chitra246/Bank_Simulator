

import gmail

email="" #----Write e,mail id from which you want to send mail
pwd="" # ----Write your google apppassword here

#Fetching info for 'to' whom to send and 'Text' msg that we want to send  
def openacn_mail(to,text):
    con=gmail(email,pwd)
   # Mail Schema - Input will be received from the  stored variables
   #the stored variable and the parameter names are kept same 
    msg=gmail.message(to=to,subject="Account Oped in ABC Bank" ,text=text) 
    con.send(msg)

def closeotp_mail(to,text):
    con=gmail(email,pwd)
   # Mail Schema - Input will be received from the  stored variables
   #the stored variable and the parameter names are kept same 
    msg=gmail.message(to=to,subject="Otp to close Account" ,text=text) 
    con.send(msg)

def forgototp_mail(to,text):
    con=gmail(email,pwd)
   # Mail Schema - Input will be received from the  stored variables
   #the stored variable and the parameter names are kept same 
    msg=gmail.message(to=to,subject="Otp to close Account" ,text=text) 
    con.send(msg)