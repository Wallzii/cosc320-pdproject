import configparser

import numpy as np
import matplotlib.pyplot as plt

import kmp
import lcss
import rabinkarp
from tryItABunch import tryItABunch, tryItABunchKMP, tryItABunchKMPEqual, tryItABunchKMPLargePat, tryItABunchKMPWrapper, \
                        tryItABunchLCSS, tryItABunchLCSSEqual, tryItABunchLCSSLargePat, tryItABunchLCSSWrapper, tryItABunchRabinKarpEqual


config = configparser.ConfigParser()
config.read('config.ini')
ANALYSIS_KMP = config.getboolean('ANALYSIS', 'RuntimeAnalysis_KMP')
ANALYSIS_KMP_WRAPPER = config.getboolean('ANALYSIS', 'RuntimeAnalysis_KMP_Wrapper')
ANALYSIS_LCSS = config.getboolean('ANALYSIS', 'RuntimeAnalysis_LCSS')
ANALYSIS_LCSS_WRAPPER = config.getboolean('ANALYSIS', 'RuntimeAnalysis_LCSS_Wrapper')
ANALYSIS_RABIN_KARP = config.getboolean('ANALYSIS', 'RuntimeAnalysis_RabinKarp')
ANALYSIS_RABIN_KARP_WRAPPER = config.getboolean('ANALYSIS', 'RuntimeAnalysis_RabinKarp_Wrapper')
ANALYSIS_ALL = config.getboolean('ANALYSIS', 'RuntimeAnalysis_All')
ANALYSIS_ALL_WRAPPER = config.getboolean('ANALYSIS', 'RuntimeAnalysis_All_Wrapper')


def KMP_wrapper_analysis(amt_patterns:int, amt_corpus_docs:int, pattern: str, string: str):
    for i in range(amt_corpus_docs):
        # print("i = {i}".format(i=i))
        for j in range(amt_patterns):
            # print("j = {j}".format(j=j))
            kmp.KMPSearch(pattern, string)


def LCSS_wrapper_analysis(amt_patterns:int, amt_corpus_docs:int, pattern: str, string: str):
    for i in range(amt_corpus_docs):
        # print("i = {i}".format(i=i))
        for j in range(amt_patterns):
            # print("j = {j}".format(j=j))
            lcss.LCSS(string, pattern)


def rabinkarp_wrapper_analysis(amt_patterns:int, amt_corpus_docs:int, pattern: str, string: str):
    for i in range(amt_corpus_docs):
        # print("i = {i}".format(i=i))
        for j in range(amt_patterns):
            # print("j = {j}".format(j=j))
            rabinkarp.RabinKarp(pattern, string)


def square_n(n:list):
    for i in range(len(n)):
        for i in range(len(n)):
            True


