import unittest
import numpy as np
import cProfile
from corrector import Corrector

class TestCarBrand(unittest.TestCase):

    def setUp(self):
        self.corrector = Corrector()

    def testCarBrandIsCorrect(self):    
        cb = 'TOYOTA'
        queried = self.corrector.query_car_brand(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual(cb,qcb)
        self.assertEqual(isDiff,0)
        
    def testCarBrandIsMisspeltEnglish(self):    
        cb = 'TOTAYO'
        queried = self.corrector.query_car_brand(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual('TOYOTA',qcb)
        self.assertEqual(isDiff,1)

    def testCarBrandIsThai(self):    
        cb = 'โตโยต้า'
        queried = self.corrector.query_car_brand(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual('TOYOTA',qcb)
        self.assertEqual(isDiff,1)

    def testCarBrandIsMisspeltThai(self):    
        cb = 'โตโญตา'
        queried = self.corrector.query_car_brand(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual('TOYOTA',qcb)
        self.assertEqual(isDiff,1)
        
    def testCarBrandIsPartial(self):    
        cb = 'ALFA'
        queried = self.corrector.query_car_brand(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual('ALFA ROMEO',qcb)
        self.assertEqual(isDiff,1)
 
    def testCarBrandIsPartialThai(self):    
        cb = 'อันฟ่า'
        queried = self.corrector.query_car_brand(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual('ALFA ROMEO',qcb)
        self.assertEqual(isDiff,1)  
  
    def testCarBrandIsEmpty(self):    
        cb = ''
        queried = self.corrector.query_car_brand(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual('-',qcb)
        self.assertEqual(isDiff,1)  
      
class TestCarModel(unittest.TestCase):

    def setUp(self):
        self.corrector = Corrector()

    def testCarModelIsCorrect(self):    
        cb = 'SERIES 3'
        queried = self.corrector.query_car_model(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual(cb,qcb)
        self.assertEqual(isDiff,0)
        
    def testCarModelIsMisspeltEnglish(self):    
        cb = 'SERIE 3'
        queried = self.corrector.query_car_model(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual('SERIES 3',qcb)
        self.assertEqual(isDiff,1)

    def testCarModelIsThai(self):    
        cb = 'ซีรีส์3'
        queried = self.corrector.query_car_model(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual('SERIES 3',qcb)
        self.assertEqual(isDiff,1)

    def testCarModelIsThaiII(self):    
        cb = 'แคมรี่'
        queried = self.corrector.query_car_model(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual('CAMRY',qcb)
        self.assertEqual(isDiff,1)

    def testCarModelIsMisspeltThai(self):    
        cb = 'ซีรี 3'
        queried = self.corrector.query_car_model(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual('SERIES 3',qcb)
        self.assertEqual(isDiff,1)

    def testCarModelIsEmpty(self):    
        cb = ''
        queried = self.corrector.query_car_model(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual('-',qcb)
        self.assertEqual(isDiff,1)

       
class TestItemName(unittest.TestCase):

    def setUp(self):
        self.corrector = Corrector()

    def testItemNameIsCorrect(self):    
        cb = 'ไส้กรองน้ำมันเครื่อง'
        queried = self.corrector.query_item_name(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual(cb,qcb)
        self.assertEqual(isDiff,0)

    def testItemNameIsCorrectII(self):    
        cb = 'ลูกหมากคันชัก'
        queried = self.corrector.query_item_name(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual(cb,qcb)
        self.assertEqual(isDiff,0)
        
    def testItemNameIsMisspelt(self):    
        cb = 'ลูกหมาคันชัก'
        queried = self.corrector.query_item_name(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual('ลูกหมากคันชัก',qcb)
        self.assertEqual(isDiff,1)
        
    def testItemNameIsMisspeltII(self):    
        cb = 'โชกอับ'
        queried = self.corrector.query_item_name(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual('โช้คอัพ',qcb)
        self.assertEqual(isDiff,1)        
        
    def testItemNameIsMisspeltIII(self):    
        cb = 'บุ๊ดโชกอับ'
        queried = self.corrector.query_item_name(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual('บู๊ชโช้คอัพ',qcb)
        self.assertEqual(isDiff,1)          

    def testItemNameIsPartial(self):    
        cb = 'กรองเครื่อง'
        queried = self.corrector.query_item_name(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual('ไส้กรองน้ำมันเครื่อง',qcb)
        self.assertEqual(isDiff,1)

    def testItemNameIsEmpty(self):    
        cb = ''
        queried = self.corrector.query_item_name(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual('-',qcb)
        self.assertEqual(isDiff,1)
        
class TestItemBrand(unittest.TestCase):

    def setUp(self):
        self.corrector = Corrector()

    def testItemBrandIsCorrect(self):    
        cb = '333'
        queried = self.corrector.query_item_brand(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual(cb,qcb)
        self.assertEqual(isDiff,0)
    
    def testItemBrandIsCorrectII(self):    
        cb = 'SL'
        queried = self.corrector.query_item_brand(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual(cb,qcb)
        self.assertEqual(isDiff,0)
                
    def testItemBrandIsMapped(self):    
        cb = 'หมี'
        queried = self.corrector.query_item_brand(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual('SL',qcb)
        self.assertEqual(isDiff,1)

    def testItemBrandIsMisspeltMapped(self):    
        cb = 'มี๋'
        queried = self.corrector.query_item_brand(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual('SL',qcb)
        self.assertEqual(isDiff,1)
 
    def testItemBrandIsEmpty(self):    
        cb = ''
        queried = self.corrector.query_item_brand(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual('-',qcb)
        self.assertEqual(isDiff,1)
       
class TestItemFitment(unittest.TestCase):

    def setUp(self):
        self.corrector = Corrector()

    def testSingleFitment(self):    
        cb = 'ซ้าย'
        queried = self.corrector.query_fitment(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual(len(qcb),1)
        self.assertEqual(cb,qcb[0])
        self.assertEqual(isDiff,0)
        
    def testMergeTwoFitment(self):    
        cb = 'ซ้าย หน้า'
        queried = self.corrector.query_fitment(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual(len(qcb),1)
        self.assertEqual('หน้าซ้าย',qcb[0])
        self.assertEqual(isDiff,1)

    def testMergeThreeFitment(self):    
        cb = 'ซ้าย ล่าง หน้า'
        queried = self.corrector.query_fitment(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual(len(qcb),1)
        self.assertEqual('หน้าซ้ายล่าง',qcb[0])
        self.assertEqual(isDiff,1)

    def testDoubleFitment(self):    
        cb = 'ซ้าย ขวา'
        queried = self.corrector.query_fitment(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        qcb = np.sort(qcb)
        self.assertEqual(len(qcb),2)
        self.assertEqual('ขวา',qcb[0])
        self.assertEqual('ซ้าย',qcb[1])
        self.assertEqual(isDiff,1)

    def testDoubleFitmentExtracted(self):    
        cb = 'หน้าซ้าย ขวา'
        queried = self.corrector.query_fitment(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        qcb = np.sort(qcb)
        self.assertEqual(len(qcb),2)
        self.assertEqual('หน้าขวา',qcb[0])
        self.assertEqual('หน้าซ้าย',qcb[1])
        self.assertEqual(isDiff,1)

    def testImplicitPair(self):    
        cb = 'คู่หน้า'
        queried = self.corrector.query_fitment(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        qcb = np.sort(qcb)
        self.assertEqual(len(qcb),2)
        self.assertEqual('หน้าขวา',qcb[0])
        self.assertEqual('หน้าซ้าย',qcb[1])
        self.assertEqual(isDiff,1)

    def testImplicitPairII(self):    
        cb = 'คู่หลัง'
        queried = self.corrector.query_fitment(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        qcb = np.sort(qcb)
        self.assertEqual(len(qcb),2)
        self.assertEqual('หลังขวา',qcb[0])
        self.assertEqual('หลังซ้าย',qcb[1])
        self.assertEqual(isDiff,1)


    def testImplicitPairIII(self):    
        cb = 'คู่หลังล่าง'
        queried = self.corrector.query_fitment(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        qcb = np.sort(qcb)
        self.assertEqual(len(qcb),2)
        self.assertEqual('หลังขวาล่าง',qcb[0])
        self.assertEqual('หลังซ้ายล่าง',qcb[1])
        self.assertEqual(isDiff,1)
 
    def testImplicitPairIV(self):    
        cb = 'คู่'
        queried = self.corrector.query_fitment(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        qcb = np.sort(qcb)
        self.assertEqual(len(qcb),2)
        self.assertEqual('ขวา',qcb[0])
        self.assertEqual('ซ้าย',qcb[1])
        self.assertEqual(isDiff,1)

         
    def testThreeDoubleFitmentExtracted(self):    
        cb = 'หน้าซ้ายบน่ ขวา'
        queried = self.corrector.query_fitment(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        qcb = np.sort(qcb)
        self.assertEqual(len(qcb),2)
        self.assertEqual('หน้าขวาบน',qcb[0])
        self.assertEqual('หน้าซ้ายบน',qcb[1])
        self.assertEqual(isDiff,1)           

    def testFitmentIsEmpty(self):    
        cb = '-'
        queried = self.corrector.query_fitment(cb)
        qcb = queried['refined']
        isDiff = queried['isDiff']
        self.assertEqual('-',qcb[0])
        self.assertEqual(isDiff,0)       
        
def suite():
    suite = unittest.TestSuite()
    #suite.addTests(unittest.makeSuite(TestCarBrand))
    suite.addTests(unittest.makeSuite(TestCarModel))
    #suite.addTests(unittest.makeSuite(TestItemName))
    #suite.addTests(unittest.makeSuite(TestItemBrand))    
    #suite.addTests(unittest.makeSuite(TestItemFitment))        
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
