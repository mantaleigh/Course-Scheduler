# Course Browser Scraper
# Samantha Voigt

from bs4 import BeautifulSoup as bs
import urllib2
import ast
import os

def getAllCourses(): 
    '''Scrapes all course information from the Wellesley College Course Browser and 
    returns a list of dictionaries corresponding to each course'''
    listOfCourses = []
    page = urllib2.urlopen('http://courses.wellesley.edu/')
    soup = bs(page)
    tableContent = soup.find('tbody')
    cellNames = ['CRN', 'Course', 'Title', 'Current Enrollment', 'Seats Available', \
    'Location(s)', 'Meeting Time(s)', 'Days(s)', 'Instructor', 'Additional Instructor(s)', \
    'Distribution(s)', 'Description', 'Prerequisites']
    for row in tableContent.find_all('tr'):
        indivClassDict = {}
        cellNum = 0
        for cell in row.find_all('th'): #every loop is a new if statement that corresponds to cellNum
            moreLink = ''
            if cell.contents != []:
                if cellNum == 0 or cellNum == 2 or cellNum == 3 or cellNum == 6 or cellNum == 10: 
                    #strip for CRN, Title, Current Enrollment, meeting times, and distribution
                    indivClassDict[cellNames[cellNum]] = str(cell.contents[0].encode("utf-8"))
                    
                    if cellNum == 10 and len(cell.contents) > 1: #when there are more than 1 distribution
                        distList = []
                        distList.append(str(cell.contents[0]).encode("utf-8"))
                        otherDist = str(cell.contents[1].encode("utf-8"))
                        #This is ugly -- fix 
                        for i in range(1,len(cell.find_all('hr'))+1): #Need to update w/more modular ways
                            if i == 1: 
                                distList.append(otherDist[otherDist.find('>')+1:otherDist.find('<',1)].strip('\n').strip())
                            if i == 2: 
                                otherDist = otherDist[otherDist.find('<',1):]
                                distList.append(otherDist[otherDist.find('>')+1:otherDist.find('<',1)].strip('\n').strip())
                        indivClassDict[cellNames[cellNum]] = distList                        
                        
                elif cellNum == 1 or cellNum == 5 or cellNum == 8 or cellNum == 9: 
                    #strip for Course, Location(s), and Instructor and Additional Instructor
                    cellStr = str(cell.contents[0].encode("utf-8"))
                    stripIndex1 = cellStr.find('">')
                    stripIndex2 = cellStr.find('</')
                    indivClassDict[cellNames[cellNum]] = cellStr[(stripIndex1+2):stripIndex2]
                elif cellNum == 4 or cellNum == 7: #strip for Seats Available and Day(s)
                    indivClassDict[cellNames[cellNum]] = str(cell.contents[1].encode("utf-8")).strip()
            #needs to be a separate if statement, not an elif 
            if cellNum <= len(cellNames):
                cellNum += 1
    
        listOfCourses.append(indivClassDict) #should go inside the first loop, but outside the second
    return listOfCourses
    
# semester should be in the format of 'FA14', 'SP15', etc...
        
def writeListFile(L, semester):
    '''Given a list of courses and the semester, writes a file with the list as 
    a string named according to the semester name given'''
    filename = semester + 'coursesFile.txt'
    courseFile = open(filename,'w')
    courseFile.write(str(L))
    courseFile.close()
    
def readCourseFile(filename): 
    '''Takes in a local filename and reads the string inside of the file into a basic 
    Python type (in this case, a list of dictionaries), and returns it.'''
    s = open(filename, 'r').read()
    return ast.literal_eval(s)
    
def updateCourseInfo(semester): 
    '''When a new file of course info needs to get written (or re-written), this 
    funtion will either update the file or write a new one. Will also return the list 
    of courses for immediate use.'''
    listOfCourses = getAllCourses()
    writeListFile(listOfCourses, semester)
    return listOfCourses

# Should only ever need to call 2 functions (readCourseFile and updateCourseInfo) when using this program
#   use readCourseFile when the course info doesn't need to be updated
#   use updateCourseInfo when the course info does need to be updated
#       both will return a usable list of courses