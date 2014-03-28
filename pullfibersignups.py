#!/usr/bin/env python

import urllib2, json, re, math, time, os, datetime, sys

thisrun = time.strftime("%Y/%m/%d %H:%M")
##### USER SETTINGS #####
##### Enter your fiberhood as spellled on the Google fiber page #####
interestedFiberhoods = ["Clayview"]
##### Defaults to URL for Kansas City
fiberurl='https://fiber.google.com/cities/kansascity/'
##### END USER SETTINGS #####

try:
  response = urllib2.urlopen(fiberurl)
  myhtml = response.read()
  myjson = re.compile('DATA.region = ({.* "id": "kansascity"});', re.DOTALL)
  matches = myjson.search(myhtml)
  myjsondata = matches.group(1)
except urllib2.HTTPError, err:
  if err.code == 500:
    print "500 Error on the page. Try again in a few minutes\n"
  else:
    print "Not sure. Here's the error: ", err

# If I get the data from a string, the method is .loads
data = json.loads(myjsondata)

for step1 in data:
  if step1 == "zones":
    for step2 in data["zones"]:
      # run through the keys in step2, which is a dictionary
      for step3 in step2:
        # Looking for fiberhoods key
        if step3 == "fiberhoods":
          for step4 in step2[step3]:
            if step4["name"] in interestedFiberhoods:
              fiberhood=step4["name"]
              maxinvites = step4["max_invites"]
              numinvites = step4["num_invites"]
              ratio=step4["invite_ratio_target_percentage"]
              goal = math.ceil(maxinvites*(ratio/100))
              print "Time:", thisrun
              print "Fiberhood:", fiberhood
              print " NEEDED:", int(goal-numinvites)
              print " Signups:", numinvites
              print " Goal:", goal
#              print " Max invites:", maxinvites
#              print " Target ratio:", ratio
              print "=========="
              # See what info is available
#              for key in step4.keys():
#                print "Key: ", key
