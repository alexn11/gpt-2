#!/usr/bin/python3


import subprocess

import cgi
import cgitb

#cgitb . enable() #for debugging


post_data = cgi . FieldStorage ()

key = post_data . getvalue ("key")
if (key is None):
  key = "None"
do_generate_random_address = (post_data . getvalue ("random") == "on")
address_text = post_data . getvalue ("address")
if (address_text is None):
  do_generate_random_address = True
  address_text = "None"

print("Content-Type: text/html\r\n\r\n")
#print("Content-Type: text/plain;charset=utf-8")

print ("<html><head><title>Sample output</title></head><body>")
print ("<br> Key:" + key)
print ("<br> Address:" + address_text)
print ("<br> Random?:" + str (do_generate_random_address))



sampler_call_arguments = [ "python3", "cgi-bin/samplegen.py", "117M", "None", "mode", key ]

if (do_generate_random_address):
  sampler_call_arguments [-2] = "random"
else:
  sampler_call_arguments [-2] = "input"
  sampler_call_arguments . append (address_text)

model_output = subprocess . check_output (sampler_call_arguments)

print ("<br> Result: <br>")
print ("<blockquote>")
print (model_output . decode ("utf-8"))
print ("</blockquote>")

print ("</body></html>")

