import requests
import time
import re
from send_sms_smtp import send_sms_smtp

url = "http://texasksa.org/일반-장터/"
my_email = "my_email"
my_pw = "my_pw"
my_phone_no = "my_phone_no"
my_gate_way = "your_carrier_gateway"

# find the curr_uid
rsp = requests.get(url).text  # download the homepage
found = re.search('kboard-list-uid">([0-9]+)<\/td>', rsp, re.M)
curr_uid = found.group(1)

while True:
  rsp = requests.get(url).text  # download the homepage

  found = re.search('kboard-list-uid">([0-9]+)<\/td>', rsp, re.M)
  newest_uid = found.group(1)

  if curr_uid < newest_uid: # new posts exist
    entire_posts = re.search('<tr class="">.+<td class="kboard-list-uid">[0-9]+.+<\/tr>', rsp, re.DOTALL)
    post = re.findall('(<tr class="">.*?<\/tr>)', entire_posts.group(0), re.DOTALL)

    text_message = "중고마켓 알림"
    for i in range(0, newest_uid - curr_uid):
      # abstract the title and the url and build the text message
      title = re.search('</span>(.*?)<span class="kboard-comments-count">', post[i]).group(1)
      post_url = "http://texasksa.org/일반-장터/" + re.search('<a href="\/.*?\/(.*?)">', post[i]).group(1)
      text_message += "\n" + title + "\n" + post_url  # make a text message

      print(text_message)
      send_sms_smtp(email=my_email, pw=my_pw, phone_no=my_phone_no, gate_way=my_gate_way, content=text_message)

      curr_uid = newest_uid # update the id

      else:
        print("sleep..")
        time.sleep(60*5)  # wait 5 minutes
        continue

