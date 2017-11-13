import PyPDF2
import re
import requests
import random
import os
import time
import smtplib
import getpass
from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import Process
from itertools import *
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from colorama import Fore, Back, Style
from colorama import init 
freshemail = []
urllist = []
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
	client = requests.session()#requests.session().get(linez).content
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

def RAGEgetEmailsWeb(url,fileoutput,zreps):#get emails from website
	pool_size = 50 # max thread count
	zpool_size = 100
	pool = Pool(pool_size)
	zpool = Pool(zpool_size)
	picz = """

______________$$$$$$$$$$____________________
_____________$$__$_____$$$$$________________
_____________$$_$$__$$____$$$$$$$$__________
____________$$_$$__$$$$$________$$$_________
___________$$_$$__$$__$$_$$$__$$__$$________
___________$$_$$__$__$$__$$$$$$$$__$$_______
____________$$$$$_$$_$$$_$$$$$$$$_$$$_______
_____________$$$$$$$$$$$$$_$$___$_$$$$______
________________$$_$$$______$$$$$_$$$$______
_________________$$$$_______$$$$$___$$$_____
___________________________$$_$$____$$$$____
___________________________$$_$$____$$$$$___
__________________________$$$$$_____$$$$$$__
_________________________$__$$_______$$$$$__
________________________$$$_$$________$$$$$_
________________________$$$___________$$$$$_
_________________$$$$___$$____________$$$$$$
__$$$$$$$$____$$$$$$$$$$_$____________$$$_$$
_$$$$$$$$$$$$$$$______$$$$$$$___$$____$$_$$$
$$________$$$$__________$_$$$___$$$_____$$$$
$$______$$$_____________$$$$$$$$$$$$$$$$$_$$
$$______$$_______________$$_$$$$$$$$$$$$$$$_
$$_____$_$$$$$__________$$$_$$$$$$$$$$$$$$$_
$$___$$$__$$$$$$$$$$$$$$$$$__$$$$$$$$$$$$$__
$$_$$$$_____$$$$$$$$$$$$________$$$$$$__$___
$$$$$$$$$$$$$$_________$$$$$______$$$$$$$___
$$$$_$$$$$______________$$$$$$$$$$$$$$$$____
$$__$$$$_____$$___________$$$$$$$$$$$$$_____
$$_$$$$$$$$$$$$____________$$$$$$$$$$_______
$$_$$$$$$$hg$$$____$$$$$$$$__$$$____________
$$$$__$$$$$$$$$$$$$$$$$$$$$$$$______________
$$_________$$$$$$$$$$$$$$$__________________
"""
	extract_emails = []
	if url.startswith("http://"):
		if url.split("/")[2].split(".")[0] == "www":
			try:
				surl = url.split("/")[2].split(".")[1] #example
			except:
				print "Error parsing URL!"
				return
		else:
			surl = url.split("/")[2].split(".")[0]
		afull = url.split("/")[2]#www.example.com
		durl = "http://" + url.split("/")[2]#http://www.example.com
	elif url.startswith("https://"):
		if url.split("/")[2].split(".")[0] == "www":
			try:
				surl = url.split("/")[2].split(".")[1] #example
			except:
				print "Error parsing URL!"
				return
		else:
			surl = url.split("/")[2].split(".")[0]
		afull = url.split("/")[2] #www.example.com
		durl = "https://" + url.split("/")[2] #https://www.example.com
	else:
		try:
			surl = url.split(".")[0]
		except:
			surl = url.split("/")[2].split(".")[0]
		afull = url
		durl = url
	try:
		r  = requests.get(durl)
	except:
		print "could not get URL!"
		return
	def parseSITE(self):
		dumpdata = []
		cleandata = []
		finaldata = []
		efinaldata = []
		eefinaldata = []
		data = self#r.text
		soup = BeautifulSoup(data, "lxml")
		try:
			for link in soup.find_all('a'):
				dumpdata.append(str(link.get("href")))
		except:
			pass
		for line in dumpdata:
			if surl in line:
				cleandata.append(line.strip())
		for linee in dumpdata:
			if linee.startswith("/"):
				cleandata.append(durl + linee.strip())
		for lined in dumpdata:
			if lined.startswith("#"):
				cleandata.append(durl + "/" + lined.strip())
		for linef in dumpdata:
			if linef.startswith("?"):
				cleandata.append(durl + "/" + linef.strip())
		client = requests.session()
		for test in cleandata:
			if not test.startswith("ftp"):
				finaldata.append(test)
		for testddd in finaldata:
			if not testddd.endswith(("gif", "png", "pdf", "PDF", "GIF", "PNG", "jpg", "JPG", "jpeg", "JPEG", "aac", "abw", "arc", "avi", "azw", "bin", "bz", "bz2", "csh", "css", "csv", "doc", "eot", "epub", "gif", "htm", "html", "ico", "ics", "jar", "jpeg", "jpg", "js", "json", "mid", "midi", "mpeg", "mpkg", "odp", "ods", "odt", "oga", "ogv", "ogx", "otf", "ppt", "rar", "rtf", "sh", "svg", "swf", "tar", "tif", "tiff", "ts", "ttf", "vsd", "wav", "weba", "webm", "webp", "woff", "woff2", "xhtml", "xls", "xlsx", "xml", "xul", "zip", "3gp", "3g2", "7z")):
				efinaldata.append(testddd)
		for testccc in efinaldata:
			if testccc.startswith("http"):
				eefinaldata.append(testccc)
		return eefinaldata
	postfunction = parseSITE(r.text)
	count_the_keys = 0
	for keyz in postfunction:
		count_the_keys += 1
	def multi(self):
		global urllist
		test = parseSITE(requests.get(self).text)
		for liiine in test:
			if liiine not in urllist:
				urllist.append(liiine)
		return
	os.system("clear")
	print Fore.MAGENTA + Style.BRIGHT + picz
	print "FLEXING IN PROGRESS!!! WE'RE LOOKING AT: " + str(count_the_keys) + " REPS!!!"
	if zreps == 2:
		for bine in postfunction:
			pool.apply_async(multi, (bine,))
		pool.close()
		pool.join()
	def secondmulti(self):
		global freshemail
