import tkinter as tk
import os
import time
import winsound
import random
def start():
    r =tk.Tk()
    r.title("Timer")
    s_initial = tk.IntVar()
    s_initial.set("000000")
    e_initial = tk.Entry(r,textvariable = s_initial,font = 40)
    e_initial.grid(column = 0,row = 0,ipadx=40,ipady=20)

    def START():
        a=e_initial.get()
        r.destroy()
        try:
            seconds = (str(a[4])+str(a[5]))
            minutes = (str(a[2])+str(a[3]))
            hours = (str(a[0])+str(a[1]))
            if int(a) == 000000:
                hours = 24
                minutes = 0
                seconds = 0
            elif int(a)>235959:
                hours = 24
                minutes = 0
                seconds = 0
            print(f"Timer has been set of {hours} hours {minutes} minutes {seconds} seconds")
            print("Don't shutdown or restart your PC Timer Won't Notify Sound")
            time.sleep(int(hours)*60+int(minutes)*60+int(seconds))
            i = 0
            while i<100:
                for j in range(30):
                    winsound.Beep(random.randint(3000,4500),6)
                i+=1
        except:
            f = open("CRASH.txt","w")
            f.write("""INTORDUCTION
    ____________
    1. The format is HHMMSS.
        eg. 001000
                here, the timer will make sound after 10 minutes
        eg. 013000
                here, the timer will make sound after 1 hours and 30 minutes
    2. six Digits Between 000000 and 235959 , Else the default value is of 24 hours.

    3. Only Number are Excepted.

    4. Something after sixth digit will not be taken.""")
            f.close()
            os.startfile("CRASH.txt")
            time.sleep(3)
            os.remove("CRASH.txt")
    b_start = tk.Button(r,text = "START",command = START)
    b_start.grid(column = 0,row = 1,stick = "w",ipadx = 43)
    r.mainloop()

