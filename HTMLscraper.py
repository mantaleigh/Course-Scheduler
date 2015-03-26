# Course Browser Scraper
# Samantha Voigt
# last edit: 3.19.15

from bs4 import BeautifulSoup as bs
import urllib2
import ast

#note that the only thing this doesn't do is scrape departments and their acronyms
#associated with it. Since, as far as I can see, there is no way to scrape every
#subject acroynym associated with a department without doing it by hand.
# --- however, this does provide a function for writing a file with the information
# --- I garnered without scraping. 

def getSoup():
    print "Creating soup..."
    page = urllib2.urlopen('http://courses.wellesley.edu/')
    return bs(page)

# ------------------------------------------------------------------------------
#                                  GET INFO 
# ------------------------------------------------------------------------------

# returns a list of the distributions, scraped from the drop down menu at the top of the page
def getDistributions():
    print "running getDistributions()"
    soup = getSoup()
    distributions = []
    dbox = soup.find(id='distribution')
    for option in dbox.find_all('option'):
        distributions.append(option.get('value'))
    return distributions[1:] #the first elt in the list is "All"- not an actual distribution

def getSubjects():
    print "running getSubjects()"
    soup = getSoup()
    subjects = []
    sbox = soup.find(id='subject')
    for option in sbox.find_all('option'):
        subjects.append(option.string)
    return subjects[1:] #the first elt in the list is "All"- not an actual subject

def getDepartments():
    #eventually hopefully this will be able to do something of use...
    pass

def getAllCourses(): 
    '''Scrapes all course information from the Wellesley College Course Browser and 
    returns a list of dictionaries corresponding to each course'''
    listOfCourses = []
    cellNames = ['CRN', 'Course', 'Title', 'Current Enrollment', 'Seats Available', \
    'Location(s)', 'Meeting Time(s)', 'Days(s)', 'Instructor', 'Additional Instructor(s)', \
    'Distribution(s)', 'Description', 'Prerequisites']
    soup = getSoup()
    tableContent = soup.find('tbody')
    
    for row in tableContent.find_all('tr'):
        indivClassDict = {}
        timeList = []
        cellNum = 0
        for cell in row.find_all('th'): #every loop is a new if statement that corresponds to cellNum
           
            if cell.contents != []:     
                if cellNum == 0 or cellNum == 2 or cellNum == 3 or (cellNum == 10 and len(cell.contents) == 1): 
                    # save CRN, Title, Current Enrollment, and distribution (if there is only one)
                    indivClassDict[cellNames[cellNum]] = cell.string.encode('utf-8')
                    
                elif (cellNum == 10 and len(cell.contents) > 1): #when there is more than 1 distribution
                    distList = []
                    for dist in cell.text.split('\n'):
                        distList.append(dist.encode('utf-8'))
                    indivClassDict[cellNames[cellNum]] = distList        
                
                elif cellNum == 6: # save times in a list
                    if len(cell.contents) > 1: 
                        for time in cell.text.split('\n'):
                            timeList.append(time.encode('utf-8'))
                    else: 
                        timeList.append(cell.string.encode('utf-8'))
                
                # Handles making a day/time dict
                elif cellNum == 7:
                    dayTimeDict = {}
                    for i in range(1, len(cell.text.split('\n'))):
                        dayName = cell.text.split('\n')[i].encode('utf-8')
                        dayTimeDict[dayName] = timeList[i-1]
                    indivClassDict['Day/Time'] = dayTimeDict
                        
                elif cellNum == 1 or cellNum == 5 or cellNum == 8 or cellNum == 9: 
                    # save Course, Location(s), and Instructor and Additional Instructor
                    if cell.find('a').contents != []:
                        indivClassDict[cellNames[cellNum]] = cell.find('a').string.encode('utf-8')
                
                elif cellNum == 4: 
                    # save Seats Available
                    indivClassDict[cellNames[cellNum]] = cell.next.next.next.string.strip('\n').encode('utf-8')
                
                # save description and the prereqs from the 'more' link
                elif cellNum == 11: 
                    linkTag = str(cell.find('a'))
                    linkPt2 = linkTag[linkTag.find('=')+2:linkTag.find(' onclick')-1]
                    moreLink = ('http://courses.wellesley.edu/' + linkPt2).replace('&amp;','&')
                    page2 = urllib2.urlopen(moreLink)
                    soup2 = bs(page2)     
                    
                    # get description:
                    descStr = ''
                    for string in soup2.find(text="Description").next.next.stripped_strings:
                        descStr = descStr + ' ' + string.encode('utf-8')
                    indivClassDict[cellNames[cellNum]] = descStr
                    
                    # get prereqs:
                    try:
                        prereqStr = soup2.find(text="Prerequisite(s)").next.next.string.encode('utf-8')
                    except AttributeError: 
                        prereqStr = 'Not provided'
                    indivClassDict['Prerequisite(s)'] = prereqStr
            
            #needs to be a separate if statement, not an elif 
            if cellNum <= len(cellNames):
                cellNum += 1
    
        listOfCourses.append(indivClassDict) #should go inside the first loop, but outside the second
        print indivClassDict['CRN']
    return listOfCourses

