#!/usr/bin/env python3

"""
MIT License

Copyright (c) 2019 Alexandre De Zotti (modifications)
Copyright (c) 2019 OpenAI
"""


import json
import os
import sys
import numpy as np
#import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

import model, sample, encoder

def convert_letter_to_binary (letter):
  letter_value = ord (letter)
  if ((letter >= 'a') and (letter <= 'z')):
    value = letter_value - ord ('a')
  elif ((letter >= 'A') and (letter <= 'Z')):
    value = letter_value - ord ('A') + 26
  elif ((letter >= '0') and (letter <= '9')):
    value = letter_value - ord ('0') + 52
  elif (letter == '-'):
    value = 62
  elif (letter == '+'):
    value = 63
  return bin (value) [ 2 : ] [ : : -1 ]

def convert_address_text_to_numbers (length, address_text):
  # each address index is a 16 bits unisgned integer
  # the address is separated in size-6 subrows
  subrows_per_row = length // 6 + (0 if ((length % 6) == 0) else 1)
  address_indexes = np . zeros ([length, ], dtype = "int32")
  row = 0
  subrow = 0
  for letter in address_text:
     binary_string = convert_letter_to_binary (letter)
     bit_index = 0
     for digit in binary_string:
       try:
         address_indexes [ 6 * subrow + bit_index ] += ((int (digit)) << row)
       except (IndexError): # some of the data will just be ignored because length is not necessarily divisible by 6
         break
       bit_index += 1
     subrow += 1
     if (subrow == subrows_per_row):
       row += 1
       subrow = 0
  return address_indexes


def read_and_make_address (length, address_text):
  return convert_address_text_to_numbers (length, address_text)



def generate_sample (
    model_name = '117M',
    seed = None,
    length = None,
    temperature = 1,
    mode = "random",
    key = "The Library Of Babel!",
    models_dir = 'models',
    address_text = None):
    """
    Interactively run the model
    :model_name=117M : String, which model to use
    :seed=None : Integer seed for random number generators, fix seed to reproduce
     results
    :length=None : Number of tokens in generated text, if None (default), is
     determined by model hyperparameters
    :temperature=1 : Float value controlling randomness in boltzmann
     distribution. Lower temperature results in less random completions. As the
     temperature approaches zero, the model will become deterministic and
     repetitive. Higher temperature results in more random completions.
    :mode : how to produce the address: 
     "input": input interactively as a sequence of integers,
     "random": according to a Poisson distribution whose parameter lambda is equal to temperature
    :key : primordial context text, used to initialize the generator
    :models_dir : path to parent folder containing model subfolders
     (i.e. contains the <model_name> folder)     
    """
    if (mode not in ("input", "random")):
     raise Exception ("mode should be either input or random")

    models_dir = os.path.expanduser(os.path.expandvars(models_dir))

    poisson_lambda = temperature

    enc = encoder.get_encoder(model_name, models_dir)
    hparams = model.default_hparams()
    with open(os.path.join(models_dir, model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))

    if length is None:
        length = hparams.n_ctx // 2
    elif length > hparams.n_ctx:
        raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

    with tf.Session(graph=tf.Graph()) as sess:

        context = tf . placeholder (tf . int32, [None, ])
        address = tf . placeholder (tf . int32, [length, ])

        np . random . seed (seed)
        tf . set_random_seed (seed)

        output = sample . sample_sequence (hparams = hparams,
                                           length = length,
                                           address = address,
                                           context = context,
                                           temperature = temperature)

        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(models_dir, model_name))
        saver.restore(sess, ckpt)

        context_tokens = enc . encode (key)

        # NOTE: temperature is now used as the lambda parameter of the poisson distribution
        if (mode == "input"):
          address_input = read_and_make_address (length, address_text)
        elif (mode == "random"):
          # FOR RANDOMLY GENERATED ADDRESS: (the prompt loop just to get the opportunity to interrupt the prgram)
          # maybe put a "end of text" token in the context?
          address_input = np . random . poisson (poisson_lambda, length)
          address_input = np . where (address_input < hparams . n_vocab, address_input, hparams . n_vocab)

        out = sess . run (output,
                          feed_dict = {
                                        context : context_tokens,
                                        address : address_input,
                                   }) [ len (context_tokens) : ]

        text = enc . decode (out)
        print (text)


def main ():
  model_name = sys . argv [1]
  models_dir = sys . argv [2]
  try:
    seed = float (sys . argv [3])
  except (ValueError):
    seed = None
  mode = sys . argv [4]
  key = sys . argv [5]
  address_text = None
  if (mode == "input"):
    address_text = sys . argv [6]

  generate_sample (model_name = model_name, seed = seed, mode = mode, key = key, address_text = address_text, models_dir = models_dir)




if (__name__ == "__main__"):
  if (sys . argv [1] == "--help"):
    print ("Examples:")
    print ("  $ python3 samplegen.py 117M models None random 'Alpha and Omega'")
    print ("  $ python3 samplegen.py 117M models None input 'Alpha and Omega' abs-+c05d9dfqgEEZ")
    sys . exit (0)
  main ()




