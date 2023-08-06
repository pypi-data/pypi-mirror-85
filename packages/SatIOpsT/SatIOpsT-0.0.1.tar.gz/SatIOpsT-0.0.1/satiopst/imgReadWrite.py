import rasterio
import numpy

def imgRead(imgpath,mode="r"):
    """
    Read Satellite image as Numpy array and image metadata
    :param imgpath: Path to the satellite image.
    :param mode: Read only
    :return: Image as numpy array and image metadata.
    """
    with rasterio.open(imgpath,mode) as img:
        imgf=img.read()
        imgmeta=img.meta
    return imgf,imgmeta


def imgWrite(imgarray,filepath,imgmeta,mode="w",bands=1):
    """
    Export satellite image from numpy array to disk.
    :param imgarray: Numpy array of image.
    :param filepath: Output file path with name and file extention.
    :param imgmeta: Metadata of the image.
    :param mode: Write only.
    :param bands: Number of bands of the image.
    :return: Export the imagearray as image.
    """
    if bands==1:
        imgmeta["count"]=bands
        with rasterio.open(filepath,mode,**imgmeta) as imgc:
            imgc.write(imgarray,1)
    else:
        imgmeta["count"]=bands
        with rasterio.open(filepath,mode,**imgmeta) as imgc:
            imgc.write(imgarray)

