# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 10:59:24 2022

@author: soyrl
"""

import subprocess
from tkinter import Tk
from tkinter.filedialog import askopenfilename

print("Please select the python.exe file to install: ")

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename_py = askopenfilename() # show an "Open" dialog box and return the path to the selected file

#Automatically install python - https://docs.python.org/3.6/using/windows.html#installing-without-ui
#https://stackoverflow.com/questions/89228/how-do-i-execute-a-program-or-call-a-system-command
#https://www.digitalocean.com/community/tutorials/how-to-use-subprocess-to-run-external-programs-in-python-3
result_python = subprocess.run([filename_py, "/quiet","/passive","InstallAllUsers=1",
                                "PrependPath=1","Include_test=0"]) 
# print("The exit code was: %d" % result_python.returncode) #Should be 0 if it worked
#https://www.activestate.com/resources/quick-reads/how-to-install-python-packages-using-a-script/