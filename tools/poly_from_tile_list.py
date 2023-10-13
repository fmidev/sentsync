#!/usr/bin/python3

import numpy as np
import argparse, sys

from shapely.geometry import Polygon
from shapely.ops import unary_union
import shapely


parser = argparse.ArgumentParser(description = "Create multipolygon from a list of tiles (tx,ty).")
parser.add_argument('-t', '--tiles', action='append', help = "CSV file with tx and ty of Sentinel tiles. Can be used multiple times. First line is header: ty,tx.")

args = parser.parse_args()

if not args.tiles:
    print("No tile list given")
    sys.exit()

res=1/1008.0
tsize=960

#tx=198
#ty=36

polygons = []
print("Reading tiles")
for tilelist in args.tiles:
    try:
        with open(tilelist,"r") as f:
            f.readline()    # header
            for line in f:
                try:
                    ty, tx = list(map(int,line.replace('\n','').split(',')))
                except:
                    print(tx,ty," failed")

                lat=np.arange(80-res/2.0,20,-res,dtype=float)
                lon=np.arange(-180+res/2.0,180,res,dtype=float)

                tlat=lat[(ty-1)*tsize:ty*tsize]
                tlon=lon[(tx-1)*tsize:tx*tsize]

                poly = Polygon([(tlon[0],tlat[0]), (tlon[-1],tlat[0]), (tlon[-1],tlat[-1]), (tlon[0],tlat[-1]), (tlon[0],tlat[0]) ])
                poly = Polygon([(tlon[0]-res,tlat[0]+res), (tlon[-1]+res,tlat[0]+res), (tlon[-1]+res,tlat[-1]-res), (tlon[0]-res,tlat[-1]-res), (tlon[0]-res,tlat[0]+res) ])
                print(poly)
                polygons.append(poly)
                

    except Exception as e:
        print("Cannot process %s" % tilelist)
        print(e)
        print("Skipped")

print("Merging")
polygons = shapely.unary_union(polygons).wkt

print(polygons)
