import csv
import random
import datetime
import time

class BookingApp:
    def __init__(self):
        self.__manicuristdic = self.getManicurist()
        self.__schedulelist = self.getSchedule()
        self.__scheduledic = {}
        for i in self.__schedulelist:
            if i.scheduleholiday.holidayname not in self.__scheduledic:
                self.__scheduledic[i.scheduleholiday.holidayname]=[]
            self.__scheduledic[i.scheduleholiday.holidayname].append(i)
        self.__waitinglist = []
        self.__timedic = self.getTime()

    def getManicurist(self):
        manicurist = {}
        with open('Manicurist.csv', 'r')as file:
            reader = csv.reader(file)
            for row in reader:
                manicuristt = Manicurists (row[0])
                manicurist[row[0]]= manicuristt
        return manicurist

    def showManicurist(self):
        print("Manicurist list:")
        Format1 = "{:<3s}{:<8s}"
        i=1
        for k,v in self.__manicuristdic.items():
            print(Format1.format(str(i),v.name))
            i+=1

    def getSchedule(self):
        schedule = []
        with open('Schedule.csv','r')as file:
            reader = csv.reader(file)
            for row in reader:
                schedulee = Schedule(row[0],row[1],row[2])
                schedule.append(schedulee)
        return schedule

    def writeToSchedule(self):
        with open('Schedule.csv','w',newline='') as file:
            writer = csv.writer(file)
            for i in self.__schedulelist:
                writer.writerow([i.scheduleholiday.holidayname,
                                i.manicurist.name,
                                i.customer.cusname])

    def showMenu(self):
        print("MAIN MENU")
        print("B - Schedule a time")
        print("C - Cancel a booking.")
        print("S - Show booking status.")
        print("Q - Quit.")

    def Booking(self,customername,targetime):
        Format1 = "{:<20s} {:<10s}"
        if targetime in self.__scheduledic:
            if len(self.__scheduledic[targetime]) >= len(self.__manicuristdic):
                print("That time is full booking, I will put you on waiting list.")
                print()
                self.__waitinglist.append([targetime,customername])
                print("Waiting list : ")
                print(Format1.format("Time","Cusotmer"))
                for i in self.__waitinglist:
                    print(Format1.format(i[0],i[1]))
                print()
            else:
                notAvalible = []
                for i in self.__scheduledic[targetime]:
                    notAvalible.append(i.manicurist.name)
                for i in self.__manicuristdic:
                    if self.__manicuristdic[i].name not in notAvalible:
                        manicurist_name = self.__manicuristdic[i].name
                self.__schedulelist.append(Schedule(targetime,manicurist_name,customername))
                self.__scheduledic[targetime].append(self.__schedulelist[-1])
                self.writeToSchedule()
                print(customername,"your booking on",targetime,"is completed",manicurist_name,'will come.')
                print()
        else:
            manicuristlist = []
            for i in self.__manicuristdic:
                manicuristlist.append(i)
            manicurist_name = random.choice(manicuristlist)
            self.__schedulelist.append(Schedule(targetime,manicurist_name,customername))
            self.__scheduledic[targetime] = []
            self.__scheduledic[targetime].append(self.__schedulelist[-1])
            self.writeToSchedule()
            print(customername, "your booking on", targetime, "is completed", manicurist_name, 'will come.')
            print()

    def Cancel(self,customername):
        Format1 = "{:<20s} {:<10s}"
        cusbooking = []
        waitingbooking = []
        for i in self.__schedulelist:
            if i.customer.cusname == customername:
                cusbooking.append(i)
        for i in self.__waitinglist:
            if i.customer.cusname == customername:
                waitingbooking.append(i)

        if len(cusbooking) <= 0 and len(waitingbooking) <= 0:
            print("Can't find your booking.")
        else:
            Format3 = "{:<20s} {:<10s} {:<10s}"
            print("Your booking information is below:")
            for i in range(len(cusbooking)):
                print(i+1,Format3.format(cusbooking[i].scheduleholiday.holidayname,"Manicurist :",cusbooking[i].manicurist.name))
            while True:
                try:
                    cancel = int(input("Which one you want to CANCEL ? "))
                    break
                except:
                    print("Please enter number of your booking.")

            targetday = cusbooking[cancel-1].scheduleholiday.holidayname

            if len(cusbooking) > 0:
                for i in self.__scheduledic[targetday]:
                    if i.customer.cusname == customername:
                        self.__scheduledic[targetday].remove(i)
                        self.__schedulelist.remove(i)
                        print(customername, "your booking on", targetday, "is canceled")
                        print()
                        for j in self.__waitinglist:
                            if j[0] == targetday:
                                print("Waiting list alternate.")
                                self.Booking(j[1],j[0])
                                break
                        break
                    else:
                        for i in waitingbooking:
                            for j in self.__waitinglist:
                                if i == j:
                                    self.__waitinglist.remove(i)
                                    print(customername, "you are on longer on",targetday,"waiting list")
                                    break

    def getTime(self):
        time = {}
        with open('Time.csv', 'r')as file:
            reader = csv.reader(file)
            i = 1
            for row in reader:
                ttime = Time(int(row[0]))
                time[i] = ttime
                i += 1
        return time

    def showTime(self):
        print("Which time ?")
        for k,v in self.__timedic.items():
            print(k, self.__timedic[k].hour, ": 00")

    def CheckTime(self,enter):
        while True:
            if enter in self.__timedic:
                enter = self.__timedic[enter].hour
                return enter
            else:
                for i in self.__timedic:
                    if self.__timedic[i].hour == enter:
                        return enter

            print("Enter wrong time, enter O to Main Menu.")
            enter = input("Or enter which time again! : ")
            if enter == "o" or enter == "O":
                return False

    def showStatus(self,target):
        if target in self.__scheduledic:
            self.getHolidaySchedulelist(target)
        else:
            for i in self.__schedulelist:
                if target == i.manicurist.name:
                    self.getManicuristSchedulelist(target)
                    bookresult = True
                    break
                else:
                    bookresult = False
            if bookresult == False:
                print("No booking record.")

    def getHolidaySchedulelist(self,holiday):
        holidaylist = self.__scheduledic[holiday]
        sortlist = []
        Format3 = "{:<10s} {:<10s}"
        n = len(holidaylist)
        if n == 0:
            print("No book record on",holiday)
        else:
            while n > 0:
                for i in holidaylist:
                    max = i.customer.cusname
                    break
                for i in holidaylist:
                    if i.customer.cusname > max:
                        max = i.customer.cusname
                for i in holidaylist:
                    if i.customer.cusname==max:
                        sortlist.append(i)
                        holidaylist.remove(i)
                        n -= 1
            print("Schecdule on",holiday,":")
            print(Format3.format("Customer","Manicurist"))
            for i in sortlist:
                print(Format3.format(i.customer.cusname,i.manicurist.name))

    def getManicuristSchedulelist(self,manicurist):
        manicuristschedulelist = []
        for i in self.__schedulelist:
            if i.manicurist.name == manicurist:
                manicuristschedulelist.append(i)
        sortlist = []
        Format3 = "{:<20s} {:<10s}"
        n = len(manicuristschedulelist)
        if n == 0:
            print("No book record with",manicurist)
        else:
            while n > 0:
                for i in manicuristschedulelist:
                    max = i.scheduleholiday.holidayname
                    break
                for i in manicuristschedulelist:
                    if i.scheduleholiday.holidayname > max:
                        max = i.scheduleholiday.holidayname
                for i in manicuristschedulelist:
                    if i.scheduleholiday.holidayname == max:
                        sortlist.append(i)
                        manicuristschedulelist.remove(i)
                        n -= 1
            print("Schedule of manicurist",manicurist,":")
            print(Format3.format("Holiday","Customer"))
            for i in sortlist:
                print(Format3.format(i.scheduleholiday.holidayname,i.customer.cusname))

    def CheckenterHoliday(self,enter):
        while True:
            if enter in self.__holidaydic:
                enter = self.__holidaydic[enter].holidayname
            for i in self.__holidaydic:
                if self.__holidaydic[i].holidayname == enter:
                    return enter
            print("Enter wrong holiday, enter O to Main Menu.")
            enter = input("Or enter holiday again! : ")
            if enter == "o" or enter == "O":
                return False

    def CheckNoDouble(self,holiday,customer):
        if holiday not in self.__scheduledic:
            return True
        for i in self.__scheduledic[holiday]:
            if i.customer.cusname == customer:
                print(customer, "already booked in the same day.")
                print()
                return False
            else:
                for j in self.__waitinglist:
                    if j[0] == holiday and j[1] == customer:
                        print("That day is full booked,",customer, "already on the waiting list.")
                        print()
                        return False
        return True

    def Bookingbydate(self,cusname):
        d = input("Please enter date (yyyy-mm-dd) need to enter '-': ")
        while True:
            try:
                date = time.strptime(d,"%Y-%m-%d")
                break
            except:
                print("Wrong enter")
                d = input("Please enter date (yyyy-mm-dd) need to enter '-': ")
        y, m, d = date[0:3]
        self.showTime()
        while True:
            try:
                t = int(input("Please enter a time in list (No.) : "))
                break
            except:
                print("wrong number!")
                t = int(input("Please enter a time in list (No.) : "))
        t = self.CheckTime(t)
        self.Booking(cusname,str(datetime.date(y,m,d,))+" "+str(t)+":00")

