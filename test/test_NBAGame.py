from nbaObjects import NBAGame

def test_isoDataConversion():
    testDateTime = '2019-11-21T00:30:00.000Z'
    expectedOutput = '00:30 Thu 21-11-19'
    
    output = NBAGame.transformDateTimeToReadable(testDateTime)

    assert expectedOutput == output