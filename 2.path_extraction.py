# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 15:22:47 2022

@author: soyrl
"""

import subprocess
from tkinter import Tk
from tkinter.filedialog import askopenfilename

#Used to extract path to be added in environmental variables
print("Please select a random file on Desktop: ") 

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename_py = askopenfilename() # show an "Open" dialog box and return the path to the selected file

while 'Desktop' not in filename_py:
    print("File is not in Desktop. Please try again. Select a file from Desktop: ")
    filename_py=askopenfilename()

user=filename_py.split('/')[2] #Get name of the current user
disk_name=filename_py.split('Users')[0] #Get name of hard disk drive

pip_install = subprocess.run(['pip', 'install','--user','translatesubs==0.2.2']) #Not working (sys.executable, '-m')
# print("The exit code was: %d" % pip_install.returncode) 

#Below for giving administration priviledges - Does not work and that's why it should be done manually
#https://stackoverflow.com/questions/47380378/run-process-as-admin-with-subprocess-run-in-python
# prog = subprocess.Popen(['runas', '/noprofile', '/user:Administrator', 'NeedsAdminPrivilege.exe']
#                          ,stdin=subprocess.PIPE)
# prog.stdin.write('password')
# prog.communicate()

path=disk_name+'Users/'+user+'/AppData/Roaming/Python/Python37/Scripts'
print('Please add the following to the environmental variables path: ')
path=path.replace('/','\\')
print(path)
input("Press Enter to exit...")