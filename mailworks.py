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


def getEmailsPDF(fileinput,fileoutput):#get emails from PDF

	file = open(fileinput,'rb')
	parser = PyPDF2.PdfFileReader(file)#parsing PDF file
	numofpages = parser.getNumPages()
	extract_emails = []
	i = 0
	while i < numofpages:
		page = parser.getPage(i)
		textpage = page.extractText()
		emails = re.findall(r'[a-zA-Z0-9\'-]{1,30}@\w{1,30}\.\w{1,3}', textpage)#seaching for email addresses
		file1 = open(fileoutput, 'a+')
		for email in emails:
			extract_emails.append(str(email))#ensures each email is added to the list
		for email in emails:
			file1.write(email+"\n")#outputs to the chosen location and file name
		i += 1
	print Fore.MAGENTA + Style.BRIGHT +"****PDF Emails Extracted...see %s***" % fileoutput
	return extract_emails


def getEmailsWeb(url,fileoutput):#get emails from website

	extract_emails = []
	client = requests.session()
	page = client.get(url)
	page_parsed = page.content
	emails = sorted(set(re.findall(r'[a-zA-Z0-9\.\'-]{1,30}@\w{1,30}\.\w{1,3}', page_parsed)))#seaching for email addresses
	file1 = open(fileoutput, 'a+')
	for email in emails:
		extract_emails.append(str(email))
	for email in emails:
		file1.write(email + "\n")
	print Fore.MAGENTA + Style.BRIGHT +"****Webite Emails Extracted...see %s***"%fileoutput
	return extract_emails


def sendEmails(email):#send emails using Gmail

	print Fore.MAGENTA + Style.BRIGHT +"\nBegining to Send Emails\n"
	gmail_user = raw_input("What is your email username? ")
	gmail_pwd = getpass.getpass("What is your email password? ")#logs into account, can be used with Gmail if low level security is implemented
	msg = MIMEMultipart()
	msg['Subject'] = raw_input("What is the message subject? ")
	att = raw_input("Where is the attachment location? ")
	i = 1
	for email in email:
		to = email
		msg['From'] = gmail_user
		msg['To'] = to
		if msg['Content-type'] == "multipart/mixed":#used to only appended message body and attachment once
			text = "say something"#enter text here for body of the message
			msg.attach(MIMEText(text, 'plain'))
			fp = open(att, 'rb')
			pdf = MIMEApplication(fp.read(), 'pdf')
			fp.close()
			pdf.add_header('Content-Disposition', 'attachment', filename = 'some.pdf')#give the pdf attachment a name
			msg.attach(pdf)
		smtpserver = smtplib.SMTP("smtp.gmail.com", 587)#message sent using Gmail...this can be changed as needed
		smtpserver.ehlo()
		smtpserver.starttls()
		smtpserver.login(gmail_user, gmail_pwd)
		smtpserver.sendmail(gmail_user, to, msg.as_string())
		print Fore.MAGENTA + Style.BRIGHT +'Message %d Sent!'%i
		i += 1
		del msg['To']#removes from next email, so only one email to address is visible during the send
		del msg['From']#not necessarily needed but wanted to keep consistent
		smtpserver.close()

while True:
	init(autoreset=True)
	print Fore.MAGENTA + Style.BRIGHT + """

   _____         .__.__  __      __             __            
  /     \ _____  |__|  |/  \    /  \___________|  | __  ______
 /  \ /  \\\\__  \ |  |  |\   \/\/   /  _ \_  __ \  |/ / /  ___/
/    Y    \/ __ \|  |  |_\        (  <_> )  | \/    <  \___ \ 
\____|__  (____  /__|____/\__/\  / \____/|__|  |__|_ \/____  >
        \/     \/              \/                   \/     \/ 

"""
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