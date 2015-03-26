# By Samantha Voigt

from Tkinter import * 
import HTMLscraper as scraper
import multiListBox as mlb

class CourseBrowserApp(Tk): 
    def __init__(self): 
        Tk.__init__(self)
        self.title('Course Browser')
        self.grid()

        try:
            self.distributions = scraper.readDistFile()
            self.subjects = scraper.readSubjFile()
            self.departments = scraper.readDeptFile()
            self.allCourses = scraper.readCoursesFile()
        except IOError:
            scraper.updateAll()
            self.distributions = scraper.readDistFile()
            self.subjects = scraper.readSubjFile()
            self.departments = scraper.readDeptFile()
            self.allCourses = scraper.readCoursesFile()

        self.selectedCourses = {} # will be used to hold the courses that are currently in the mlb --> the ones that fit the criteria 
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
       
        self.mlb = CourseResultsBox(self.bottomFrame)
        self.mlb.grid_(row=2, column=0, sticky=E+W)
        
        # Button section ---------->
        updateButton = Button(self.buttonFrame, text='Update Courses', command=scraper.updateCourseInfo)
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

#               PLEASE SELECT STRUGGLES 

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
        colors = ['orange', 'green', 'purple', 'yellow', 'blue']
        selectedItem = self.mlb.getScheduleInfo() #need to re-format day/time
        if self.scheduleInProgress == None:  
            self.scheduleInProgress = Schedule(selectedItem)
            self.scheduleInProgress.createBlankSchedule()
        else:
            self.scheduleInProgress.addCourse(selectedItem)

     # need to figure out how to get if the schedule has been closed through the x button to set it to None


class Schedule(Toplevel):
    def __init__(self, selectedItem):
        Toplevel.__init__(self)
        self.title('Proposed Schedule')
        self.canvasWidth = 500
        self.canvasHeight = 525
        self.canvas = Canvas(self, width=self.canvasWidth,height=self.canvasHeight)
        self.canvas.pack(expand=YES, fill=BOTH)
        self.addCourse(selectedItem)

    def createBlankSchedule(self):
        vDistApart = self.canvasHeight/15
        hDistApart = self.canvasWidth/6
        self.canvas.create_line(0,25, self.canvasWidth, 25)
        hour = 8
        amOrPm = 'am'
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for i in range(1,16): # create the horizontal lines and the hour markings
            self.canvas.create_text(hDistApart/2-25, (vDistApart*i-20), text=str(hour)+':00' + ' ' + amOrPm, fill="red", anchor=W)
            hour += 1
            if hour == 13:
                hour = 1
                amOrPm = 'pm'
            self.canvas.create_line(0, (vDistApart*i)+25, self.canvasWidth, (vDistApart*i)+25)
            self.canvas.create_line(hDistApart, (vDistApart*i)-(vDistApart/2)+25, self.canvasWidth, (vDistApart*i)-(vDistApart/2)+25, dash=(4,4))

        for i in range(1, 7): # create the vertical lines and the day markings
            self.canvas.create_line(hDistApart*i, 0, hDistApart*i, self.canvasHeight+25)
            if i > 1:
                self.canvas.create_text(hDistApart*i-(hDistApart/2), 15, text=days[i-2], fill='red')            

    def addCourse(self, selectedItem):
        #print selectedItem #testing, reference
        CRN = selectedItem['CRN']
        title = selectedItem['Title']
        course = selectedItem['Course']

        #day/times:
        def makeDayTimeList(selectedItem): 
            #Right now this only works for 1-3 different day/time combinations -- adapt w/ loops?
            dayTimeList = []
            strippedDayTime = selectedItem['Day/Time'].strip(' | ')
            if strippedDayTime.count('|') == 0:
                dayTimeList.append(strippedDayTime)
            else: #if there is more than one day/time "section"
                charIndex = strippedDayTime.rfind('|')
                dayTimeList.append(strippedDayTime[:charIndex-1].strip())
                dayTimeList.append(strippedDayTime[charIndex+2:].strip())

            for n in dayTimeList:
                if n.count('|') != 0:
                    charIndex = n.rfind('|')
                    dayTimeList.append(n[:charIndex-1].strip())
                    dayTimeList.append(n[charIndex+1:].strip())
                    dayTimeList.pop(dayTimeList.index(n))
            return dayTimeList

        # what about things like W2...?
        dayTimeList = makeDayTimeList(selectedItem)
        print dayTimeList
        for n in dayTimeList:
            daysPerTime = []
            daysStr = n[:n.find(':')]
            if 'Th' in daysStr:
                daysPerTime.append('Th')
                daysStr = daysStr.strip('Th')
            daysPerTime += list(daysStr)

            print daysPerTime
                
                
            
        
        
        

        

