import rasterio
import numpy as np
from xml.dom import minidom

# extract the visible red and nir bands

imageFile = "20171026_231256_1025_3B_AnalyticMS.tif"
metadataFile = "20171026_231256_1025_3B_AnalyticMS_metadata.xml"

def calcNDVI(image, metadata):
    # Load red and NIR bands
    with rasterio.open(image) as src:
        bandRed = src.read(3)
    with rasterio.open(image) as src:
        bandNIR = src.read(4)

    # Normalise to TOA reflectance
    xmldoc = minidom.parse(metadata)
    nodes = xmldoc.getElementsByTagName("ps:bandSpecificMetadata")

    # xml parser refers to bands by number 1-4
    coeffs = {}
    for node in nodes:
        bn = node.getElementsByTagName("ps:bandNumber")[0].firstChild.data
        if bn in ['1', '2', '3', '4']:
            i = int(bn)
            value = node.getElementsByTagName("ps:reflectanceCoefficient")[0].firstChild.data
            coeffs[i] = float(value)

    bandRed = bandRed * coeffs[3] # mulitply band by coefficients
    bandNIR = bandNIR * coeffs[4] # mulitply band by coefficients

    # Perform the NDVI calculation
    np.seterr(divide="ignore", invalid='ignore') # allow div by zero
    ndvi = (bandNIR.astype(float) - bandRed.astype(float)) / (bandNIR + bandRed) # the NDVI calc

    # Save the imageFile
    # Set the spatial extents of out image to mirror the input
    kwargs = src.meta
    kwargs.update(dtype=rasterio.float32, count=1)

    # write the file
    with rasterio.open("NDVI_"+imageFile, 'w', **kwargs) as dst:
        dst.write_band(1, ndvi.astype(rasterio.float32))
        dst.close()

calcNDVI(imageFile, metadataFile)