#		print self
		try:
			emails = sorted(set(re.findall(r'[a-zA-Z0-9\.\'-]{1,30}@\w{1,30}\.\w{1,3}', requests.session().get(self).content)))
		except:
			print "COULD NOT RETRIEVE FROM LINK, NEED TO HIT THE GYM MORE!"
			pass
		try:
			for email in emails:
				if email not in freshemail:
					freshemail.append(email)
					file1 = open(fileoutput, 'a+')
					file1.write(str(email) + "\n")
					file1.close()
		except:
			pass
		return
	if zreps == 2:
		more = 0
		for zmore in urllist:
			more += 1
	os.system("clear")
	print "********************************************"
	print "REPS COMPLETE! EXTRACTING EMAILS FROM LINKS!"
	if zreps == 2:
		print "Looks like " + str(more) + " URLS, this could take a while..."
	else:
		print "Looks like " + str(count_the_keys) + " URLS, this shouldnt be too long..."
	print "********************************************"
	if zreps == 2:
		for zebra in urllist:
			zpool.apply_async(secondmulti, (zebra,))
#		secondmulti(zebra)
		zpool.close()
		zpool.join()
	else:
		for lion in postfunction:
			zpool.apply_async(secondmulti, (lion,))
		zpool.close()
		zpool.join()
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
	choice1 = raw_input("\nPlease input \"w\" to extract from a website, \"f\" for a PDF file, \"r\" to pillage a webite or \"q\" for quit?  ")
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
	elif input == 'r':
		print Fore.MAGENTA + Style.BRIGHT + """
_______________ _______________________ ________   
\__    ___/    |   \______   \______   \\_____  \  
  |    |  |    |   /|       _/|    |  _/ /   |   \ 
  |    |  |    |  / |    |   \|    |   \/    |    \

  |____|  |______/  |____|_  /|______  /\_______  /
                           \/        \/         \/ 
_____________________    _____    _______   ____  __.
\_   _____/\______   \  /  _  \   \      \ |    |/ _|
 |    __)   |       _/ /  /_\  \  /   |   \|      <  
 |     \    |    |   \/    |    \/    |    \    |  \ 
 \___  /    |____|_  /\____|__  /\____|__  /____|__ \

     \/            \/         \/         \/        \/ 
"""
		print Fore.MAGENTA + Style.NORMAL +"\nYou chose to blast a website for all emails with " + Style.BRIGHT + "zero fucks.\n"
		url = raw_input("Enter a URL to grab emails (better to add http:// or https://): ")
		output_path = raw_input("Please chose a output file location (e.g., C:\Users\<user>\Documents\): ")
		output_filename = raw_input("Please chose a file name (e.g., emails.txt): ")
		reps = int(raw_input("1 or 2 levels deep?: "))
		if reps > 2:
			print "1 or 2 only dummy!"
			break
		output = os.path.join(output_path,output_filename)
		got_emails = RAGEgetEmailsWeb(url,output,reps)
#		sendEmails(got_emails)
	elif input == 'q':
		break
	else:
		print Fore.MAGENTA + Style.BRIGHT +"\nNot a valid entry;", "please choose \"w\" or \"f\".\n"
		continue
