import configparser


config = configparser.ConfigParser()
config.read('config.ini')
VERBOSE = config.getboolean('DEFAULT', 'VerboseMode')
ANALYSIS_LCSS = config.getboolean('ANALYSIS', 'RuntimeAnalysis_LCSS')

