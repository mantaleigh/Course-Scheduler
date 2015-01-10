# By Samantha Voigt

from Tkinter import * 
import HTMLscraper as scraper

class CourseBrowserApp(Tk): 
    def __init__(self): 
        Tk.__init__(self)
        self.title('Course Browser')
        self.grid()
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
        '':''}
        self.createWidgets()
        
    def createWidgets(self): 
        
        # Frames
        topFrame = Frame(self, bd=2, relief=GROOVE, takefocus=True)
        topFrame.pack()
        topFrameLeft = Frame(topFrame, takefocus=True, bd=2, relief=GROOVE)
        topFrameLeft.pack(side=LEFT)
        topFrameRight = Frame(topFrame, takefocus=True, bd=2, relief=GROOVE)
        topFrameRight.pack(side=RIGHT)
        #middleFrame = Frame(self, bd=2, relief=GROOVE, takefocus=True)
        #middleFrame.pack()
        bottomFrame = Frame(self, bd=2, relief=GROOVE, takefocus=True)
        bottomFrame.pack()
        buttonFrame = Frame(self, bd=2, relief=GROOVE, takefocus=True)
        buttonFrame.pack()
        
        
        # 'Search By' section ------->
        searchByLabel = Label(topFrameLeft, text='SEARCH BY:', fg='navy',font='Times 16 bold')
        searchByLabel.grid(row=0, column=0, sticky=W+E, padx=30)
        searchByBoxes = ['Distribution', 'Subject', 'Department', 'Time/Days', 'Professor']
        searchByVars = []
        rowAvail = 1
        for box in searchByBoxes: 
            var = IntVar()
            button = Checkbutton(topFrameLeft,text=box,variable=var)
            button.grid(row=rowAvail, column=0, sticky=W+E, padx=30)
            searchByVars.append(var)
            rowAvail += 1
      
        # 'Show Only' section ------->
        showOnlyLabel = Label(topFrameRight, text='SHOW ONLY:', fg='navy', font='Times 16 bold')
        showOnlyLabel.grid(row=0, column=1, sticky=W+E, padx=30)
        rowAvail = 1
        showOnlyBoxes = ['If seats are available*','100 levels','200 levels','300 levels']
        showOnlyVars = []
        for box in showOnlyBoxes: 
            var = IntVar()
            button = Checkbutton(topFrameRight, text=box, variable=var)
            button.grid(row=rowAvail, column=1, sticky=W+E, padx=30)
            showOnlyVars.append(var)
            rowAvail += 1
        
        # Results ("Courses That Fit") section -------->
        coursesThatFitLabel = Label(bottomFrame, text="COURSES THAT FIT YOUR CRITERIA:", \
        font='Times 18 bold', fg='navy')
        coursesThatFitLabel.grid(sticky=E+W, padx=2, row=0)
        
        scrollbar = Scrollbar(bottomFrame, orient=VERTICAL)
        scrollbar.grid(row=2, column=1, sticky=N+S)
        listbox = Listbox(bottomFrame, yscrollcommand=scrollbar.set, width=52, selectmode=MULTIPLE)
        listbox.grid(row=2, column=0, sticky=E+W)
        scrollbar['command'] = listbox.yview
        
        for i in range(1000): 
            listbox.insert(END, str(i))

        
        # Button section ---------->
        updateButton = Button(buttonFrame, text='Update Courses')
        updateButton.grid(row=0, column=4)
        makeScheduleButton = Button(buttonFrame, text="Make Schedule")
        makeScheduleButton.grid(row=0, column=3)
        saveCRNs = Button(buttonFrame, text="Save CRN(s)")
        saveCRNs.grid(row=0, column=2)

app = CourseBrowserApp()
app.mainloop()