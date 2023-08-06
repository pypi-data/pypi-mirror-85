from autopair_autocorrectml.vsms import Vsms
from collections import OrderedDict,Counter
from functools import reduce
import numpy as np
import pandas as pd
import pickle
import functools
import operator
import itertools
import string
import re
import ray
import psutil
from pathlib import Path
class Corrector(Vsms):
    
    def __init__(self):
        try :
            file = open( Path(__file__).parent / './resource/model/vsm_entity.pkl','rb')
            self.vsm_entity = pickle.load(file)
            file.close()
        except:            
            self.compute()
            file = open(Path(__file__).parent / './resource/model/vsm_entity.pkl','rb')
            self.vsm_entity = pickle.load(file)
            file.close()

    def query_car_brand(self,s):
        queried = self._Vsms__queryName(s,self.vsm_entity['car_brand'])
        return queried
    
    def query_car_model(self,s):
        queried = self._Vsms__queryName(s,self.vsm_entity['car_model'])
        return queried

    def query_item_name(self,s):
        queried = self._Vsms__queryDetail(s,self.vsm_entity['item_name'])
        return queried

    def query_item_brand(self,s):
        queried = self._Vsms__queryName(s,self.vsm_entity['item_brand'])
        return queried

    def query_fitment(self,s):      
        s = s.replace('คู่', 'ซ้ายขวา')
        appeared = [w for w in self.vsm_entity['fitment'] if w in list(set([''.join(list(OrderedDict.fromkeys([x,y,z]))) for x,y,z in list(itertools.product([w for w in self.vsm_entity['fitment'] if w in s],[w for w in self.vsm_entity['fitment'] if w in s],[w for w in self.vsm_entity['fitment'] if w in s]))]))]
        appeared = np.array([list(filter(lambda x: x != '-',w)) if '-' in w and len(w) != 1 else w for w in appeared])
        count_appearance = dict(functools.reduce(operator.add, map(Counter, [{x:1} if y in x else {x:0} for x in appeared for y in appeared]))) if len(appeared) > 0 else {'-':1}
        parsed = list([key for key in count_appearance.keys() if count_appearance[key]==max(count_appearance.values())])
        return {'refined': parsed,'isDiff': 0 if len(parsed) == 1 and parsed[0] == s else 1}
        
    def compute(self):
        mandatory_path = Path(__file__).parent / './resource/raw/mandatory_11.22.xlsx'
        corrector_path = Path(__file__).parent / './resource/raw/corrected_v1.xlsx'
        ray.init(num_cpus=psutil.cpu_count())

        car_entity = pd.read_excel(mandatory_path,sheet_name='car_brand',header=1,usecols='A:D')       
        car_entity = car_entity[['car_brand','car_model','nickname']].drop_duplicates(keep='last').reset_index(drop=True).sort_values(by=['car_brand','car_model']).dropna()

        #Car brand
        carBrand_entity = car_entity['car_brand'].unique()
        carBrand_cleaned_lookup = pd.read_excel(corrector_path,sheet_name='car_brand',header=None,usecols='A:B')
        carBrand_cleaned_lookup = np.concatenate([[['','-']],carBrand_cleaned_lookup.dropna().values, [[k,k] for k in carBrand_cleaned_lookup.dropna()[1].unique()]]) if carBrand_cleaned_lookup.shape[0] > 0 else [['','-']]
        carBrand_cleaned_lookup = {k:v for k,v in carBrand_cleaned_lookup}
        carBrand_entity = np.unique(list(carBrand_cleaned_lookup.keys())+list(carBrand_entity))
        carBrand_entity = pd.DataFrame(np.unique(carBrand_entity),self._Vsms__createVSMDictList(ray,np.unique(carBrand_entity),True)).reset_index().rename(columns={'index':'vsm',0:'car_brand'}).set_index('car_brand')
        fixed = pd.DataFrame(carBrand_entity.apply(lambda x:carBrand_cleaned_lookup[x.name] if x.name in carBrand_cleaned_lookup else x.name,axis=1),columns=['fixed'])
        carBrand_entity = pd.concat([fixed,carBrand_entity],axis=1).set_index('fixed',drop=True)
        non_dup = ~carBrand_entity.reset_index().astype(str).applymap(lambda x: x.strip() if isinstance(x, str) else x).duplicated().values
        carBrand_entity = carBrand_entity.loc[non_dup]
        vsmCarBrand=self._Vsms__parseVSMDict(ray,carBrand_entity)
        vsmCarBrand_entity_full = vsmCarBrand['fullVSM']
        vsmCarBrand_entity_reduced = vsmCarBrand['reducedVSM']        
          
        #Car model
        carModel_entity = car_entity['car_model'].unique()        
        carModel_cleaned_lookup = pd.read_excel(corrector_path,sheet_name='car_model',header=None,usecols='A:B')
        carModel_cleaned_lookup = np.concatenate([[['','-']],carModel_cleaned_lookup.dropna().values, [[k,k] for k in carModel_cleaned_lookup.dropna()[1].unique()]]) if carModel_cleaned_lookup.shape[0] > 0 else [['','-']]
        carModel_cleaned_lookup = {k:v for k,v in carModel_cleaned_lookup}
        carModel_entity = np.unique(list(carModel_cleaned_lookup.keys())+list(carModel_entity))
        carModel_entity = pd.DataFrame(np.unique(carModel_entity),self._Vsms__createVSMDictList(ray,np.unique(carModel_entity),True)).reset_index().rename(columns={'index':'vsm',0:'car_model'}).set_index('car_model')
        fixed = pd.DataFrame(carModel_entity.apply(lambda x:carModel_cleaned_lookup[x.name] if x.name in carModel_cleaned_lookup else x.name,axis=1),columns=['fixed'])
        carModel_entity = pd.concat([fixed,carModel_entity],axis=1).set_index('fixed',drop=True)
        non_dup = ~carModel_entity.reset_index().astype(str).applymap(lambda x: x.strip() if isinstance(x, str) else x).duplicated().values
        carModel_entity = carModel_entity.loc[non_dup]
        vsmCarModel=self._Vsms__parseVSMDict(ray,carModel_entity)
        vsmCarModel_entity_full = vsmCarModel['fullVSM']
        vsmCarModel_entity_reduced = vsmCarModel['reducedVSM']        
        
        #Fitment and unit               
        fitment_entity = np.concatenate(pd.read_excel(mandatory_path,sheet_name='fitment_detail',header=1,usecols='B').values)
        added_fitment = np.concatenate(pd.read_excel(corrector_path,sheet_name='fitment_detail',header=None,usecols='A').values)
        fitment_entity = np.unique(np.concatenate([fitment_entity, added_fitment]))
        fitment_entity = np.unique([re.sub(r'\s+', '', s) for s in fitment_entity if not any(p in s for p in string.punctuation)])
        fitment_entity = np.array(list(reduce(lambda a, b: dict(a, **b), [{''.join(sorted(ss)):ss} for ss in fitment_entity]).values()))
        unit_entity = pd.read_excel(mandatory_path,sheet_name='stock_uom',header=1,usecols='A').iloc[:,0].values
        
        #Item category double lookup
        itemCat_entity = pd.read_excel(mandatory_path,sheet_name='item_cat',header=1,usecols='A:F')
        itemCat_entity['Category_1'] = itemCat_entity['Category_1'].ffill()
        itemCat_entity['code_1'] = itemCat_entity['code_1'].ffill()
    
        for c in itemCat_entity['Category_1']:
            sub = itemCat_entity[itemCat_entity['Category_1']==c].copy()
            sub['Category_2'] = sub['Category_2'].ffill()
            sub['code_2'] = sub['code_2'].ffill()
            itemCat_entity.loc[itemCat_entity['Category_1']==c] = sub
            
        itemCat_entity = itemCat_entity.drop_duplicates()    
        itemCat_entity = itemCat_entity.drop(['code_1','code_2','code_3'],axis=1)       
        itemCat_entity_category_lookup = {k.strip():v.strip() for k,v in pd.concat([itemCat_entity[['Category_2','Category_1']].T.reset_index(drop=True).T,itemCat_entity[['Category_3','Category_1']].T.reset_index(drop=True).T],axis=0).dropna().values}
        
        itemName_entity = np.unique(list(itemCat_entity_category_lookup.keys()))
        itemName_cleaned_lookup = pd.read_excel(corrector_path,sheet_name='item_name',header=None,usecols='A:B')
        itemName_cleaned_lookup = np.concatenate([[['','-']],itemName_cleaned_lookup.dropna().values, [[k,k] for k in itemName_cleaned_lookup.dropna()[1].unique()]]) if itemName_cleaned_lookup.shape[0] > 0 else [['','-']]
        itemName_cleaned_lookup = {k:v for k,v in itemName_cleaned_lookup}
        itemName_entity = np.unique(list(itemName_cleaned_lookup.keys())+list(itemName_entity))        
        itemName_entity = pd.DataFrame(np.unique(itemName_entity),self._Vsms__createVSMDictList(ray,np.unique(itemName_entity),False)).reset_index().rename(columns={'index':'vsm',0:'item_name'}).set_index('item_name')
        fixed = pd.DataFrame(itemName_entity.apply(lambda x:itemName_cleaned_lookup[x.name] if x.name in itemName_cleaned_lookup else x.name,axis=1),columns=['fixed'])
        itemName_entity = pd.concat([fixed,itemName_entity],axis=1).set_index('fixed',drop=True)
        non_dup = ~itemName_entity.reset_index().astype(str).applymap(lambda x: x.strip() if isinstance(x, str) else x).duplicated().values
        itemName_entity = itemName_entity.loc[non_dup]
        vsmItemName=self._Vsms__parseVSMDict(ray,itemName_entity)
        vsmItemName_entity_full = vsmItemName['fullVSM']
        vsmItemName_entity_reduced = vsmItemName['reducedVSM']        
        catg  = [itemCat_entity_category_lookup[s] if s in itemCat_entity_category_lookup else 'ไม่พบ' for s in vsmItemName_entity_reduced.index]
        vsmItemCat_entity_reduced = vsmItemName_entity_reduced.copy()
        vsmItemCat_entity_reduced.set_index([catg],inplace=True)
        vsmItemCat_entity_full = vsmItemName_entity_full.copy()
        
        #Item brand
        itemBrand_entity = pd.read_excel(mandatory_path,sheet_name='item_brand',header=1,usecols='B').astype(str)['brand'].values
        itemBrand_cleaned_lookup = pd.read_excel(corrector_path,sheet_name='item_brand',header=None,usecols='A:B')
        itemBrand_cleaned_lookup = np.concatenate([[['','-']],itemBrand_cleaned_lookup.dropna().values, [[k,k] for k in itemBrand_cleaned_lookup.dropna()[1].unique()]]) if itemBrand_cleaned_lookup.shape[0] > 0 else [['','-']]
        itemBrand_cleaned_lookup = {k:v for k,v in itemBrand_cleaned_lookup}
        itemBrand_entity = np.unique(list(itemBrand_cleaned_lookup.keys())+list(itemBrand_entity))        
        itemBrand_entity = pd.DataFrame(np.unique(itemBrand_entity),self._Vsms__createVSMDictList(ray,np.unique(itemBrand_entity),True)).reset_index().rename(columns={'index':'vsm',0:'item_brand'}).set_index('item_brand')
        fixed = pd.DataFrame(itemBrand_entity.apply(lambda x:itemBrand_cleaned_lookup[x.name] if x.name in itemBrand_cleaned_lookup else x.name,axis=1),columns=['fixed'])
        itemBrand_entity = pd.concat([fixed,itemBrand_entity],axis=1).set_index('fixed',drop=True)
        non_dup = ~itemBrand_entity.reset_index().astype(str).applymap(lambda x: x.strip() if isinstance(x, str) else x).duplicated().values
        itemBrand_entity = itemBrand_entity.loc[non_dup]        
        vsmItemBrand=self._Vsms__parseVSMDict(ray,itemBrand_entity)
        vsmItemBrand_entity_full = vsmItemBrand['fullVSM']
        vsmItemBrand_entity_reduced = vsmItemBrand['reducedVSM']        

        vsm_entity = {}
        vsm_entity['car_brand']  = {'full':vsmCarBrand_entity_full,'reduced':vsmCarBrand_entity_reduced}
        vsm_entity['car_model']  = {'full':vsmCarModel_entity_full,'reduced':vsmCarModel_entity_reduced}
        vsm_entity['item_name'] = {'full':vsmItemName_entity_full,'reduced':vsmItemName_entity_reduced}
        vsm_entity['item_cat'] = {'full':vsmItemCat_entity_full,'reduced':vsmItemCat_entity_reduced}               
        vsm_entity['item_brand'] = {'full':vsmItemBrand_entity_full,'reduced':vsmItemBrand_entity_reduced}
        vsm_entity['fitment'] = fitment_entity
        vsm_entity['unit'] = unit_entity    
        
        file = open(Path(__file__).parent / './resource/model/vsm_entity.pkl','wb')
        pickle.dump(vsm_entity,file)
        file.close()
        
        ray.shutdown()

def main():
    c = Corrector()
    
if __name__ == "__main__":
    main()