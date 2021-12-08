import numpy as np
import yaml
import pandas as pd
import glob
import matplotlib as mpl
import matplotlib.pyplot as plt
from astroquery.simbad  import Simbad
from astropy.time import Time
from .update_database import *
from .bc_bjd import *
config = yaml.safe_load(open("config/config.yaml"))

def retrieve_data(input_star_name, test_query_simbad, test_bjd_conversion):
    table = Simbad.query_objectids(input_star_name)
    simbad_name_retrieve = np.array(table['ID'][0], 'str')
    print(simbad_name_retrieve)

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
        times = np.array(df_output['Time_BJD'])

    if test_bjd_conversion == False:
        df_output = pd.read_csv(retrieve_file)
        times = np.array(df_output['Time'])

    #prints retrieved data
    print(df_output)

    #Plotting data
    print('plotting data')

    #Converts time to year
    Time_convert = Time(times, format='jd', scale='utc')
    Time_year = Time_convert.to_value('decimalyear')


    RV = np.array(df_output['RV'])
    Uncert = np.array(df_output['Uncertainty'])
    instr = np.array(df_output['Instrument'])
    unique_instr = np.unique(instr)

    #plot details
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
    plt.rcParams["figure.figsize"] = (10,6)
    plt.rcParams['lines.markersize']= 4

    fig, ax1 = plt.subplots()
    ax2 = ax1.twiny()

    for i in range(len(unique_instr)):
        match_instr_data = np.where(unique_instr[i] == instr)[0]
        rms = np.sqrt(np.mean((RV[match_instr_data] - np.mean(RV[match_instr_data]))**2))
        ax1.errorbar(times[match_instr_data] - 2457000, RV[match_instr_data] - np.nanmean(RV[match_instr_data]), yerr = [Uncert[match_instr_data], Uncert[match_instr_data]], xerr=None, fmt= 'o', label = unique_instr[i] + '[' + str(len(RV[match_instr_data])) + '/' + str(len(RV)) + '],' +' RMS:' + "{:10.1f}".format(rms) + ' m/s')
        ax2.errorbar(Time_year[match_instr_data], RV[match_instr_data] - np.nanmean(RV[match_instr_data]), yerr = [Uncert[match_instr_data], Uncert[match_instr_data]], xerr=None, fmt= 'o', label = unique_instr[i] + '[' + str(len(RV[match_instr_data])) + '/' + str(len(RV)) + '],' +' RMS:' + "{:10.1f}".format(rms) + ' m/s')

    #axis labels
    if test_bjd_conversion == True:
        ax1.set_xlabel('Time [BJD - 2457000]')
    if test_bjd_conversion == False:
        ax1.set_xlabel('Time - 2457000')

    ax2.set_xlabel('Time [Year]')
    ax1.set_ylabel('Radial Velocity [m/s]')

    #plot name and legend
    plt.title(str(input_star_name))
    plt.legend(loc = 1)

    #to save plot as a png
    # path = r'Plots/'
    # plt.savefig(path + input_star_name + '.png', format = 'png', bbox_inches='tight')


    plt.show()

    # plt.close()
