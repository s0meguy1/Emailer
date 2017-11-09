import PyPDF2
import re
import requests
import os
import smtplib
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from colorama import Fore, Back, Style
from colorama import init 


def getEmailsPDF(fileinput,fileoutput):
    #try:
	file = open(fileinput,'rb')
	parser = PyPDF2.PdfFileReader(file)
	numofpages = parser.getNumPages()
	extract_emails = []
	i = 0
	while i < numofpages:
		page = parser.getPage(i)
		textpage = page.extractText()
		emails = re.findall(r'[a-zA-Z0-9\'-]{1,30}@\w{1,30}\.\w{1,3}', textpage)
		file1 = open(fileoutput, 'a+')
		for email in emails:
			extract_emails.append(str(email))
		for email in emails:
			file1.write(email+"\n")
		i += 1
	print Fore.MAGENTA + Style.BRIGHT +"****PDF Emails Extracted...see %s***" % fileoutput
	return extract_emails
	#except IOError:
		#print "File not found"

def getEmailsWeb(url,fileoutput):
    #try:
	extract_emails = []
	client = requests.session()
	page = client.get(url)
	page_parsed = page.content
	emails = sorted(set(re.findall(r'[a-zA-Z0-9\.\'-]{1,30}@\w{1,30}\.\w{1,3}', page_parsed)))
	file1 = open(fileoutput, 'a+')
	for email in emails:
		extract_emails.append(str(email))
	for email in emails:
		file1.write(email + "\n")
	print Fore.MAGENTA + Style.BRIGHT +"****Webite Emails Extracted...see %s***"%fileoutput
	return extract_emails
    #except IOError:
       # print "Input Incorrect."

def sendEmails(email):
    #try:
	print Fore.MAGENTA + Style.BRIGHT +"\nBegining to Send Emails\n"
	gmail_user = raw_input("What is your email username? ")
	gmail_pwd = getpass.getpass("What is your email password? ")
	name = raw_input("What is your name? ")
	phone = raw_input("What is your phone number? ")
	msg = MIMEMultipart()
	msg['Subject'] = raw_input("What is the message subject? ")
	att = raw_input("Where is the attachment location? ")
	i = 1
	for email in email:
		to = email
		msg['From'] = gmail_user
		msg['To'] = to
		if msg['Content-type'] == "multipart/mixed":
			text = "My name is %s, and I\'m a Member of Crest Security Assurance (a SBA 8(a) WOSB).  I\'m hoping to get an opportunity to have a sit-down with your team to see if you would be interested in partnering with a Cybersecurity Small Business to support future or current task orders.\n"%name
			text += "\nI have attached our capabilities brief for your consideration.\n\n"
			text += "Thank you for your prompt response.\n\n"
			text += "%s\n"%name
			text += "Member\n"
			text += "Crest Security Assurance, LLC\n"
			text += "(P)%s\n"%phone
			text += "(F)571-298-3783\n"
			text += "%s\n"%gmail_user
			text += "www.crestassure.com\n"
			text += "www.linkedin.com/company/crest-security-assurance\n"
			text += "www.facebook.com/crestassure\n"
			text += "12905 Larkmeade Ln, Woodbridge, VA 22193"
			text += "\nSBA 8(a) Certified, WOSB, Virginia Certifed-DBE/MBE, SDB"
			msg.attach(MIMEText(text, 'plain'))
			fp = open(att, 'rb')
			pdf = MIMEApplication(fp.read(), 'pdf')
			fp.close()
			pdf.add_header('Content-Disposition', 'attachment', filename = 'Crest Capabilities Statement.pdf')
			msg.attach(pdf)
		smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
		smtpserver.ehlo()
		smtpserver.starttls()
		smtpserver.login(gmail_user, gmail_pwd)
		smtpserver.sendmail(gmail_user, to, msg.as_string())
		print Fore.MAGENTA + Style.BRIGHT +'Message %d Sent!'%i
		i += 1
		del msg['To']
		del msg['From']
		smtpserver.close()
	#except IOError:
		#print "Something went wrong"
		
while True:
	init(autoreset=True)
	print Fore.MAGENTA + Style.BRIGHT + """
  _________                       __      __             __            
 /   _____/__________    _____   /  \    /  \___________|  | __  ______
 \_____  \\____ \__  \  /     \  \   \/\/   /  _ \_  __ \  |/ / /  ___/
 /        \  |_> > __ \|  Y Y  \  \        (  <_> )  | \/    <  \___ \ 
/_______  /   __(____  /__|_|  /   \__/\  / \____/|__|  |__|_  /____  >
        \/|__|       \/      \/         \/                   \/     \/ """
	choice1 = raw_input("\nPlease input \"w\" to extract from a website, \"f\" for a PDF file, or \"q\" for quit?  ")
	input = choice1.lower()
	if input == 'w':
		print Fore.MAGENTA + Style.BRIGHT +"\nYou chose to pull from webiste.\n"
		url = raw_input("Enter a URL to grab emails (e.g., https://www.google.com): ")
		output_path = raw_input("Please chose a output file location (e.g., C:\Users\<user>\Documents\): ")
		output_filename = raw_input("Please chose a file name (e.g., emails.txt): ")
		output = os.path.join(output_path,output_filename)
		got_emails = getEmailsWeb(url,output)
		sendEmails(got_emails)
		break
	elif input == 'f':
		print Fore.MAGENTA + Style.BRIGHT +"\nYou chose to pull from a PDF.\n"
		fileinput = raw_input("Please input the file location: ")
		output_path = raw_input("Choose a output file location (e.g., C:\Users\<user>\Documents\): ")
		output_filename = raw_input("Please chose a file name (e.g., emails.txt): ")
		output = os.path.join(output_path, output_filename)
		got_emails = getEmailsPDF(fileinput,output)
		sendEmails(got_emails)
		break
	elif input == 'q':
		break
	else:
		print Fore.MAGENTA + Style.BRIGHT +"\nNot a valid entry;", "please choose \"w\" or \"f\".\n"
		continue