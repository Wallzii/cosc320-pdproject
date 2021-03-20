# cosc320-pdproject
Plagiarism detection problem for COSC 320. Use and analysis of KMP, LCSS, and Rabin-Karp.

## To-Do's:
- Natural language processing for tokenization, stopward removal, stemming, etc. (nltk?)
- Figure out strategy for iterating over corpus documents against the plagiarized document.

## Known Issues:
- ~~Multiple punctuations at the end of sentences parsed by split_sentences() create empty sentences equal to the amount of punctuations after the first.~~

## Example Output (Verbose):
```
Verbose output enabled.
----------------------------------------
# of documents in Corpus: 2
Document keys in Corpus: ['test01.txt', 'test02.txt']
----------------------------------------

----------------------------------------
Filename of Document: test01.txt
# of paragraphs: 6
# of sentences: 24
----------------------------------------

Paragraphs in Document 'test01.txt':
test01.txt->paragraphs[0]: I believe that computers have a positive effect on people. They help you stay in touch with family in a couple different ways they excercise your mind and hands and help you learn and make things easier.
test01.txt->paragraphs[1]: Computer's help you keep in touch with people. Say you live in @LOCATION1 and you miss your @CAPS1. You can just send an e-mail and talk all you want. If you don't just want to limit it to words you can add pictures so they can see how much you've grown or if you are well. Even if you're just e-mailing someone down the block it is just as effective as getting up and walking over there. You can also use a computer to make a scrap book card or slide show to show how much you love the person you give them to.
test01.txt->paragraphs[2]: Computers @MONTH1 not excercise you whole body but it excersises you mind and hands. You could play solitaire on the computer and come away @PERCENT1 smarter than before. You can play other games of strategy like checkers and chess while still sitting at home being comfortable.
test01.txt->paragraphs[3]: Your hands always play a big role while you're on the computer. They need to move the mouse and press the keys on a keyboard. Your hands learn all the keys from memorization. It's like the computer's teaching handi-coordination and studying habit for the future.
test01.txt->paragraphs[4]: Computers make human lives easier. Not only do they help kids turn in a nice neatly printed piece or paper for home work but they also help the average person. Teachers use it to keep peoples grades in order and others use it to write reports for various jobs. The @CAPS2 probably uses one to write a speech or to just keep his day in order. Computers make it easier to learn certain topics like the @LOCATION2 history. You can type something into a searcher site and have ton's of websites for one person with, who knows how much imformation. Instead of flipping through all the pages in a dictionary you can look for an online dictionary, type in the word and you have the definition.
test01.txt->paragraphs[5]: Computers have positive effects on people because they help you keep close to your family, they challenge your mind to be greater and excercise your hands and they make life easier for kids and the average person. This is why, I think computers have good effects on society.
Sentences in Document 'test01.txt':
test01.txt->sentence[0]: I believe that computers have a positive effect on people
test01.txt->sentence[1]: They help you stay in touch with family in a couple different ways they excercise your mind and hands and help you learn and make things easier
test01.txt->sentence[2]: Computer's help you keep in touch with people
test01.txt->sentence[3]: Say you live in @LOCATION1 and you miss your @CAPS1
test01.txt->sentence[4]: You can just send an e-mail and talk all you want
test01.txt->sentence[5]: If you don't just want to limit it to words you can add pictures so they can see how much you've grown or if you are well
test01.txt->sentence[6]: Even if you're just e-mailing someone down the block it is just as effective as getting up and walking over there
test01.txt->sentence[7]: You can also use a computer to make a scrap book card or slide show to show how much you love the person you give them to
test01.txt->sentence[8]: Computers @MONTH1 not excercise you whole body but it excersises you mind and hands
test01.txt->sentence[9]: You could play solitaire on the computer and come away @PERCENT1 smarter than before
test01.txt->sentence[10]: You can play other games of strategy like checkers and chess while still sitting at home being comfortable
test01.txt->sentence[11]: Your hands always play a big role while you're on the computer
test01.txt->sentence[12]: They need to move the mouse and press the keys on a keyboard
test01.txt->sentence[13]: Your hands learn all the keys from memorization
test01.txt->sentence[14]: It's like the computer's teaching handi-coordination and studying habit for the future
test01.txt->sentence[15]: Computers make human lives easier
test01.txt->sentence[16]: Not only do they help kids turn in a nice neatly printed piece or paper for home work but they also help the average person
test01.txt->sentence[17]: Teachers use it to keep peoples grades in order and others use it to write reports for various jobs
test01.txt->sentence[18]: The @CAPS2 probably uses one to write a speech or to just keep his day in order
test01.txt->sentence[19]: Computers make it easier to learn certain topics like the @LOCATION2 history
test01.txt->sentence[20]: You can type something into a searcher site and have ton's of websites for one person with, who knows how much imformation
test01.txt->sentence[21]: Instead of flipping through all the pages in a dictionary you can look for an online dictionary, type in the word and you have the definition
test01.txt->sentence[22]: Computers have positive effects on people because they help you keep close to your family, they challenge your mind to be greater and excercise your hands and they make life easier for kids and the average person
test01.txt->sentence[23]: This is why, I think computers have good effects on society
```

