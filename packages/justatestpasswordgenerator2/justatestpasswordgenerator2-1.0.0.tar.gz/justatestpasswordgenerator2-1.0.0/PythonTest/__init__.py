print("This program is a random password generator.")

import random

s = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"

passlen = int(input("How many characters would you like your password to be?:"))
p = "".join(random.sample(s, passlen))
print(p) 
