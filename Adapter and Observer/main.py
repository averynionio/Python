from functools import reduce
from abc import ABC,abstractmethod
class Observer(ABC):
    @abstractmethod
    def update(self):
        pass

class Student(Observer):
    def __init__(self,studentName):
        self.__studentName = studentName
        self.__HWScore = []
        self.__EMScore = []
        self.__enrollCourse = Course(None,None,None)

    @property
    def studentName(self):
        return self.__studentName

    @property
    def HWScore(self):
        return self.__HWScore

    @property
    def EMScore(self):
        return self.__EMScore

    @property
    def enrollCourse(self):
        return self.__enrollCourse

    def addHWScore(self,score):
        self.__HWScore.append(score)
        self.update(self.__HWScore,self.__EMScore)

    def addExamScore(self,score):
        self.__EMScore.append(score)
        self.update(self.__HWScore, self.__EMScore)

    def addEnroll(self,course):
        self.__enrollCourse = Course(course.courseTitle,course.courseNo,course.office)

    def update(self, HW,EM):
        final = Fianl2.getFinal(self,HW,EM)
        self.__enrollCourse.update(final,self)

    def getFianl(self,math):
        final = math.getFinal(self, self.__HWScore, self.EMScore)
        print(self.studentName,"Final Score:","{:.2f}".format(final))

    def __str__(self):
        return self.__studentName

class Fianl1:
    def getFinal(self,HW,EX):
        final = (sum(HW)/len(HW)*0.4)+(sum(EX)/len(EX)*0.6)
        return final

class Fianl2:
    def getFinal(self,HW,EX):
        HWscore = sorted(HW, reverse=True)
        try:
            HWsum = reduce(lambda s1, s2: s1 + s2, HWscore[0:5])
        except:
            HWsum = sum(HW)
        EXsum = sum(EX)
        try:
            final = (HWsum / min(len(HW), 5) * 0.4) + (EXsum / len(EX) * 0.6)
        except:
            if HWsum == 0:
                final = (EXsum / len(EX) * 0.6)
            else:
                final = (HWsum / min(len(HW), 5) * 0.4)
        return final

class Course(Observer):
    def __init__(self,courseTitle,courseNo,office):
        self.__courseTitle = courseTitle
        self.__courseNo = courseNo
        self.__office = office
        self.__studentList =[]
        self.__studentScore = {}

    @property
    def studentList(self):
        return self.__studentList

    @property
    def courseTitle(self):
        return self.__courseTitle

    @property
    def courseNo(self):
        return self.__courseNo

    @property
    def office(self):
        return self.__office

    def addStudent(self,student):
        self.__studentList.append(student)
        student.addEnroll(self)

    def update(self,final,student):
        self.__studentScore[student.studentName] = final
        self.__office.update(student,final)

    def getStudentAverages(self):
        for i in self.__studentList:
            self.__studentScore[i.studentName] = Fianl1().getFinal(i.HWScore,i.EMScore)
        return self.__studentScore

class RecordOffice(Observer):
    def __init__(self):
        self.__gradeList = []
        self.__courseScoreDic = {}

    def addCourse(self,course):
        dic = course.getStudentAverages()
        for name, score in dic.items():
            dic[name] = self.transScore(score)

        self.__courseScoreDic[course.courseTitle] = dic
        self.__gradeList.append(self.__courseScoreDic)

    def transScore(self,score):
        grade = ""
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"
        return grade

    def update(self,student,final):
        name = student.studentName
        for i in self.__gradeList:
            for course, grade in i.items():
                if name in grade:
                    newScore = self.transScore(final)
                    if grade[name] != newScore:
                        grade[name] = newScore
                        print(name,"Your score has been changed!")
                        print("New grade record:")
                        self.display(course)
                        break

    def display(self,course):
        for courseName,scoreList in self.__courseScoreDic.items():

            if course == courseName:
                print("Course",course,'Score List:')
                for student, score in scoreList.items():
                    print(student,'Final Grade = ',score)

class main():
    office = RecordOffice()
    amy = Student("Amy")
    ivy = Student("Ivy")
    jay = Student("Jay")
    kay = Student("Kay")
    CS487 = Course("OOT", 487,office)
    CS455 = Course("Algorithm", 455,office)

    CS487.addStudent(amy)
    CS487.addStudent(ivy)
    CS455.addStudent(jay)
    CS455.addStudent(kay)

    amy.addHWScore(90)
    amy.addHWScore(95)
    amy.addHWScore(98)
    amy.addHWScore(95)
    amy.addHWScore(95)
    amy.addHWScore(60)
    amy.addHWScore(50)
    amy.addExamScore(90)
    amy.addExamScore(90)
    amy.addExamScore(92)

    print("Student Amy Final Score, using Math1 & Math 2")
    amy.getFianl(Fianl1)
    amy.getFianl(Fianl2)
    amy.getFianl(Fianl1)

    ivy.addHWScore(80)
    ivy.addHWScore(88)
    ivy.addHWScore(90)
    ivy.addExamScore(86)
    ivy.addExamScore(89)

    jay.addHWScore(76)
    jay.addExamScore(79)

    kay.addHWScore(100)
    kay.addExamScore(95)

    print()
    office.addCourse(CS487)
    office.addCourse(CS455)
    office.display(CS487.courseTitle)
    print()
    office.display(CS455.courseTitle)
    print()
    print("Add Kay's Score and auto-change the Grade")
    kay.addExamScore(40)


main()

