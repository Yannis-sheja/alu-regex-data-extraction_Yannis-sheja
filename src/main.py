import re 
import json

INPUT = "input/raw-text.txt"

with open(INPUT, "r") as file:
    text = file.read()

email = r"^\b[\w._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"     #This is verify for the email
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

phone_number = r"\+250\d{9}\b"  #This is verify for phone number
#It mainly checks for Rwandan numbers only: +250 then any 9 digits

phone_numbers = re.findall(phone_number, text)

Pattern_24H = r"\b(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?\b(?!s?[APap][Mm])" #This is to verify for time in 24h
# So, 00-23 hours, then 00-59 minutes and then seconds which is optional
#Seconds are skipped whenever AM/PM follows
Pattern_12H = r"\b(?:0?[1-9]1[0-2]):[0-5]\d\s?[APap][Mm]\b"         #This is verify for time 12h 
#So, 1-12 hours, then 00-59 minutes and then the AM/PM

time_in_24H = re.findall(Pattern_24H, text)
time_in_12H = re.findall(Pattern_12H, text)

credit_card = r"\b\d{4}[ -]?\d{4}[ -]?\d{4}\b"  #This is to verify for a credit card
# Here we have four groups of four digits each, you can add space, dashes or no separator at all

credit_cards = re.findall(credit_card, text)

hidden_cards = []
for number in credit_cards: 
    digits = re.sub(r"[ -]","", number)     # This is to drop the seperators first so that the last -4 slice always lines up
    hidden_cards.append("**** **** **** " + digits[-4:])    #Here every number is hidden except the last four digits

#####CHECKING FOR RISKS#####
#Anything that is pulled out of the log file is just data, never something to run.
#If the text contains what looks like a script or HTML Injection or a
#SQL-style attack string, this will catch it instead of trusting it blindly.

risks = r"<script|<img|drop\s+table|delete\s+from|javascript:"
risk_flag = bool(re.search(risks, text, flags = 2))

final_report = {
    "emails": {
        "official":alu_official,
        "alumni": alu_alumni,
        "si": alu_si,
        "others": not_alu_emails,
        "hidden email": hidden_emails
    },
    "phone_numbers": phone_numbers,
    "time": {
        "24H_format": time_in_24H,
        "12H_format": time_in_12H
    },
    "credit_card": hidden_cards,
    "security_check": {
        "Status": "Completed",
        "External_text_executed": False,
        "Threat_detected": risk_flag
    }
} 

with open("output/sample-output.json", "w") as output_stream:
    json.dump(final_report, output_stream, indent=4)


