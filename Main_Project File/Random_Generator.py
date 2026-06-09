import random

def captcha():
    num=list(range(10))
    letters=list("abcdefghijklmnopqrstuvwxyz")

    cap=random.choices(num+num+letters,k=4)
    s=""
    for i in cap:
        s+=str(i)
        s+=" "
    return s

def password():
    num=list(range(10))
    letters=list("abcdefghijklmnopqrstuvwxyz")
    pwd=random.choices(num+num+letters,k=5)
    s=""
    for i in pwd:
        s+=str(i)
    return s


def closeotp():
    otp=random.randint(1000,9999)
    return otp

def forgototp():
    otp=random.randint(1000,9999)
    return otp
