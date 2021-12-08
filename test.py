import EZRV
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# EZRV.update_internal_dataframe()
#
# df_new_star = pd.read_csv('tks_data.csv')
# TKS = df_new_star['name']
# TKS_unique = np.unique(TKS)
#
# for i in range(len(TKS_unique)):
#     print(TKS_unique[i])
#
# EZRV.update_database('TOI_new/TOI174.csv')
EZRV.update_database('Example/example_file.csv')

# EZRV.remove_outdated_data('Example/example_file.csv', 'HARPS', False)

# EZRV.retrieve_data('HD 45652', False, False)

# # for plots
# df_internal = pd.read_csv('Metadata/Internal_Simbad_Names.csv')
# database_names = df_internal['simbad_name']
#
#
# for i in range(2800,3227,1):
#     EZRV.retrieve_data(database_names[i], False, False)
