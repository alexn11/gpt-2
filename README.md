# Explanations

Access the infinity of pausible texts using GPT2. Query any text (up to some fixed number of tokens) using a unique address.

This fork of GPT2 has been converted into a toy web app. In the [Library of Babel](https://libraryofbabel.info/) one can search in any page that could ever be written. This system is able to generate these pages using a unique identifier which is an address of a unique page. Most of these pages consists of meaningless sequences of alphabetical characters separated by spaces and periods.

On the other hand language models arising from NLP techniques can be used to generate random texts with mostly correct grammar. Such models often decompose texts into tokens which correspond essentially to words rather than letters. This is the case for example for the GPT2 system.

In order to generate some text a seed is first given as an input to the system. Then the system compute for each token an estimate of the probability that they appear as the following token. Each token can be ranked according to its estimated probability.

Here an address is some sequence of integers of fixed length. Given such a sequence of integers the modified sample generator picks each token whose rank is given by the corresponding integer in the address sequence. The consequence is that lower indexes in an address correspond to more probable text. This makes it easier to access to meaningfull texts (up to the limits of the model).

The implementation consists mainly in modifying the way tokens are sampled in _samplegen.py_.

Also a web back end has been incorporated in order to make the address selection easier (as well as setting the seed). The back end relies on Python's HTTP server. This should not be used beyond the scope of play-testing.

Another limitation of this application is the fact that the text generated depends strongly on the seed used. In particular this makes it difficult to access any text other than one which is more likely to follow the seed.

# Use

Make sure that you can run the sample generator from the original GPT2 project.

In the _http_ directory, launch
```
python -m http.server 8000 --bind 127.0.0.1 --cgi
```
and open the address _127.0.0.1_ in a web browser.

The name of the library is the seed which is fed into the generator.

The address can be any text or sequence of characters. It is automatically filtred in order to fit to a specific format. Another possiblity is to choose to generate an address randomly.

After clicking _generate_, this should launch _samplegen.py_ with the appropriate parameters. Once the text of the page has been generated, it is returned by the server to the browser.


