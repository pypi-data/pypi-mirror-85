from tkinter import *
from tkinter import filedialog
import os

import datetime 
now = datetime.datetime.now()
now = now.strftime('%m_%d_%Y')

root = Tk() 
root.title('BackUp Manager (by S.Seth)') 
root.geometry('500x420')

def targetfolder_button():
    # Allow user to select a directory and store it in global var
    global target_path
    filename = filedialog.askdirectory()
    target_path.set(filename)
    print("Selected Folder for Backup:", filename)

def destinationfolder_button():
	# Allow user to select a directory and store it in global var
	global destination_path
	filename = filedialog.askdirectory()
	destination_path.set(filename)
	print("Backup Destination Folder:", filename)

def retrieve_input():
	global inputValue
	inputValue=textBox.get("1.0","end-1c")
	print("File extensions for backup:", inputValue)

def close_window (): 
	root.destroy()


# Create label 
l1 = Label(master=root, text = "Select the directory for Backup",foreground="Blue") 
l1.config(font =("San Francisco", 12)) 

l2 = Label(master=root, text = "Backup Destination Folder",foreground="red") 
l2.config(font =("San Francisco", 12)) 

target_path = StringVar()
lbl1 = Label(master=root,textvariable=target_path)
destination_path = StringVar()
lbl2 = Label(master=root,textvariable=destination_path)


btn1 = Button(text="Browse", command=targetfolder_button)
btn2 = Button(text="Browse", command=destinationfolder_button)

# Take the file extentions 
l3 = Label(master=root, text = "Type file extentions for backup\n (use comma for multiple file types)\n [Example: py,c,txt]\n (don't put spaces after comma)",foreground="green") 
l3.config(font =("San Francisco", 12)) 

checkmark1 = IntVar(value=0)
chk1 = Checkbutton(root, text='Save Extensions', variable=checkmark1)

inputValue = str()
textBox=Text(root, height=2, width=20)
buttonCommit=Button(root, height=1, width=10, text="Commit", command=lambda: retrieve_input())
lbl3 = Label(master=root,textvariable=inputValue)

# Read the Saved Extentions from file
saved_ext = open("saved_extensions", "r")
content = saved_ext.read()
content = content.strip('\n')
ext_list = content.split(',')
saved_ext.close()

textBox.insert(END,content)


checkmark2 = IntVar(value=1)
chk2 = Checkbutton(root, text='Zip the backup', variable=checkmark2)
 
btn3 = Button ( text = "Proceed", command = close_window)


l1.pack()
btn1.pack()
lbl1.pack()
l2.pack()
btn2.pack()
lbl2.pack()
l3.pack()
textBox.pack()
chk1.pack()
buttonCommit.pack()
lbl3.pack()
chk2.pack()
btn3.pack()


mainloop()

extensions = inputValue.split(',')
for ext in extensions:
	cmd = "find " + target_path.get() + " -name '*."+ ext + "' | cpio -pdm " + destination_path.get() + "/Backup_" + now 
	print ("Excuting commands:", cmd)
	os.system(cmd)

if (checkmark1.get() == 1):
	print (inputValue, file=open("saved_extensions", "w"))

if (checkmark2.get() == 1):
	print ("Zipping the backup folder.")
	cmd_zip = "zip -r backup_"+ now +".zip " + destination_path.get() + "/Backup_" + now
	os.system(cmd_zip)

print ("\n ==============================")
print ("Backup Successful! @", now)














