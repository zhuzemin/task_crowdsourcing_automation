import json
import os

DEBUG = True

def debug(s):
    if DEBUG:
        print(s)

class loadMatchingRule():
    MatchingRuleObjectList=[]

    def __init__(self,folderPath):
        debug('loadMatchingRuleObject')
        self.loadMatchingRule(folderPath)

    def loadMatchingRule(self,folderPath):
        for file in os.listdir(folderPath):
            if file.endswith(".json"):
                debug("file: "+file)
                debug("folderPath: "+folderPath)
                with open(folderPath+'/'+file, 'r') as f:
                    #try:
                    string=f.read()
                    debug("f: "+string)
                    MatchingRuleObject=json.loads(string)
                    debug("MatchingRuleObject['filename']: "+MatchingRuleObject['filename'])
                    if MatchingRuleObject['categoryStrList'] is not None:
                        MatchingRuleObject['filename']=file
                        MatchingRuleObject['avairable']=True
                        MatchingRuleObject['categoryStrList']
                        debug('file: '+file)
                    else:
                        MatchingRuleObject['filename']=file
                        MatchingRuleObject['avairable']=False
                        MatchingRuleObject['categoryStrList']=['File format corrupt']

                    '''except:
                        MatchingRuleObject={
                            'categoryStrList':['File format corrupt'],
                            'avairable':False,
                            'filename':file
                        }
                        #debug("MatchingRuleObject: "+str(MatchingRuleObject))'''
                self.MatchingRuleObjectList.append(MatchingRuleObject)
