import numpy
import pandas

def imagetoframe(imgarray):
    """
    Convert  image numpy.array to pandas dataframe.
    :param imgarray: Image as Numpy array
    :return: Return as dataframe
    """
    imlist=[] # Blank list to store 1D array
    for i in range(imgarray.shape[0]):
        i2=imgarray[i].flatten() # Convert 2D array to 1D array
        imlist.append(i2) # Append to list
        imga=numpy.asarray(imlist) # Convert to array
        imgat=imga.transpose() # Transpose matrix for daataframe convertion
        satdf=pandas.DataFrame(imgat)
    return satdf

def frametoimage(imgframe,imgmeta):
    """
    Convert image from pandas dataframe to numpy array
    :param imgframe: Image dataframe.
    :param imgmeta: Metadata of the raw satellite image.
    :return: From image dataframe to numpy array.
    """
    width=imgmeta["width"]
    height=imgmeta["height"]
    cou=len(imgframe.columns)
    narray=imgframe.to_numpy()
    if cou==1:
        tm=narray.transpose()
        rs=tm.reshape(height,width)
    else:
        tm=narray.transpose()
        iml=[]
        for i in range(tm.shape[0]):
            band=tm[i,:]
            band=band.reshape(height,width)
            iml.append(band)
        rs=numpy.asarray(iml)
    return rs
