import numpy as np
import yaml
import pandas as pd
import glob
from astroquery.simbad  import Simbad


config = yaml.safe_load(open("config/config.yaml"))

def retrieve_data(input_star_name):
    table = Simbad.query_objectids(input_star_name)
    simbad_name_retrieve = np.array(table['ID'][0], 'str')
    print(simbad_name_retrieve)
