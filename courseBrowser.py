# By Samantha Voigt

from Tkinter import *
import HTMLscraper as scraper
from schedule import Schedule
from scrolledFrame import ScrolledFrame
from courseResultsBox import CourseResultsBox
from scrollableOptionFrame import ScrollableOptionFrame

class CourseBrowserApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Course Browser')
        self.grid()
        self.scrape = scraper.BrowserScraper()

        try:
            self.distributions = self.scrape.readDistFile()
            self.subjects = self.scrape.readSubjFile()
            self.departments = self.scrape.readDeptFile()
            self.allCourses = self.scrape.readCoursesFile()
        except IOError:
            self.scrape.updateAll()
            self.distributions = self.scrape.readDistFile()
            self.subjects = self.scrape.readSubjFile()
            self.departments = self.scrape.readDeptFile()
            self.allCourses = self.scrape.readCoursesFile()

        self.selectedCourses = self.allCourses # will be used to hold the courses that are currently in the mlb --> the ones that fit the criteria
                                               # starts out being all courses
        self.createdOptions = []
        self.toSearchVars = {}
        self.scheduleInProgress = None

#        self.pleaseSelectExists = False # please select label exists
        self.showCoursesButtonExists = False # show courses button exists

        self.createFrames()
        self.createWidgets()

    def createFrames(self):
        '''Creates the frames (and a canvas) to organize all the information in the main app and create scrollbars'''

        # smaller frames are packed into the main frame, smaller frames use grid

        self.mainFrame = ScrolledFrame(self)
        self.mainFrame.pack(fill=BOTH, expand=TRUE)

        self.topFrame = Frame(self.mainFrame.interior, bd=2, relief=GROOVE, takefocus=True)
        self.topFrame.pack()
        self.topFrameLeft = Frame(self.topFrame, takefocus=True, bd=2, relief=GROOVE)
        self.topFrameLeft.pack(side=LEFT)
        self.topFrameRight = Frame(self.topFrame, takefocus=True, bd=2, relief=GROOVE)
        self.topFrameRight.pack(side=RIGHT)
        self.middleFrame = Frame(self.mainFrame.interior, bd=2, relief=GROOVE, takefocus=True)
        self.middleFrame.pack()
        self.bottomFrame = Frame(self.mainFrame.interior, bd=2, relief=GROOVE, takefocus=True)
        self.bottomFrame.pack()
        self.buttonFrame = Frame(self.mainFrame.interior, bd=2, relief=GROOVE, takefocus=True)
        self.buttonFrame.pack()

    def createWidgets(self):

        # 'Search By' section ------->
        searchByLabel = Label(self.topFrameLeft, text='SEARCH BY:', fg='navy',font='Times 16 bold')
        searchByLabel.grid(row=0, column=0, sticky=W+E, padx=20)
        searchByBoxes = ['Distribution', 'Subject', 'Department', 'Time/Days']
        colAvail = 1
        self.searchVars = {}
        for box in searchByBoxes:
            var = IntVar()
            button = Checkbutton(self.topFrameLeft,text=box,variable=var)
            button.grid(row=0, column=colAvail, sticky=W+E, padx=5)
            self.searchVars[box] = var
            colAvail += 1

        # 'Show Only' section ------->
        showOnlyLabel = Label(self.topFrameRight, text='SHOW ONLY:', fg='navy', font='Times 16 bold')
        showOnlyLabel.grid(row=0, column=0, sticky=W+E, padx=20)
        colAvail = 1
        self.showVars = {}
        showOnlyBoxes = ['If seats are available*','100 levels','200 levels','300 levels']
        for box in showOnlyBoxes:
            var = IntVar()
            button = Checkbutton(self.topFrameRight, text=box, variable=var)
            button.grid(row=0, column=colAvail, sticky=W+E, padx=5)
            self.showVars[box] = var
            colAvail += 1

        criteriaOptionsButton = Button(self.middleFrame, text="Give me options!", command=self.createCriteriaOptions)
        criteriaOptionsButton.pack(fill=X)

        # Results ("Courses That Fit") section -------->
        coursesThatFitLabel = Label(self.bottomFrame, text="COURSES THAT FIT YOUR CRITERIA:", \
        font='Times 18 bold', fg='navy')
        coursesThatFitLabel.grid(sticky=E+W, padx=2, row=0)
        coursesHelpText = Label(self.bottomFrame, \
            text="Hit Return/Enter on a course row to see the description, prerequisites, & additional instructors for that course", \
        font='Times 12 italic')
        coursesHelpText.grid(sticky=E+W, row=1)

        self.mlb = CourseResultsBox(self.bottomFrame, self.scrape)
        self.mlb.grid_(row=2, column=0, sticky=E+W)

        # Button section ---------->
        updateButton = Button(self.buttonFrame, text='Update Courses', command=self.scrape.updateCourseInfo)
        updateButton.grid(row=0, column=0)
        makeScheduleButton = Button(self.buttonFrame, text="Add Course To Schedule", command = self.makeSchedule)
        makeScheduleButton.grid(row=0, column=1)
        delScheduleButton = Button(self.buttonFrame, text="Restart Schedule", command = None) #need to update command
        delScheduleButton.grid(row=0, column=2)
        notes = Label(self.buttonFrame, text="Note that some fields may not reflect recent changes, and that updating the courses may take a few minutes.", font='Times 12 italic')
        notes.grid(row=1, columnspan=3)

    def checkSearchButtons(self):
        '''Check the state of the 'Search By' checkbuttons and returns a list w/the name of those that were clicked '''
        criteriaList = []
        for key, value in self.searchVars.items():
            state = value.get()
            if state != 0:
                criteriaList.append(key)
        return criteriaList

    def checkShowButtons(self):
        '''Check the state of the 'Show Only' checkbuttons and returns a list w/the name of those that were clicked. '''
        criteriaList = []
        for key, value in self.showVars.items():
            state = value.get()
            if state != 0:
                criteriaList.append(key)
        return criteriaList

    def createCriteriaOptions(self):
        criteriaList = self.checkSearchButtons() # check to see what is selected
        showCoursesButton = Button(self.middleFrame, text="Show me courses!", command=None)

