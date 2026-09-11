import re 
import json

INPUT = "input/raw-text.txt"

with open(INPUT, "r") as file:
    text = file.read()

email = r"^\b[\w._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"     #This is the regex pattern for the email
#So, Email is: Username(letter, digits, underscore, dot,%,+ and -) + @ + Domain + Domain extension

emails = re.findall(email, text)

alu_official = []
alu_alumni = []
alu_si = []
not_alu_emails = []
hidden_emails = []

for entry in emails:
    username, domain = entry.split("@")
    hidden_emails.append(username[0]+ "***@" + domain)  # Only the first letter of the username will stay visible the rest will be hidden

    if entry.endswith("@alumni.alueducation.com"):  # This must be checked before the official @alueducation.com
        alu_alumni.append(entry)                    #This is mainly because they all end in the same text
        print("ALU ALUMNI=", entry)
    elif entry.endswith("@si.alueducation.com"):    #The same reason for the SI domain
        alu_si.append(entry)
        print("ALU SI=", entry)
    elif entry.endswith("@alueducation.com"):
        alu_official.append(entry)
        print("ALU OFFICIAL=", entry)
    else:
        not_alu_emails.append(entry)
        print("OTHER EMAILS=", entry)

phone_number = r"\+250\d{9}\b"  #This is the regex pattern for phone number
#It mainly checks for Rwandan numbers only: +250 then any 9 digits

phone_numbers = re.findall(phone_number, text)

Pattern_24H = 

