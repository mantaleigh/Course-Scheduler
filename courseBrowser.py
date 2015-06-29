# By Samantha Voigt

from Tkinter import *
import HTMLscraper as scrape
from schedule import Schedule
from scrolledFrame import ScrolledFrame
from courseResultsBox import CourseResultsBox
from scrollableOptionFrame import ScrollableOptionFrame

class CourseBrowserApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Course Browser')
        self.reader = scrape.ScraperReader()

        try:
            self.distributions = self.reader.readDistFile()
            self.subjects = self.reader.readSubjFile()
            self.departments = self.reader.readDeptFile()
            self.allCourses = self.reader.readCoursesFile()
        except IOError:
            self.scraper = scrape.BrowserScraper()
            self.scraper.updateAll()
            self.distributions = self.scraper.readDistFile()
            self.subjects = self.scraper.readSubjFile()
            self.departments = self.scraper.readDeptFile()
            self.allCourses = self.scraper.readCoursesFile()

        self.selectedCourses = self.allCourses # will be used to hold the courses that are currently in the resultsBox --> the ones that fit the criteria
                                               # starts out being all courses
        self.createdOptions = []
        self.toSearchVars = {}
        self.scheduleInProgress = None

        self.pleaseSelectExists = False # please select label exists
        self.showCoursesButtonExists = False # show courses button exists

        self.createFrames()
        self.createWidgets()

    def createFrames(self):
        '''Creates the frames (and a canvas) to organize all the information in the main app and create scrollbars'''

        self.mainFrame = ScrolledFrame(self)
        self.mainFrame.pack(fill=BOTH, expand=TRUE)

        self.topFrame = Frame(self.mainFrame.interior, bd=2, relief=GROOVE, takefocus=True)
        self.topFrame.pack(fill=X)
        self.topFrameLeft = Frame(self.topFrame, takefocus=True, bd=2, relief=GROOVE)
        self.topFrameLeft.pack(side=LEFT, expand=YES, fill=X)
        self.topFrameRight = Frame(self.topFrame, takefocus=True, bd=2, relief=GROOVE)
        self.topFrameRight.pack(side=RIGHT, expand=YES, fill=X)
        self.middleFrame = Frame(self.mainFrame.interior, bd=2, relief=GROOVE, takefocus=True)
        self.middleFrame.pack(fill=X)
        self.bottomFrame = Frame(self.mainFrame.interior, bd=2, relief=GROOVE, takefocus=True)
        self.bottomFrame.pack(fill=BOTH, expand=YES)
        self.buttonFrame = Frame(self.mainFrame.interior, bd=2, relief=GROOVE, takefocus=True)
        self.buttonFrame.pack(fill=X, expand=YES)

    def createWidgets(self):

        # 'Search By' section ------->
        searchByLabel = Label(self.topFrameLeft, text='SEARCH BY:', fg='navy',font='Times 16 bold')
        searchByLabel.pack(side=LEFT, fill=X, expand=YES)
        searchByBoxes = ['Distribution', 'Subject', 'Department', 'Time/Days']
        self.searchVars = {}
        for box in searchByBoxes:
            var = IntVar()
            button = Checkbutton(self.topFrameLeft,text=box,variable=var)
            button.pack(side=LEFT, fill=X, expand=YES)
            self.searchVars[box] = var

        # 'Show Only' section ------->
        showOnlyLabel = Label(self.topFrameRight, text='SHOW ONLY:', fg='navy', font='Times 16 bold')
        showOnlyLabel.pack(side=LEFT, fill=X, expand=YES)
        self.showVars = {}
        showOnlyBoxes = ['If seats are available*','100 levels','200 levels','300 levels']
        for box in showOnlyBoxes:
            var = IntVar()
            button = Checkbutton(self.topFrameRight, text=box, variable=var)
            button.pack(side=LEFT, fill=X, expand=YES)
            self.showVars[box] = var

        criteriaOptionsButton = Button(self.middleFrame, text="Give me options!", command=self.createCriteriaOptions)
        criteriaOptionsButton.pack(fill=X)

        # Results ("Courses That Fit") section -------->
        coursesThatFitLabel = Label(self.bottomFrame, text="COURSES THAT FIT YOUR CRITERIA:", \
        font='Times 18 bold', fg='navy')
        coursesThatFitLabel.pack(fill=X)
        coursesHelpText = Label(self.bottomFrame, \
            text="Hit Return/Enter on a course row to see the description, prerequisites, & additional instructors for that course", \
        font='Times 12 italic')
        coursesHelpText.pack(fill=X)

        self.resultsBox = CourseResultsBox(self.bottomFrame, self.allCourses)
        self.resultsBox.pack_(fill=X, expand=YES)

        # Button section ---------->
        notes = Label(self.buttonFrame, text="Note that some fields may not reflect recent changes, and that updating the courses may take a few minutes.", font='Times 12 italic')
        notes.pack()
        updateButton = Button(self.buttonFrame, text='Update Courses', command=self.updateCourses)
        updateButton.pack(side=LEFT, fill=X, expand=YES)
        makeScheduleButton = Button(self.buttonFrame, text="Add Course To Schedule", command=self.makeSchedule)
        makeScheduleButton.pack(side=LEFT, fill=X, expand=YES)



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

#               The please select label needs to be fixed so that it shows up when nothing is selected,
#               and dissapears when something is.

        pleaseSelectLabel = Label(self.middleFrame, text="Please select some search criteria for options to be displayed", fg='red', font='Times 14 italic')


        if criteriaList == []:
            if(not self.pleaseSelectExists):
                pleaseSelectLabel.pack(fill=X)
                self.pleaseSelectExists = True
        else:
            if(self.pleaseSelectExists):
                pleaseSelectLabel.pack_forget() # TODO: This isn't working... why?
                self.pleaseSelectExists = False

                #add in all the "new" options -- the ones that haven't been displayed yet
        if(not self.showCoursesButtonExists and criteriaList != []):
            showCoursesButton.pack(fill=X)
            self.showCoursesButtonExists = True
        for option in criteriaList:
            if option not in self.createdOptions:
                optionFrame = ScrollableOptionFrame(self.middleFrame, option, self.distributions, self.subjects, self.departments, self.toSearchVars)
                optionFrame.pack(side=LEFT, fill=X, expand=YES)
                self.createdOptions.append(option)


    def makeSchedule(self):
        selectedItem = self.resultsBox.getScheduleInfo()
        try:
            self.scheduleInProgress.addCourse(selectedItem)
        except (TclError, AttributeError): # except when no schedule exists (either scheduleInProgress is None or it has been closed)
            self.scheduleInProgress = Schedule(selectedItem, self.selectedCourses)


    def updateCourses(self):
        scraper = scrape.BrowserScraper()
        updatedCourses = scraper.updateAll()
        self.resultsBox.updateCourseInfo(updatedCourses)

