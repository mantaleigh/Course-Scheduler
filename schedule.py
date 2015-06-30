# Samantha Voigt
# Schedule TopLevel window for the courseBrowser
# also additional Toplevel windows that "come off" the Schedule

from Tkinter import *
import os

class Schedule(Toplevel):
    def __init__(self, selectedItem, selectedCourses):
        Toplevel.__init__(self)
        self.title('Proposed Schedule')
        self.canvasWidth = 500
        self.canvasHeight = 525
        self.vDistApart = self.canvasHeight/15
        self.hDistApart = self.canvasWidth/6
        self.colors = ['orange', 'green', 'purple', 'yellow', 'cyan', 'turquoise']
        self.currentColorIndex = 0

        # make canvas
        self.canvas = Canvas(self, width=self.canvasWidth,height=self.canvasHeight)
        self.canvas.pack(expand=YES, fill=BOTH)

        self.selectedCourses = selectedCourses # to use later
        self.scheduledCourses = []

        self.createBlankSchedule()
        self.createWidgets()
        self.addCourse(selectedItem)

    def createWidgets(self): 
        self.helpLabel = Label(self, text="Note that saving the CRNs to desktop currently only works on Mac (will fix)", fg='blue', font='Times 14 italic')
        self.helpLabel.pack(expand=YES)
        restartButton = Button(self, text="Restart Schedule", command=self.restart)
        restartButton.pack(side=LEFT, expand=YES)
        saveButton = Button(self, text="Save CRNs", command=self.saveCRNs)
        saveButton.pack(side=LEFT, expand=YES)

    def createBlankSchedule(self):
        self.canvas.create_line(0,25, self.canvasWidth, 25)
        hour = 8
        amOrPm = 'am'
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for i in range(1,16): # create the horizontal lines and the hour markings
            self.canvas.create_text(self.hDistApart/2-25, (self. vDistApart*i-20), text=str(hour)+':00' + ' ' + amOrPm, fill="red", anchor=W)
            hour += 1
            if hour == 12:
                amOrPm = 'pm'
            if hour == 13:
                hour = 1
            # solid lines
            self.canvas.create_line(0, (self.vDistApart*i)+25, self.canvasWidth, (self.vDistApart*i)+25)
            # dotted lines
            self.canvas.create_line(self.hDistApart, (self.vDistApart*i)-(self.vDistApart/2)+25, self.canvasWidth, (self.vDistApart*i)-(self.vDistApart/2)+25, dash=(4,4))

        for i in range(1, 7): # create the vertical lines and the day markings
            self.canvas.create_line(self.hDistApart*i, 0, self.hDistApart*i, self.canvasHeight+25)
            if i > 1:
                self.canvas.create_text(self.hDistApart*i-(self.hDistApart/2), 15, text=days[i-2], fill='red')

    def addCourse(self, selectedItem):
        if selectedItem not in self.scheduledCourses: # if it hasn't already been added
            self.scheduledCourses.append(selectedItem)
            CRN = selectedItem['CRN']
            course = selectedItem['Course']
            color = self.colors[self.currentColorIndex] # color for the selected course
            if self.currentColorIndex < (len(self.colors)-1): # increment for the next course to have a different color
                self.currentColorIndex+=1
            else: self.currentColorIndex = 0

            # TODO
            # currently looping through all selected courses because I don't have an easily usable 
            # version of day and times stored in the table. --- need to improve 
            for item in self.selectedCourses.values():
                if item['CRN'] == CRN:
                    times = item['Day/Time'] # is a dictionary

            dayToiValDict = {'M': 1, 'T': 2, 'W': 3, 'Th': 4, 'F': 5} # matches a day abbr. w/ the i value from createBlankSchedule used to make the corresponding leftmost line
            for day in times: # days are the keys of the dictionary
                # get upmost distance and bottom most distance that corresponds to the time
                time = times[day]
                startTime = time[:time.find('-')].strip()
                endTime = time[time.find('-')+2:].strip()
                startHour = int(startTime[:startTime.find(':')].strip())
                endHour = int(endTime[:endTime.find(':')].strip())
                startMin = int(startTime[startTime.find(':')+1:startTime.find(':')+3].strip())
                endMin = int(endTime[endTime.find(':')+1:startTime.find(':')+3].strip())

                if 'am' in startTime: starti = startHour - 8 # 8am corresponds to i of 0
                else:
                    if startHour == 12: starti = 4 # noon is an i of 4
                    else: starti = startHour + 4 

                # same thing as above except for the end time
                if 'am' in endTime: endi = endHour - 8
                else:
                    if endHour == 12: endi = 4
                    else: endi = endHour + 4

                if startMin != 0: 
                    startMinDisplacement = float(startMin)/60.0
                else: startMinDisplacement = 0

                if endMin != 0: 
                    endMinDisplacement = float(endMin)/60.0
                else: endMinDisplacement = 0

                dayi = dayToiValDict[day]

                # point 1 is the top left corner, then the points proceed clockwise
                polygonPt2_X = polygonPt3_X = self.hDistApart*dayi
                polygonPt1_X = polygonPt4_X = self.hDistApart*(dayi+1)
                polygonPt1_Y = polygonPt2_Y = (starti+startMinDisplacement)*self.vDistApart+25
                polygonPt3_Y = polygonPt4_Y = (endi+endMinDisplacement)*self.vDistApart+25

                self.canvas.create_polygon(polygonPt1_X, polygonPt1_Y, polygonPt2_X, polygonPt2_Y, polygonPt3_X, polygonPt3_Y, polygonPt4_X, polygonPt4_Y, fill=color, tags="courses")
                self.canvas.create_text(polygonPt2_X+5, polygonPt1_Y+20, anchor=NW, text="CRN: " + CRN, tags="courses") # +5 is just for offset from top and left
                self.canvas.create_text(polygonPt2_X+5, polygonPt1_Y+5, anchor=NW, text=course[:course.index('-')-1], tags="courses") # +5 is just for offset from top and left

    def restart(self): 
        self.canvas.delete("courses")
        self.scheduledCourses = [] # clear out all the stored courses

    # TODO: put all of this in the command, not another function
    def saveCRNs(self): 
        FileNamePrompt(self.scheduledCourses)

