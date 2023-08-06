from abydos import distance, phonetic
from nltk.tokenize import SyllableTokenizer
from ssg import syllable_tokenize


import numpy as np
import pandas as pd

import functools
import operator
import Levenshtein
import re
import tltk
import pythainlp
import collections
import string


class Vsms():
    
    def __init__(self):
        np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

    def __queryName(self,s,vsmDF):
        parsedFull,parsedReduced = self.__parseVSMRecord(self.__createVSMDict(s,True),vsmDF['reduced'],s)
        score = np.sum(np.abs(vsmDF['reduced'].values - parsedReduced.values),axis=1).astype(float)#/size
        if min(score) < 1e-2:
            refined = vsmDF['reduced'].index[np.argmin(score)]
            refinedSuggest = {'refined':refined,'score':0.0,'origScore':0.0,'isDiff':0 if refined==s else 1}
        else:
            allScore = np.sort(score)
            topIdx = min( i for i in np.array([np.argmin(allScore <= allScore[5]),np.argmin(allScore < allScore[5]),np.argmin(allScore <= allScore[10])]) if i >0)
            top = np.argsort(score)[:topIdx]
            fullList = list(vsmDF['reduced'].index[top])
            fullListScore = score[top]
            refinedSuggest = self.__refinedSearch(parsedFull,parsedReduced,vsmDF['full'].loc[top],vsmDF['reduced'].iloc[top],fullListScore)
            refinedSuggest['origScore'] = fullListScore[fullList.index(refinedSuggest['refined'])]
            refinedSuggest['isDiff'] = 0 if refinedSuggest['refined']==s else 1
        return refinedSuggest

    def __queryDetail(self,s,vsmDF):
       parsedFull,parsedReduced = self.__parseVSMRecord(self.__createVSMDict(s,False),vsmDF['reduced'],s)
       score = np.sum(np.abs(vsmDF['reduced'].values - parsedReduced.values),axis=1).astype(float)#/size
       subS = re.sub('[a-zA-Z0-9 ]*','',s)
       if subS != s:
           parsedFullT,parsedReducedT = self.__parseVSMRecord(self.__createVSMDict(subS,False),vsmDF['reduced'],subS)
           scoreT = np.sum(np.abs(vsmDF['reduced'].values - parsedReducedT.values),axis=1).astype(float)#/size
           (parsedFull,parsedReduced,score) = (parsedFull,parsedReduced,score) if min(score) <= min(scoreT) else (parsedFullT,parsedReducedT,scoreT)      
       if min(score) < 1e-2:
           refined = vsmDF['reduced'].index[np.argmin(score)]
           refinedSuggest = {'refined':refined,'score':0.0,'origScore':0.0,'isDiff':0 if refined==s else 1}
       else:
           allScore = np.sort(score)
           topIdx = min( i for i in np.array([np.argmin(allScore <= allScore[5]),np.argmin(allScore < allScore[5]),np.argmin(allScore <= allScore[10])]) if i >0)
           top = np.argsort(score)[:topIdx]
           fullList = list(vsmDF['reduced'].index[top])
           fullListScore = score[top]
           refinedSuggest = self.__refinedSearch(parsedFull,parsedReduced,vsmDF['full'].loc[top],vsmDF['reduced'].iloc[top],fullListScore)
           refinedSuggest['origScore'] = fullListScore[fullList.index(refinedSuggest['refined'])]
           refinedSuggest['isDiff'] = 0 if refinedSuggest['refined']==s else 1
       return refinedSuggest

    def __parseVSMDict(self,ray,df):
       vsmDF = pd.DataFrame(columns=dict(functools.reduce(operator.add, map(collections.Counter, df['vsm'].values))).keys(),index=df.index)
       @ray.remote
       def get(subDf):        
           return np.array([self._Vsms__parseVSMRecord(row['vsm'],vsmDF,row.name) for _,row in subDf.iterrows()],dtype='object')
       
       vsmObject  = np.concatenate(ray.get([get.remote(l) for l in Vsms.chunks(df,ray.cluster_resources()['CPU'])]))
       fullVSM    = pd.concat(list(map(lambda xx: xx[0].set_index(pd.MultiIndex.from_product([[xx[1][0]],xx[0].index])),zip(list(map(lambda x: x[0], vsmObject)),enumerate(df.T)))))
       reducedVSM = pd.concat(list(map(lambda x: x[1], vsmObject)))
    
       return {'fullVSM':fullVSM,'reducedVSM':reducedVSM}

    def __parseVSMRecord(self,vsmDictReduced,vsmDFreduced,name):
       currow = np.array([[ 0 if Levenshtein.jaro_winkler(k,s) < 0.5 else 0.50*(distance.JaroWinkler().sim(str(phonetic.NRL().encode(k)),str(phonetic.NRL().encode(s)))) + 0.50*(distance.MetaLevenshtein().sim(k,s)) for s in vsmDFreduced.columns] for k,v in vsmDictReduced.items()])
       fullVSM = pd.DataFrame(currow,index=vsmDictReduced.keys(),columns=vsmDFreduced.keys())
       reducedVSM = (fullVSM.T.copy() * np.array([v for v in vsmDictReduced.values()])).T  
       mask   = np.zeros(reducedVSM.values.shape)
       mask[np.arange(reducedVSM.values.shape[0]),reducedVSM.values.argmax(axis=-1)] = reducedVSM.values.max(axis=-1)
       reducedVSM = pd.DataFrame([np.max(mask,axis=0)],index=[name],columns=vsmDFreduced.keys())
       return fullVSM,reducedVSM
    
    def __refinedSearch(self,qFull,qReduced,topVsmDFfull,topVsmDFreduced,origScore):
       refinedColumns = topVsmDFreduced.T.loc[(topVsmDFreduced>0).any()].T.columns
       parsedQX = qFull[refinedColumns]
       #idxMax = parsedQX.apply(np.argmax).values
       parsedQXval = parsedQX.max()
       parsedQXweight = parsedQX.shape[0]
       parsedTX = topVsmDFfull[refinedColumns]
       allScoreRefined = np.concatenate([[np.sum(np.abs(parsedQXval - parsedTX.loc[i].max()) * ((1/parsedQXweight + 1/parsedTX.loc[i].shape[0])/2))] for i in parsedTX.index.get_level_values(0).drop_duplicates()])
       allScoreRefined = 0.5*(allScoreRefined+origScore)
       refined = topVsmDFreduced.index[np.argmin(allScoreRefined)]
       result = {'refined':refined,'score':allScoreRefined.min()}        
       return result

    def __createVSMDictList(self,ray,inputStringList,self_check):
       @ray.remote
       def get(l):
           return [self.__createVSMDict(s,self_check) for s in l]
       results = np.concatenate(ray.get([get.remote(l) for l in Vsms.chunks(inputStringList,ray.cluster_resources()['CPU'])]))
       return results 
    
    def __createVSMDict(self,inputString,self_check):   
       inputString = str(inputString)
       inputString = re.sub('[ \u200b]+',' ',re.sub(r"([0-9]+(\.[0-9]+)?)",r" \1 ", str(inputString)).strip()).strip()       
       inputString = re.compile('[%s]' % re.escape('!"#$%&\'()*+,/:;<=>?@[\\]^_`{|}~')).sub(' ',inputString)
       rex=re.compile(r'([a-zA-Z0-9]+)(['+pythainlp.thai_letters+']+)')
       processed = rex.sub(r'\1 \2',inputString).strip()
       rex=re.compile(r'(['+pythainlp.thai_letters+']+)([a-zA-Z0-9]+)')
       inputString = rex.sub(r'\1 \2',processed).strip()
       inputString = inputString.translate(str.maketrans({key: " {0} ".format(key) for key in string.punctuation}))
       inputStringArr = inputString.strip().split()
       #cnt_digits = len([s for s in ''.join(inputStringArr) if s.isdigit()])
       wordDict = []
       
       nth = np.sum([pythainlp.util.isthai(s) for s in inputStringArr])
       #ndi = np.sum([s.isdigit() for s in inputStringArr])
        
       mask = np.array([0 if pythainlp.util.isthai(s) else ( 1 if s.isdigit() else 2 ) for s in inputStringArr])
         
       if len(inputStringArr) == 0:
           wordDict.append([{'':1.0}])
       else:
           for s in inputStringArr:
               if s.isdigit():
                   subWordDict = [{k:1} for k in s]
                   #subWordDict = [{k:v} for k,v in subWordDict.items()]
                   #initialSum= np.sum(list(subWordDict.values()))
                   #subWordDict.update((k,v/initialSum) for k,v in subWordDict.items())
                   #if len(subWordDict.keys()) > 1:
                   #    subWordDict = [{k:(1/len(subWordDict.keys()))} for i,k in enumerate(subWordDict)]
                   #else:
                   #subWordDict = [subWordDict]
               elif pythainlp.util.isthai(s):
                   s = re.sub(r"[่-๋]","",s)
                   s = re.sub("ดีส","ดิส",s)
                   s = re.sub("บู[ชด]","บุช",s)
                   romanized = np.concatenate([x.split() for x in self.__preciseRomanizeThai(syllable_tokenize(s))])   
                   romanized = np.concatenate([re.compile('[%s]' % re.escape('!"#$%&\'()*+,/:;<=>?@[\\]^_`{|}~-')).sub(' ',s).split() for s in romanized])
                   if self_check:
                       romanized = np.concatenate(([''.join(romanized)],romanized))                               
                       #subWordDict = [{k:(len(romanized)-i)/sum(range(len(romanized)+1))} for i,k in enumerate(romanized)]
                       subWordDict = [{k:1} for i,k in enumerate(romanized)]
                   else:
                       #subWordDict = [{k:(1/len(romanized))} for i,k in enumerate(romanized)]
                       subWordDict = [{k:1} for i,k in enumerate(romanized)]
               else:    
                   subWordDict = SyllableTokenizer(sonority_hierarchy = ["aeiouy","lmnrwy","zvsf","bcdgtkpqxhj"]).tokenize(s.lower())
                   if self_check:
                       subWordDict = np.concatenate(([''.join(subWordDict)],subWordDict))                               
                       #subWordDict = [{k:(len(subWordDict)-i)/sum(range(len(subWordDict)+1))} for i,k in enumerate(subWordDict)]
                       subWordDict = [{k:1} for i,k in enumerate(subWordDict)]
                   else:
                   #    if any([pythainlp.util.isthai(s) for s in inputStringArr]):
                   #        subWordDict = [{k:(1/len(subWordDict)/np.sum(mask==False))} for i,k in enumerate(subWordDict)]
                   #    else:
                       #subWordDict = [{k:(1/len(subWordDict))} for i,k in enumerate(subWordDict)]
                       subWordDict = [{k:1} for i,k in enumerate(subWordDict)]
               wordDict.append(subWordDict)

       if 0 in mask and nth != len(inputStringArr):
           invIdx=np.where((np.diff(mask)!=0) & (np.array(mask[:-1])==0))[0]+1
           wordDict = np.split(wordDict,invIdx)
           for i,d in enumerate(wordDict):
               wordDict[i] = np.concatenate(d)       
       elif len(np.unique(mask))==1:
           wordDict = [np.concatenate(wordDict) if len(wordDict)>0 else wordDict[0]]
          
       group = len(wordDict)
      
       for dd in wordDict:
           for i,d in enumerate(dd):
               if self_check:
                   d.update((k,v*(len(dd)-i)/sum(range(len(dd)+1))) for k,v in d.items())
               else :
                   d.update((k,v*1/len(dd)) for k,v in d.items())
                   
       groupMask = np.array([(len(wordDict)-i)/sum(range(len(wordDict)+1)) for i in range(len(wordDict))])            
       
       for i,d in enumerate(wordDict):
           for dd in d:
               if self_check:
                  dd.update((k,v/group) for k,v in dd.items())
               else:
                  dd.update((k,v*groupMask[i]) for k,v in dd.items())
                  
       wordDict = np.concatenate(wordDict) if len(wordDict)>0 else wordDict[0]               
       
       #for d in wordDict:
       #   d.update((k,v/group) for k,v in d.items())

       wordDict = dict(functools.reduce(operator.add, map(collections.Counter, wordDict)))          

       #if not self_check:
       #   total = sum(list(wordDict.values()))
       #   wordDict.update((k,v/total) for k,v in wordDict.items())
       #print(wordDict)
       return wordDict
   
    def __preciseRomanizeThai(self,inputArray):
        rt = '[' + re.escape(''.join(pythainlp.thai_characters)) + ']'
        rtltk = re.compile('<s/>')
        romanized = [re.sub(rtltk,'',self.__customTH2roman(w)).strip() if pythainlp.util.isthai(w) else w for w in inputArray]
        romanized = [re.sub(rt, '', w) for w in romanized]
        return romanized
  
    def __customTH2roman(self,txt):
        NORMALIZE_ROM = [ ('O', 'o'), ('x', 'ae'), ('@', 'oe'), ('N', 'ng'), ('U','ue'), ('?',''), ('|',' '), ('~','-'),('^','-'),("'",'-')]
        inx = tltk.nlp.g2p(txt).split('<s/>')[0]
        (th, tran) = inx.split('<tr/>')
        tran = re.sub(r"([aeiouUxO@])\1",r"\1",tran)
        tran = re.sub(r"[0-9]",r"",tran)
        for k, v in NORMALIZE_ROM:
            tran = tran.replace(k, v)
        tran = re.sub(r"([aeiou])j",r"\1i",tran)
        tran = tran.replace('j','y')
        tran = re.sub(r"\-([^aeiou])",r" \1",tran).strip()
        return(tran)
    
    @staticmethod     
    def chunks(l, n):
       n = int(len(l)/4)+1
       n = max(1, n)
       return list(l[i:i+n] for i in range(0, len(l), n))
    