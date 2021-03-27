import time
from random import choice
from string import ascii_uppercase


# tryItABunch: runs a function a bunch, and times how long it takes.
#
# Input: myFn: a function which takes as input a list of integers
# Output: lists nValues and tValues so that running myFn on a list of length nValues[i] took (on average over numTrials tests) time tValues[i] milliseconds.
#
# Other optional args:
#    - startN: smallest n to test
#    - endN: largest n to test
#    - stepSize: test n's in increments of stepSize between startN and endN
#    - numTrials: for each n tests, do numTrials tests and average them
#    - listMax: the input lists of length n will have values drawn uniformly at random from range(listMax)
def tryItABunch(myFn, startN=10, endN=100, stepSize=10, numTrials=20, listMax = 10):
    nValues = []
    tValues = []
    for n in range(startN, endN, stepSize):
        if n % 250 == 0:
            print("{name}(), m < n: {n}...".format(name=myFn.__name__,n=n))
        # run myFn several times and average to get a decent idea.
        runtime = 0
        for t in range(numTrials):
            lst = [ choice(range(listMax)) for i in range(n) ] # generate a random list of length n
            start = time.time()
            myFn( lst )
            end = time.time()
            runtime += (end - start) * 1000 # measure in milliseconds
        runtime = runtime/numTrials
        nValues.append(n)
        tValues.append(runtime)
    return nValues, tValues


# Analysis specific to KMPSearch (standard n > m):
def tryItABunchKMP(myFn, startN=10, endN=100, stepSize=10, numTrials=20, patternLength = 10):
    nValues = []
    tValues = []
    for n in range(startN, endN, stepSize):
        if n % 1000 == 0:
            print("{name}(), m < n: {n}...".format(name=myFn.__name__,n=n))
        # run myFn several times and average to get a decent idea.
        runtime = 0
        for t in range(numTrials):
            pattern = ''.join(choice(ascii_uppercase) for i in range(patternLength)) # generate a random string of length patternLength
            # print(pattern)
            string = ''.join(choice(ascii_uppercase) for i in range(n)) # generate a random string of length n
            # print(string)
            start = time.time()
            myFn( pattern, string )
            end = time.time()
            runtime += (end - start) * 1000 # measure in milliseconds
        runtime = runtime/numTrials
        nValues.append(n)
        tValues.append(runtime)
    print("Analysis of {name}(), where m < n, finished!".format(name=myFn.__name__))
    return nValues, tValues


# Analysis specific to KMPSearch (n = m variant):
def tryItABunchKMPEqual(myFn, startN=10, endN=100, stepSize=10, numTrials=20):
    nValues = []
    tValues = []
    for n in range(startN, endN, stepSize):
        if n % 1000 == 0:
            print("{name}(), m = n: {n}...".format(name=myFn.__name__,n=n))
        # run myFn several times and average to get a decent idea.
        runtime = 0
        for t in range(numTrials):
            pattern = ''.join(choice(ascii_uppercase) for i in range(n)) # generate a random string of length listMax
            string = ''.join(choice(ascii_uppercase) for i in range(n)) # generate a random string of length list2Max
            start = time.time()
            myFn( pattern, string )
            end = time.time()
            runtime += (end - start) * 1000 # measure in milliseconds
        runtime = runtime/numTrials
        nValues.append(n)
        tValues.append(runtime)
    print("Analysis of {name}(), where m = n, finished!".format(name=myFn.__name__))
    return nValues, tValues


# Analysis specific to KMPSearch (n < m variant):
def tryItABunchKMPLargePat(myFn, startN=10, endN=100, stepSize=10, numTrials=20, stringLength = 500):
    nValues = []
    tValues = []
    for n in range(startN, endN, stepSize):
        if n % 1000 == 0:
            print("{name}(), m > n: {n}...".format(name=myFn.__name__,n=n))
        # run myFn several times and average to get a decent idea.
        runtime = 0
        for t in range(numTrials):
            pattern = ''.join(choice(ascii_uppercase) for i in range(n)) # generate a random string of length listMax
            string = ''.join(choice(ascii_uppercase) for i in range(stringLength)) # generate a random string of length list2Max
            start = time.time()
            myFn( pattern, string )
            end = time.time()
            runtime += (end - start) * 1000 # measure in milliseconds
        runtime = runtime/numTrials
        nValues.append(n)
        tValues.append(runtime)
    print("Analysis of {name}(), where m > n, finished!".format(name=myFn.__name__))
    return nValues, tValues


# Analysis specific to KMPSearch, but using the corpus document wrapper function:
def tryItABunchKMPWrapper(myFn, startN=10, endN=100, stepSize=10, numTrials=20, amtPatternsSmaller = False, amtPatternsLarger = False):
    nValues = []
    tValues = []
    for n in range(startN, endN, stepSize):
        if n % 50 == 0:
            print("{name}(), m < n: {n}...".format(name=myFn.__name__,n=n))
        # run myFn several times and average to get a decent idea.
        runtime = 0
        for t in range(numTrials):
            pattern = ''.join(choice(ascii_uppercase) for i in range(n)) # generate a random string of length n
            string = ''.join(choice(ascii_uppercase) for i in range(n)) # generate a random string of length n
            if amtPatternsSmaller is True:
                amt_patters = (int)(n / 2)
            elif amtPatternsLarger is True:
                amt_patters = (int)(n * 2)
            else:
                amt_patters = n
            amt_corpus_docs = n
            start = time.time()
            myFn(amt_patters, amt_corpus_docs, pattern, string)
            end = time.time()
            runtime += (end - start) * 1000 # measure in milliseconds
        runtime = runtime/numTrials
        nValues.append(n)
        tValues.append(runtime)
    print("Analysis of {name}(), where z = {z} and w = {w}, finished!".format(name=myFn.__name__), z=amt_corpus_docs, w=amt_patters)
    return nValues, tValues