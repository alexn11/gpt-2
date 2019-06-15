#!/usr/bin/python3

# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, Alexandre De Zotti
# License: MIT License


"""
That's just a toy CGI and should not be used in production environment.
There is absolutely no safety feature or verification whatsoever.
It is REALLY not advised to use this script on any server/website/etc accessible from the internet since this might be dangerous.
"""


import subprocess

import cgi
import cgitb
#cgitb . enable() #for debugging



address_allowed_char = set ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-+")

def check_address (address_text):
  return all ((c in address_allowed_char) for c in address_text)
  

def decode_and_filter_output (model_output):
  decoded_output = model_output . decode ("utf-8")
  clean_output = decoded_output . replace ("<|endoftext|>", "<br><p>")
  # remove html etc....
  return "<p>" + clean_output


def main ():
  is_address_wrong = False
  post_data = cgi . FieldStorage ()
  key = post_data . getvalue ("key")
  if (key is None):
    key = "None"
  do_generate_random_address = (post_data . getvalue ("random") == "on")
  address_text = post_data . getvalue ("address")
  if (address_text is None):
    do_generate_random_address = True
    address_text = "None"
  else:
    if (not check_address (address_text)):
      is_address_wrong = True

  print("Content-Type: text/html\r\n\r\n")
  print ("<html><head><title>Sample output</title></head><body>")
  if (is_address_wrong):
    print ("<h1>Error: index is incorrect</h1>")
    print ("Check that the index contains only letters, numbers, +, - (no space) <br>")
    print ("</body></html>")
    return

  print ("<br> <b>Library name :</b> <i>" + key + "</i>")
  print ("<br> <b>Page index :</b> ")
  if (address_text == "None"):
    print ("(none)")
  else:
    print ("<br>" + address_text)
  print ("<br> <b>Random :</b> " + str (do_generate_random_address))

  sampler_call_arguments = [ "python3", "cgi-bin/samplegen.py", "117M", "cgi-bin/models", "None", "mode", key ]

  if (do_generate_random_address):
    sampler_call_arguments [-2] = "random"
  else:
    sampler_call_arguments [-2] = "input"
    sampler_call_arguments . append (address_text)

  model_output = subprocess . check_output (sampler_call_arguments)

  print ("<br> <b>Result : </b> <br>")
  print ("<blockquote>")
  print (decode_and_filter_output (model_output))
  print ("</blockquote>")

  print ("<a href='/'>Back</a>")

  print ("</body></html>")

if (__name__ == "__main__"):
  main ()














