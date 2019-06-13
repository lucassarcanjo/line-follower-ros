#! /usr/bin/env python
import json

def loadConfigs():
    with open("/home/lucas/lego/src/seguidor_linha/scripts/data.json", "r") as file:
        return json.load(file)
        
def remap(x, oMin, oMax, nMin, nMax):

    #range check
    if oMin == oMax:
        print "Warning: Zero input range"
        return None

    if nMin == nMax:
        print "Warning: Zero output range"
        return None

    #check reversed input range
    reverseInput = False
    oldMin = min(oMin, oMax)
    oldMax = max(oMin, oMax)
    if not oldMin == oMin:
        reverseInput = True

    #check reversed output range
    reverseOutput = False   
    newMin = min(nMin, nMax)
    newMax = max(nMin, nMax)
    if not newMin == nMin :
        reverseOutput = True

    portion = (x-oldMin)*(newMax-newMin)/(oldMax-oldMin)
    if reverseInput:
        portion = (oldMax-x)*(newMax-newMin)/(oldMax-oldMin)

    result = portion + newMin
    if reverseOutput:
        result = newMax - portion

    return result


if __name__ == "__main__":
    ret = loadConfigs()

    # print str(ret['sensorLeftBlackValue'])
    pass