if __name__ == '__main__':
    if not ANALYSIS_KMP and not ANALYSIS_KMP_WRAPPER and not ANALYSIS_LCSS and not ANALYSIS_LCSS_WRAPPER and not ANALYSIS_RABIN_KARP and not ANALYSIS_RABIN_KARP_WRAPPER:
        print("No algorithm analyses are enabled. Please enable at least one analysis option in 'config.ini' under the [ANALYSIS] header.")

    # Runtime analysis of KMP (set RuntimeAnalysis_KMP to True in 'config.ini'):
    if ANALYSIS_KMP:
        # Plot basic n^2 function:
        # nValues, tValues = tryItABunch(square_n, startN=10, endN=1000, stepSize=10, numTrials=20, listMax = 10)
        # plt.plot(nValues, tValues, color="blue", label="n^2") 

        # Plot KMPSearch(): m = n:
        nValuesEqual, tValuesEqual = tryItABunchKMPEqual( kmp.KMPSearch, startN = 50, endN = 20000, stepSize=50, numTrials=10)
        plt.plot(nValuesEqual, tValuesEqual, color="blue", label="KMPSearch() m = n")

        # Plot KMPSearch(): m < n:
        # nValues, tValues = tryItABunchKMP( kmp.KMPSearch, startN = 50, endN = 20000, stepSize=50, numTrials=10, patternLength = 20)
        # plt.plot(nValues, tValues, color="red", label="KMPSearch() m < n")

        # # Plot KMPSearch(): m > n:
        # nValuesLargePat, tValuesLargePat = tryItABunchKMPLargePat( kmp.KMPSearch, startN = 50, endN = 20000, stepSize=50, numTrials=10, stringLength = 20)
        # plt.plot(nValuesLargePat, tValuesLargePat, color="green", label="KMPSearch() m > n")

        plt.xlabel("Length of string, n", fontsize=28)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.ylabel("Time(ms)", fontsize=28)
        plt.legend(fontsize=22)
        plt.title("KMPSearch Runtimes", fontsize=30)
        plt.show()


    if ANALYSIS_KMP_WRAPPER:
        # Plot KMP_wrapper(): w = z
        nValuesWrap, tValuesWrap = tryItABunchKMPWrapper( KMP_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1)
        plt.plot(nValuesWrap, tValuesWrap, color="red", label="KMP_wrapper(KMPSearch()) w = z; n = z, m = z")
        
        # Plot KMP_wrapper(): w < z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchKMPWrapper( KMP_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1, amtPatternsSmaller = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="yellow", label="KMP_wrapper(KMPSearch()) w < z, w = (z / 2); n = z, m = z")
        
        # Plot KMP_wrapper(): w > z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchKMPWrapper( KMP_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1, amtPatternsLarger = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="green", label="KMP_wrapper(KMPSearch()) w > z, w = (z * 2); n = z, m = z")

        plt.xlabel("Length of set S[], z", fontsize=28)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.ylabel("Time(ms)", fontsize=28)
        plt.legend(fontsize=22)
        plt.title("KMPSearch Runtimes within Wrapper Function", fontsize=30)
        plt.show()


    # Runtime analysis of LCSS (set RuntimeAnalysis_LCSS to True in 'config.ini'):
    if ANALYSIS_LCSS:
        # Plot basic n^2 function:
        # nValues, tValues = tryItABunch(square_n, startN=10, endN=1000, stepSize=10, numTrials=20, listMax = 10)
        # plt.plot(nValues, tValues, color="blue", label="n^2") 

        # Plot LCSS(): m = n:
        nValuesEqual, tValuesEqual = tryItABunchLCSSEqual( lcss.LCSS, startN = 50, endN = 2000, stepSize=50, numTrials=10)
        plt.plot(nValuesEqual, tValuesEqual, color="blue", label="LCSS() m = n")

        # Plot LCSS(): m < n:
        # nValues, tValues = tryItABunchLCSS( lcss.LCSS, startN = 50, endN = 10000, stepSize=50, numTrials=10, patternLength = 20)
        # plt.plot(nValues, tValues, color="red", label="LCSS() m < n")

        # # Plot LCSS(): m > n:
        # nValuesLargePat, tValuesLargePat = tryItABunchLCSSLargePat( lcss.LCSS, startN = 50, endN = 10000, stepSize=50, numTrials=10, stringLength = 20)
        # plt.plot(nValuesLargePat, tValuesLargePat, color="green", label="LCSS() m > n")

        plt.xlabel("Length of string, n", fontsize=28)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.ylabel("Time(ms)", fontsize=28)
        plt.legend(fontsize=22)
        plt.title("LCSS Runtimes", fontsize=30)
        plt.show()


    if ANALYSIS_LCSS_WRAPPER:
        # Plot LCSS_wrapper(): w = z
        nValuesWrap, tValuesWrap = tryItABunchLCSSWrapper( LCSS_wrapper_analysis, startN = 50, endN = 500, stepSize=50, numTrials=1)
        plt.plot(nValuesWrap, tValuesWrap, color="red", label="LCSS_wrapper(LCSS()) w = z; n = z, m = z")
        
        # Plot LCSS_wrapper(): w < z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchLCSSWrapper( LCSS_wrapper_analysis, startN = 50, endN = 250, stepSize=50, numTrials=1, amtPatternsSmaller = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="yellow", label="LCSS_wrapper(LCSS()) w < z, w = (z / 2); n = z, m = (z / 2)")
        
        # Plot LCSS_wrapper(): w > z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchLCSSWrapper( LCSS_wrapper_analysis, startN = 50, endN = 250, stepSize=50, numTrials=1, amtPatternsLarger = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="green", label="LCSS_wrapper(LCSS()) w > z, w = (z * 2); n = z, m = (z * 2)")

        plt.xlabel("Length of set S[], z", fontsize=28)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.ylabel("Time(ms)", fontsize=28)
        plt.legend(fontsize=22)
        plt.title("LCSS Runtimes within Wrapper Function", fontsize=30)
        plt.show()


    # Runtime analysis of RabinKarp (set RuntimeAnalysis_RabinKarp to True in 'config.ini'):
    if ANALYSIS_RABIN_KARP:
        # Plot basic n^2 function:
        # nValues, tValues = tryItABunch(square_n, startN=10, endN=1000, stepSize=10, numTrials=20, listMax = 10)
        # plt.plot(nValues, tValues, color="blue", label="n^2")

        # Plot RabinKarp(): m = n:
        nValuesEqual, tValuesEqual = tryItABunchKMPEqual( rabinkarp.RabinKarp, startN = 50, endN = 20000, stepSize=50, numTrials=10)
        # nValuesEqual2, tValuesEqual2 = tryItABunchRabinKarpEqual( rabinkarp.RabinKarp, startN = 50, endN = 10000, stepSize=50, numTrials=10)
        plt.plot(nValuesEqual, tValuesEqual, color="blue", label="RabinKarp() m = n")
        # plt.plot(nValuesEqual2, tValuesEqual2, color="darkblue", label="RabinKarp() m = n")

        # Plot RabinKarp(): m < n:
        # nValues, tValues = tryItABunchKMP( rabinkarp.RabinKarp, startN = 50, endN = 20000, stepSize=50, numTrials=10, patternLength = 20)
        # plt.plot(nValues, tValues, color="red", label="RabinKarp() m < n")

        # # Plot RabinKarp(): m > n: *** THIS IS AN INVALID TEST AS m MUST BE <= n ***
        # nValuesLargePat, tValuesLargePat = tryItABunchKMPLargePat( rabinkarp.RabinKarp, startN = 50, endN = 20000, stepSize=50, numTrials=10, stringLength = 20)
        # plt.plot(nValuesLargePat, tValuesLargePat, color="green", label="RabinKarp() m > n")

        plt.xlabel("Length of string, n", fontsize=28)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.ylabel("Time(ms)", fontsize=28)
        plt.legend(fontsize=22)
        plt.title("RabinKarp Runtimes", fontsize=30)
        plt.show()


    if ANALYSIS_RABIN_KARP_WRAPPER:
        # Plot KMP_wrapper(): w = z
        nValuesWrap, tValuesWrap = tryItABunchKMPWrapper( rabinkarp_wrapper_analysis, startN = 50, endN = 2000, stepSize=50, numTrials=1)
        plt.plot(nValuesWrap, tValuesWrap, color="red", label="rabinkarp_wrapper(RabinKarp()) w = z; n = z, m = z")
        
        # Plot KMP_wrapper(): w < z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchKMPWrapper( rabinkarp_wrapper_analysis, startN = 50, endN = 2000, stepSize=50, numTrials=1, amtPatternsSmaller = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="yellow", label="rabinkarp_wrapper(RabinKarp()) w < z, w = (z / 2); n = z, m = z")
        
        # Plot KMP_wrapper(): w > z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchKMPWrapper( rabinkarp_wrapper_analysis, startN = 50, endN = 2000, stepSize=50, numTrials=1, amtPatternsLarger = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="green", label="rabinkarp_wrapper(RabinKarp()) w > z, w = (z * 2); n = z, m = z")

        plt.xlabel("Length of set S[], z", fontsize=28)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.ylabel("Time(ms)", fontsize=28)
        plt.legend(fontsize=22)
        plt.title("RabinKarp Runtimes within Wrapper Function", fontsize=30)
        plt.show()


    if ANALYSIS_ALL:
        '''
        KMP ANALYSIS
        '''
        # Plot KMPSearch(): m = n:
        nValuesEqual, tValuesEqual = tryItABunchKMPEqual( kmp.KMPSearch, startN = 50, endN = 20000, stepSize=50, numTrials=10)
        plt.plot(nValuesEqual, tValuesEqual, color="red", label="KMPSearch() m = n")
        # Plot KMPSearch(): m < n:
        # nValues, tValues = tryItABunchKMP( kmp.KMPSearch, startN = 50, endN = 20000, stepSize=50, numTrials=10, patternLength = 20)
        # plt.plot(nValues, tValues, color="red", label="KMPSearch() m < n")
        # # Plot KMPSearch(): m > n:
        # nValuesLargePat, tValuesLargePat = tryItABunchKMPLargePat( kmp.KMPSearch, startN = 50, endN = 20000, stepSize=50, numTrials=10, stringLength = 20)
        # plt.plot(nValuesLargePat, tValuesLargePat, color="red", label="KMPSearch() m > n")

        '''
        LCSS ANALYSIS
        '''
        # Plot LCSS(): m = n:
        # nValuesEqual, tValuesEqual = tryItABunchLCSSEqual( lcss.LCSS, startN = 50, endN = 2000, stepSize=50, numTrials=10)
        # plt.plot(nValuesEqual, tValuesEqual, color="green", label="LCSS() m = n")
        # Plot LCSS(): m < n:
        # nValues, tValues = tryItABunchLCSS( lcss.LCSS, startN = 50, endN = 2000, stepSize=50, numTrials=10, patternLength = 20)
        # plt.plot(nValues, tValues, color="green", label="LCSS() m < n")
        # # Plot LCSS(): m > n:
        # nValuesLargePat, tValuesLargePat = tryItABunchLCSSLargePat( lcss.LCSS, startN = 50, endN = 2000, stepSize=50, numTrials=10, stringLength = 20)
        # plt.plot(nValuesLargePat, tValuesLargePat, color="green", label="LCSS() m > n")

        '''
        RABIN-KARP ANALYSIS
        '''
        # Plot RabinKarp(): m = n:
        nValuesEqual, tValuesEqual = tryItABunchKMPEqual( rabinkarp.RabinKarp, startN = 50, endN = 20000, stepSize=50, numTrials=10)
        # nValuesEqual, tValuesEqual = tryItABunchRabinKarpEqual( rabinkarp.RabinKarp, startN = 50, endN = 10000, stepSize=50, numTrials=10)
        plt.plot(nValuesEqual, tValuesEqual, color="blue", label="RabinKarp() m = n")
        # Plot RabinKarp(): m < n:
        # nValues, tValues = tryItABunchKMP( rabinkarp.RabinKarp, startN = 50, endN = 20000, stepSize=50, numTrials=10, patternLength = 20)
        # plt.plot(nValues, tValues, color="blue", label="RabinKarp() m < n")
        # # Plot RabinKarp(): m > n:
        # nValuesLargePat, tValuesLargePat = tryItABunchKMPLargePat( rabinkarp.RabinKarp, startN = 50, endN = 20000, stepSize=50, numTrials=10, stringLength = 20)
        # plt.plot(nValuesLargePat, tValuesLargePat, color="blue", label="RabinKarp() m > n")

        plt.xlabel("Length of string, n", fontsize=28)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.ylabel("Time(ms)", fontsize=28)
        plt.legend(fontsize=22)
        plt.title("Algorithm Runtimes", fontsize=30)
        plt.show()


    if ANALYSIS_ALL_WRAPPER:
        '''
        KMP WRAPPER ANALYSIS
        '''
        # Plot KMP_wrapper(): w = z
        nValuesWrap, tValuesWrap = tryItABunchKMPWrapper( KMP_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1)
        plt.plot(nValuesWrap, tValuesWrap, color="red", label="KMP_wrapper(KMPSearch()) w = z; n = z, m = z")
        # Plot KMP_wrapper(): w < z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchKMPWrapper( KMP_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1, amtPatternsSmaller = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="red", label="KMP_wrapper(KMPSearch()) w < z, w = (z / 2); n = z, m = z")
        # Plot KMP_wrapper(): w > z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchKMPWrapper( KMP_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1, amtPatternsLarger = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="red", label="KMP_wrapper(KMPSearch()) w > z, w = (z * 2); n = z, m = z")


        '''
        LCSS WRAPPER ANALYSIS
        '''
        # Plot LCSS_wrapper(): w = z
        # nValuesWrap, tValuesWrap = tryItABunchLCSSWrapper( LCSS_wrapper_analysis, startN = 50, endN = 500, stepSize=50, numTrials=1)
        # plt.plot(nValuesWrap, tValuesWrap, color="green", label="LCSS_wrapper(LCSS()) w = z; n = z, m = z")
        # Plot LCSS_wrapper(): w < z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchLCSSWrapper( LCSS_wrapper_analysis, startN = 50, endN = 500, stepSize=50, numTrials=1, amtPatternsSmaller = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="green", label="LCSS_wrapper(LCSS()) w < z, w = (z / 2); n = z, m = z")
        # Plot LCSS_wrapper(): w > z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchLCSSWrapper( LCSS_wrapper_analysis, startN = 50, endN = 500, stepSize=50, numTrials=1, amtPatternsLarger = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="green", label="LCSS_wrapper(LCSS()) w > z, w = (z * 2); n = z, m = z")

        '''
        RABIN-KARP WRAPPER ANALYSIS
        '''
        # Plot KMP_wrapper(): w = z
        nValuesWrap, tValuesWrap = tryItABunchKMPWrapper( rabinkarp_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1)
        plt.plot(nValuesWrap, tValuesWrap, color="blue", label="rabinkarp_wrapper(RabinKarp()) w = z; n = z, m = z")
        # Plot KMP_wrapper(): w < z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchKMPWrapper( rabinkarp_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1, amtPatternsSmaller = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="blue", label="rabinkarp_wrapper(RabinKarp()) w < z, w = (z / 2); n = z, m = z")
        # Plot KMP_wrapper(): w > z
        # nValuesWrapLessPatterns, tValuesWrapLessPatterns = tryItABunchKMPWrapper( rabinkarp_wrapper_analysis, startN = 50, endN = 1000, stepSize=50, numTrials=1, amtPatternsLarger = True)
        # plt.plot(nValuesWrapLessPatterns, tValuesWrapLessPatterns, color="blue", label="rabinkarp_wrapper(RabinKarp()) w > z, w = (z * 2); n = z, m = z")

        plt.xlabel("Length of set S[], z", fontsize=28)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.ylabel("Time(ms)", fontsize=28)
        plt.legend(fontsize=22)
        plt.title("Algorithm Runtimes within Wrapper Functions", fontsize=30)
        plt.show()