import configparser


config = configparser.ConfigParser()
config.read('config.ini')
VERBOSE = config.getboolean('DEFAULT', 'VerboseMode')
ANALYSIS_LCSS = config.getboolean('ANALYSIS', 'RuntimeAnalysis_LCSS')

class Match:
    def __init__(self, starting_index: int, ending_index: int):
        self.starting_index = starting_index
        self.ending_index = ending_index


def LCSS(S: str, T: str) -> float:
    """
    S = String
    T = Pattern
    m = S.length
    n = T.length
    """
    m = len(S)
    n = len(T)
    # matches = []

    max_length = 0
    ending_index = 0
    lookup_table = [[0 for x in range(n + 1)] for y in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if S[i - 1] == T[j - 1]:
                lookup_table[i][j] = lookup_table[i - 1][j - 1] + 1
                if lookup_table[i][j] > max_length:
                    max_length = lookup_table[i][j]
                    ending_index = i
    # starting_index = ending_index - max_length
    # matches.append(Match(starting_index, ending_index))
    
    # print("Starting index:", ending_index - max_length)
    # print("Ending index:", ending_index)
    # print(lookup_table))
    # for match in matches:
    #     print(match.starting_index)
    if VERBOSE:
        print("Longest match between paragraph and corpus document occurs at index {x}.".format(x=ending_index - max_length))
        print("Longest match was: {match}".format(match=S[ending_index - max_length: ending_index]))
    hit_rate = max_length / m * 100
    return hit_rate


if __name__ == '__main__':
    # LCSS test cases:
    # string = "ABABDABACDABABCABABABABDABACDABABCABAB"
    # pattern = "ABABCABAB"

    # string = "ABABCABCABABABD"
    # pattern = "ABABD"

    string = "TheSunIsBrightSunIsDark"
    pattern = "SunIs"

    match = LCSS(string, pattern)
    print("Match percentage: {match:.2f}%".format(match=match))
