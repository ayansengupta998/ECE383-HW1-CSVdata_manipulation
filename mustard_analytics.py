# COMPSCI 383 Homework 0 
#  
# Fill in the bodies of the missing functions as specified by the comments and docstrings.


import sys
import csv
from datetime import datetime
import pandas
from collections import Counter


csvobj =''
# Exercise 0. (8 points)
#  
def read_data(file_name):
    """Read in the csv file and return a list of tuples representing the data.

    Transform each field as follows:
      date: datetime.date
      mileage: integer
      location: string
      gallons: float
      price: float (you'll need to get rid of the '$')

    Do not return a tuple for the header row.  And for the love of all that's holy, do not use
    primitive string functions for parsing (use the csv modules instead).

    Hint: to parse the date field, use the strptime function in the datetime module, and then
    use datetime.date() to create a date object.

    See: 
      https://docs.python.org/3/library/csv.html
      https://docs.python.org/3/library/datetime.html

    """
    rows = []  # this list should contain one tuple per row
    temp_list =[]
    csvobj = csv.reader(open(file_name,newline ='')) #open csv file with csv module and instantiate a reader obj
    next(csvobj) #iterates over the first row essentially skiiping it in this context
    temp_list = [list(x) for x in csvobj] #making the list of lists by adding one row at a time from reader obj
    for x in range(len(temp_list)): #iterate over list of list and convert date in string to date obj and the other fields to their respective formats 
      temp_list[x][0] =  datetime.strptime(temp_list[x][0],'%m/%d/%Y').date()
      temp_list[x][1] = int(temp_list[x][1])
      temp_list[x][3] = float(temp_list[x][3])
      list1 = list(temp_list[x][4]) #making a new list with the string values casted as a list (str are immutable in python)
      list1[0] =''#deletes the $
      temp_list[x][4] = ''.join(list1) #cput in the new values without the $
      temp_list[x][4] = float(temp_list[x][4]) #cast to float iteratively
    rows = [tuple(row) for row in temp_list]
    return rows  # a list of (date, mileage, location, gallons, price) tuples


# Exercise 1. (5 points)
#
def total_cost(rows): #calculate total cost spent on gas as a float
    total = 0.0
    for x in range(len(rows)):
      total = total + rows[x][3]*rows[x][4]
    return total  


# Exercise 2. (5 points)
#
def num_single_locs(rows):
    """Return the number of refueling locations that were visited exactly once.
    
    Hint: store the locations and counts (as keys and values, respectively) in a dictionary, 
    then count up the number of entries with a value equal to one.  
    """
   
    temp_list =[]
    flag = 0
    for x in range(len(rows)):
      temp_list.append(rows[x][2]) #make a list of all the locations in the list of tuples passed to the function
    count = Counter(temp_list) #use the Counter function from the collections library to make a counter obj (sub class of dict)
    temp_dict = dict(count) #cast as a native dict and store the dict in the temp_dict variable
    for cnt in temp_dict.values():#iterate trough each value and add +1 to count when the value is 1 
      if(cnt == 1):
        flag = flag +1
    return flag  # fix this line to return an int


# Exercise 3. (7 points)
#
def most_common_locs(rows):
    """Return a list of the 10 most common refueling locations, along with the number of times
    they appear in the data, in descending order.  
    
    Each list item should be a two-element tuple of the form (name, count).  For example, your
    function might return a list of the form: 
      [ ("Honolulu, HI", 42), ("Shermer, IL", 19), ("Box Elder, MO"), ... ]

    Hint: store the locations and counts in a dictionary as above, then convert the dictionary 
    into a list of tuples using the items() method.  Sort the list of tuples using sort() or 
    sorted().

    See:
      https://docs.python.org/3/tutorial/datastructures.html#dictionaries
      https://docs.python.org/3/howto/sorting.html#key-functions
    """
    temp_list =[]
    flag = 0
    for x in range(len(rows)):
      temp_list.append(rows[x][2]) #make a list of all the locations in the list of tuples passed to the function
    count = Counter(temp_list) #use the Counter function from the collections library to make a counter obj (sub class of dict)
    temp_dict = dict(count)
    list_arg = [x for x in temp_dict.items()] #list of tuple
    list_arg.sort(key = lambda tup : tup[1], reverse=True) #sort descending using the second value of the tuple
    list_arg = list_arg[0:10] #only return the first 10 strings since the list is in descending order
    return list_arg # fix this line to return a list of strings


# Exercise 4. (7 points)
#
def state_totals(rows):
    """Return a dictionary containing the total number of visits (value) for each state as 
    designated by the two-letter abbreviation at the end of the location string (keys).  

    The return value should be a Python dictionary of the form:
      { "CA": 42, "HI": 19, "MA": 8675309, ... }

    Hint: to do this, you'll need to pull apart the location string and extract the state 
    abbreviation.  Note that some of the entries are malformed, and containing a state code but no
    city name.  You still want to count these cases (of course, if the location is blank, ignore
    the entry.
    """
    count = 0
    temp_dict = {}
    for x in range(len(rows)):
        location = rows[x][2]
        for i in location:
            count= count +1
            if i ==',':
                location = location[count+1:]
                count =0
                break
        if (location in temp_dict):
            temp_dict[location] = temp_dict[location] + 1
        else:
            temp_dict[location] = 1
    return temp_dict

   


