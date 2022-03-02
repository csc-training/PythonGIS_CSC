#!/usr/bin/env python3

import os
import rasterio
from rasterio.mask import mask
import fiona
from fiona.transform import transform_geom
import numpy as np
import glob


def download_with_url(url, outdir):
    S2SAFEfile = 0

    return S2SAFEfile


def find_bands(S2SAFEfile, pixelsize):
    
    bandlocation =  [S2SAFEfile,'*','*','IMG_DATA']
    

    bandpaths = {}
    for band in [2,3,4,8]:
        pathbuildinglist =  bandlocation + ['R' + str(pixelsize) + 'm','*' + str(band)+ '_' + str(pixelsize) +'m.jp2'] 
        bandpathpattern = os.path.join(*pathbuildinglist)
        bandpath = glob.glob(bandpathpattern)[0]
    
        bandpaths[band] = bandpath

    #type: dict[bandnumber] - bandpath
    return bandpaths

#bandpaths = find_bands("./data/S2B_MSIL2A_20210926T094029_N0301_R036_T35VLG_20210926T110446.SAFE",10)
#print(bandpaths)

def create_multiband_tif(bandpaths):


    outfilename = "./data/S2B_RGBNIR_20210926.tif"
    with rasterio.open(bandpaths[4]) as src:
        meta = src.meta
        crs = src.crs
        out_meta = meta.copy()
        out_meta.update({"driver": "GTiff","count":4})
    with rasterio.open(outfilename, "w", **out_meta) as dest:
        for i,band in enumerate(bandpaths.keys()):
            with rasterio.open(bandpaths[band]) as src:
                banddata = src.read(1)
                dest.write(banddata, i+1)

    return outfilename, crs

#mytif,crs= create_multiband_tif(bandpaths)
#print(mytif)
#mytif= "./data/S2B_RGBNIR_20210926.tif"
mytif = "./data/Clc2018_FI20m.tif"
#crs = "EPSG:32635"
#¤with rasterio.open(mytif) as data:
#    rastercrs = data.crs.to_string()

def read_shapefile():

    # creates 33 MB clipped tif
    with fiona.open("./data/seurasaari.shp", "r") as shapefile:
        polygons = [feature["geometry"] for feature in shapefile] #if feature['properties']['name'] == 'Helsinki']
        print(polygons)
        #polycrs = str(shapefile.crs['init']).upper()
    # following had 88 MB
    #with fiona.open("../L4/data/Helsinki_borders.shp", "r") as shapefile:
    #    polygons = [feature["geometry"] for feature in shapefile]

    return polygons#, polycrs

polygon = read_shapefile()
"""
# following does not work for whatever reason
def fix_crs(polygon, polycrs, rastercrs):
    print(polycrs)
    print(rastercrs)
    print(polygon)

    transformedpoly = transform_geom(polycrs, rastercrs, polygon)
    return transformedpoly

polycrs='EPSG:3067'
rastercrs='EPSG:32635'
fixedpolygon = fix_crs(polygon, polycrs, rastercrs)
"""

def clip_area(mytif, polygons):
    with rasterio.open(mytif) as src:
        out_image, out_transform = mask(src, polygons, crop=True)
        out_meta = src.meta
        out_meta.update({"driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform})

    with rasterio.open("./data/Clc2018_Seurasaari.tif", "w", **out_meta) as dest:
    #with rasterio.open("./data/S2B_RGBNIR_20210926_Helsinki.tif", "w", **out_meta) as dest:
        dest.write(out_image)

clip_area(mytif, polygon)