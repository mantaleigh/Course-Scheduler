# Samantha Voigt
# Class that represents the different option frames available for the course browser app

from Tkinter import *

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
