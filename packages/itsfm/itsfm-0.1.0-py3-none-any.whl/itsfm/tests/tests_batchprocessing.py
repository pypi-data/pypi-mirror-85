# -*- coding: utf-8 -*-
"""Tests for batch_processing
Created on Mon May  4 17:59:56 2020

@author: tbeleyur
"""
import os
import pandas as pd
import unittest
import itsfm
from itsfm.batch_processing import *

class RemovePunctuations(unittest.TestCase):
    
    
    def test_1(self):
        eg_str = "[miaow "
        exp = "miaow"
        self.assertEqual(remove_punctuations(eg_str), exp)
    def test_2(self):
        eg_str = "[miaow]  "
        exp = "miaow"
        self.assertEqual(remove_punctuations(eg_str), exp)
    def test_3(self):
        eg_str = "[miaow ] ]"
        exp = "miaow"
        self.assertEqual(remove_punctuations(eg_str), exp)
    def test_4(self):
        eg_str = "[miaow *$%"
        exp = "miaow"
        cleaned = remove_punctuations(eg_str, signs_to_remove=['*','$','%'])
        self.assertEqual(cleaned, exp)

class TestString2Func(unittest.TestCase):
    
    def test_1(self):
         x = "[measure_rms, measure_peak_amplitude]"
         list_w_funcs = to_list_w_funcs(x)
    def test_2(self):
        x = "[measure_rms, measure_peak_amplitude, miaow]"
        with self.assertRaises(ValueError):
            list_w_funcs = to_list_w_funcs(x)
        


class TestSaveMeasurements(unittest.TestCase):
    
    def setUp(self):
        self.filepath = 'testfile.csv'
        self.filename = 'tesfile.wav'
        self.measures = pd.DataFrame(data={'a':[10,30], 
                                            'b':['fm1','cf1']})
    def test_initiate_fresh(self):
        save_measurements_to_file(self.filepath,
                                  self.filename,
                                  [], self.measures)
        df = pd.read_csv(self.filepath).iloc[:,1:]

        self.assertTrue(df.equals(self.measures))
    
    def test_adding_to_previous_file(self):
        '''
        '''
        save_measurements_to_file(self.filepath,
                                  self.filename,
                                  [], self.measures)
        
        new_measures = self.measures.copy()
        new_measures['a'] *= 2 
        
        all_measures = pd.concat((self.measures, new_measures)).reset_index(drop=True)
        
        save_measurements_to_file(self.filepath,
                                  self.filename,
                                  self.measures, new_measures)
        
        df = pd.read_csv(self.filepath).iloc[:,1:]
        self.assertTrue(df.equals(all_measures))
        
    
    def tearDown(self):
        os.remove(self.filepath)
        
class CheckOneRowWorking(unittest.TestCase):
    
    def test_simple(self):
       data = {'a': [10,20], 'b':[30,40]}
       
       df = pd.DataFrame(data=data, index=range(2))
       
       exp_df = pd.DataFrame(data={'a':[20], 'b':[40]})
       
       oned_series = df.loc[1]
       
       oned_df = make_to_oned_dataframe(oned_series)
       
       self.assertTrue(oned_df.equals(exp_df))

class SubsetBatchData(unittest.TestCase):
    
    def setUp(self):
        self.df = pd.DataFrame(data={'a':range(10), 'b':range(10)})
    
    def test_simple(self):
        '''when no kwargs are given, then input=output
        '''
        output = subset_batch_data(self.df)
        self.assertTrue(self.df.equals(output))
        
    def test_w_start(self):
        start = 3
        output = subset_batch_data(self.df, _from=start)
        
        exp = self.df.loc[3:,:]
        self.assertTrue(exp.equals(output))
    
    def test_w_stop(self):
        stop = 7
        output = subset_batch_data(self.df, _till=stop)
        exp = self.df.loc[:7]
        
        self.assertTrue(output.equals(exp))
    
    def test_onerowusedproperly(self):
        with self.assertRaises(ImproperArguments):
            subset_batch_data(self.df, one_row=4, _from=3, _till=8)

class TestMeasurementFileRemoval(unittest.TestCase):
    
    def setUp(self):
        df = pd.DataFrame(data={'a':range(10), 'b':range(10)})
        df.to_csv('measurement1.csv')
    
    def test_delete_measurementfile(self):
        measurement_file_action(del_measurement=True)
        
        num_matches = len(glob('measurement*'))
        self.assertEqual(num_matches, 0)
    
    def tearDown(self):
        measurement_files = glob('measurement*')
        if len(measurement_files) >0:
            for each in measurement_files:
                os.remove(each)

            
        
        
        
        
        

if __name__ == '__main__':
    unittest.main()