def KMPSearch(pattern, string):
    m = len(pattern)
    n = len(string)
    lps = LPS(pattern)
    
    print("Pattern: {pattern}".format(pattern=pattern))
    print("String: {string}".format(string=string))
    print("Longest prefix suffix: {lps}".format(lps=lps))
    
    matched = 0
    total_matches = 0

    for i in range(n):
        # print("START:\ti = {i}, matched = {matched}".format(i=i, matched=matched))
        while matched > 0 and pattern[matched] != string[i]:
            # print("WhilePre: {m}".format(m=matched))
            matched = lps[matched - 1]
            # print("WhilePost: {m}".format(m=matched))
        if pattern[matched] == string[i]:
            # print("Match: pattern[{p}] = string[{s}]".format(p=pattern[matched], s=string[i]))
            matched += 1
            # print("MatchedFirstIf: {m}".format(m=matched))
        if matched == m:
            print("Pattern occurs at index {x}.".format(x=(i - m) + 1))
            matched = lps[matched - 1]
            total_matches += 1
            # print("MatchedLastIf: {m}".format(m=matched))
        # print("END:\t\ti = {i}, matched = {matched}\n".format(i=i, matched=matched))
    print("Pattern was found in string {matches} time(s).".format(matches=total_matches))
    print("There is a {:.2f}% hit rate of the pattern in string.".format((total_matches * m) / n * 100))

def LPS(pattern):
    m = len(pattern)
    PI = [0] * m
    k = 0

    for i in range(1,m):
        # print("LPS for i: {i}".format(i=i))
        while k > 0 and pattern[k] != pattern[i]:
            # print("k = {k}, pattern[{pk}] != pattern[{i}]".format(k=k, pk=pattern[k],i=pattern[i]))
            k = PI[k - 1]
        if pattern[k] == pattern[i]:
            k += 1
        PI[i] = k
    # print("PI: {pi}".format(pi=PI))
    return PI

# KMP test cases:
# string = "ABABDABACDABABCABAB"
# pattern = "ABABCABAB"

# string = "ABABCABCABABABD"
# pattern = "ABABD"

# string = "TheSunIsBrightSunIsDark"
# pattern = "SunIs"

# KMPSearch(pattern, string)