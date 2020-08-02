import requests
import time
import re
from send_sms_smtp import send_sms_smtp

flea_url = "http://texasksa.org/일반-장터/"
housing_url = "http://texasksa.org/하우징/"
my_email = "your_email@gmail.com" # need to change parameters for send_sms_smtp if not gmail
my_pw = "my_pw" 
my_phone_addr = "phone_no@your_carrier.com"

# Find uid
def find_uid(url):
  rsp = requests.get(url).text  # download the homepage
  found = re.search('kboard-list-uid">([0-9]+)<\/td>', rsp, re.M)
  uid = int(found.group(1))
  return uid

# Make the summary of posts
# Filter texts that we need from the website
def make_text(url, uid_diff):
  if uid_diff == 0:
    return ""
  if uid_diff < 0:
    return "ID mismatching.. check the code"
  
  rsp = requests.get(url).text  # download the homepage
  entire_posts = re.search('<tr class="">.+<td class="kboard-list-uid">[0-9]+.+<\/tr>', rsp, re.DOTALL)
  post = re.findall('(<tr class="">.*?<\/tr>)', entire_posts.group(0), re.DOTALL)
  
  text = ""
  for i in range(0, uid_diff):
    # abstract the title and the url and build the text message
    title = re.search('</span>(.*?)<span class="kboard-comments-count">', post[i]).group(1)
    title = re.sub('\s+', ' ', title) # replace multiple whitespaces to one space
    title = re.sub('^\s', '', title) # remove the whitespace at the beginning
  
    post_url = url + re.search('<a href="\/.*?\/(.*?)">', post[i]).group(1)

    text += str(title) + "\n" + str(post_url) + "\n\n"  # make a text message
  
  text = re.sub('\s+$', ' ', text)
  return text



# Find curr_uids
curr_flea_uid = find_uid(flea_url)
curr_housing_uid = find_uid(housing_url)

while True:
  # Find the new uids
  newest_flea_uid = find_uid(flea_url)
  newest_housing_uid = find_uid(housing_url)
  
  # Create the text message
  text_message = "중고마켓 알림"
  
  if curr_flea_uid < newest_flea_uid or curr_housing_uid < newest_housing_uid: # new posts exist
    if curr_flea_uid < newest_flea_uid: # add flea posts
      text_message += "\n\n"
      text_message += make_text(flea_url, newest_flea_uid - curr_flea_uid)
    if curr_housing_uid < newest_housing_uid: # add housing posts
      text_message += "\n\n"
      text_message += make_text(housing_url, newest_housing_uid - curr_housing_uid)
    
    # Send the message
    send_sms_smtp(email=my_email, pw=my_pw, phone_addr=my_phone_addr, content=text_message)
    
    # Update uids
    curr_flea_uid = newest_flea_uid 
    curr_housing_uid = newest_housing_uid
  
  else:
    print("sleep..")
    time.sleep(60*5)  # wait 5 minutes
    continue
  
