import cv2 as cv
import numpy as np



def centre_in_region(triangle,ext_contour):
    for point in triangle:
        if cv.pointPolygonTest(ext_contour,triangle['centre'],False)>=0:
        # if cv.pointPolygonTest(ext_contour,(point),False)>=0:
        
            return True
    return False    

