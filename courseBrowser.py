# By Samantha Voigt

from Tkinter import * 
import HTMLscraper as scraper
import multiListBox as mlb

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
        coursesThatFitLabel = Label(self.bottomFrame, text="COURSES THAT FIT YOUR CRITERIA:", \
        font='Times 18 bold', fg='navy')
        coursesThatFitLabel.grid(sticky=E+W, padx=2, row=0)
        coursesHelpText = Label(self.bottomFrame, \
            text="Hit Return/Enter on a course row to see the description, prerequisites, & additional instructors for that course", \
        font='Times 12 italic')
        coursesHelpText.grid(sticky=E+W, row=1)
       
        mlb = CourseResultsBox(self.bottomFrame)
        mlb.grid_(row=2, column=0, sticky=E+W)
        
        # Button section ---------->
        updateButton = Button(self.buttonFrame, text='Update Courses', command=scraper.updateCourseInfo)
        updateButton.grid(row=0, column=0)
        makeScheduleButton = Button(self.buttonFrame, text="Add Course To Schedule")
        makeScheduleButton.grid(row=0, column=1)
        notes = Label(self.buttonFrame, text="Note that some fields may not reflect recent changes, and that updating the courses may take a few minutes.", 
        font='Times 12 italic')
        notes.grid(row=1, columnspan=2)

class CourseResultsBox(): 
        def __init__(self, master, **kwargs): 
            columnHeaders = ['CRN', 'Course', 'Title', 'Seats Available', 
            'Location(s)', 'Day/Time', 'Instructor', 'Distribution(s)']
            columnTuples = [('CRN',45), ('Course',90), ('Title',200), ('Seats Avail.',75),\
            ('Location(s)',100), ('Day/Time',200), ('Instructor',125), ('Distribution(s)',250)]
            self.box = mlb.MultiListbox(master, columnTuples)
            self.createStartingTableContent(columnHeaders)
            self.box.bind("<Return>", self.onReturn)
            self.extraInfoApp = None
     
        def grid_(self, **kwargs): 
            self.box.grid(**kwargs)
        
        def onReturn(self, event): 
            if self.extraInfoApp!=None: self.extraInfoApp.destroy()
            CRN = self.box.get(self.box.curselection())[0]
            allCourses = scraper.readCourseFile()
            selectedCourseInfo = (item for item in allCourses if item['CRN'] == CRN).next()
            description = selectedCourseInfo['Description']
            prereqs = selectedCourseInfo['Prerequisite(s)']
            if 'Additional Instructor(s)' in selectedCourseInfo:
                self.extraInfoApp = ExtraInfoApp(description, prereqs, additionalInstructor=selectedCourseInfo['Additional Instructor(s)'])
                self.extraInfoApp.mainloop()
            else: 
                self.extraInfoApp = ExtraInfoApp(description, prereqs)
                self.extraInfoApp.mainloop()
        
        def createStartingTableContent(self, columnHeaders):
            '''Adds all course data into the listbox'''
            for course in scraper.readCourseFile():
                courseInfo = []
                for header in columnHeaders: 
                    try: 
                        if type(course[header]) is str:
                            courseInfo.append(course[header])
                        
                        elif type(course[header]) is list: 
                            combinedElt = ''
                            for elt in course[header]: 
                                combinedElt = combinedElt + elt + ' | '
                            courseInfo.append(combinedElt)
                                
                        elif type(course[header]) is dict: 
                            dictionary = course[header]
                            keys = dictionary.keys()
                            combinedVals = ''
                            for key in keys: 
                                combinedVals = combinedVals + ' | ' + key + ': ' + dictionary[key]
                            courseInfo.append(combinedVals + ' |')
                    except KeyError: 
                        courseInfo.append('')
            
                self.box.insert (END, courseInfo)  
        
        def updateCourseInfo(self, columnHeaders): 
            pass
            
class ExtraInfoApp(Toplevel): 
    def __init__(self, description, prereqs, additionalInstructor=None): 
        Toplevel.__init__(self)
        self.title('Extra Information')
        #self.grid()
        self.createFrames(additionalInstructor)
        self.createWidgets(description, prereqs, additionalInstructor)
    
    def createFrames(self, additionalInstructor):
        self.descFrame = Frame(self, bd=2, relief=GROOVE, takefocus=True)
        self.descFrame.pack()
        self.prereqFrame = Frame(self, bd=2, relief=GROOVE, takefocus=True)
        self.prereqFrame.pack()
        if additionalInstructor != None: 
            self.addtlInstFrame = Frame(self, bd=2, relief=GROOVE, takefocus=True)
            self.addtlInstFrame.pack()
    
    #can probably pretty this up (less repetition) with a dictionary or list
    def createWidgets(self, description, prereqs, additionalInstructor):
        descriptionLabel = Label(self.descFrame,font='Times 18 bold', fg='navy', text="DESCRIPTION:")
        descriptionLabel.pack()
        descriptionText = Message(self.descFrame, text=description)
        descriptionText.pack()
        prereqLabel = Label(self.prereqFrame, font='Times 18 bold', fg='navy', text="PREREQUISITE(S):")
        prereqLabel.pack()
        prereqText = Message(self.prereqFrame, text=prereqs)
        prereqText.pack()
        if additionalInstructor != None: 
            instructorLabel = Label(self.addtlInstFrame, font='Times 18 bold', fg='navy', text="ADDITIONAL INSTRUCTOR(S):")
            instructorLabel.pack()
            instructorText = Label(self.addtlInstFrame, text=additionalInstructor)
            instructorText.pack()

app = CourseBrowserApp()
app.mainloop()