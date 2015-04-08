# Samantha Voigt
# Course Results Box for the course browser app

from Tkinter import *
import multiListBox as mlb
import HTMLscraper as scraper

class CourseResultsBox():
        def __init__(self, master, **kwargs):
            self.columnHeaders = ['CRN', 'Course', 'Title', 'Seats Available',
            'Location(s)', 'Day/Time', 'Instructor', 'Distribution(s)']
            columnTuples = [('CRN',45), ('Course',90), ('Title',200), ('Seats Avail.',75),\
            ('Location(s)',100), ('Day/Time',200), ('Instructor',125), ('Distribution(s)',250)]
            self.box = mlb.MultiListbox(master, columnTuples)
            try:
                self.selectedCourses = scraper.readCoursesFile() # starts out as all the courses
            except IOError:
                scraper.updateCourseInfo()
                self.selectedCourses = scraper.readCoursesFile()
            self.populateTableContent()
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
            selectedCourseInfo = (item for item in self.selectedCourses if item['CRN'] == CRN).next()
            description = selectedCourseInfo['Description']
            prereqs = selectedCourseInfo['Prerequisite(s)']
            if 'Additional Instructor(s)' in selectedCourseInfo:
                self.extraInfoApp = ExtraInfoApp(description, prereqs, additionalInstructor=selectedCourseInfo['Additional Instructor(s)'])
                self.extraInfoApp.mainloop()
            else:
                self.extraInfoApp = ExtraInfoApp(description, prereqs)
                self.extraInfoApp.mainloop()

        def populateTableContent(self):
            '''Deletes previous course data and adds course data (from selectedCourses) into the listbox'''
            for course in self.selectedCourses:
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

                        # there needs to be a better way to consolidate the times
                        elif type(course[header]) is dict:
                            dictionary = course[header]
                            timeToDayDict = {} # dict of times and their corresponding days
                            for key in dictionary: # key is the day, value is the time
                                if dictionary[key] not in timeToDayDict:
                                    timeToDayDict[dictionary[key]] = key
                                else:
                                    timeToDayDict[dictionary[key]] = timeToDayDict[dictionary[key]] + key

                            dayTimeStr = ''
                            for time in timeToDayDict:
                                dayTimeStr = dayTimeStr + timeToDayDict[time] + ": " + time + "|"
                            courseInfo.append(dayTimeStr)
                    except KeyError: #When the key doesn't exist (ex: for courses w/no additional instructor)
                        courseInfo.append('') #use blank string

                self.box.insert(END, courseInfo)

        # updates the table using a new list of dicts that represent courses
        def updateCourseInfo(self, newCourses):
            self.selectedCourses = newCourses
            populateTableContent()

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
