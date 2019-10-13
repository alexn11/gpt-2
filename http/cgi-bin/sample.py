#import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

import model



def sample_sequence(*, hparams, length, address, start_token=None, context=None, temperature=1):
    if start_token is None:
        assert context is not None, 'Specify exactly one of start_token and context!'
    else:
        assert context is None, 'Specify exactly one of start_token and context!'
        context = tf.fill([1, ], start_token)

    def step(hparams, tokens, past=None):
        #print (">>step >> tokens="+str(tokens))
        X = tf . expand_dims (tokens, 0)
        #print (">>step>> X = "+str(X))
        #print (">>step>> past="+str(past))
  
        lm_output = model . model (hparams = hparams, X = X, past = past, reuse = tf.AUTO_REUSE)

        logits = lm_output ['logits'][:, :, :hparams.n_vocab]
        presents = lm_output ['present']
        presents . set_shape (model.past_shape(hparams=hparams, batch_size=1))
        return {
            'logits': logits,
            'presents': presents,
        }

    with tf.name_scope('sample_sequence'):
        # Don't feed the last context token -- leave that to the loop below
        # TODO: Would be slightly faster if we called step on the entire context,
        # rather than leaving the last token transformer calculation to the while loop.
        context_output = step (hparams, context [ : -1 ])

        def body(past, prev, output, addr):
            next_outputs = step (hparams, prev, past = past)
            logits = next_outputs ['logits'] [:, -1, :]
            samples = tf . gather_nd (tf . argsort (logits [0, :], direction = "DESCENDING"), [ [ addr [ 0 ] ], ])
            #print (">>>> next past=" + str (tf.concat([past, next_outputs['presents']], axis=-2)))
            #print (">>>> next prev=" + str(samples))
            #print (">>>> next output="+str(tf.concat([output, samples], axis=0)))
            #print (">>>> next addr="+str(addr[1:]))
            return [
                tf.concat([past, next_outputs['presents']], axis=-2),
                samples,
                tf.concat([output, samples], axis=0),
                addr [ 1 : ],
            ]

        def cond(*args):
            return True

        #print (">>>> past="+str(context_output["presents"]))
        #print (">>>> prev="+str(context [ -1 : ]))
        #print (">>>> output=context")
        #print (">>>> context="+str(context))
        #print (">>>> address="+str(address))

        _, _, tokens, _ = tf.while_loop(
            cond=cond, body=body,
            maximum_iterations=length,
            loop_vars=[
                context_output ['presents'],
                context [ -1 : ],
                context,
                address,
            ],
            shape_invariants=[
                tf.TensorShape(model.past_shape(hparams=hparams, batch_size=1)),
                tf.TensorShape([None, ]), # 1 really
                tf.TensorShape([None, ]),
                tf . TensorShape ([None, ]),
            ],
            back_prop=False,
        )

        return tokens
