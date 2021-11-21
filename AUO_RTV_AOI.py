import cv2
import numpy as np

img_oringinal = cv2.imread("C:/Users/USER/Sublime Text 3 (3211)/python/image/PCB.jpg", 0)
cv2.imshow("img_oringinal", img_oringinal)

#======================================================================================RTV Defect抓取
#56~1428
img_oringinal_RTV = img_oringinal[0:57][0:1429]
#cv2.imshow("img_oringinal_RTV", img_oringinal_RTV)

a, img_oringinal_RTV_th = cv2.threshold(img_oringinal_RTV, 30, 255, cv2.THRESH_BINARY_INV)#RTV區域二值化(原黑-->白)
#cv2.imshow("img_oringinal_RTV_th", img_oringinal_RTV_th)

#for _ in range(9):
 #   img_erode = cv2.erode(img_oringinal_RTV_th, (5, 5))
  #  img_oringinal_RTV_th = img_erode
    
img_erode = cv2.erode(img_oringinal_RTV_th, (5, 5), iterations=8)#白被侵蝕
#cv2.imshow("img_erode", img_erode)


kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
for _ in range(10):
    img_dilate = cv2.dilate(img_erode, kernel)#白被膨脹
    img_erode = img_dilate
   
#img_dilate = cv2.dilate(img_erode, (5, 5), iterations=100)
#cv2.imshow("img_dilate", img_dilate)

defect_point_lst = []
a, b=cv2.findContours(img_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#print(a)
for num in a:
    defect_point_lst.append(num)
#print(defect_point_lst)

for j in range(len(defect_point_lst)):
    x, y, w, h = cv2.boundingRect(defect_point_lst[j])
    RTV_result = cv2.rectangle(img_oringinal_RTV, (x, y), (x+w, y+h), (255, 0, 0), 2)#框選出defect
#cv2.imshow("result1", RTV_result)

#================================================================================COF位置抓取
# img_oringinal已含RTV框選的圖了
a1, img_oringinal_th = cv2.threshold(img_oringinal, 120, 255, cv2.THRESH_BINARY)#30
cv2.imshow("img_oringinal_th", img_oringinal_th)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 1))
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 6))
img_erode = cv2.erode(img_oringinal_th, kernel, iterations=2)#白被侵蝕
cv2.imshow("img_erode", img_erode)
'''
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 12))
for _ in range(10):
    img_dilate = cv2.dilate(img_erode, kernel)
    img_erode = img_dilate
cv2.imshow("img_dilate", img_dilate)
'''
COF_Area_lst = []
a_1, b_1=cv2.findContours(img_erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

for num in a_1:
    COF_Area_lst.append(num)
#print(defect_point_lst)

for j in range(len(COF_Area_lst)):
    x, y, w, h = cv2.boundingRect(COF_Area_lst[j])
    if w > 300 and h > 300:
        COF_Area_result = cv2.rectangle(img_oringinal, (x, y), (x+w, y+h), (255, 0, 0), 2)#框出COF區域
cv2.imshow("COF_Area_result", COF_Area_result)

cv2.waitKey(0)
cv2.destroyAllWindows()

