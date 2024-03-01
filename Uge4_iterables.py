from faker import Faker
import numpy as np
import matplotlib.pyplot as plt
import string
fake = Faker()


###
### DEFINING FUNCTIONS
###

#takes an open file and reads it line by line using yield
def yield_line(file): 
    yline = len(file.readlines())
    file.seek(0)
    for i in range(yline):
        yield file.readline()

# prints lines in txt file longer than n characters (including spaces)
def long_names(filename,n):
    long_names = []
    f = open(filename, mode = 'r+')
    lines = len(f.readlines())
    f.seek(0)
    name = yield_line(f)
    
    for i in range(lines):
        temp_name = next(name)
        if len(temp_name)>=n:
            long_names.append(temp_name)
            print(temp_name)

    f.close()
    return long_names
    

# function used to find sunny cities in data of hours of sun i found.
# If city has more than n hours of sun a year, city and country is printed
# aswell as most sunny month and hours of sun for that month
def sunshine(filename, n, printtext = False):
     f = open(filename, mode = 'r+')
     lines = len(f.readlines())
     f.seek(0)
     city = yield_line(f)
     months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
     sunshine_cites = []
     sunshine_hours = []
     
     # The file has 1 line for each city, so here looping through cities
     for i in range(lines):
         #using the iterator to acces next line in file
         temp_city = next(city)
         
         #splitting string into list to extract data
         city_sun = temp_city.split()
         
         #last entry has total sun hours per year
         #split is necesary to handle differing formats concerning the use of thousands-dividers within file
         temp_sun = city_sun[-1].split('.')
         
         # The indices below match the columns with data for individual months
         sun_months = city_sun[3:15]
         
         #small IF statement to dodge 1st row with column names
         #with the full file loaded I would use .pop(0) or just pandas, which entirely avoids this issue
         if i >= 1:
             
             #converting last entry into integer for sorting 
             #again dodging annoying data entry inconsitencies with .split()
             total_sun = int(str(''.join(temp_sun)).split(',')[0])
             if total_sun>=n:
                 
                 for j in range(len(sun_months)):
                     
                     #more correction of types so I can actually use the numbers
                     sun_months[j] = float(sun_months[j].split(',')[0])
                     
                 #print statement for cities with more than n hours of sunlight
                 if printtext == True:
                     #Prints city name and country if city has more than n hours of sun a year
                     print(city_sun[2]+', '+city_sun[1])
                     #Prints the month with most sun for the city as well as corresponding sun hours
                     print(months[sun_months.index(max(sun_months))]+': '+str(max(sun_months)))
                     temp_avg = sum(sun_months)/12
                     print('Avg: '+ str(temp_avg)[0:6]+'\n')
                     
                 #saving 2 lists: city + country as string , and a list of lists of 12 months sunlight data
                 #in case you want to plot the data
                 sunshine_cites.append(city_sun[2]+', '+city_sun[1])
                 sunshine_hours.append(sun_months)
     f.close()
     
     
     return sunshine_cites, sunshine_hours


#function for analysing names (file /w 1 name/line)
#returns list for histograms of name length and first and last initials
#also returns a matrix for 3d histograms of firstname/lastname initials combinations
def name_stats(filename):
    
    #defining list with only 0 so I can add to histogram data when I find a match
    names_length = np.zeros(30)
    first_initial = np.zeros(26)
    last_initial = np.zeros(26)
    initials_matrix = np.zeros((26,26))
    
    #define list of letters to compare with
    alphabet = list(string.ascii_lowercase)
    
    #open file and determine number of lines
    f = open(filename, mode = 'r+')
    lines = len(f.readlines())
    f.seek(0)
    
    #initiate iterable
    ns_name = yield_line(f)
    
    # Looping through names
    for i in range(lines):
        
        #use iterable to go to next line
        #setting all characters to lowercase so we don't miss any
        ns_temp_name = next(ns_name).lower()
        #splitting the full name
        splt_name = ns_temp_name.split(' ')
        #removing spaces to determine length of name
        no_spaces = ''.join(splt_name)
        
        #looping through alphabet while keeping track of how far along we are
        count = 0
        for a in alphabet:
            
            #checking for first initial match
            if splt_name[0][0] == a:
                
                #stats for first initial
                first_initial[count] += 1
                
                #second alphabet loop to check initials combinations
                mcount = 0
                for b in alphabet:
                    if splt_name[1][0] == b:
                        initials_matrix[count][mcount] += 1
                    mcount += 1
            
            #last initial match
            if splt_name[1][0] == a:
                #stats for last initial
                last_initial[count] +=1
            count += 1
            
        # name length stats for each name (remember arrays start at 0!)
        names_length[len(no_spaces)-1] += 1

    #close file, return stats gathered
    f.close()
    return names_length, first_initial, last_initial, initials_matrix


