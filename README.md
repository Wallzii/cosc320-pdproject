# cosc320-pdproject
Plagiarism detection problem for COSC 320. Use and analysis of KMP, LCSS, and Rabin-Karp.

## To-Do's:
- Natural language processing for tokenization, stopward removal, stemming, etc. (nltk?)
- ~~Figure out strategy for iterating over corpus documents against the plagiarized document.~~
- ~~Find graphing package to track algorithm runtime.~~

## Known Issues:
- ~~Multiple punctuations at the end of sentences parsed by split_sentences() create empty sentences equal to the amount of punctuations after the first.~~

## Example Output (limited dataset, non-verbose mode):
```
Scanning for potentially plagiarized document...
Valid document found: 'plag.txt'
Document 'plag.txt' contains 7 paragraph(s) and 26 sentence(s), and has an overall length of 2394 characters.

Scanning for documents to add to corpus...
Valid set of documents created.

Compiling corpus from set of documents...
A valid corpus has been created.
Corpus contains 4 document(s): ['test01.txt', 'test02.txt', 'test03.txt', 'test04.txt']
KMPSearch() starting...
---> Potentially plagiarized input: 'plag.txt'
---> Corpus document: 'test01.txt' (document 0 of 4)

KMPSearch() starting...
---> Potentially plagiarized input: 'plag.txt'
---> Corpus document: 'test02.txt' (document 1 of 4)

KMPSearch() starting...
---> Potentially plagiarized input: 'plag.txt'
---> Corpus document: 'test03.txt' (document 2 of 4)

KMPSearch() starting...
---> Potentially plagiarized input: 'plag.txt'
---> Corpus document: 'test04.txt' (document 3 of 4)


Plagiarism detection on document 'plag.txt' against ['test01.txt', 'test02.txt', 'test03.txt', 'test04.txt'] was successfully completed.

---> Total documents checked: 	4

---> Highest hit rate: 			97.75%
---> Associated document: 		test01.txt

---> Lowest hit rate: 			4.98%
---> Associated document: 		test03.txt

All results:
	test01.txt: 97.75%
	test03.txt: 4.98%
	test04.txt: 23.71%

Files without hits have been excluded in the results above.
```

