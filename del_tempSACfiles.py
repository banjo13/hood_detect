import numpy as np
import pandas as pd
import os
dfH = pd.read_csv('/Users/banjo/home/bnjo/hood/util/catalogs/_2002informationHORIZONTAL.csv')
# dfH
dfV = pd.read_csv('/Users/banjo/home/bnjo/hood/util/catalogs/_2002informationVERTICAL.csv')


def delete_tmp(df):
    names = df['name']
    for name in names:
        name = str(name)
#     os.remove(name)
#     print(name)
        if os.path.isfile(name):
            os.remove(name)
        else:    ## Show an error ##
            print("Error: %s file not found" % name)
    
delete_tmp(dfH)
delete_tmp(dfV)