#               The please select label needs to be fixex so that it shows up when nothing is selected,
#               and dissapears when something is.

 #       pleaseSelectLabel = Label(self.middleFrame, text="Please select some search criteria for options to be displayed", fg='red', font='Times 14 italic')


##        if criteriaList == []:
##            if(not self.pleaseSelectExists):
##                pleaseSelectLabel.pack()
##                self.pleaseSelectExists = True
##        else:
            #only pack the showCoursesButton when options are displaying and it hasn't been packed already
            #destroy the pleaseSelectLabel if no criteria were selected
##            if(self.pleaseSelectExists):
##                pleaseSelectLabel.pack_forget()
##                self.pleaseSelectExists = False

                #add in all the "new" options -- the ones that haven't been displayed yet
        for option in criteriaList:
            if option not in self.createdOptions:
                optionFrame = ScrollableOptionFrame(self.middleFrame, option, self.distributions, self.subjects, self.departments, self.toSearchVars)
                optionFrame.pack(side=LEFT)
                self.createdOptions.append(option)
        if(not self.showCoursesButtonExists and self.createdOptions != []):
            showCoursesButton.pack(fill=X)
            self.showCoursesButtonExists = True

    def makeSchedule(self):
        selectedItem = self.mlb.getScheduleInfo()
        try:
            self.scheduleInProgress.addCourse(selectedItem)
        except (TclError, AttributeError): # except when no schedule exists (either scheduleInProgress is None or it has been closed)
            self.scheduleInProgress = Schedule(selectedItem, self.selectedCourses)


app = CourseBrowserApp()
app.mainloop()