## Example Output (limited dataset, verbose mode):
```
Verbose output enabled.
Scanning for potentially plagiarized document...
Valid document found: 'plag.txt'
Document 'plag.txt' contains 7 paragraph(s) and 26 sentence(s), and has an overall length of 2394 characters.

Scanning for documents to add to corpus...
Valid set of documents created.

Compiling corpus from set of documents...
A valid corpus has been created.
Corpus contains 4 document(s): ['test01.txt', 'test02.txt', 'test03.txt', 'test04.txt']

KMPSearch() starting...
---> Potentially plagiarized input: 'plag.txt'
---> Corpus document: 'test01.txt' (document 0 of 4)

Pattern occurs in string at index 0.
Pattern was found in string 1 time(s).
There is a 2.57% hit rate of the pattern in string.
Pattern occurs in string at index 59.
Pattern was found in string 1 time(s).
There is a 6.44% hit rate of the pattern in string.
Pattern occurs in string at index 207.
Pattern was found in string 1 time(s).
There is a 2.03% hit rate of the pattern in string.
Pattern occurs in string at index 254.
Pattern was found in string 1 time(s).
There is a 2.30% hit rate of the pattern in string.
Pattern occurs in string at index 307.
Pattern was found in string 1 time(s).
There is a 2.21% hit rate of the pattern in string.
Pattern occurs in string at index 358.
Pattern was found in string 1 time(s).
There is a 5.45% hit rate of the pattern in string.
Pattern occurs in string at index 481.
Pattern was found in string 1 time(s).
There is a 5.09% hit rate of the pattern in string.
Pattern occurs in string at index 596.
Pattern was found in string 1 time(s).
There is a 5.45% hit rate of the pattern in string.
Pattern occurs in string at index 719.
Pattern was found in string 1 time(s).
There is a 3.74% hit rate of the pattern in string.
Pattern occurs in string at index 804.
Pattern was found in string 1 time(s).
There is a 3.78% hit rate of the pattern in string.
Pattern occurs in string at index 890.
Pattern was found in string 1 time(s).
There is a 4.77% hit rate of the pattern in string.
Pattern occurs in string at index 998.
Pattern was found in string 1 time(s).
There is a 2.79% hit rate of the pattern in string.
Pattern occurs in string at index 1062.
Pattern was found in string 1 time(s).
There is a 2.70% hit rate of the pattern in string.
Pattern occurs in string at index 1124.
Pattern was found in string 1 time(s).
There is a 2.12% hit rate of the pattern in string.
Pattern occurs in string at index 1173.
Pattern was found in string 1 time(s).
There is a 3.87% hit rate of the pattern in string.
Pattern occurs in string at index 1261.
Pattern was found in string 1 time(s).
There is a 1.49% hit rate of the pattern in string.
Pattern occurs in string at index 1296.
Pattern was found in string 1 time(s).
There is a 5.54% hit rate of the pattern in string.
Pattern occurs in string at index 1421.
Pattern was found in string 1 time(s).
There is a 4.46% hit rate of the pattern in string.
Pattern occurs in string at index 1522.
Pattern was found in string 1 time(s).
There is a 3.56% hit rate of the pattern in string.
Pattern occurs in string at index 1603.
Pattern was found in string 1 time(s).
There is a 3.42% hit rate of the pattern in string.
Pattern occurs in string at index 1681.
Pattern was found in string 1 time(s).
There is a 5.49% hit rate of the pattern in string.
Pattern occurs in string at index 1805.
Pattern was found in string 1 time(s).
There is a 6.35% hit rate of the pattern in string.
Pattern occurs in string at index 1948.
Pattern was found in string 1 time(s).
There is a 9.54% hit rate of the pattern in string.
Pattern occurs in string at index 2162.
Pattern was found in string 1 time(s).
There is a 2.66% hit rate of the pattern in string.

------------------------------------------------------------
Total plagiarism hit rate of 'plag.txt' in 'test01.txt': 97.75%
This document has an extremely high plagiarism threshhold and has been flagged for review.
------------------------------------------------------------

KMPSearch() starting...
---> Potentially plagiarized input: 'plag.txt'
---> Corpus document: 'test02.txt' (document 1 of 4)

No pattern matches found.

------------------------------------------------------------
Total plagiarism hit rate of 'plag.txt' in 'test02.txt': 0.00%
This document is not plagiarized.
------------------------------------------------------------

KMPSearch() starting...
---> Potentially plagiarized input: 'plag.txt'
---> Corpus document: 'test03.txt' (document 2 of 4)

Pattern occurs in string at index 862.
Pattern was found in string 1 time(s).
There is a 1.74% hit rate of the pattern in string.
Pattern occurs in string at index 909.
Pattern was found in string 1 time(s).
There is a 1.97% hit rate of the pattern in string.
Pattern occurs in string at index 1462.
Pattern was found in string 1 time(s).
There is a 1.27% hit rate of the pattern in string.

------------------------------------------------------------
Total plagiarism hit rate of 'plag.txt' in 'test03.txt': 4.98%
It is unlikely that this document is plagiarized.
------------------------------------------------------------

KMPSearch() starting...
---> Potentially plagiarized input: 'plag.txt'
---> Corpus document: 'test04.txt' (document 3 of 4)

Pattern occurs in string at index 862.
Pattern was found in string 1 time(s).
There is a 1.39% hit rate of the pattern in string.
Pattern occurs in string at index 909.
Pattern was found in string 1 time(s).
There is a 1.57% hit rate of the pattern in string.
Pattern occurs in string at index 1462.
Pattern was found in string 1 time(s).
There is a 1.02% hit rate of the pattern in string.
Pattern occurs in string at index 1497.
Pattern was found in string 1 time(s).
There is a 3.79% hit rate of the pattern in string.
Pattern occurs in string at index 1622.
Pattern was found in string 1 time(s).
There is a 3.05% hit rate of the pattern in string.
Pattern occurs in string at index 1723.
Pattern was found in string 1 time(s).
There is a 2.44% hit rate of the pattern in string.
Pattern occurs in string at index 1804.
Pattern was found in string 1 time(s).
There is a 2.34% hit rate of the pattern in string.
Pattern occurs in string at index 1882.
Pattern was found in string 1 time(s).
There is a 3.76% hit rate of the pattern in string.
Pattern occurs in string at index 2006.
Pattern was found in string 1 time(s).
There is a 4.35% hit rate of the pattern in string.

------------------------------------------------------------
Total plagiarism hit rate of 'plag.txt' in 'test04.txt': 23.71%
This document has an extremely high plagiarism threshhold and has been flagged for review.
------------------------------------------------------------

Plagiarism detection on document 'plag.txt' against ['test01.txt', 'test02.txt', 'test03.txt', 'test04.txt'] was successfully completed.

---> Total documents checked: 	4

---> Highest hit rate: 			97.75%
---> Associated document: 		test01.txt

---> Lowest hit rate: 			4.98%
---> Associated document: 		test03.txt

All results:
	test01.txt: 97.75%
	test03.txt: 4.98%
	test04.txt: 23.71%

Files without hits have been excluded in the results above.
```
