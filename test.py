import EZRV
import pandas as pd
import matplotlib.pyplot as plt

# EZRV.update_internal_dataframe()

# EZRV.update_database('Example/example_file.csv')

# EZRV.remove_outdated_data('Example/example_file.csv', 'HARPS', False)


#
# for plots
df_internal = pd.read_csv('Metadata/Internal_Simbad_Names.csv')
database_names = df_internal['simbad_name']
# 598,3228,1

for i in range(2800,3227,1):
    EZRV.retrieve_data(database_names[i], False, False)
