# By Samantha Voigt

from Tkinter import * 
import HTMLscraper as scraper
import multiListBox

class CourseBrowserApp(Tk): 
    def __init__(self): 
        Tk.__init__(self)
        self.title('Course Browser')
        self.grid()
        
        #this data needs to be stored somewhere else, and scraped w/ the other data
        self.distributions = ['Arts, Music, Theatre, Film, Video', 'Epistemology & Cognition', \
        'Historical Studies', 'Language & Literature', 'Mathematical Modeling', \
        'Natural & Physical Sciences', 'QRB', 'QRF', 'Religion, Ethics, & Moral Philosophy', \
        'Social & Behavioral Analysis']
        self.subjects = ['Africana Studies', 'American Studies', 'Anthropology', 'Arabic', \
        'Art History', 'Art-Studio', 'Astronomy', 'Biochemistry', 'Biological Science', \
        'Cinema and Media Studies', 'Chemistry', 'Chinese Language and Culture', \
        'Classical Civilization', 'Cognitive and Linguistic Science', 'Comparative Literature', \
        'Computer Science', 'East Asian Languages and Cultures', 'Economics', 'Education', \
        'English', 'Engineering', 'Environmental Studies', 'Extradepartmental', 'French', \
        'Geosciences', 'German', 'Greek', 'Hebrew', 'History', 'Hindi/Urdu', 'Italian Studies', \
        'Japanese Lang and Culture', 'Korean Lang and Culture', 'Latin', 'Linguistics', 'Mathematics', \
        'Medieval/Renaissance', 'Middle Eastern Studies', 'Music', 'Neuroscience', \
        'Physical Education', 'Peace and Justice Studies', 'Philosophy', 'Physics', \
        'Political Science', 'Portugeuse', 'Psychology', 'Quantitive Reasoning', \
        'Russian Area Studies', 'Religion', 'Russian', 'South Asia Studies', 'Sociology', \
        'Spanish', 'Sustainability', 'Swahili', 'Theatre Studies', 'Women\'s & Gender Studies', \
        'Writing']
        self.departments = {'Africana Studies': 'AFR', 'American Studies': 'AMST', \
        'Anthropology': 'ANTH', 'Art':['ARTH','ARTS'], 'Astronomy':'ASTR', 'Biological Chemistry':'BIOC', \
        'Biological Sciences':'BISC', 'Cinema & Media Studies':'CAMS', 'Chemistry':'CHEM', \
        'Cognitive and Linguistic Sci':['CLSC','LING'], 'Classical Studies':['CLCV','LAT','GRK'], \
        'Comparative Literature':'CPLT', 'Computer Science':'CS', 'East Asian Languages and Culture':['CHIN', 'EALC', 'JPN', 'KOR'],\
        'Economics':'ECON', 'Education':'EDUC', 'English':'ENG', 'Environmental Studies':'ES', \
        'Extradepartmental':['ENGR','EXTD'], 'French':'FREN', 'Geosciences':'GEOS', \
        'German':'GER', 'History':'HIST', 'Italian Studies':'ITAS', 'Jewish Studies':'HEBR', \
        'Mathematics':'MATH', 'Medieval Renaissance Studies':'ME/R', 'Middle Eastern Studies':['ARAB','MES'], \
        'Music':'MUS', 'Neuroscience':'NEUR', 'Physical Education':'PE', 'Peace and Justice Studies':'PEAC', \
        'Philosophy':'PHIL', 'Physics':'PHYS','Political Science':['POL', 'POL1', 'POL2', 'POL3', 'POL4'], \
        'Psychology':'PSYC', 'Quantitative Reasoning':'QR', 'Russian Area Studies':'RAST', \
        'Religion':'REL', 'Russian':'RUSS', 'South Asia Studies':['HNUR','SAS'], 'Sociology':'SOC', \
        'Spanish':'SPAN', 'Sustainability':'SUST', 'Theatre Studies':'THST', 'Women\'s and Gender Studies':'WGST',\
        'Writing':'WRIT'}
        
        self.createFrames()
        self.createWidgets()
        
    def createFrames(self): 
        
        # Frames
        self.topFrame = Frame(self, bd=2, relief=GROOVE, takefocus=True)
        self.topFrame.pack()
        self.topFrameLeft = Frame(self.topFrame, takefocus=True, bd=2, relief=GROOVE)
        self.topFrameLeft.pack(side=LEFT)
        self.topFrameRight = Frame(self.topFrame, takefocus=True, bd=2, relief=GROOVE)
        self.topFrameRight.pack(side=RIGHT)
        #self.middleFrame = Frame(self, bd=2, relief=GROOVE, takefocus=True)
        #self.middleFrame.pack()
        self.bottomFrame = Frame(self, bd=2, relief=GROOVE, takefocus=True)
        self.bottomFrame.pack()
        self.buttonFrame = Frame(self, bd=2, relief=GROOVE, takefocus=True)
        self.buttonFrame.pack()
   
    def createWidgets(self): 
        
        # 'Search By' section ------->
        searchByLabel = Label(self.topFrameLeft, text='SEARCH BY:', fg='navy',font='Times 16 bold')
        searchByLabel.grid(row=0, column=0, sticky=W+E, padx=20)
        searchByBoxes = ['Distribution', 'Subject', 'Department', 'Time/Days', 'Professor']
        searchByVars = []
        colAvail = 1
        for box in searchByBoxes: 
            var = IntVar()
            button = Checkbutton(self.topFrameLeft,text=box,variable=var)
            button.grid(row=0, column=colAvail, sticky=W+E)
            searchByVars.append(var)
            colAvail += 1
      
        # 'Show Only' section ------->
        showOnlyLabel = Label(self.topFrameRight, text='SHOW ONLY:', fg='navy', font='Times 16 bold')
        showOnlyLabel.grid(row=0, column=0, sticky=W+E, padx=20)
        colAvail = 1
        showOnlyBoxes = ['If seats are available*','100 levels','200 levels','300 levels']
        showOnlyVars = []
        for box in showOnlyBoxes: 
            var = IntVar()
            button = Checkbutton(self.topFrameRight, text=box, variable=var)
            button.grid(row=0, column=colAvail, sticky=W+E)
            showOnlyVars.append(var)
            colAvail += 1
      
        
        # Results ("Courses That Fit") section -------->
        columnTuples = [('CRN',60), ('Course',80), ('Title',100), ('Seats Avail.',80),\
        ('Location(s)',100), ('Time(s)',80), ('Day(s)',60), ('Instructor',100), \
        ('Adtl. Instructor(s)',100), ('Distribution(s)',100), ('Description',100), ('Prerequisites',100)]
        coursesThatFitLabel = Label(self.bottomFrame, text="COURSES THAT FIT YOUR CRITERIA:", \
        font='Times 18 bold', fg='navy')
        coursesThatFitLabel.grid(sticky=E+W, padx=2, row=0)
       
        mlb = CourseResultsBox(self.bottomFrame, columnTuples)
        mlb.grid_(row=2, column=0, sticky=E+W)
        
        # Button section ---------->
        updateButton = Button(self.buttonFrame, text='Update Courses')
        updateButton.grid(row=0, column=4)
        makeScheduleButton = Button(self.buttonFrame, text="Add To Schedule")
        makeScheduleButton.grid(row=0, column=3)
        #saveCRNs = Button(buttonFrame, text="Save CRN")
        #saveCRNs.grid(row=0, column=2)

class CourseResultsBox(Tk): 
        def __init__(self, master, columnTuples, **kwargs): 
            self.box = multiListBox.MultiListbox(master, columnTuples, command=self.onReturn)
            self.createTableContent()
     
        def grid_(self, **kwargs): 
            self.box.grid(**kwargs)
        
        def onReturn(self): 
            print 'hit Return or double clicked' #placeholder...
        
        def createTableContent(self): 
            # Placeholder...
            for i in range (100):
                self.box.insert (END, ('Important Message: %d' % i,
                                'John Doe',
                                '10/10/%04d' % (1900+i), 
                                i, i, i, i, i, i, i, i, i))
                

app = CourseBrowserApp()
app.mainloop()