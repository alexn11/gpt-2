# Explanations

Access the infinity of pausible texts using GPT2. Query any text (up to some fixed number of tokens) using a unique address.

This fork of GPT2 has been converted into a toy WebApp based on the publicly released version of GPT2 kernel. In the [Library of Babel](https://libraryofbabel.info/) one can search in any page that could ever be writen. Their system is able to generate such page using a unique identifier that can be assimilated as an address. On the other side language models arising from NLP techniques can be used to generate random texts with correct grammar. Such models often decompose texts into tokens which correspond essentially to words rather than letters. This is the case for example for the GPT2 system.

In order to generate some text a seed is first given as an input to the system. Then the system compute for each token an estimate probability that they should appear as the next token in the text. Each token can be ranked according to its estimated probability. Given a sequence of integers which correspond to an address of page, the modified sample generator pick each token whose rank is given by the corresponding integer in the address sequence. The consequence is that lower indexes in an addresse correspond to more probable text. This makes it easier to access to meaningfull texts, up to the limits of the model.

The implementation consists mainly in modifying the way token are sampled in _samplegen.py_. Also a web back end has been incorporated in order to make the address selection easier (as well as setting the seed). The web back end relies on Python HTTP toy server. This of course cannot be used beyond the scope of play-testing. Another limitation of this application is the fact that the text generated depends strongly on the seed used. In particular this makes it difficult to access any text other than which is likely to follow the seed given.

# Use

Launch in the _http_ directory
```
python -m http.server 8000 --bind 127.0.0.1 --cgi
```
and open 127.0.0.1 in a web browser.

The name of the library is the seed feed into the generator. The address can be any text, sequence of characters (it is automatically filtred in order to fit a specific format). Another possiblity is to choose to generate an address randomly. Then click _generate_. This should launch _samplegen.py_ with the appropriate parameters on your local machine. Once the text of the page has been generated, it is returned by the server to the browser.


