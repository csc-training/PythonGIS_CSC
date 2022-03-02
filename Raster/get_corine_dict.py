

import pandas as pd


catxls =  'https://geoportal.ymparisto.fi/meta/julkinen/dokumentit/CorineMaanpeite2018Luokat.xls'
catdf = pd.read_excel(catxls, index_col=None)

catdf.columns

catdf_lim = catdf[['Value','Level4Eng']].set_index('Value')

catdict = catdf_lim.to_dict()['Level4Eng']




