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
        topFrame.pack()
        topFrameLeft = Frame(topFrame, takefocus=True, bd=2, relief=GROOVE)
        topFrameLeft.pack(side=LEFT)
        topFrameRight = Frame(topFrame, takefocus=True, bd=2, relief=GROOVE)
        topFrameRight.pack(side=RIGHT)
        #middleFrame = Frame(self, bd=2, relief=GROOVE, takefocus=True)
        #middleFrame.pack()
        bottomFrame = Frame(self, bd=2, relief=GROOVE, takefocus=True)
        bottomFrame.pack()
        
        
        # 'Search By' section ------->
        searchByLabel = Label(topFrameLeft, text='SEARCH BY:', fg='navy',font='Times 16 bold')
        searchByLabel.grid(row=0, column=0, sticky=W+E, padx=20)
        searchByBoxes = ['Distribution', 'Department', 'Time/Days', 'Professor']
        searchByVars = []
        rowAvail = 1
        for box in searchByBoxes: 
            var = IntVar()
            button = Checkbutton(topFrameLeft,text=box,variable=var)
            button.grid(row=rowAvail, column=0, sticky=W+E, padx=20)
            searchByVars.append(var)
            rowAvail += 1
      
        # 'Show Only' section ------->
        showOnlyLabel = Label(topFrameRight, text='SHOW ONLY:', fg='navy', font='Times 16 bold')
        showOnlyLabel.grid(row=0, column=1, sticky=W+E, padx=20)
        rowAvail = 1
        showOnlyBoxes = ['If seats are available*','100 levels','200 levels','300 levels']
        showOnlyVars = []
        for box in showOnlyBoxes: 
            var = IntVar()
            button = Checkbutton(topFrameRight, text=box, variable=var)
            button.grid(row=rowAvail, column=1, sticky=W+E, padx=20)
            showOnlyVars.append(var)
            rowAvail += 1
        
        # Results ("Courses That Fit") section -------->
        coursesThatFitLabel = Label(bottomFrame, text="COURSES THAT FIT YOUR CRITERIA:", \
        font='Times 18 bold', fg='navy')
        coursesThatFitLabel.grid(sticky=E+W, padx=2)
        
        lb = Listbox(bottomFrame)       
        scrollbar = Scrollbar(lb, orient=VERTICAL)
        lb.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=lb.yview)
        scrollbar.grid(sticky=N+S)
        
        for i in range(1000): 
            lb.insert(END, str(i))
        
        lb.grid(row=1, rowspan=4, sticky=N+E+S+W)
        lb.columnconfigure(0, weight=1)
        scrollbar.grid(column=2, sticky=N+S)

        
        
        

app = CourseBrowserApp()
app.mainloop()