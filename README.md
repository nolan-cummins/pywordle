# PyWordle!
This [Firefox]([url](https://addons.mozilla.org/en-US/firefox/addon/pywordle/))/Chrome addon connects to a PythonAnywhere service that parses through the HTML of Wordle/Wordler to extract your current game state, calculate the best words to guess, and displays the first 5, from most to least likely. 
*Note: I have only tested this in Firefox, but it SHOULD work in chrome, according to ChatGPT...*

# How does it work?
According to the New York Times, their editors select words daily from the [Oxford English Dictionary]([url](https://www.oed.com/)). Unfortunately, the OED, with over 600,000 words, is behind a paywall, locked only for researchers with license access. To get around this, I generated a list of 2,250,601 possible combinations of 5 letters based on the phonetic and written limitations of English. After cross-referencing with the OED website using an automated Python script, we found 39,513 valid words. Many of these words, however, are archaic, obsolete, and/or outdated. To adjust for this, I used the 2012 Google Ngram dataset, which describes the frequency between the years 1500 and 2012 every word in the Google Books library appears, to calculate a # instances per million words for every valid word. For example, the word "words" appears, on average, 466.08 times for every million English words.

The Wordle rules are simple:
- "absent" letters will never appear
- "present" letters are present, but in the wrong location
- "correct" letters are...correct

Using this as a filter, we can easily determine every possible word for a given game state, and after sorting by the frequency, we can get what word the Editors, who chose the words, most likely selected.
