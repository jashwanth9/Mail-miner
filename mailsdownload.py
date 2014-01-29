# Something in lines of http://stackoverflow.com/questions/348630/how-can-i-download-all-emails-with-attachments-from-gmail
# Make sure you have IMAP enabled in your gmail settings.
# Right now it won't download same file name twice even if their contents are different.
 
import email
import getpass, imaplib
import os
import sys
from datetime import datetime

def extract_body(payload):
    if not payload:
        return 'no body'
    else:
        if isinstance(payload,str):
            return payload
        else:
            return '\n'.join([extract_body(part.get_payload()) for part in payload])


detach_dir = '.'
if 'attachments' not in os.listdir(detach_dir):
    os.mkdir('attachments')
 
userName = raw_input('Enter your GMail username:')
passwd = getpass.getpass('Enter your password: ')
 
#try:
imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
typ, accountDetails = imapSession.login(userName, passwd)
if typ != 'OK':
    print 'Not able to sign in!'
    raise

print 'sign in complete'

imapSession.select('[Gmail]/All Mail')
typ, data = imapSession.search(None, 'ALL')
if typ != 'OK':
    print 'Error searching Inbox.'
    raise

counter=1

# Iterating over all emails
for msgId in data[0].split():
    typ, messageParts = imapSession.fetch(msgId, '(RFC822)')
    if typ != 'OK':
        print 'Error fetching mail.'
        raise
 
    emailBody = messageParts[0][1]
    mail = email.message_from_string(emailBody)
    for part in mail.walk():
        #if part.get_content_maintype() == 'multipart':
            # print part.as_string()
            # continue

        #if part.get('Content-Disposition') is None:
            # print part.as_string()
            # continue

        print 'reading messages'

        subject = part['subject']
        #print(subject)
        payload = part.get_payload(decode=True)
        body = extract_body(payload)
        #print(body)

            #fileName = part.get_filename()
        fileName = ''.join(str(datetime.now().time()))
        counter+=1

        if bool(fileName):
            filePath = os.path.join(detach_dir, 'attachments', fileName)
            if not os.path.isfile(filePath) :
                print fileName
                fp = open(filePath, 'wb')
                fp.write(body)
                fp.close()

imapSession.close()
imapSession.logout()
#except :

 #   print 'Not able to download all attachments.'