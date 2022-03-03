

import pandas as pd

def read_excel():

    catxls =  'https://geoportal.ymparisto.fi/meta/julkinen/dokumentit/CorineMaanpeite2018Luokat.xls'
    catdf = pd.read_excel(catxls, index_col=None)

    return catdf


def get_limited_df():

    catdf = read_excel()

    catdf_lim = catdf[['Value','Level4Eng']].set_index('Value')

    return catdf_lim 



def get_corine_dict():
    
    catdf = read_excel()

    catdf_lim = get_limited_df()

    catdict = catdf_lim.to_dict()['Level4Eng']

    return catdict , catdf_lim