## Example Output (Non-Verbose):
```
Corpus contains 2 document(s): ['test01.txt', 'test02.txt']
Document 'test01.txt' contains 6 paragraph(s) and 24 sentence(s).
Paragraphs in 'test01.txt': ['I believe that computers have a positive effect on people. They help you stay in touch with family in a couple different ways they excercise your mind and hands and help you learn and make things easier.', "Computer's help you keep in touch with people. Say you live in @LOCATION1 and you miss your @CAPS1. You can just send an e-mail and talk all you want. If you don't just want to limit it to words you can add pictures so they can see how much you've grown or if you are well. Even if you're just e-mailing someone down the block it is just as effective as getting up and walking over there. You can also use a computer to make a scrap book card or slide show to show how much you love the person you give them to.", 'Computers @MONTH1 not excercise you whole body but it excersises you mind and hands. You could play solitaire on the computer and come away @PERCENT1 smarter than before. You can play other games of strategy like checkers and chess while still sitting at home being comfortable.', "Your hands always play a big role while you're on the computer. They need to move the mouse and press the keys on a keyboard. Your hands learn all the keys from memorization. It's like the computer's teaching handi-coordination and studying habit for the future.", "Computers make human lives easier. Not only do they help kids turn in a nice neatly printed piece or paper for home work but they also help the average person. Teachers use it to keep peoples grades in order and others use it to write reports for various jobs. The @CAPS2 probably uses one to write a speech or to just keep his day in order. Computers make it easier to learn certain topics like the @LOCATION2 history. You can type something into a searcher site and have ton's of websites for one person with, who knows how much imformation. Instead of flipping through all the pages in a dictionary you can look for an online dictionary, type in the word and you have the definition.", 'Computers have positive effects on people because they help you keep close to your family, they challenge your mind to be greater and excercise your hands and they make life easier for kids and the average person. This is why, I think computers have good effects on society.']
Sentences in 'test01.txt': ['I believe that computers have a positive effect on people', 'They help you stay in touch with family in a couple different ways they excercise your mind and hands and help you learn and make things easier', "Computer's help you keep in touch with people", 'Say you live in @LOCATION1 and you miss your @CAPS1', 'You can just send an e-mail and talk all you want', "If you don't just want to limit it to words you can add pictures so they can see how much you've grown or if you are well", "Even if you're just e-mailing someone down the block it is just as effective as getting up and walking over there", 'You can also use a computer to make a scrap book card or slide show to show how much you love the person you give them to', 'Computers @MONTH1 not excercise you whole body but it excersises you mind and hands', 'You could play solitaire on the computer and come away @PERCENT1 smarter than before', 'You can play other games of strategy like checkers and chess while still sitting at home being comfortable', "Your hands always play a big role while you're on the computer", 'They need to move the mouse and press the keys on a keyboard', 'Your hands learn all the keys from memorization', "It's like the computer's teaching handi-coordination and studying habit for the future", 'Computers make human lives easier', 'Not only do they help kids turn in a nice neatly printed piece or paper for home work but they also help the average person', 'Teachers use it to keep peoples grades in order and others use it to write reports for various jobs', 'The @CAPS2 probably uses one to write a speech or to just keep his day in order', 'Computers make it easier to learn certain topics like the @LOCATION2 history', "You can type something into a searcher site and have ton's of websites for one person with, who knows how much imformation", 'Instead of flipping through all the pages in a dictionary you can look for an online dictionary, type in the word and you have the definition', 'Computers have positive effects on people because they help you keep close to your family, they challenge your mind to be greater and excercise your hands and they make life easier for kids and the average person', 'This is why, I think computers have good effects on society']
```
