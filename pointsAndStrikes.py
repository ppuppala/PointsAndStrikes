# See 'V1-Planning.txt' in the Documentation folder for an 
# 	overall description.

# Created By:		Praneet Puppala
# Initial Creation:     July 10, 2014
# Last Modified:	July 19, 2014

from sets import Set
from collections import defaultdict
import csv
import sys
import random

# for email sending
import smtplib
from email.mime.text import MIMEText

# Function for counting number of strikes a person has
def getNumStrikes(p):
	counter = 0
	for item in p:
		if (item[1] == str(-1)):
			counter += 1

	if (counter == 1):
		return "1 strike"
	else:
		return str(counter) + " strikes"

# PART ONE: Read existing file of points and strikes and create hash table
current = open('CYC-pointsAndStrikes-2014.csv','raU')
curr_dict = defaultdict(list)
cols = defaultdict(list) # each val in each col is appended to a list

reader = csv.DictReader(current) # read rows into dict format
for row in reader:  # read row as {col1:val1, col2:val2, etc.}
	curr_dict[(row['Name'],row['Email'])] = []
	for (k,v) in row.items(): # go over each col name and value
		if k != 'Name' and k != 'Email':
			curr_dict[(row['Name'],row['Email'])].append((k,v))
	
# PART TWO: Create set for excused attendances using curr_dict from above
expectedSet = Set(curr_dict.keys())

# PART TWO (cont): Open actual file and create set of actual attendees
actualFile = raw_input("Actual Attendance File Name: ")
actual = open(actualFile, 'rU')

actualSet = Set([])

rowNum = 0
for row in csv.reader(actual):
	if (rowNum != 0):	# Skip first row
		name = row[0]
		email = row[1]
		tup = (name, email)
		actualSet.add(tup)
	rowNum += 1

# Open excused file and create set of excused attendees
excusedFile = raw_input("Excused Attendance File Name: ")
excused = open(excusedFile, 'rU')

excusedSet = Set([])

rowNum = 0
for row in csv.reader(excused):
	if (rowNum != 0):	# Skip first row
		name = row[0]
		email = row[1]
		tup = (name, email)
		excusedSet.add(tup)
	rowNum += 1

# PART THREE: Find expected not in excused and not in actual and 
#    send emails to them

expectedSet = expectedSet.difference(excusedSet)
strikes = expectedSet.difference(actualSet)

eventName = raw_input("Name of event: ")

# Update curr_dict wih event attendance for proper strike counting in email
for p in expectedSet.intersection(actualSet):
	curr_dict[p].append((eventName, '1'))

for p in strikes:
	curr_dict[p].append((eventName, '-1'))

for p in excusedSet:
	curr_dict[p].append((eventName, '0'))

# Email credentials
gmail_user = ENTER EMAIL
gmail_pswd = ENTER PSWD
me = "psp31595@gmail.com"
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(gmail_user, gmail_pswd)

# remove excused members from expected list
for p in strikes:
	body = "Hi " + p[0] + ", \n\nYou have received a strike for missing the " + eventName + " event without being excused. You now have " + getNumStrikes(curr_dict[p]) + ".\n\nPlease contact either Yash or Jason if you have any questions.\n\nSincerely,\nCYC UMD"
	msg = MIMEText(body)
	msg['Subject'] = "Strike Notification for Event: " + eventName
	msg['From'] = 'psp31595@gmail.com'
	msg['To'] = p[1]
	msg['BCC'] = 'puppala2@terpmail.umd.edu'
	TOADDR = [p[1]]
	BCCADDR = ['puppala2@terpmail.umd.edu']
	server.sendmail(gmail_user, TOADDR+BCCADDR, msg.as_string())
	print "Successfully sent mail to " + p[0]

server.close()

# PART FOUR: Update running log of points and strikes.
current.close()
writer = csv.writer(open('CYC-pointsAndStrikes-2014.csv','wb'))

header = ['Name', 'Email']
for item in curr_dict[random.choice(curr_dict.keys())]:
	header.append(item[0])
writer.writerow(header)

for item in curr_dict.items():
	line = [item[0][0], item[0][1]]
	for info in item[1]:
		line.append(info[1])
	writer.writerow(line)

# Close opened files
actual.close()
current.close()
excused.close()