class FileNamePrompt(Toplevel): 
    def __init__(self, scheduledCourses): 
        Toplevel.__init__(self)
        self.title('Save CRNs')
        self.scheduledCourses = scheduledCourses
        self.helpText = Label(self, text="Please enter a name for the CRN file:", fg='blue', font='Times 14 italic')
        self.helpText.pack(expand=YES, fill=BOTH)
        self.fileNameField = Entry(self)
        self.fileNameField.insert(0, "CRN_file_name")
        self.fileNameField.pack(expand=YES)
        self.saveButton = Button(self, text="Save to Desktop", command=self.save)
        self.saveButton.pack()
        self.cancelButton = Button(self, text="Cancel", command=self.destroy)
        self.cancelButton.pack()

    def save(self): 
        filename = self.fileNameField.get() + ".txt"
        completeName = os.path.join(os.path.expanduser('~'), 'Desktop', filename)
        try:
            crnFile = open(completeName, "w")
            for course in self.scheduledCourses:
                crnFile.write(course['CRN'] + ': ' + course['Title'] + '\n')
            crnFile.close()
            StatusPrompt("Success", "Your file was successfully saved to your desktop.")
            self.destroy()
        except IOError: 
            StatusPrompt("Error", "There was a problem saving your file.")
            print IOError
            self.destroy()

# generic status prompt
class StatusPrompt(Toplevel): 
    def __init__(self, titleText, statusText): 
        Toplevel.__init__(self)
        self.title(titleText)
        self.text = Label(self, text=statusText, font='Times 14')
        self.text.pack(expand=YES, fill=BOTH)
        self.okButton = Button(self, text="Ok", command=self.destroy)
        self.okButton.pack(expand=YES)

