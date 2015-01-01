# Course Browser Scraper

from bs4 import BeautifulSoup as bs
import urllib2
import ast

def getAllCourses(): 
    '''Scrapes all course information from the Wellesley College Course Browser and 
    returns a list of dictionaries corresponding to each course'''
    listOfCourses = []
    page = urllib2.urlopen('http://courses.wellesley.edu/')
    soup = bs(page)
    tableContent = soup.find('tbody')
    cellNames = ['CRN', 'Course', 'Title', 'Current Enrollment', 'Seats Available', \
    'Location(s)', 'Meeting Time(s)', 'Days(s)', 'Instructor', 'Additional Instructor(s)', \
    'Distribution(s)']
    for row in tableContent.find_all('tr'):
        indivClassDict = {}
        cellNum = 0
        for cell in row.find_all('th'): #every loop is a new if statement that corresponds to cellNum
            if cell.contents != []:
                if cellNum == 0 or cellNum == 2 or cellNum == 3 or cellNum == 6 or cellNum == 10: 
                    #strip for CRN, Title, Current Enrollment, meeting times, and distribution
                    indivClassDict[cellNames[cellNum]] = str(cell.contents[0].encode("utf-8"))
                elif cellNum == 1 or cellNum == 5 or cellNum == 8 or cellNum == 9: 
                    #strip for Course, Location(s), and Instructor and Additional Instructor
                    cellStr = str(cell.contents[0].encode("utf-8"))
                    stripIndex1 = cellStr.rfind('">')
                    stripIndex2 = cellStr.rfind('</')
                    indivClassDict[cellNames[cellNum]] = cellStr[(stripIndex1+2):stripIndex2]
                elif cellNum == 4 or cellNum == 7: #strip for Seats Available and Day(s)
                    indivClassDict[cellNames[cellNum]] = str(cell.contents[1].encode("utf-8")).strip()
        
            #needs to be a separate if statement, not an elif 
            if cellNum <= len(cellNames):
                cellNum += 1
    
        listOfCourses.append(indivClassDict) #should go inside the first loop, but outside the second
    return listOfCourses
        
def writeListOfCoursesFile(L):
    '''Writes a file with '''
    courseFile = open('coursesFile.txt','w')
    courseFile.write(str(L))
    courseFile.close()
    
def readListDictFile(filename): 
    s = open(filename, 'r').read()
    return ast.literal_eval(s)
    
   

writeListOfCoursesFile(getAllCourses())

#listOfCourses = readListDictFile('coursesFile.txt')
#print listOfCourses[0]