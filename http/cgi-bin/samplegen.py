#!/usr/bin/env python3

import json
import os
import sys
import numpy as np
import tensorflow as tf

import model, sample, encoder

def read_and_make_address (length, address_text):
  address = np . zeros ([length, ], dtype = "int32")
  address_tokens = address_text . split ()
  token_index = 0
  for token in address_tokens:
    address [token_index] = int (token)
    token_index += 1
  return address


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



model_name = sys . argv [1]
try:
  seed = float (sys . argv [2])
except (ValueError):
  seed = None
mode = sys . argv [3]
key = sys . argv [4]
address_text = None
if (mode == "input"):
  address_text = sys . argv [5]

models_dir = "cgi-bin/models"

generate_sample (model_name = model_name, seed = seed, mode = mode, key = key, address_text = address_text, models_dir = models_dir)


