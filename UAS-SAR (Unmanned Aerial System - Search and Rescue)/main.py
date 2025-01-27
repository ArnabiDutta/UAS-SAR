import cv2 as cv
import numpy as np
from pointpolytest import *
from Rplanning import *

prlist=[]
prioritylist=[]
no_houses=[]


def create_masks(image):
    hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    
    red_lower = np.array([0, 50, 50])
    red_upper = np.array([10, 255, 255])
    
    blue_lower = np.array([100, 50, 50])
    blue_upper = np.array([130, 255, 255])
    
    green_lower = np.array([36, 50, 50])
    green_upper = np.array([70, 255, 255])
    
    brown_lower = np.array([10, 100, 20])
    brown_upper = np.array([20, 255, 200])
    
    mask_red = cv.inRange(hsv_image, red_lower, red_upper)
    mask_blue = cv.inRange(hsv_image, blue_lower, blue_upper)
    mask_green = cv.inRange(hsv_image, green_lower, green_upper)
    mask_brown = cv.inRange(hsv_image, brown_lower, brown_upper)

    return mask_red, mask_blue, mask_green, mask_brown

def overlay(image, mask, overlay_color):
    colored_image = np.copy(image)
    colored_image[mask > 0] = overlay_color
    return colored_image

def houses(image, mask_red, mask_blue):
    # red_priority = 1
    # blue_priority = 2

    # grey=cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    # blurred=cv.GaussianBlur(grey,(7,7),0)
    # edges=cv.Canny(blurred,50,150)
    
    contours_red, _ = cv.findContours( mask_red, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours_blue, _ = cv.findContours( mask_blue, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # contours,_=cv.findContours(edges,cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)



    red_houses= 0
    blue_houses = 0
    red_centroids=[]
    blue_centroids=[]
    centroids=[]
    
    for rcontour in contours_red:
        area=cv.contourArea(rcontour)
        approx = cv.approxPolyDP(rcontour, 0.04 * cv.arcLength(rcontour, True), True)

        if area>200 and len(approx)==3:
            cv.drawContours(image,[rcontour],-1,(0,0,0),5)
            red_houses+=1

            M=cv.moments(approx)
            cXr = int(M["m10"] / M["m00"])
            cYr = int(M["m01"] / M["m00"])
            cv.circle(image, (cXr, cYr), 5, (255, 255, 255), -1)
            red_centroids.append({'centre':(cXr,cYr)})


    for bcontour in contours_blue:
        area=cv.contourArea(bcontour)
        approx = cv.approxPolyDP(bcontour, 0.04 * cv.arcLength(bcontour, True), True)

        if area>200 and len(approx)==3:
            cv.drawContours(image,[bcontour],-1,(0,0,0),5)
            blue_houses+=1

            M=cv.moments(approx)
            cXb = int(M["m10"] / M["m00"])
            cYb = int(M["m01"] / M["m00"])
            cv.circle(image, (cXb, cYb), 5, (255, 255, 255), -1)
            blue_centroids.append({'centre':(cXb,cYb)})

    centroids=red_centroids+blue_centroids


    # centroids=[]
    # for contour in contours:
    #     # area=cv.contourArea(contour)
    #     # approx=cv.approxPolyDP(contour,0.04 * cv.arcLength(contour, True), True)
    #     # if len(approx)==3 and area>200:
    #     #     cv.drawContours(image,[contour],-1,(0,0,0),5)
    #         M=cv.moments(mask_blue)
    #         cX = int(M["m10"] / M["m00"])
    #         cY = int(M["m01"] / M["m00"])
    #         cv.circle(image, (cX, cY), 5, (255, 255, 255), -1)
    #         centroids.append({'centre':(cX,cY)})
    # print(len(red_centroids),len(blue_centroids))
    return red_houses, blue_houses, red_centroids, blue_centroids,centroids


def process_image(image):
    # imgresize=cv.resize(image,(400,600))
    image=cv.GaussianBlur(image,(7,7),0)
    mask_red, mask_blue, mask_green, mask_brown = create_masks(image)
    
    image = overlay(image, mask_brown, [0, 255, 255])  # Yellow on brown
    image = overlay(image, mask_green, [255, 255, 0])  # Cyan on green
    
    red_houses, blue_houses,_,_,_= houses(image, mask_red, mask_blue)
    # print((red_houses),(blue_houses))
    

    green_contours,_=cv.findContours(mask_green,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    brown_contours,_=cv.findContours(mask_brown,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)

    _,_,red_centroids,blue_centroids,centroids=houses(image,mask_red,mask_blue)



    Hrg=0
    Hrb=0

    Hblg=0
    Hblb=0


    for T in red_centroids:
        for green_contour in green_contours:
            if centre_in_region(T,green_contour):
                Hrg+=1
            
        for brown_contour in brown_contours:
            if centre_in_region(T,brown_contour):
                Hrb+=1
                break        
    for T in blue_centroids:
        for green_contour in green_contours:
            if centre_in_region(T,green_contour):
                Hblg+=1
        
        for brown_contour in brown_contours:
            if centre_in_region(T,brown_contour):
                Hblb+=1
                break

    # print(f"Red Houses in green region={Hrg}")
    # print(f"Red Houses in brown region={Hrb}")
    # print(f"Blue Houses in green region={Hblg}")
    # print(f"Blue Houses in brown region={Hblb}")  


    
    
    # return       

    # Hg, Hb = count_houses_on_region(mask_green, mask_brown, red_houses, blue_houses)
    
    # priority_sums = sum_priority(red_houses, blue_houses)
    
    # print("Number of houses on green region:", Hg)
    # print("Number of houses on brown region:", Hb)
    # print("Sum of priorities (Green region, Brown region):", priority_sums)
    
    return image,Hrg,Hrb,Hblg,Hblb,centroids

for i in range(1,12):
    path = "E:\\Kardarshev Scale\\UASVictory\\TestCasesUAS\\uas takimages\\uas takimages\\"
    path = path + str(i) + ".png"
    image = cv.imread(path) 
    result_image,Hrg,Hrb,Hblg,Hblb,centroids= process_image(image)

    no_burnt=Hrb+Hblb
    no_green=Hrg+Hblg

    no_houses.append([no_burnt,no_green])


    priority_red=1
    priority_blue=2

    # total priority of houses on green grass
    Pg=int((priority_red*Hrg)+(priority_blue*Hblg))

    # total priority of houses on burnt grass
    Pb=int((priority_red*Hrb)+(priority_blue*Hblb))

    prioritylist.append([Pb,Pg])
    # rescue_ratio 
    Pr=Pb/Pg

    prlist.append(Pr)
    # print=centroids

    path = nearest_neighbor(centroids)
    draw_path(result_image, path)

    # path, total_distance = nearest_neighbor_path(centroids, result_image)
    # print("Path:", path)
    # print("Total Distance:", total_distance)
    # cv.imshow("Path on Image", image)
    # combined_image = cv.hconcat(result_image)

    cv.imshow(('Result'+str(i)), result_image)
    cv.waitKey(500)
    cv.destroyAllWindows()


print('no_houses=',no_houses)
print("priority_houses = ", prioritylist)
print("Priority Ratio = ", prlist)



dict={}
for i in range(len(prlist)):
    dict[('image'+str(i+1))]=prlist[i]

keys=list(dict.keys())
values=list(dict.values())
sorted_values_index=np.argsort(values)
sorted_dict={keys[i]:values[i] for i in sorted_values_index}

sorted_images=list(sorted_dict.keys())
print("sequence in terms of rescue ratio in descending order=",sorted_images[::-1])









