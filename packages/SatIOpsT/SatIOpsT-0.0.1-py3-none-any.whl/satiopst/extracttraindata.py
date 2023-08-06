from .imageFrame import imagetoframe
import rasterio
from rasterio.mask import mask
import geopandas
import pandas


def extractbypolygon(imgpath,shppath,mode="r",class_col=None):
    """
    Extract pixel-wise satellite image values according to class shapefile.
    :param imgpath: Path to the Satellite image.
    :param shppath: Path to the ESRI ShapeFile.
    :param mode: Read only.
    :param class_col: Name of the column containing Class ID.
    :return: Table containing spectral information and corosponding class.
    """
    if class_col==None:
        print("Please enter the column name containing class information")
    else:
        img=rasterio.open(imgpath,mode)
        shp=geopandas.read_file(shppath)
        clsid=list(shp[class_col].unique())
        tdataf=pandas.DataFrame()
        for i in clsid:
            shpm=shp[shp[class_col]==i]
            maski,t=mask(img,shpm["geometry"])
            df=imagetoframe(maski)
            df = df[(df.T != 0).any()]
            df[class_col]=int(i)
            tdataf=tdataf.append(df)
            tdataf=tdataf.reset_index(drop=True)
        return tdataf
