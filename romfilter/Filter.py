'''
Created on 22 Oct 2019

@author: Yvo
'''
import os;

from shutil import move;

class Filter(object):

    trimList = []
    filteredDirectoryName = 'REMOVED';
    
    
    def __init__(self, filePath, files = [], extensions = [], tags = [], removeDuplicates = False, matchSingleTag = False):

        matchAllTags = not matchSingleTag;
        allowDuplicate = not removeDuplicates;
        print('\n----------------------------------------Start Filter----------------------------------------------');
        #filter by extension
        for file in files:
            extensionMatch = False;
            tagMatch = True;

            #Filter by extension
            for option in extensions:
                if option[1].get() == True and option[0] == file[2]:
                    extensionMatch = True;
                    
            #Filter by tag
            if extensionMatch:    
                allowedList = [];
                for fileTags in file[3]:
                    allowed = True;
                    
                    #Compare tag to allowed list
                    for option in tags:
                        if matchAllTags and option[1].get() == True and fileTags == option[0]:                     
                            allowed = True;
                        
                        elif matchAllTags and option[1].get() == False and fileTags == option[0]:
                            allowed = False;

                    allowedList.append(allowed); #List if each tag is allowed or not
                
                #Match based on whether a single tag is false or any tag is true
                for boolean in allowedList:
                    if not boolean and matchAllTags: #If a tag is False and we match all tags
                        tagMatch = False;
                    
                    elif boolean and not matchAllTags: #If a tag is True and we match one tag
                        tagMatch = True;
            
            #List files to remove based on tags and extensions
            if not extensionMatch or not tagMatch:
                print(file[0]+'  Will be removed');
                self.trimList.append(file);
                
        print('\n-----------------------------------------End Filter-----------------------------------------------');
        #If we don't allow duplicates, begin removing them always keeps first found.
        print('\n-----------------------------------------Check Duplicates-----------------------------------------');


        if not allowDuplicate:
            for file in files:
                trimmed = False;
                for deletedFile in self.trimList:
                    if file[0] == deletedFile[0]:
                        #print(file[0]+' Has already been removed no need to compare');
                        trimmed = True;
                
                if not trimmed:
                    for file2 in files:
                        trimmed2 = False;
                        for deletedFile in self.trimList:
                            if file2[0] == deletedFile[0]:
                                #print(file2[0]+' Has already been removed no need to compare 2');
                                trimmed2 = True;
                        
                        if not trimmed2:
                            if file[1] == file2[1] and file[0] != file2[0]:
                                print(file2[0]+'  Duplicate will be removed');
                                self.trimList.append(file2);
                            
        
        print('\n---------------------------------------End Duplication Check--------------------------------------');
            
        #Check if filter directory exists
        trash = filePath+self.filteredDirectoryName+'/';
        print('\nDoes the REMOVED directory exist in ' +filePath+' ?');
                
        if os.path.isdir(trash):
            print('\nTrue, folder "REMOVED" already exists, skipping');
                
        else:
            print('\nFalse, creating new folder "REMOVED"');
            os.mkdir(trash);
                    
                    
        #Move filtered files
        print('\n----------------------------------------Start Moving----------------------------------------------');
        for file in self.trimList:
            
            if not os.path.isfile(filePath+file[0]):
                print('ERROR 404: '+filePath+file[0]+' not found');
            else:
                                
                move(filePath+file[0], trash+file[0]);
            
            

        print('\n---------------------------------------End Moving-------------------------------------------------');
