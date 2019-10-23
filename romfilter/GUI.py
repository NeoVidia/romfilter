'''
Created on 22 Oct 2019

@author: Yvo
'''



from tkinter import filedialog, Frame, Label, Button, Checkbutton, Text, BooleanVar, Toplevel, Tk, LEFT, BOTTOM, RIGHT, YES, TOP, END, BOTH, DISABLED, NORMAL;
#from tkinter.filedialog import FileDialog;
from romfilter.FileAnalyzer import FileAnalyzer;
from romfilter.Filter import Filter;
import ctypes;
import os;


if __name__ == '__main__':
    pass

class MainWindow (object):
    
    Analyzers = None;
    FilterGUI = None;
    
    user32 = None;
    root = None;
    
    directoryFrame = None;
    directoryLabel = None;
    directoryText = None;
    directoryButton = None;
    
    analyzeFrame = None;
    analyzeButton = None;
    
    windowWidth = 870;
    windowHeight = 150;
    
    screenwidth = 800;
    screenheight = 600;
    
    defaultPath = '';
    #defaultPath = 'F:/Firefox/SG_GN-MD-32X/FULL Sega Genesis -- Mega Drive -- 32X (GoodGen 3.00)[GoodMerged]/';

    
    def __init__(self):
        print('Initializing Main GUI');
        
        
        #Create window        
        self.user32 = ctypes.windll.user32;
        self.screenWidth = self.user32.GetSystemMetrics(0);
        self.screenHeight = self.user32.GetSystemMetrics(1);
        screenX = int(self.screenWidth / 2 - self.windowWidth / 2);
        screenY = int(self.screenHeight / 2 - self.windowHeight / 2);
        
        #Set window attributes
        self.root = Tk();
        self.root.title('Rom Filter');
        self.root.geometry('+%d+%d' % (screenX, screenY));

        #Initialize UI elements
        self.directoryFrame = Frame(self.root);
        self.directoryLabel = Label(self.directoryFrame, text = 'Directory:');
        self.directoryText = Text(self.directoryFrame, height = 1, width = 80, padx = 10);
        self.directoryButton = Button(self.directoryFrame, text='Browse...', command = self.GetDirectory);
        
        self.analyzeFrame = Frame(self.root);
        self.analyzeButton = Button(self.analyzeFrame, text='Analyze', command = self.Analyze);
        
        #Create UI
        self.directoryLabel.pack(side=LEFT, padx = 15, pady = 15);
        self.directoryText.pack(side=LEFT);
        self.directoryButton.pack(side=LEFT, padx = 15, pady = 15);
        
        self.analyzeButton.pack(side=LEFT);
        
        self.directoryFrame.pack(side = TOP);
        self.analyzeFrame.pack(side = BOTTOM, padx = 15, pady = 5);
        
        #Lock path field
        self.directoryText.config(state=DISABLED);
        
        #Populate UI
        self.SetDirectory(self.defaultPath);
        
        
        
    def AskDirectoryDialog(self):
        filePath = filedialog.askdirectory(initialdir=os.getcwd(), title='Please select ROMs folder')+'/';
        filePath = filePath.replace('\\\\', '/');
        if len(filePath) > 0:
            return filePath;
        
    def SetDirectory(self, filePath):
        #Unlock path field
        self.directoryText.config(state=NORMAL);
        self.directoryText.delete(1.0, END);
        self.directoryText.insert(1.0, filePath);
        #Lock path field
        self.directoryText.config(state=DISABLED);
    
    def GetDirectory(self):
        path = self.AskDirectoryDialog();
        self.SetDirectory(path);

        
    def Analyze(self):  
        
        #Fix any path issues
        filePath = self.directoryText.get(1.0, END);
        if filePath[-1:] != '/' or filePath[-1:] != '\\':
            filePath = filePath + '/';
        filePath = filePath.replace('\\', '/');
        filePath  = filePath.replace('\n', '');
        print("Analyzing: "+filePath);
        
        if not os.path.isdir(filePath):
            print('ERROR 301: Path is not valid!');
        else:
            
            #Analyze selected directories
            Analyzer = FileAnalyzer(filePath);
            Analyzer.Analyze(Analyzer.GetFileList());
        
            #Call filter GUI
            createFilterWindow = GUISorting();
            createFilterWindow.CreateWindow(filePath,
                                            Analyzer.GetOrganizedFileList(),
                                            Analyzer.GetExtensionList(),
                                            Analyzer.GetTagsList());
    

