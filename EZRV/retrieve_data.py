import numpy as np
import yaml
import pandas as pd
import glob
import matplotlib as mpl
import matplotlib.pyplot as plt
from astroquery.simbad  import Simbad
from .update_database import *
from .bc_bjd import *
config = yaml.safe_load(open("config/config.yaml"))

def retrieve_data(input_star_name, test_query_simbad, test_bjd_conversion):
    table = Simbad.query_objectids(input_star_name)
    simbad_name_retrieve = np.array(table['ID'][0], 'str')
    print(simbad_name_retrieve)

    #match simbad_name_retrieve to corresponding file in our database- use the first simbad name to match_name
    print('retrieving data')
    if test_query_simbad == True :
        df_internal = update_internal_dataframe()
        internal_starname = df_internal['simbad_name']
        print(internal_starname)
    if test_query_simbad == False :
        df_internal = pd.read_csv(config['default_directory'] + '/Metadata/Internal_Simbad_Names.csv')


    match_name = np.where(df_internal['simbad_name'] == simbad_name_retrieve)[0]

    retrieve_file = df_internal['filename'].iloc[match_name[0]]

    if test_bjd_conversion == True:
        df_output = time_conversion(retrieve_file)
        Time = np.array(df_output['Time_BJD'])
    if test_bjd_conversion == False:
        df_output = pd.read_csv(retrieve_file)
        Time = np.array(df_output['Time'])

    print(df_output)


    #PLOT! RV vs Time for retrieved file
    #make into function

    RV = np.array(df_output['RV'])
    Uncert = np.array(df_output['Uncertainty'])
    # rms = np.sqrt(np.mean((RV - np.mean(RV))**2))


    instr = np.array(df_output['Instrument'])
    unique_instr = np.unique(instr)

    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams.update({'font.size': 10})
    plt.rcParams['legend.fontsize'] = plt.rcParams['font.size']
    plt.rcParams['savefig.dpi'] = 72
    plt.rcParams['xtick.major.size'] = 3
    plt.rcParams['xtick.minor.size'] = 3
    plt.rcParams['xtick.major.width'] = 1
    plt.rcParams['xtick.minor.width'] = 1
    plt.rcParams['ytick.major.size'] = 3
    plt.rcParams['ytick.minor.size'] = 3
    plt.rcParams['ytick.major.width'] = 1
    plt.rcParams['ytick.minor.width'] = 1
    plt.rcParams['legend.frameon'] = True
    plt.rcParams['xtick.major.pad']='8'
    plt.rcParams['ytick.major.pad']='8'

    for i in range(len(unique_instr)):
        match_instr_data = np.where(unique_instr[i] == instr)[0]
        rms = np.sqrt(np.mean((RV[match_instr_data] - np.mean(RV[match_instr_data]))**2))
        plt.errorbar(Time[match_instr_data] - 2457000, RV[match_instr_data], yerr = [Uncert[match_instr_data], Uncert[match_instr_data]], xerr=None, fmt= 'o', label = unique_instr[i] + '[' + str(len(RV[match_instr_data])) + '/' + str(len(RV)) + '],' +' RMS:' + "{:10.1f}".format(rms) + ' m/s')

    if test_bjd_conversion == True:
        plt.xlabel('Time [BJD - 2457000]')

    #add second axis in years (look at astropy time converst jd to year): plt.twinx()
    if test_bjd_conversion == False:
        plt.xlabel('Time - 2457000')


    plt.ylabel('Radial Velocity [m/s]')
    plt.title(str(input_star_name))
    plt.legend(loc = 1)
    plt.show()
    plt.close()





    #if match == True then print data(dataframe)/data file and plot