# ------------------------------------------------------------------------------
#                                WRITE INFO 
# ------------------------------------------------------------------------------

def writeCoursesFile(L):
    '''Given a list of courses, writes a file with the list'''
    filename = 'coursesFile.txt'
    courseFile = open(filename,'w')
    courseFile.write(str(L))
    courseFile.close()

def writeDistFile(L):
    '''Given a list of distributions, writes a file with the list'''
    filename = 'distributionFile.txt'
    distFile = open(filename, 'w')
    distFile.write(str(L))
    distFile.close()

def writeSubjFile(L):
    '''Given a list of subjects, writes a file with the list'''
    filename = 'subjectFile.txt'
    subjFile = open(filename, 'w')
    subjFile.write(str(L))
    subjFile.close()

# agh anger how make dept scraping work
def writeDeptFile():
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
    
def readCoursesFile(): 
    '''Returns the basic python type (list of dicts) that corresponds to the string inside of the coursesFile'''
    s = open('coursesFile.txt', 'r').read()
    return ast.literal_eval(s)

def readDistFile(): 
    '''Returns the basic python type (list) that corresponds to the string inside of the distibutions file'''
    s = open('distributionFile.txt', 'r').read()
    return ast.literal_eval(s)

def readSubjFile(): 
    '''Returns the basic python type (list) that corresponds to the string inside of the subject file'''
    s = open('subjectFile.txt', 'r').read()
    return ast.literal_eval(s)

def readDeptFile(): 
    '''Returns the basic python type (dict) that corresponds to the string inside of the deptartment file'''
    s = open('departmentFile.txt', 'r').read()
    return ast.literal_eval(s)

# ------------------------------------------------------------------------------
#                   UPDATE INFO -- calls above functions
# ------------------------------------------------------------------------------

def updateCourseInfo(): 
    '''When a new file of course info needs to get written (or re-written), this 
    funtion will either update the file or write a new one. Will also return the list 
    of courses for immediate use. '''
    listOfCourses = getAllCourses()
    writeCoursesFile(listOfCourses)
    return listOfCourses

def updateAllExceptCourses():
    '''scrapes and writes/rewrites all info except courses. Returns None'''
    writeDistFile(getDistributions())
    writeSubjFile(getSubjects())
    writeDeptFile()

def updateAll():
    '''Scrapes and writes/rewrites all info including courses, department list, distribution
    list, and subject list. Returns the list of courses.'''
    listOfCourses = getAllCourses()
    writeCoursesFile(listOfCourses)
    writeDistFile(getDistributions())
    writeSubjFile(getSubjects())
    writeDeptFile()
    return listOfCourses

