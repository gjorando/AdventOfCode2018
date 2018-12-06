#!/usr/bin/env python3

import numpy as np
from PIL import Image

def voronoi(points,shape):
    """
        Inspired by https://gist.github.com/bert/1188638#file-voronoi-py
    """
    depthmap = np.ones(shape,np.float)*1e308
    colormap = np.zeros(shape,np.int)

    def hypot(X,Y):
        return abs(X-x) + abs(Y-y)

    for i,(x,y) in enumerate(points):
        paraboloid = np.fromfunction(hypot,shape)
        colormap = np.where(paraboloid < depthmap,i,colormap)
        depthmap = np.where(paraboloid <
depthmap,paraboloid,depthmap)

    return colormap

def draw_map(colormap, points=None):
    shape = colormap.shape
    colormap = colormap+1
   
    palette = (np.random.randint(0, 2**24, size=len(np.unique(colormap)))<<8) | 0xFF
    if not points is None:
        for (x,y) in points:
            colormap[x-1:x+2,y-1:y+2] = 0

    palette = np.insert(palette, 0, 0x000000FF)

    colormap = np.transpose(colormap)
    pixels = np.empty(colormap.shape+(4,),np.int8)

    pixels[:,:,3] = palette[colormap] & 0xFF
    pixels[:,:,2] = (palette[colormap]>>8) & 0xFF
    pixels[:,:,1] = (palette[colormap]>>16) & 0xFF
    pixels[:,:,0] = (palette[colormap]>>24) & 0xFF
    
    image = Image.frombytes("RGBA",shape,pixels)
    image.show()

X = np.genfromtxt("input", delimiter=",", dtype=int)

margin = 50
x_min, y_min = X.min(0)
x_max, y_max = X.max(0)
frame = (margin + x_max-x_min, margin + y_max-y_min)

# We center the points
X[:,0] = X[:,0] - x_min + (frame[0]-(x_max-x_min))/2
X[:,1] = X[:,1] - y_min + (frame[1]-(y_max-y_min))/2

voronoi_grid = voronoi(X, frame)

infinite_shapes = np.unique(np.concatenate((voronoi_grid[0,:], voronoi_grid[-1,:], voronoi_grid[:,-1], voronoi_grid[:,0])))

_, shape_sizes = np.unique(voronoi_grid, return_counts = True)

masked_sizes = np.ma.array(shape_sizes, mask=False)
masked_sizes.mask[infinite_shapes] = True

result = masked_sizes.max()

print("Answer for puzzle #11: {}".format(result))

draw_map(voronoi_grid, X)
