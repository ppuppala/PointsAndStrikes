# See 'V1-Planning.txt' in the Documentation folder for an 
# 	overall description.

# Created By:		Praneet Puppala
# Initial Creation: July 3, 2014
# Last Modified:	July 4, 2014

from sets import Set
import csv
import sys
# for email sending
import smtplib
from email.mime.text import MIMEText

# PART ONE: Create set of expected attendees and set of actual attendees

# Open expected file and create set of expected attendees
expected = open(sys.argv[2],'rU')

expectedSet = Set([])

# CSV reader from python csv module to automatically deal with any
#	weird CSV fomatting
rowNum = 0
for row in csv.reader(expected):
	if (rowNum != 0):	# Skip first row 
		email = row[1]
		expectedSet.add(str(email))
	rowNum += 1

# Open actual file and create set of actual attendees
actual = open(sys.argv[1], 'rU')

actualSet = Set([])

rowNum = 0
for row in csv.reader(actual):
	if (rowNum != 0):	# Skip first row
		email = row[1]
		actualSet.add(str(email))
	rowNum += 1

# PART TWO: Find expected not in actual and send emails to them

# Email body from local plain text file 
body = open('strikeEmailBody.txt', 'rb')
msg = MIMEText(body.read())
body.close()

# Email credentials
gmail_user = "psp31595@gmail.com"
gmail_pswd = SET PASSWD
me = "psp31595@gmail.com"
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(gmail_user, gmail_pswd)

for missing in expectedSet.difference(actualSet):
	msg['Subject'] = 'Strike Notification'
	msg['From'] = 'psp31595@gmail.com'
	msg['To'] = missing
	server.sendmail(gmail_user, missing, msg.as_string())
	print "Successfully sent mail to " + missing

server.close()

# Close opened files
expected.close()
actual.close()

