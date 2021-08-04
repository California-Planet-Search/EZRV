import numpy as np
import yaml
import pandas as pd

config = yaml.safe_load(open("config/config.yaml"))
print(config)
print(config['my_dict'])
print(config['my_dict']['s_index'])

def update_database(file_name):
    print(pd.read_csv(file_name))
