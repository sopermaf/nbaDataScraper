'''
This program should be able to
retrieve info on a particular
NBA team and include info on upcoming
games as well as their record
'''
import json
import sys
from nbaObjects import NBAGameDay


if __name__=="__main__":
    retrievalMethod = sys.argv[1] # -f || -r
    retrievalRef = sys.argv[2] # filename or date YYYYMMDD

    dayData = NBAGameDay()
    if retrievalMethod == '-f':
        dayData.initDataLocalFile(retrievalRef)
    elif retrievalMethod == '-r':
        dayData.initDataRemote(retrievalRef)
    else:
        raise ValueError(
            'INVALID ARGS'
        )
    
    dayData.print()
