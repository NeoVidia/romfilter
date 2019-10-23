'''
Created on 22 Oct 2019

@author: Yvo
'''
import os;
import re;

class FileAnalyzer(object):

    
    filePath = None;
    
    fileList = []
    organizedFileList = [];
    tagList = [];
    extensionList = []

    def __init__(self, filePath):
        print('Initializing fileitem Analyzer');
        
        self.fileList = [];
        self.organizedFileList = [];
        self.tagList = [];
        self.extensionList = []

        #List Files
        self.filePath = filePath;
        self.fileList = [x for x in os.listdir(filePath) if os.path.isfile(filePath+x)];
        
    def GetFileList(self):
        return self.fileList;
    
    def GetOrganizedFileList(self):
        return self.organizedFileList;
    
    def GetExtensionList(self):
        return self.extensionList;

    def GetTagsList(self):
        return self.tagList;
    

    
    def Analyze(self, fileList):
        #Split filename into name, tags and extensions
        print("\nFiles:")
        for fileitem in fileList:
            #Split filename
            filename = re.split('(\(.+)', fileitem); #Name of the ROM in position 0
            extension = re.split('(\\.[^.]+)$', fileitem); #fileitem extension in position 1

            trimmedfile = fileitem.replace(' ', '');
            tags = re.split('(\(.+?\))|(\[.+?\])|(\\.[^.]+)$', trimmedfile); #Tags
            tags = list(filter(None, tags));
            del tags[0];
            del tags[-1];
            
            self.organizedFileList.append([fileitem, filename[0], extension[1], tags]); # Organized data [Full Filename, ROM name, Extension, [list of tags]
            print(fileitem);
        
        #Find each unique extension
        print("\nExtensions:")
        for fileitem in self.organizedFileList:
            match = False;
            for uniqueExtension in self.extensionList:
                if fileitem[2] == uniqueExtension:
                    match = True;
                    break;
            if match != True:
                print(fileitem[2]);
                self.extensionList.append(fileitem[2]);
                
        #Find each unique tag 
        print("\nTags:")
        for fileitem in self.organizedFileList:
            for filetag in fileitem[3]:
                match = False;
                for uniqueTag in self.tagList:
                    if filetag == uniqueTag:
                        match = True;
                        break;
                if match != True:
                    print(filetag);
                    self.tagList.append(filetag);
                    
                
                
        print('\n\nFound %d Files, %d unique extensions, %d unique tags' % (len(self.organizedFileList), len(self.extensionList), len(self.tagList)));
        return self.organizedFileList;
    

