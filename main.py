import cv2 as cv
import numpy as np
import csv
import time as tm
import random
from datetime import date
import datetime
import calendar

start_time = tm.time()
video = cv.VideoCapture(0)
ret, frame1 = video.read()
ret, frame2 = video.read()
person_counter = 0

row = ["Time of Day", "Monday", "Tuesday", "Wednesday",
       "Thursday", "Friday", "Saturday", "Sunday"]
with open("data/week1.csv", 'a', newline='') as data:
    writer = csv.writer(data)
    writer.writerow(row)

# These two functions provide the day of the week


def get_day():
    current_date = date.today()
    year = current_date.year
    month = current_date.month
    day = current_date.day
    dayOfWeek = dayGetter(day, month, year)
    return dayOfWeek


global dayNum


def dayGetter(day, month, year):
    days = ["Mon", "Tues", "Wed", "Thur", "Fri", "Sat", "Sun"]
    # dayIndex is an object of datetime
    dayIndex = datetime.date(year, month, day)
    global dayNum
    dayNum = dayIndex.weekday()
    # .weekday is a method of this object (returns a number)
    day_of_week = days[dayIndex.weekday()]
    return (day_of_week)


day = get_day()

windowWidth = frame1.shape[1]
windowHeight = frame1.shape[0]
print(windowWidth)
print(windowHeight)


previous_x = windowWidth/2


def largestContour(contours):
    largest = 0
    for contour in contours:
        if cv.contourArea(contour) > largest:
            largest = cv.contourArea(contour)
    return largest


def findContour(contours, area):
    stuff = (1, 2, 3, 4)
    for contour in contours:
        if cv.contourArea(contour) == area:
            print(cv.contourArea(contour))
            stuff = (x, y, w, h) = cv.boundingRect(contour)
    return stuff


going_left = False
going_right = False
counter = 0
contourCount = 0
while video.isOpened():
    cv.resize(frame1, (640, 480))
   # cv.resize(frame2, (640, 480))
    going_left = False
    going_right = False
    day = get_day()
    counter += 1
    difference = cv.absdiff(frame1, frame2)
    cv.imshow("divy", difference)
    greyScale = cv.cvtColor(difference, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(greyScale, (21, 21), 0)
    dilated = cv.dilate(blurred, None, iterations=1)
    fram3 = cv.Canny(blurred, 125, 175)
    _, thresh = cv.threshold(blurred, 20, 255, cv.THRESH_BINARY)
    dilated = cv.dilate(thresh, None, iterations=3)
    contours, _ = cv.findContours(
        dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #contourS = [0]
    # contour = max(contours, key = cv.contourArea)
    cv.putText(frame1, f"Num: {person_counter}", (10, 50),
               cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv.LINE_AA)
    for contour in contours:

        (x, y, w, h) = cv.boundingRect(contour)
        if cv.contourArea(contour) > 10000:
            cv.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 3)
            contourCount += 1
            if contourCount == 1:
                previous_x = x
            # print(previous_x)
            if previous_x < x:
                print("Right")
                going_right = True

            elif previous_x > x:
                print("Left")
                going_left = True

            if going_left == True:
                print(x + w)
                if (x > 150 and x < 160) or (x + w > 150 and x + w < 160):
                    print("GOING LEFT")
                    person_counter += 1
                    going_left = False

            if going_right == True:
                if x + w > windowWidth - 165 and x + w < windowWidth - 145:
                    print("GOING RIGHT")
                    if person_counter <= 0:
                        person_counter = 0
                    else:
                        person_counter -= 1
                    going_right = False

            if counter % 3 == 0:
                previous_x = x

    # print(contourS)
    resize = cv.resize(frame1, (640, 480))
    cv.imshow("frame1", resize)
    """
    #contour = max(contours)
    con = largestContour(contours)
    print(con)
    print("HI")
    cons = findContour(contours, con)
    cv.rectangle(frame1, (cons[0], cons[1]),
                 (cons[0]+cons[2], cons[1]+cons[3]), (0, 255, 0), 3)
    if cons[0] > 310 and cons[0] < 320:
        if (counter % 2) == 1:
            previous_x = cons[0]
    if (counter % 2) == 0:
        if cons[0] > 320:
            going_right = True
        if cons[0] >= 100 and cons[0] <= 105:
            person_counter += 1
    
    #(x, y, w, h) = cv.boundingRect(cons)

    for contour in contours:
       
        #going_right = 0
        #going_left = 0
        #if cv.contourArea(contour) < 20000:
        #    continue
        (x, y, w, h) = cv.boundingRect(contour)
        #print(f"Previous x is: {previous_x}, x is: {x}")
        #if cv.contourArea(contour) < 900:
        #    continue
        #print(cv.contourArea(contour))

            # ADD FPS %3 == 0 (EVERY THIRD FRAME), DO PREVIOUS_X < X THEN INCREASE COUNTER ETC

        if (w > 125 and h > 175) and (w < 700 and h < 800):
            cv.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 3)
        # CORRECT DIMENSIONS
        # if x < 200 and x > 190:
        #    person_counter += 1
        # if (x > 280 and x < 290):
        if (previous_x < x):
            person_counter += 1
 #   if (x < 280):
      #  if x < 270:
          #  going_left = 1

        # if (x < 590 and x > 580):
        if previous_x > x:
            if person_counter == 0:
                person_counter = 0
            elif person_counter > 0:
                person_counter -= 1

        previous_x = x
       # if (x > 100 and x < 110 and going_left == 1):
        # person_counter += 1
    """
    #cv.imshow("TEST", frame1)
    # cv.imshow("TEST2", fram3)
    frame1 = frame2
    ret, frame2 = video.read()

    currentTime = "0:0"
    # if int(fps)%70==0:
    if int(tm.time()-start_time) == 10:
        start_time = tm.time()
        print(f"HI")
        # if(day == "Sun"):
        time = datetime.datetime.now()
        if time.minute < 10:
            currentTime = "{}:0{}".format(time.hour, time.minute)
        else:
            currentTime = "{}:{}".format(time.hour, time.minute)

            # Figure out how to replace zeros with blanks
        if int(tm.time() - start_time) >= 604800:
            file = open("data/week2.csv")
            reader = csv.reader(file)
            lines = len(list(reader))
            if lines == 0:
                row = ["Time of Day", "Monday", "Tuesday", "Wednesday",
                       "Thursday", "Friday", "Saturday", "Sunday"]
                writer = csv.writer(file)
                writer.writerow(row)

            row = [currentTime, 0, 0, 0, 0, 0, 0, 0]
            row[dayNum + 1] = person_counter
            with open("data/week2.csv", 'a', newline='') as data:
                writer = csv.writer(data)
                writer.writerow(row)
        else:
            row = [currentTime, 0, 0, 0, 0, 0, 0, 0]
            row[dayNum + 1] = person_counter
            with open("data/week1.csv", 'a', newline='') as data:
                writer = csv.writer(data)
                writer.writerow(row)

    if cv.waitKey(40) & 0xFF == ord('q'):
        break

# Counts number of rows in the csv
row_count = sum(1 for row in csv.reader(open('data/test.csv')))
print(row_count)
print(f"The time is {tm.time()}")
cv.destroyAllWindows()
video.release()
print(f"The number of people are {person_counter}")