class GUISorting (object):
    FilterGUI = None;
    
    windowWidth = 400;
    windowHeight = 600;
    
    screenWidth = 800;
    screenHeight = 600;
    
    
    fileList = []
    extensionList = []
    tagList = []

    
    directory = None;
    maxOptions = 45;
    
    
    buttonRemoveDuplicate = None;
    buttonMatchSingleTag = None;
    
    bgColor = 'white';
    altBgColor = 'antique white';
    
    duplicate_var = None;
    singleTag_var = None;
    
    def CreateWindow(self, filePath, files = [], extensions = [], tags = []):

        
        self.directory = filePath;
        self.fileList = files;
        self.duplicate_var = BooleanVar();
        self.singleTag_var = BooleanVar();

        #Define Window
        self.FilterGUI = Toplevel();
        self.FilterGUI.title("Please select prefered filters");
        
        screenX = int(self.screenWidth / 2 - self.windowWidth / 2);
        screenY = int(self.screenHeight / 2 - self.windowHeight / 2);
        self.FilterGUI.geometry('+%d+%d' % (screenX, screenY));
        
        #Create static UI elements
        #Frames
        optionFrame = Frame(self.FilterGUI);
        extensionsFrame = Frame(optionFrame);
        tagsFrame = Frame(optionFrame);
        
        #Labels
        labelExtensions = Label(extensionsFrame, text = 'Extensions');
        labelTags = Label(tagsFrame, text = 'Tags');
        labelRemoveDuplicated = Label(self.FilterGUI, text = 'Remove Duplicate: ');
        labelMatchSingleTag = Label(self.FilterGUI, text = 'Match single Tag: ');
        
        #Buttons
        startButton = Button(self.FilterGUI, text = 'Filter ROMS', command = self.FilterRoms, padx = 10);
        self.buttonRemoveDuplicate = Checkbutton(self.FilterGUI, variable = self.duplicate_var);
        self.buttonMatchSingleTag = Checkbutton(self.FilterGUI, variable = self.singleTag_var);
        
        #Pack static UI elements
        labelExtensions.pack(side = TOP);
        labelTags.pack(side = TOP);
        
        
        #Create Dynamicly Generated UI Elements
        #Extensions
        extensionWidgets = [];
        tagWidgets = []
        
        
        
        
        verticalFrame = Frame(extensionsFrame);
        verticalPos = 0;
        bgcolor = self.bgColor;
        
        for option in extensions:
            #Split options into smaller lists
            if verticalPos >= self.maxOptions: 
                verticalFrame = Frame(extensionsFrame);
                verticalPos = 0;
                
            #interchanging colors for readability
            if ((verticalPos+1) % 2) == 1:
                bgcolor = self.altBgColor;
            else:
                bgcolor = self.bgColor;
                
            var = BooleanVar();
            tempframe = Frame(verticalFrame, width = 100, height = 16);
            Label(tempframe, text = option+':  ', bg = bgcolor).pack(side = LEFT, fill = 'x', expand = YES);
            extension = Checkbutton(tempframe, variable = var, bg = bgcolor);
            extension.select();
            extension.pack(side = RIGHT);
            
            self.extensionList.append([option, var]);
            extensionWidgets.append(tempframe);
            verticalFrame.pack(side = LEFT, fill = 'y', expand = YES);
            verticalPos += 1;
        
        
        
        verticalFrame = Frame(tagsFrame);
        verticalPos = 0;
        for option in tags:
            #Split options into smaller lists
            if verticalPos >= self.maxOptions:
                verticalFrame = Frame(tagsFrame);
                verticalPos = 0;
                
            #interchanging colors for readability
            if ((verticalPos+1) % 2) == 1:
                bgcolor = self.altBgColor;
            else:
                bgcolor = self.bgColor;
                
            var = BooleanVar();
            tempframe = Frame(verticalFrame, width = 280, height = 16, bg = bgcolor);
            Label(tempframe, text = option+':  ', bg = bgcolor).pack(side = LEFT, fill = 'x', expand = YES);
            tag = Checkbutton(tempframe, variable = var, bg = bgcolor);
            tag.select();
            tag.pack(side = RIGHT);
            
            self.tagList.append([option, var]);
            
            tagWidgets.append(tempframe);
            verticalFrame.pack(side = LEFT, fill = 'y', expand = YES);
            verticalPos += 1;
        
        print(len(files));
        print(len(extensions));
        print(len(tags));
            
        #Pack Dynamic Elements
        for elementType in extensionWidgets:
            elementType.pack(side = TOP);
            elementType.pack_propagate(0)
            
        for elementType in tagWidgets:
            elementType.pack(side = TOP);
            elementType.pack_propagate(0)
            
        
        #Push UI Elements
        extensionsFrame.pack(side = LEFT, fill = BOTH, expand = YES, padx = 30);
        tagsFrame.pack(side = LEFT, fill = BOTH, expand = YES);
        
        optionFrame.pack(side = TOP, expand = YES);
        
        
        startButton.pack(side = RIGHT, padx = 15, pady = 15);
        labelRemoveDuplicated.pack(side = RIGHT);
        self.buttonRemoveDuplicate.pack(side = RIGHT);
        labelMatchSingleTag.pack(side = RIGHT);
        self.buttonMatchSingleTag.pack(side = RIGHT);
        
        #buttonRemoveDuplicate.select();

        self.FilterGUI.resizable(False, False)
        
    def FilterRoms(self):
        print(self.directory)
        self.directory  = self.directory.replace('\n', '');
        Filter(self.directory,
                         self.fileList,
                         self.extensionList,
                         self.tagList,
                         self.duplicate_var.get(),
                         self.singleTag_var.get());

         
        self.FilterGUI.destroy();
        