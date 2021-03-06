# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 09:00:47 2020

Last Updated on Tue Nov 17 2020

@authors: ANDREA.SHEN, NICK.GAUGLER
"""
# Standard library imports
import pandas as pd
from time import time

# Third party imports
from pathlib import Path

# Local application imports
import B_PIF_PLCY
import C_PIF_VEH
import D_PIF_HIST


class cls_Reports_Data:
    def __init__(self):
        self.python_code_filepath = Path(__file__).parents[0]
        
        self.get_parameters_csv()
        self.state_abbr = self.parameters['state_abbr']
        self.main_dir = self.parameters['main_dir']
        if self.parameters['suffix'] == '""':
            self.suffix_product = str()
            self.nbnh_run_indicator = False
        else:
            self.suffix_product = self.parameters['suffix']
            self.nbnh_run_indicator = True
        self.quotes_indicator = self.parameters['quotes_ind'] == 'True'
        
        self.cd_dir = self.main_dir+'/python/aob_tool_reports/code'        
        
    def get_parameters_csv(self):
        parameters_filepath = self.python_code_filepath / ('aob_tool_reports_parameters.csv')
        self.parameters = pd.read_csv(parameters_filepath, header=None, index_col=0)[1].to_dict()

"""This is the main cycle that runs the various functions above"""
if __name__ == '__main__':
    start_time = time()
    cls_run = cls_Reports_Data()
    print("--NOTE: Working AOB folderpath is {} --".format(cls_run.main_dir))
    main_dir=cls_run.main_dir
    state_abbr = cls_run.state_abbr
    suffix_product = cls_run.suffix_product
    B_PIF_PLCY.pif_plcy_main(cls_run)
    phase_1_time = time()
    print("---Reports_PLCY completed in {}s seconds ---".format(round(time() - start_time,2)))
    PIF_CAP_HH, PIF_UNCAP_HH, NB_UNCAP_HH  = C_PIF_VEH.pif_veh_main(cls_run)
    phase_2_time = time()
    print("---Reports_VEH completed in {}s seconds ---".format(round(time() - phase_1_time,2)))
    D_PIF_HIST.pif_hist_main(cls_run, PIF_CAP_HH, PIF_UNCAP_HH, NB_UNCAP_HH)
    print("---Reports_Historgrams completed in {}s seconds ---".format(round(time() - phase_2_time,2)))

    
    print("---Total Runtime: {}s seconds ---".format(round(time() - start_time,2)))
          
