# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2018-10-21
# Copyright (C) 2018, Alexandre De Zotti
# License: MIT License

import numpy

from samplegen import convert_address_text_to_numbers, convert_letter_to_binary

from query import check_address


def test_check_address ():
  assert (check_address ("" . join (list (map (chr, range (97, 123))))))
  assert (check_address ("" . join (list (map (chr, range (65, 91))))))
  assert (check_address ("" . join (list (map (chr, range (48, 58))))))
  assert (check_address ("ab+s-d06ZT"))
  assert (not check_address ("5461dfsaeE*f54"))
  assert (not check_address ("" . join (list (map (chr, range (32, 48))))))
  assert (not check_address ("" . join (list (map (chr, range (58, 68))))))
  assert (not check_address ("" . join (list (map (chr, range (90, 126))))))


def test_convert_address_text_to_numbers ():
  length = 512
  address_text = "a" * (86 * 16)
  address_indexes = convert_address_text_to_numbers (length, address_text)
  only_zeros = numpy . zeros (length, dtype = "int32")
  assert (numpy . array_equal (address_indexes, only_zeros))
  address_indexes = convert_address_text_to_numbers (length, "a")
  assert (numpy . array_equal (address_indexes, only_zeros))
  address_text = "-C8ab+"
  address_indexes = convert_address_text_to_numbers (length, address_text)
  relevant_indexes = 6 * len (address_text)
  remainder_len = len (address_indexes) - relevant_indexes
  assert (numpy . array_equal (address_indexes [ relevant_indexes : ], only_zeros [ : remainder_len ]))
  assert (numpy . array_equal (address_indexes [ : relevant_indexes ], numpy . array ([ 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, ], dtype = "int32")))
  address_text = "b" + (85 * "a") + "c" + (85 * "a") + "b"
  address_indexes = convert_address_text_to_numbers (length, address_text)
  assert (address_indexes [0] == 5)
  assert (address_indexes [1] == 2)
  assert (numpy . array_equal (address_indexes [ 2 : ], only_zeros [ : 510]))


def test_convert_letter_to_binary ():
  assert (convert_letter_to_binary ("a") == "0")
  assert (convert_letter_to_binary ("b") == "1")
  assert (convert_letter_to_binary ("z") == "10011")
  assert (convert_letter_to_binary ("A") == "01011")
  assert (convert_letter_to_binary ("Z") == "110011")
  assert (convert_letter_to_binary ("0") == "001011")
  assert (convert_letter_to_binary ("2") == "011011")
  assert (convert_letter_to_binary ("9") == "101111")
  assert (convert_letter_to_binary ("-") == "011111")
  assert (convert_letter_to_binary ("+") == "111111")
  try:
   convert_letter_to_binary ("aa")
  except (TypeError):
   pass
  else:
   raise (AssertionError)


print ("running tests...")


test_convert_letter_to_binary ()
test_convert_address_text_to_numbers ()
test_check_address ()

print ("all good.")

