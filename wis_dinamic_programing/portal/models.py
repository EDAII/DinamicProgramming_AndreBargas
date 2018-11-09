from django.db import models
import random
from datetime import date, datetime, time, timedelta
import collections
import bisect

class Activity(object):
    def __init__(self):
        # create a stating time for the activity
        self.value = random.randint(0, 200)
        # save a value to the activity


        # save time to a class atribute
        # combine the time with a date, assuming that is today
        # self.beginTime = datetime.combine(date.today(), begin)
        self.beginTime = datetime(datetime.now().year, datetime.now().month, datetime.now().day, random.randint(0, 23), random.randint(0, 59))

        # create a duration time for the activity
        delta = timedelta(minutes= random.randint(0, 59), hours = random.randint(0, 23))
        #set to a class atribute
        self.deltaTime = delta

        #get the finish time of the activity by doing starting plus the duration
        self.finishTime = self.beginTime + delta


def quickSortForActivity(times_list):
   quickSortHelper(times_list,0,len(times_list)-1)

def quickSortHelper(times_list,first,last):
   if first<last:

       splitpoint = partition(times_list,first,last)

       quickSortHelper(times_list,first,splitpoint-1)
       quickSortHelper(times_list,splitpoint+1,last)


def partition(alist,first,last):
   pivotvalue = alist[first].finishTime

   leftmark = first+1
   rightmark = last

   done = False
   while not done:

       while leftmark <= rightmark and alist[leftmark].finishTime <= pivotvalue:
           leftmark = leftmark + 1

       while alist[rightmark].finishTime >= pivotvalue and rightmark >= leftmark:
           rightmark = rightmark -1

       if rightmark < leftmark:
           done = True
       else:
           temp = alist[leftmark]
           alist[leftmark] = alist[rightmark]
           alist[rightmark] = temp

   temp = alist[first]
   alist[first] = alist[rightmark]
   alist[rightmark] = temp
   return rightmark

def printActivityList(list):
    num = 1
    n_day = list[0].beginTime.day
    for element in list:
        if(n_day != element.beginTime.day):
            print
            print
            print("Dia %s Mes %s Ano %s" % (element.beginTime.day, element.beginTime.month, element.beginTime.year))
            n_day = element.beginTime.day
            num=1
        print("atividade %s" % num)
        print(element.beginTime)
        print(element.finishTime)
        num = num + 1


def create_activities(number_of_activities):
    activities = []
    for x in range(0, number_of_activities):
        new_element = Activity()
        activities.append(new_element)
    return activities


def compute_intervals(I):
    # compara as proximas atividades compativeis
    start = [i.beginTime for i in I]
    finish = [i.finishTime for i in I]

    compatible_activities = []
    for j in range(len(I)):
        i = bisect.bisect_right(finish, start[j]) - 1  # rightmost interval f_i <= s_j
        compatible_activities.append(i)

    return compatible_activities


def schedul_activities(activities):

    # sort activities
    quickSortForActivity(activities)

    p = compute_intervals(activities)

    # compute OPTs iteratively in O(n), here we use DP
    OPT = collections.defaultdict(int)
    OPT[-1] = 0
    OPT[0] = 0
    for j in range(1, len(activities)):
        OPT[j] = max(activities[j].value + OPT[p[j]], OPT[j - 1])

    # given OPT and p, find actual solution intervals in O(n)
    result = []
    def compute_solution(j):
        if j >= 0:  # will halt on OPT[-1]
            if activities[j].value + OPT[p[j]] > OPT[j - 1]:
                result.append(activities[j])
                compute_solution(p[j])
            else:
                compute_solution(j - 1)
    compute_solution(len(activities) - 1)


    return(result)