# Exercise 5. (7 points)
#
def num_unique_dates(rows):
    """Return the total number unique dates in the calendar that refueling took place.

    That is, if you ignore the year, how many different days had entries? (This number should be 
    less than or equal to 366!)
 
    Hint: the easiest way to do this is create a token representing the calendar day.  These could
    be strings (using strftime()) or integers (using date.toordinal()).  Store them in a Python set
    as you go, and then return the size of the set.

    See:
      https://docs.python.org/3/library/datetime.html#date-objects
    """
   
    mySet = set()
    with open('mustard_data.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for line in csv_reader:
            date = line[0]
            
            date_split = date.split("/")
            for i in range(0, 2):
                date_split[i] = int(date_split[i])

                if date_split[i] < 10:
                    date_split[i] = '0' + str(date_split[i])
                else:
                    date_split[i] = str(date_split[i])
            entre = ""
            for i in range(0, 2):
                entre = entre + date_split[i] + '/'
            entre = entre + date_split[2]

            date = datetime.strptime(entre, '%m/%d/%Y')
            date = date.strftime('%B, %d')
            mySet.add(date)

    return len(mySet)  # fix this line to return an int



# Exercise 6. (7 points)
#
def month_avg_price(rows):

    """Return a dictionary containing the average price per gallon as a float (values) for each 
    month of the year (keys).

    The dictionary you return should have 12 entries, with full month names as keys, and floats as
    values.  For example:
        { "January": 3.12, "February": 2.89, ... }

    See:
      https://docs.python.org/3/library/datetime.html
    """
    
    dict = {}
    tuple= ()
    dictCount = {}
    with open('mustard_data.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for line in csv_reader:
            date =line[0]
            date_split = date.split("/")
            for i in range(0, 2):                           #I padded the zeros
                date_split[i] = int(date_split[i])

                if date_split[i] < 10:
                    date_split[i] = '0' + str(date_split[i])
                else:
                    date_split[i] = str(date_split[i])
            entre = ""
            for i in range(0, 2):
                entre = entre + date_split[i] + '/'
            entre = entre + date_split[2]

            date = datetime.strptime(entre, '%m/%d/%Y')
            date = date.strftime('%#B')
            #print(date)

            price = line[4]
            price = price.replace("$", "")
            price = float(price)
            if date in dict:
                dict[date] = dict[date]+price
            else:
                dict[date] = price
            if date in dictCount:
                dictCount[date] = dictCount[date] + 1
            else:
                dictCount[date] = 1

    for entre in dict.keys():
        dict[entre] = dict[entre]/float(dictCount[entre])
    
    return dict  # fix this line to return a dictionary


    
    

    


# Exercise 7. (4 points)
#
def these_are_my_words():
    """Return a string constructed from the course syllabus and code of conduct."""

    word1 = "be"  # Change this string to be the i-th word of the Homework Lateness Policy
                   # of the Course Syllabus found on Moodle, where i is the first digit of your
                   # Spire ID (don't forget to start counting at 0). spire ID = 31477475

    word2 = "and"  # Change this string to the j-th word of the Expected Behavior section
                   # of the Code of Conduct found on Moodle, where j is the last digit of your
                   # Spire ID (don't forget to start counting at 0).
    
    return " ".join([word1, word2])


# EXTRA CREDIT (+0 points, do this for fun and glory)
#
def highest_thirty(rows):
    """Return the start and end dates for top three thirty-day periods with the most miles driven.

    The periods should not overlap.  You should find them in a greedy manner; that is, find the
    highest mileage thirty-day period first, and then select the next highest that is outside that
    window).
    
    Return a list with the start and end dates (as a Python datetime object) for each period, 
    followed by the total mileage, stored in a tuple:  
        [ (1995-02-14, 1995-03-16, 502),
          (1991-12-21, 1992-01-16, 456),
          (1997-06-01, 1997-06-28, 384) ]
    """
    #
    # fill in function body here
    #
    return []  # fix this line to return a list of tuples


# The main() function below will be executed when your program is run to allow you to check the 
# output of each function.
def main(file_name):
    rows = read_data(file_name)
    print("Exercise 0: {} rows\n".format(len(rows)))

    cost = total_cost(rows)
    print("Exercise 1: ${:.2f}\n".format(cost))

    singles = num_single_locs(rows)
    print("Exercise 2: {}\n".format(singles))

    print("Exercise 3:")
    for loc, count in most_common_locs(rows):
        print("\t{}\t{}".format(loc, count))
    print("")

    print("Exercise 4:")
    for state, count in sorted(state_totals(rows).items()):
        print("\t{}\t{}".format(state, count))
    print("")

    unique_count = num_unique_dates(rows)
    print("Exercise 5: {}\n".format(unique_count))

    print("Exercise 6:")
    for month, price in sorted(month_avg_price(rows).items(),
                               key=lambda t:datetime.strptime(t[0], '%B').month):
        print("\t{}\t${:.2f}".format(month, price))
    print("")

    words = these_are_my_words()
    print("Exercise 7: {}\n".format(words))

    print("Extra Credit:")
    for start, end, miles in sorted(highest_thirty(rows)):
        print("\t{}\t{}\t{} miles".format(start.strftime("%Y-%m-%d"),
                                          end.strftime("%Y-%m-%d"), miles))
    print("")


#########################

if __name__ == '__main__':
    
    data_file_name = "mustard_data.csv" 
    main(data_file_name)




