# Rplanning.py
import cv2 as cv
import numpy as np
import math

def euclidean_distance(point1, point2):
  
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def nearest_neighbor(centroids):
  
    if len(centroids) == 0:
        return []

    path = [centroids[0]['centre']]
    visited = set(path)


    while len(visited) < len(centroids):
        last_node = path[-1]
        nearest = None
        min_distance = float('inf')

        for centroid in centroids:
            node = centroid['centre']
            if node not in visited:
                distance = euclidean_distance(last_node, node)
                if distance < min_distance:
                    min_distance = distance
                    nearest = node

        
        path.append(nearest)
        visited.add(nearest)

    return path

def draw_path(image, path):
  
    for i in range(len(path) - 1):
        cv.line(image, path[i], path[i + 1], (0, 255, 0), 3)  
    
    cv.line(image, path[-1], path[0], (0, 255, 0), 3)