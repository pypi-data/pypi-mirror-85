# -*- coding: utf-8 -*-
"""
Module to check if different vieweing options work
@author: tbeleyur
"""
import itsfm
import os
import soundfile as sf
from itsfm.simulate_calls import *
from itsfm.batch_processing import save_overview_graphs

call_props = {'upfm':(40000, 0.005),
              'cf':(50000, 0.01),
              'downfm':(80000, 0.0025)}
fs = 250*10**3
audio, _ =  make_cffm_call(call_props, fs)

filepath = os.path.join("C:/Users/tbeleyur/Desktop/testing", "matching_annotaudio_Aditya_2018-08-17_23_14.WAV")
audio, fs = sf.read(filepath)

output = itsfm.segment_and_measure_call(audio, fs,
                                        signal_level=-50,
                                        segment_method='pwvd',
                                        max_acc=2.0,
                                        )

out_inspect = itsfm.itsFMInspector(output, audio,fs)

one, _ = out_inspect.visualise_geq_signallevel()
two, _ = out_inspect.visualise_cffm_segmentation()
three,_ = out_inspect.visualise_frequency_profiles()
four, _, _ = out_inspect.visualise_fmrate()
five, _, _ = out_inspect.visualise_accelaration()


subplots_to_graph = [one, two, three, four, five]



save_overview_graphs(subplots_to_graph, 'miaow', 'bow',
                     0)