###
### GENERATING TEXT FILE & EXECUTING FUNCTIONS
###


# using faker module to write file with L names on the format "Firstname Lastname" (1 of each)
# 1 name per line
fnames = open('fake_names.txt',mode='w')
l =10000
for i in range(l):
    fnames.write(fake.first_name()+' '+fake.last_name()+'\n')
fnames.write(fake.first_name()+' '+fake.last_name())

fnames.close()
#long_names('fake_names.txt', 20)

#Calling name_stats function so we have stats to plot
alphabet2 = list(string.ascii_lowercase)
test_length, test_finit, test_linit, tmatrix = name_stats('fake_names.txt') 


###
###  FIGURES: PRESENTING THE DATA
###



#Variables to plot (X and Y are just the alphabet, but matplotlib's 3d plots dont seem to like string)
X = range(26)
Y = range(26)
X, Y = np.meshgrid(X, Y)
Z = tmatrix
bottom = np.zeros((26,26))
width = depth = 1
X, Y,Z, bottom= X.ravel(), Y.ravel(),Z.ravel(), bottom.ravel()
#print(test_length, sum(test_length))


#plotting First initial / Last initial data in a 3d histogram
# use '%matplotlib qt' in terminal for best view of the 3d plot
fig = plt.figure()
plt.rcParams.update({'font.size': 8})
ax = fig.add_subplot(projection='3d')
ax.bar3d(X, Y, bottom, width, depth, Z, shade=True, alpha=0.55)
ax.set_title('Occurance of Combinations of Initials')
ax.set_xticks(range(0,26))
ax.set_xticklabels(alphabet2)
ax.set_yticks(range(0,26))
ax.set_yticklabels(alphabet2)
plt.ylabel('First Name Initial')
plt.xlabel('Last Name Initial')
ax.set_zlabel('Number of Ocurrances')

# Simple indpependent histograms for first and last initials
plt.figure()
plt.hist(np.arange(26),bins=26,weights=test_finit, alpha=1,color='b')
plt.hist(np.arange(26),bins=26,weights=test_linit, alpha=0.5,color='r')
plt.legend(['First Initial','Last Initial'], loc='upper right')
plt.title('Occurances of Initials')
plt.xticks((np.arange(26)+0.5)*26/27,alphabet2)
plt.xlabel('Initial')
plt.ylabel('Number of Occurances')


# Histogram of name lengths
# Making a list with a name-length value for each name to extract some statistics from
inverse_length_array = []
for i in range(len(test_length)):
    for j in range(int(test_length[i])):
        inverse_length_array.append(i+1)
# Plotting the histogram
plt.figure()
plt.hist(np.arange(len(test_length)),bins=len(test_length),weights=test_length,color='c')
plt.text(20,1750,'Mean:    '+str(np.mean((inverse_length_array)))[0:5])
plt.text(20,1675,'Avg:       '+str(np.average((inverse_length_array)))[0:5])
plt.text(20,1600,'Std dev: '+str(np.std((inverse_length_array)))[0:4])
plt.title('Name length histogram')
plt.xlabel('Length of name')
plt.ylabel('Number of Occurances')



# Plotting some extracted stats from the sunshine-hours datafile i found online
# cities (having a line each in the file) are filtered according to yearly hours of sun
# cities above a given minimum (n_test) are returned from the 'sunshine' function and plotted here
plt.figure()
n_test = 3900
ymin = 200
ymax = 500
cities, data = sunshine('sunshine_stats.txt', n_test)
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
for d in range(len(data)):
    plt.plot(months,data[d])
plt.legend(cities)
plt.text(0,ymax-((ymax-ymin)/12),'Avg per month: '+str(np.mean((data)))[0:5])
plt.title('Sun-hours Stats for cities with more than '+str(n_test)+' hours of sun a year')
plt.ylabel('Hours of sunshine')
plt.xlabel('Month')
plt.ylim((ymin,ymax))
plt.show()



