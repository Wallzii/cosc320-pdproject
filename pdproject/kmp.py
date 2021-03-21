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
        while matched > 0 and pattern[matched] != string[i]:
            matched = lps[matched - 1]
        if pattern[matched] == string[i]:
            matched += 1
        if matched == m:
            print("Pattern occurs at index {x}.".format(x=(i - m) + 1))
            matched = lps[matched - 1]
            total_matches += 1
    print("Pattern was found in string {matches} time(s).".format(matches=total_matches))
    print("There is a {:.2f}% hit rate of the pattern in string.".format((total_matches * m) / n * 100))

def LPS(pattern):
    m = len(pattern)
    PI = [0] * m
    k = 0

    for i in range(1,m):
        while k > 0 and pattern[k] != pattern[i]:
            k = PI[k - 1]
        if pattern[k] == pattern[i]:
            k += 1
        PI[i] = k
    return PI

if __name__ == '__main__':
    # KMP test cases:
    string = "ABABDABACDABABCABABABABDABACDABABCABAB"
    pattern = "ABABCABAB"

    # string = "ABABCABCABABABD"
    # pattern = "ABABD"

    # string = "TheSunIsBrightSunIsDark"
    # pattern = "SunIs"

    KMPSearch(pattern, string)