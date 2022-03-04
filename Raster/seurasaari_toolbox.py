

#download_from_url

import os
import urllib

def get_filename(url):
    """
    Parses filename from given url
    """
    if url.find('/'):
        return url.rsplit('/', 1)[1]

def download_data(url):
    # Filepaths
    outdir = r"data"

    # Create folder if it does not exist
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # Parse filename
    fname = get_filename(url)
    outfp = os.path.join(outdir, fname)
    # Download the file if it does not exist already
    if not os.path.exists(outfp):
        print("Downloading", fname)
        r = urllib.request.urlretrieve(url, outfp)


#########################

# fix_plot

import numpy as np

def stretch(array):
    
    min_percent = 2   # Low percentile
    max_percent = 98  # High percentile
    lo, hi = np.nanpercentile(array, (min_percent, max_percent))

    # Apply linear "stretch" - lo goes to 0, and hi goes to 1
    res_img = (array.astype(float) - lo) / (hi-lo)

    #clamp range to [0, 1] 
    res_img = np.maximum(np.minimum(res_img*1, 1), 0)

    return res_img

# Function to normalize the grid values
def normalize(array):
    """Normalizes numpy arrays into scale 0.0 - 1.0"""
    array_min, array_max = array.min(), array.max()

    return ((array - array_min)/(array_max - array_min))


#######

# get_corine_legend



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
    catdf_lim = get_limited_df()
    catdict = catdf_lim.to_dict()['Level4Eng']

    return catdict

##########################

#get_json_feature

import json

def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    return [json.loads(gdf.to_json())['features'][0]['geometry']]


########################

#make_falso_color_image


import rasterio

def read_band(s2, bandnumber):
    
    band = s2.read(bandnumber)
    # rescale
    band = band / 10000
    # remove all artifacts
    band[ band>1 ] = 1

    return band


import numpy as np

def make_false_color_stack(raster):

    nir = read_band(raster,4)
    red = read_band(raster,3)
    green = read_band(raster,2)

    nirs = stretch(nir)
    reds = stretch(red)
    greens = stretch(green)

    # Create RGB false color composite stack
    rgb = np.dstack((nirs, reds, greens))

    return rgb

##############################

#zonal_stats_percentage

def get_zonal_stats_percentage(zstats):

    zstat_perc = {}
    sum = 0
    total = zstats[0]['count']
    for key in zstats[0].keys():
        if not key == 'count':
            amount = zstats[0][key]
            perc=  round(amount/total *100)
            zstat_perc[key] = perc
            sum += perc
    
    return zstat_perc


#######################

def get_forest_codes():

    # Lets consider only vegetation
    vegetation = ['Broad-leaved forest on mineral soil',
    'Coniferous forest on mineral soil',
    'Coniferous forest on rocky soil',
    'Mixed forest on mineral soil',
    'Mixed forest on rocky soil']

    catdf_lim = get_limited_df()

    vegdf = catdf_lim[catdf_lim['Level4Eng'].isin(vegetation)]

    veglist = vegdf.index.to_list()

    return veglist

###########################

def create_forest_mask(corinearray,forestcodes):
    mask = (corinearray == int(forestcodes[0])) |  (corinearray == int(forestcodes[1])) | (corinearray == int(forestcodes[2])) | (corinearray == int(forestcodes[3])) | (corinearray == int(forestcodes[4]))
    
    # currently mask is boolean, but we rather want it binary:

    mask = mask.astype('uint8')
    
    return mask

###########################
import geopandas as gpd

def get_reprojected_shapefilename(rastercrs, shapefilename):
    df = gpd.read_file(shapefilename)
    df = df.to_crs(rastercrs)
    outname = os.path.join('data',os.path.splitext(os.path.basename(shapefilename))[0] + '_repr_32635.shp')
    df.to_file(driver = 'ESRI Shapefile', filename= outname)
    return outname