class CourseResultsBox(): 
        def __init__(self, master, **kwargs): 
            self.columnHeaders = ['CRN', 'Course', 'Title', 'Seats Available', 
            'Location(s)', 'Day/Time', 'Instructor', 'Distribution(s)']
            columnTuples = [('CRN',45), ('Course',90), ('Title',200), ('Seats Avail.',75),\
            ('Location(s)',100), ('Day/Time',200), ('Instructor',125), ('Distribution(s)',250)]
            self.box = mlb.MultiListbox(master, columnTuples)
            self.createStartingTableContent()
            self.box.bind("<Return>", self.onReturn)
            self.extraInfoApp = None
     
        def grid_(self, **kwargs): 
            self.box.grid(**kwargs)

        def getScheduleInfo(self):
            '''Returns the CRN, course name, title, and days/times as a dictionary'''
            d = {}
            for num in [0,1,2,5]:
                d[self.columnHeaders[num]] = self.box.get(self.box.curselection())[num]
            return d
        
        def onReturn(self, event):
            '''Creates the extra info toplevel frame when return is hit while selecting a course in the listbox''' 
            if self.extraInfoApp!=None: self.extraInfoApp.destroy()
            CRN = self.box.get(self.box.curselection())[0] #get CRN (the first value) from the selection
            selectedCourseInfo = (item for item in self.allCourses if item['CRN'] == CRN).next()
            description = selectedCourseInfo['Description']
            prereqs = selectedCourseInfo['Prerequisite(s)']
            if 'Additional Instructor(s)' in selectedCourseInfo:
                self.extraInfoApp = ExtraInfoApp(description, prereqs, additionalInstructor=selectedCourseInfo['Additional Instructor(s)'])
                self.extraInfoApp.mainloop()
            else: 
                self.extraInfoApp = ExtraInfoApp(description, prereqs)
                self.extraInfoApp.mainloop()
        
        def createStartingTableContent(self):
            '''Adds all course data into the listbox'''
            #shouldn't need to put inside try/except since this is only called from within courseBrowserApp, where this is taken care of
            allCourses = scraper.readCoursesFile()
            for course in allCourses:
                courseInfo = []
                for header in self.columnHeaders: 
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
                                combinedVals = combinedVals + key + ': ' + dictionary[key] + ' | '
                            courseInfo.append(combinedVals)
                    except KeyError: #When the key doesn't exist (ex: for courses w/no additional instructor)
                        courseInfo.append('') #use blank string
            
                self.box.insert (END, courseInfo)  
        
        # will be used to update the info in the listbox given the criteria
        def updateCourseInfo(self): 
            pass
            
class ExtraInfoApp(Toplevel): 
    def __init__(self, description, prereqs, additionalInstructor=None): 
        Toplevel.__init__(self)
        self.title('Extra Information')
        self.createFrames(additionalInstructor)
        self.createWidgets(description, prereqs, additionalInstructor)
    
    def createFrames(self, additionalInstructor):
        '''Creates the frames to hold all the extra information.'''
        self.descFrame = Frame(self, bd=2, relief=GROOVE, takefocus=True)
        self.descFrame.pack()
        self.prereqFrame = Frame(self, bd=2, relief=GROOVE, takefocus=True)
        self.prereqFrame.pack()
        if additionalInstructor != None: 
            self.addtlInstFrame = Frame(self, bd=2, relief=GROOVE, takefocus=True)
            self.addtlInstFrame.pack()
    
    #can probably pretty this up (less repetition) with a dictionary or list
    def createWidgets(self, description, prereqs, additionalInstructor):
        '''Creates the widgets for the extra information (description, prerequisites, or additional instructor)'''
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

class ScrollableOptionFrame(Frame):
    def __init__(self, master, option, allDistributions, allSubjects, allDepartments, searchVars, **options):
        Frame.__init__(self, master, **options)
        self.allDistributions = allDistributions
        self.allSubjects = allSubjects
        self.allDepartments = allDepartments
        self.option = option
        self.toSearchVars = searchVars
        
        self.canvas = Canvas(self, borderwidth=0)
        self.frame = Frame(self.canvas, relief=SUNKEN)
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.config(scrollregion=(0,0,250,1500))
        
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.vsb.pack(side=RIGHT, fill=Y)
            
        self.canvas.create_window((0,0), window=self.frame, anchor=N+W)

        self.populate()

    def populate(self):
        '''populate the scrollable frame with all info'''
        if self.option.upper() == "time/days".upper():
            textStr = self.option.upper() + ":"
        else:
            textStr = self.option.upper() + "S:"
        distLabel = Label(self.frame, text=textStr, fg='navy', font='Times 16 bold', justify=CENTER)
        distLabel.pack(fill=X)
        if self.option.upper() == "distribution".upper(): infoList = self.allDistributions
        elif self.option.upper() == "subject".upper(): infoList = self.allSubjects
        elif self.option.upper() == "department".upper(): infoList = sorted(self.allDepartments.keys())
        elif self.option.upper() == "time/days".upper(): infoList = ['Monday', 'Tuesday', 'Wednesday', \
                                                                     'Thursday', 'Friday']
                                    # need to figure out how to search by time frame
                
        length = len(infoList)
        self.vars = {}
        for i in range(length):
            var = IntVar()
            button = Checkbutton(self.frame, text=infoList[i], variable=var, justify=LEFT)
            self.vars[infoList[i]] = var
            button.pack(fill=X, anchor=W)
        self.toSearchVars[self.option] = self.vars

# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
class ScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        hscrollbar = Scrollbar(self, orient=HORIZONTAL)
        hscrollbar.pack(fill=X, side=BOTTOM, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
        canvas.pack(fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

app = CourseBrowserApp()
app.mainloop()
