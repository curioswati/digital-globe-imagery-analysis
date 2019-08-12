"""
code reference: https://gis.stackexchange.com/questions/104362/how-to-get-extent-out-of-geotiff
"""
import gdal
import glob
import sys

from gdalconst import GA_ReadOnly

if len(sys.argv) < 3:
    print("please enter event(pre/post), image id and date")
    sys.exit(0)

event, container_id, date = sys.argv[1:]
tifs = glob.iglob('data/flooding-in-india/{}/{}_{}*.tif'.format(event, date, container_id))

for tif in tifs:
    data = gdal.Open(tif, GA_ReadOnly)
    geoTransform = data.GetGeoTransform()
    minx = geoTransform[0]
    maxy = geoTransform[3]
    maxx = minx + geoTransform[1] * data.RasterXSize
    miny = maxy + geoTransform[5] * data.RasterYSize
    print('{}: {}, {}, {}, {}'.format(tif, minx, miny, maxx, maxy))
    data = None
