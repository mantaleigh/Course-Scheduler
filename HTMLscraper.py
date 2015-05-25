# Course Browser Scraper
# Samantha Voigt
# last edit: 3.29.15

from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
import urllib2
import ast

#note that the only thing this doesn't do is scrape departments and their acronyms
#associated with it. Since, as far as I can see, there is no way to scrape every
#subject acroynym associated with a department without doing it by hand.
# --- however, this does provide a function for writing a file with the information
# --- I garnered without scraping.

class BrowserScraper():
    def __init__(self): 
        self.soup = bs(urllib2.urlopen('http://courses.wellesley.edu/'))

    # ------------------------------------------------------------------------------
    #                                  GET INFO
    # ------------------------------------------------------------------------------

    # returns a list of the distributions, scraped from the drop down menu at the top of the page
    def getDistributions(self):
        print "running getDistributions()"
        distributions = []
        dbox = self.soup.find(id='distribution')
        for option in dbox.find_all('option'):
            distributions.append(option.get('value'))
        return distributions[1:] #the first elt in the list is "All"- not an actual distribution

    def getSubjects(self):
        print "running getSubjects()"
        subjects = []
        sbox = self.soup.find(id='subject')
        for option in sbox.find_all('option'):
            subjects.append(option.string)
        return subjects[1:] #the first elt in the list is "All"- not an actual subject

    def getDepartments(self):
        #eventually hopefully this will be able to do something of use...
        pass

    # ------ methods that take information from a row of cells and saves it into a given dictionary ------
    def saveCRN(self, rowCells, courseDict): 
        if rowCells[0].contents != []:
          courseDict['CRN'] = rowCells[0].string.encode('utf-8')

    def saveTitle(self, rowCells, courseDict): 
        if rowCells[2].contents != []:
           courseDict['Title'] = rowCells[2].string.encode('utf-8')

    def saveCurrentEnrollment(self, rowCells, courseDict): 
        if rowCells[3].contents != []:
            courseDict['Current Enrollment'] = rowCells[3].string.encode('utf-8')

    def saveDistributions(self, rowCells, courseDict): 
        if rowCells[10].contents != []: 
            if len(rowCells[10].contents) == 1: # if there is only one distribution
                courseDict['Distribution(s)'] = rowCells[10].string.encode('utf-8')
            else: 
                distList = []
                for dist in rowCells[10].text.split('\n'): 
                    distList.append(dist.encode('utf-8'))
                courseDict['Distribution(s)'] = distList

    def saveDaysAndTimes(self, rowCells, courseDict): 
        timeCell = rowCells[6]
        dayCell = rowCells[7]
        if (timeCell.contents != [] and dayCell.contents != []):
            dayTimeDict = {}
            timeList = []
            if len(timeCell.contents) > 1: # if there is more than one meeting time
                for time in timeCell.text.split('\n'): 
                    timeList.append(time.encode('utf-8'))
            else: 
                timeList.append(timeCell.string.encode('utf-8'))

            # match up the days to the times
            for i in range(1, len(dayCell.text.split('\n'))): # for each day section (usually only 1 or 2)
                allDaysForOneTime = dayCell.text.split('\n')[i] # get all the days for a certain time
                for day in ["Th", "M", "T", "W", "F"]: #Th must be first since it's two chars and might be confused with T
                    if day in allDaysForOneTime: 
                        dayTimeDict[day] = timeList[i-1] # save that day and corresponding time into the dict
                        allDaysForOneTime = allDaysForOneTime.replace(day, "") # update the allDays var to be all days we haven't covered
            courseDict['Day/Time'] = dayTimeDict

    def saveCourse(self, rowCells, courseDict): 
        if rowCells[1].find('a').contents != []:
            courseDict['Course'] = rowCells[1].find('a').string.encode('utf-8')

    def saveLocation(self, rowCells, courseDict): 
        if rowCells[5].find('a').contents != []:
            courseDict['Location(s)'] = rowCells[5].find('a').string.encode('utf-8')
   
    def saveInstructor(self, rowCells, courseDict): 
        if rowCells[8].find('a').contents != []:
            courseDict['Instructor'] = rowCells[8].find('a').string.encode('utf-8')

    def saveAddInstructor(self, rowCells, courseDict): 
        if rowCells[9].contents != []:
            courseDict['Additional Instructor(s)'] = rowCells[9].find('a').string.encode('utf-8')

    def saveSeatsAvail(self, rowCells, courseDict): 
        cell = rowCells[4]
        if cell.contents != []:
            courseDict['Seats Available'] = cell.next.next.next.string.strip('\n').encode('utf-8')

    def saveDescriptionAndPrereqs(self, rowCells, courseDict): 

        # TODO - Making a new soup for the new page takes a long time. How can I quicken this? 

        cell = rowCells[11]
        # information lies in the "more" link
        linkTag = str(cell.find('a'))
        linkPt2 = linkTag[linkTag.find('=')+2:linkTag.find(' onclick')-1]
        moreLink = ('http://courses.wellesley.edu/' + linkPt2).replace('&amp;','&')
        page2 = urllib2.urlopen(moreLink)
        #descriptionHTML = SoupStrainer(text="Description")
        soup2 = bs(page2) #, parseOnlyThese=descriptionHTML)
        print soup2

        # # get description
        descStr = ''
        try: 
            for string in soup2.find(text="Description").next.next.stripped_strings:
                descStr = descStr + ' ' + string.encode('utf-8')
        except AttributeError: # Except when the description is curiously blank...
            descStr = 'Not provided'
        courseDict['Description'] = descStr

        # # get prereqs
        try: 
            prereqStr = soup2.find(text="Prerequisite(s)").next.next.string.encode('utf-8')
        except AttributeError: # when there are no prereqs
            prereqStr = 'Not provided'
        courseDict['Prerequisite(s)'] = prereqStr


    def getAllCourses(self):
        '''Scrapes all course information from the Wellesley College Course Browser and
        returns a list of dictionaries corresponding to each course'''
        dictOfCourses = {} # will hold all the class dictionaries
        tableContent = self.soup.find('tbody')

        for row in tableContent.find_all('tr'): # each row corresponds to an individual course
            indivClassDict = {}
            cellNum = 0
            cells = row.find_all('th')

            self.saveCRN(cells, indivClassDict)
            self.saveCourse(cells, indivClassDict)
            self.saveTitle(cells, indivClassDict)
            self.saveCurrentEnrollment(cells, indivClassDict)
            self.saveSeatsAvail(cells, indivClassDict)
            self.saveLocation(cells, indivClassDict)
            self.saveDaysAndTimes(cells, indivClassDict)
            self.saveInstructor(cells, indivClassDict)
            self.saveAddInstructor(cells, indivClassDict)
            self.saveDistributions(cells, indivClassDict)
            self.saveDescriptionAndPrereqs(cells, indivClassDict)

            dictOfCourses[indivClassDict['CRN']] = indivClassDict #should go inside the first loop, but outside the second
            print "Saving course with CRN: " + indivClassDict['CRN'] #since it takes a fair amount of time to scrape all the data, this helps know that the program is running
        return dictOfCourses

    # ------------------------------------------------------------------------------
    #                                WRITE INFO
    # ------------------------------------------------------------------------------

    def writeCoursesFile(self, D):
        '''Given a dict of courses, writes a file with the dict'''
        filename = 'coursesFile.txt'
        courseFile = open(filename,'w')
        courseFile.write(str(D))
        courseFile.close()

    def writeDistFile(self, D):
        '''Given a dict of distributions, writes a file with the dict'''
        filename = 'distributionFile.txt'
        distFile = open(filename, 'w')
        distFile.write(str(D))
        distFile.close()

    def writeSubjFile(self, D):
        '''Given a dict of subjects, writes a file with the dict'''
        filename = 'subjectFile.txt'
        subjFile = open(filename, 'w')
        subjFile.write(str(D))
        subjFile.close()

    # agh anger how make dept scraping work
    def writeDeptFile(self):
        '''Writes a file with pre-found data (a dict)... no parameters (yet)'''
        departments = {'Africana Studies': 'AFR', 'American Studies': 'AMST', \
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
        filename = 'departmentFile.txt'
        deptFile = open(filename, 'w')
        deptFile.write(str(departments))
        deptFile.close()

    # ------------------------------------------------------------------------------
    #                                READ INFO
    # ------------------------------------------------------------------------------

    def readCoursesFile(self):
        '''Returns the basic python type (list of dicts) that corresponds to the string inside of the coursesFile'''
        s = open('coursesFile.txt', 'r').read()
        return ast.literal_eval(s)

    def readDistFile(self):
        '''Returns the basic python type (list) that corresponds to the string inside of the distibutions file'''
        s = open('distributionFile.txt', 'r').read()
        return ast.literal_eval(s)

    def readSubjFile(self):
        '''Returns the basic python type (list) that corresponds to the string inside of the subject file'''
        s = open('subjectFile.txt', 'r').read()
        return ast.literal_eval(s)

    def readDeptFile(self):
        '''Returns the basic python type (dict) that corresponds to the string inside of the deptartment file'''
        s = open('departmentFile.txt', 'r').read()
        return ast.literal_eval(s)

    # ------------------------------------------------------------------------------
    #                   UPDATE INFO -- calls above functions
    # ------------------------------------------------------------------------------

    def updateCourseInfo(self):
        '''When a new file of course info needs to get written (or re-written), this
        funtion will either update the file or write a new one. Will also return the list
        of courses for immediate use. '''
        listOfCourses = self.getAllCourses()
        self.writeCoursesFile(listOfCourses)
        return listOfCourses

    def updateAllExceptCourses(self):
        '''scrapes and writes/rewrites all info except courses. Returns None'''
        self.writeDistFile(self.getDistributions())
        self.writeSubjFile(self.getSubjects())
        self.writeDeptFile()

    def updateAll(self):
        '''Scrapes and writes/rewrites all info including courses, department list, distribution
        list, and subject list. Returns the list of courses.'''
        listOfCourses = self.getAllCourses()
        self.writeCoursesFile(listOfCourses)
        self.writeDistFile(self.getDistributions())
        self.writeSubjFile(self.getSubjects())
        self.writeDeptFile()
        return listOfCourses
