import configparser


config = configparser.ConfigParser()
config.read('config.ini')
VERBOSE = config.getboolean('DEFAULT', 'VerboseMode')
ANALYSIS_LCSS = config.getboolean('ANALYSIS', 'RuntimeAnalysis_RabinKarp')


def RabinKarp(pattern: str, string: str) -> float:
    n = len(string)
    m = len(pattern)
    d = 256
    q = 101
    hash_p = 0
    hash_t = 0
    h = 1

    if m > n:
        print("Invalid pattern length: pattern is longer than string; aborting RabinKarp.")
        return 0

    total_matches = 0

    for i in range(m - 1):
        h = (h * d) % q

    for i in range(m):
        hash_p = (d * hash_p + ord(pattern[i])) % q
        hash_t = (d * hash_t + ord(string[i])) % q

    # print("Hash_P: {hash}".format(hash=hash_p))
    # print("Hash_T: {hash}".format(hash=hash_t))

    for i in range(n - m + 1):
        if hash_p == hash_t:
            # print("TEST")
            for j in range(m):
                if string[i + j] != pattern[j]:
                    break
                else:
                    j += 1
            if j == m:
                if VERBOSE: print("Pattern found at position {x}.".format(x=i))
                total_matches += 1
        if i < (n - m):
            hash_t = (d*(hash_t - ord(string[i])*h) + ord(string[i + m])) % q
            if hash_t < 0:
                hash_t = hash_t + q
    hit_rate = (total_matches * m) / n * 100
    if total_matches != 0:
        if VERBOSE:
            print("Pattern was found in string {matches} time(s).".format(matches=total_matches))
            print("There is a {:.2f}% hit rate of the pattern in string.".format(hit_rate))
    return hit_rate


if __name__ == '__main__':
    # LCSS test cases:
    string = "ABABDABACDABABCABABABABDABACDABABCABAB"
    pattern = "ABABCABAB"

    # string = "ABABCABCABABABD"
    # pattern = "ABABD"

    # string = "TheSunIsBrightSunIsDark"
    # pattern = "SunIs"

    RabinKarp(pattern, string)
    # print("Match percentage: {match:.2f}%".format(match=match))
