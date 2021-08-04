import numpy as np
import yaml
config = yaml.safe_load(open("config/config.yaml"))
print(config)
print(config['my_dict'])
print(config['my_dict']['s_index'])

def test(a):
    print(a)
