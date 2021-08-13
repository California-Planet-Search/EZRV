import numpy as np
import yaml
import pandas as pd

config = yaml.safe_load(open("config/config.yaml"))
# print(config)
# print(config['my_dict'])
# print(config['my_dict']['s_index'])

def update_database(file_name):
    # print(pd.read_csv(file_name))

    input_dict  = config['input_dict']
    data_dir = config['data_dir']


    df_input = pd.read_csv(file_name)

    database = glob.glob('../Database/*.csv')

    for i in range(10)
        filename = database[i]
        starname = database[i][:-4]
        name = np.array(starname)
        df = pd.DataFrame(data = filename , name)
        print(df)