class Manicurists:
    def __init__(self,name):
        self.__name = name

    @property
    def name(self):
        return self.__name

class Holiday:
    def __init__(self,holidayname):
        self.__holidayname = holidayname

    @property
    def holidayname(self):
        return self.__holidayname

class Customer:
    def __init__(self,cusname):
        self.__cusname = cusname

    @property
    def cusname(self):
        return self.__cusname

class Schedule:
    def __init__(self,scheduleholiday,manicurist,customer):
        self.__manicurist = Manicurists(manicurist)
        self.__scheduleholiday = Holiday(scheduleholiday)
        self.__customer = Customer(customer)

    @property
    def manicurist(self):
        return self.__manicurist

    @property
    def scheduleholiday(self):
        return self.__scheduleholiday

    @property
    def customer(self):
        return self.__customer

class Time:
    def __init__(self,hour):
        self.hour = hour

def main():
    app = BookingApp()
    app.showManicurist()
    print()
    while True:
        app.showMenu()
        print()
        command = input("Command: ")
        command = command.lower()
        if command == "b":
            while True:
                customername = input("Please enter your name to book or enter O to Main Menu. ")
                if customername == "O" or customername == 'o' or customername == "0":
                    break
                app.Bookingbydate(customername)
        elif command == "c":
            while True:
                customername = input("Please enter your name to cancel or enter O to Main Menu. ")
                if customername == "O" or customername == 'o' or customername == '0':
                    break
                app.Cancel(customername)
        elif command == "s":
            target = input("Please enter a manicurist name or a holiday : ")
            app.showStatus(target)
            print()

        elif command == "q":
            print('Bye!')
            break
        else:
            print("Not a valid command. Please try again.\n")

if __name__ == "__main__":
    main()