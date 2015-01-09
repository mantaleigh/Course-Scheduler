# By Samantha Voigt

from Tkinter import * 
import HTMLscraper as scraper

class CourseBrowserApp(Tk): 
    def __init__(self): 
        Tk.__init__(self)
        self.title('Course Browser')
        self.grid()
        self.createWidgets()
        
    def createWidgets(self): 
        
        # Frames
        topFrame = Frame(self, bd=2, relief=GROOVE, takefocus=True)
        topFrame.grid(sticky=N+E+S+W)
        bottomFrame = Frame(self, bd=2, relief=GROOVE, takefocus=True)
        bottomFrame.grid(sticky=N+E+S+W)
        
        
        # 'Search By' section ------->
        searchByLabel = Label(topFrame, text='SEARCH BY:', fg='black',font='Times 16 bold')
        searchByLabel.grid(row=0, column=0, sticky=W+E, padx=10)
        searchByBoxes = ['Distribution', 'Department', 'Time/Days', 'Professor']
        searchByVars = []
        rowAvail = 1
        for box in searchByBoxes: 
            var = IntVar()
            button = Checkbutton(topFrame,text=box,variable=var)
            button.grid(row=rowAvail, column=0, sticky=W+E, padx=10)
            searchByVars.append(var)
            rowAvail += 1
      
        # 'Show Only' section ------->
        showOnlyLabel = Label(topFrame, text='SHOW ONLY:', fg='black', font='Times 16 bold')
        showOnlyLabel.grid(row=0, column=1, sticky=W+E, padx=10)
        rowAvail = 1
        showOnlyBoxes = ['If seats are available*','100 levels','200 levels','300 levels']
        showOnlyVars = []
        for box in showOnlyBoxes: 
            var = IntVar()
            button = Checkbutton(topFrame, text=box, variable=var)
            button.grid(row=rowAvail, column=1, sticky=W+E, padx=10)
            showOnlyVars.append(var)
            rowAvail += 1
        
        coursesThatFitLabel = Label(bottomFrame, text="COURSES THAT FIT YOUR CRITERIA:", \
        font='Times 18 bold', padx=10)
        coursesThatFitLabel.grid(row=rowAvail, sticky=E+W)
        
    
        
        
        

app = CourseBrowserApp()
app.mainloop()