#!/usr/bin/env python3

import numpy as np
from PIL import Image

def sum_distances(points,shape):
    answer = np.zeros(shape,np.int)

    def hypot(X,Y):
        return abs(X-x) + abs(Y-y)

    for i,(x,y) in enumerate(points):
        answer+= np.fromfunction(hypot,shape, dtype=int)

    return answer

X = np.genfromtxt("input", delimiter=",", dtype=int)

limit = 10000

margin = 50
x_min, y_min = X.min(0)
x_max, y_max = X.max(0)
frame = (margin + x_max-x_min, margin + y_max-y_min)

# We center the points
X[:,0] = X[:,0] - x_min + (frame[0]-(x_max-x_min))/2
X[:,1] = X[:,1] - y_min + (frame[1]-(y_max-y_min))/2

distances = sum_distances(X, frame)

masked_distances = np.ma.array(distances, mask=False)
distances_mask = distances >= limit
masked_distances.mask[distances_mask] = True

mask_bytes = (1-distances_mask)

pixels = np.zeros((frame[1], frame[0], 4), np.int8)

pixels[:,:,3] = 0xFF
pixels[:,:,2] = mask_bytes.transpose().astype(np.int8)*0xFF
pixels[:,:,1] = pixels[:,:,2]
pixels[:,:,0] = pixels[:,:,2]

image = Image.frombytes("RGBA", frame, pixels)
image.show()

result = np.sum(mask_bytes)

print("Answer for puzzle #12: {}".format(result))
