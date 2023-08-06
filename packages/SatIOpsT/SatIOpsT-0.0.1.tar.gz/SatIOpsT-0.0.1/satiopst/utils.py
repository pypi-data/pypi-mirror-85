import rasterio
from rasterio.mask import mask
import geopandas
import numpy

def icrop(imgpath,shppath):
    """
    Crop satellite image using ESRI shapefile
    :param imgpath: Path to the satelllite image.
    :param shppath: Path to the ESRI ShapeFile.
    :return: Croped image as numpy array with same extent of original image.
    """
    shp=geopandas.read_file(shppath)
    img=rasterio.open(imgpath,"r")
    mask1,a=mask(img, shp.envelope)
    return mask1

def imask(imgpath,shppath,nodata=0):
    """
    Mask satellite image using ESRI shapefile
    :param imgpath: Path to the satelllite image.
    :param shppath: Path to the ESRI ShapeFile.
    :param nodata: Value for nodata or out of the area of interest.
    :return: Masked image as numpy array with same extent of original image.
    """
    shp=geopandas.read_file(shppath)
    img=rasterio.open(imgpath,"r")
    if nodata!=0:
        mask1,a=mask(img, shp["geometry"])
        mask1[mask1==0]=nodata
    else:
        mask1,a=mask(img, shp["geometry"])
    return mask1

def layerStack(imglist):
    """
    Stack satellite image bands.
    :param imglist: List of satellite image paths.
    :return: Stacked image as numpy array and metadata.
    """
    ilist=[]
    for i in imglist:
        with rasterio.open(i,"r") as im:
            im2=im.read(1)
            immeta=im.meta
        ilist.append(im2)
    ilist=numpy.asarray(ilist)
    immeta["count"]=ilist.shape[0]
    return ilist,immeta

