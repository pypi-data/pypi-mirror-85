#!/usr/bin/env python

"""GetJob, This code is to send mails with different context depending of company info.
:2020 by Ronald Rivera
"""
import csv
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import re
import json
import ssl
import smtplib
import sys
from time import sleep

class GetJob():
  #load values
  def __init__(self, profile, sms_path, bulk_path, doc_path, *args, **kwargs):
    self.profile = json.load(open(profile))
    self.sms_path = sms_path
    self.bulk_path = bulk_path
    self.doc_path = doc_path
    
  def send(self):
    mails_data = self._parse_csv(self.bulk_path)
    print ("Total mails to send: %s" % len(mails_data))
    print ("Time: %s" % datetime.now())    
    #number of fails
    failed = 0
    for data in mails_data:
      message = self._config_mail(data)
      # Send email
      context = ssl.create_default_context()
      try:
        #python 2
        if(sys.version_info[0] == 2):
          smtp_server = smtplib.SMTP(self.profile['smtp']['server'], self.profile['smtp']['port'])
          smtp_server.ehlo()
          smtp_server.starttls()
          smtp_server.ehlo()
        else:
          #python 3
          smtp_server = smtplib.SMTP_SSL(host=self.profile['smtp']['server'], port=self.profile['smtp']['port'], context=context)
          smtp_server.starttls(context)
          
        smtp_server.login(self.profile['mail'], self.profile['smtp']['password'])
        smtp_server.sendmail(self.profile['mail'], data[2], message)
        #Sleep for .25 secs to take load off the SMTP server
        sleep(0.25)
      except IOError:
        failed = failed + 1
        print "Failed to send: %s" % failed
      
  def _config_mail(self, data):
    #header format mail
    to = "%s <%s>" % (data[0], data[2])
    sender = "%s <%s>" % (self.profile['name'], self.profile['mail'])
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = to
    message["Subject"] = self._lang(data[5], data[1])
    message["Bcc"] = to  # Recommended for mass emails
    #Body
    if data[6] == '0': 
      text = self._replace_str(data, self.sms_path+data[3]+"_"+data[5]+".txt")
      type = "plain"
    else:
      text = self._replace_str(data, self.sms_path+data[3]+"_"+data[5]+".html")
      type = "html"
      
    message.attach(MIMEText(text, type))    
    #PDF file in binary mode
    with open(self.doc_path, "rb") as attach:
      #define mime type
      doc = MIMEBase("application", "octet-stream")
      doc.set_payload(attach.read())
    # Encode to ASCII characters  
    encoders.encode_base64(doc)
    # Add header
    doc.add_header(
      "Content-Disposition",
      "attachment; filename= %s" % (self._lang('re_'+data[5], self.profile['name']) + os.path.splitext(self.doc_path)[1]),
    )
    #Attach and convert message in string
    message.attach(doc)
    return message.as_string()
  
  def _replace_str(self, data, file):
    try:
      with open(file, 'rwb') as text_file:
        read_file = text_file.read()
        rep = {
          "[name]": data[0], 
          "[position]": data[1], 
          "[sender]": self.profile['name'], 
          "[phone]": self.profile['phone'], 
          "[link]": self.profile['link']
        }  
        text_file.close()
        return self._replace(read_file, rep)
    except IOError:
      raise IOError("Error template mail path")
    
  #ref: https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string  
  def _replace(self, string, rep_dict):
    pattern = re.compile("|".join([re.escape(k) for k in sorted(rep_dict, key=len, reverse=True)]), flags=re.DOTALL)
    return pattern.sub(lambda x: rep_dict[x.group(0)], string)
    
  def count_recipients(self, bulk_path = None):
    return len(self._parse_csv(bulk_path))
  
  def _lang(self, l, pos):
    if l == "en":
      return self.profile['lang'][l] + " " + pos
    else:
      return self.profile['lang'][l] + " " + pos
     
  def _parse_csv(self, bulk_path = None):
    """
    Parse the entires each row csv and return to array
    """  
    if not bulk_path:
      bulk_path = self.bulk_path
    try:
      bulk_file = open(bulk_path, 'rwb')
    except IOError:
      raise IOError("Error csv path")
    bulk_reader = csv.reader(bulk_file, delimiter=',')
    bulk_headlings = next(bulk_reader)
    bulk_list = []
    for i, rowi in enumerate(bulk_reader):
      for j, rowj in enumerate(bulk_headlings):
        bulk_headlings[j] = rowi[j]
      bulk_list.append(bulk_headlings[:len(bulk_headlings)])
    bulk_file.close()  
    return bulk_list
  
def main(sys_args):
  profile = sys_args[0]
  sms_path = sys_args[1]
  bulk_path = sys_args[2]
  doc_path = sys_args[3]
  if os.path.splitext(profile)[1] != '.json':
    print("The profile argument doesn't seem to contain a valid json file.")
    sys.exit()
    
  if os.path.splitext(bulk_path)[1] != '.csv':
    print("The profile argument doesn't seem to contain a valid json file.")
    sys.exit()  

  try:
    profile, sms_path, bulk_path, doc_path
  except ValueError:
    print("Not enough argumants supplied. GetJob requests 1 option and 3 arguments: ./getjob.py profile sms_path  bulk_path doc_path")
    sys.exit()
  mail = GetJob(profile, sms_path, bulk_path, doc_path)
  mail.send()
  
if __name__ == '__main__':
  main(sys.argv[1:])