# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 11:14:42 2022
@author: soyrl
"""
# Code uploaded in https://github.com/nsourlos/subtitles_translation
# This tool does a better job in translating subs to Greek than the website: https://subtitlestranslator.com/en/
# It also works without error for Greek subs compared to https://github.com/Montvydas/translatesubs. 

# It works if subtitles only have one language, not many

# This tool uses https://pypi.org/project/googletrans/. This library works without having to use an API key 
# since it generates a ticket by reverse engineering on the obfuscated and minified code used by Google 
# to generate such token, and implemented on the top of Python. However, this could be blocked at any time.
# For the translation to work we need an Internet Connection!

from tkinter import Tk
from tkinter.filedialog import askopenfilenames
from googletrans import Translator
import math

#https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog
print("Please select the srt files to translate:")

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filenames = askopenfilenames() # show an "Open" dialog box and return the path to the selected file

for filename in filenames: #Loop over each of the selected files to translate
    
    #Check for valid file types
    if filename.split('.')[-1]!='srt' and filename.split('.')[-1]!='txt' and filename.split('.')[-1]!='sub':
        print("File {} not processed. Please select a valid file type (.srt, .txt, .sub)".format(filename))
    
    else:
        print("Processing file:",filename)
        print('\n')
      
        with open (filename,'r',encoding='utf-8') as f: #Read file with subtitles to translate
            lines=f.readlines()
        
        translator = Translator(raise_exception=True) #Initialize translator with the option to raise error if it doesn't work
        
        #Initialize lists to keep track of the actual subs and of the timesteps        
        only_subs=[]
        only_nums=[]
        
        track=10 #Initialize an index to keep track if we have timesteps or actual subtitles below
        
        for ind,line in (enumerate(lines)): #Loop over the lines of our subtitle file
            
            if len(line)!=1 and line.split(':')[0][:-1].isdigit()==False: #If not an empty line and not timesteps
            #We have actual subtitle text if in here
              
                if ind==track+1 or ind==track+2: #To keep track of text split in 2-3 lines in the same timestep
                    only_subs[-1]=only_subs[-1][:-1]+' '+str((line)) #If text in many lines for a given timestep, combine it in one

                else:
                    only_subs.append(line) #If just in one line add it to the subtitles list
                    only_nums.append('aaaaaaaaaa') #Add in the list with timesteps an indicator of where translated text should be filled at the end
                    
                track=ind #Set the track ind equal to the current ind
                
            else: #If in here we have timesteps
                only_nums.append(line) #Add that to the respective list


        #https://github.com/ssut/py-googletrans/issues/74
        #googletrans does multiple translations in one session, not in one request, so it can't improve the speed.
        #A way to change that is to give string as input and not list
        #Problem with that is a character limit of 15k (13.6k in practice) https://py-googletrans.readthedocs.io/en/latest/
        #Therefore, we need to split in many chunks/bulks.
        
        #This is the slow way - If used the code below can't be ignored - Not suggested
        # trans_files=translator.translate(only_subs, src='auto', dest='el') #Slow way
        # translation=[i.text for i in trans_files] #Get the actual translation
        
        
        all_subs=''.join(only_subs) #Combine all subtitle text in one string
        num_chunks=math.ceil(len(all_subs)/10000) #This is the number of the chunks to split the whole text
        
        #Split into many chunks and translate each of them
        translation=[]
       
        chunk_previous=0 #Initiaze an index to keep track which characters of the subtitle text to translate in each chunk
        
        for num_chunk in range(num_chunks): #Loop over the total number of chunks
            
            if num_chunk==0: #For the first chunk
                
                #https://www.w3schools.com/python/ref_string_rfind.asp
                chunk_i=all_subs[:10000].rfind('\n') #Find where the last newline occurs before the 10k character   
                
                #Translate the above characters (including the '/n') 
                chunk_i_trans=translator.translate(all_subs[:chunk_i+1], src='auto', dest='el').text 

            elif num_chunk==num_chunks: #For the final chunk

                chunk_i_trans=translator.translate(
                    all_subs[chunk_previous+1:], src='auto', dest='el').text 
                #Final chunk will have the remainings of the previous chunks as well. 
                #It will not give an error even if it's more than 10k characters (~15k the limit).
        
            else: #For the other chunks
            
                chunk_i=all_subs[chunk_previous+1:chunk_previous+1+10000].rfind('\n') #Keep track of the number of characters of current chunk
                
                chunk_i_trans=translator.translate(
                    all_subs[chunk_previous+1:chunk_i+chunk_previous+1], src='auto', dest='el').text
                    #+1 to start after \n character of split and +1 to include \n of split
        
            translation.append(chunk_i_trans) #Append the translated chunk to the list that contains them all
        
            if num_chunk!=num_chunks-1: #If we are not in the final chunk add a newline at the end of each chunk
                translation.append('\n')
            else:
                pass
            
            chunk_previous=chunk_previous+chunk_i+1 #Index of first character of next chunk to translate

        
        final_translation=''.join(translation) #Convert list of chunks to string with text
        list_trans=final_translation.split('\n') #Split this string after each newline character to be filled with timesteps and actual translation

        #It might be difficult to have a good translation when a sentence extends in more than 2 timesteps since googletrans can't capture these 
        #long-range dependencies, especially if the original subs consist of many newline characters and many '...' between timesteps.
        
        index_to_replace=0 #Keep track of the index of the list with the translation to be used in the final file
        new_srt=[] #Initialize empty list to be filled with the timesteps and of the translated version of the subtitles
        
        for index,sub in enumerate(only_nums): #loop over the file with the timesteps that also contains an indicator of where translation should be
           
            if sub=='aaaaaaaaaa': #If the line consists of the indicator to fill translated subtitles
                new_srt.append(list_trans[index_to_replace]) #Fill lines with indicators, one at a time
                index_to_replace=index_to_replace+1 #Increase index of the list that has only the translation
           
            else: #Otherwise fill the current line with the timestep in the final list
                new_srt.append(sub)
              
        
        #Change first lines of file since wrong timestep/information there
        first_text=new_srt[0][1:] #Text of the translation in the first line
        first_duration=new_srt[1] #Timestep of that first translated text
        new_srt.insert(0,'1\n') #Insert the index that indicates the number of the timestep
        
        #Replace the first lines based on the above
        new_srt[1]=first_duration 
        new_srt[2]=first_text
        
        #If any of the lines of the final translation list does not end with the newline character, add it to it
        for line,elem in enumerate(new_srt):
            if elem.endswith('\n')==False:
               new_srt[line]=new_srt[line]+'\n'
        
        
        #Create translated srt file in same location as the original with same name plus '_output.srt' at the end
        with open("/".join(filename.split('/')[:-1])+'/'+filename.split('/')[-1].split('.')[0]+
                  '_output.srt', 'w',encoding='utf-8') as f: 
            #Generate new srt file, UTF-8 encoded with translation only
            for line in new_srt:
                f.write(line)