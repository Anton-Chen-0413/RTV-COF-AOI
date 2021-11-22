# RTV-COF-AOI
RTV &amp; COF Defect detection
import cv2
import numpy as np

def nothing(x):
    pass

def oddGauss(threshold3):
    if threshold3 % 2 !=0:
        threshold3_odd = threshold3
        return threshold3_odd
    elif threshold3 == 0:
        return 1
    else:
        threshold3_odd = threshold3 -1
        return threshold3_odd
    

cv2.namedWindow('Canny',0)
cv2.createTrackbar('Gausskernel', 'Canny',1, 50, nothing)#30
cv2.createTrackbar('Binary_TH', 'Canny', 1, 100, nothing)#150
cv2.createTrackbar('Rrode1', 'Canny',1, 50, nothing)#150
cv2.createTrackbar('Rrode2', 'Canny',1, 50, nothing)#150
cv2.createTrackbar('erodeloop', 'Canny',1, 50, nothing)#150
cv2.createTrackbar('dilate1', 'Canny',1, 50, nothing)#150
cv2.createTrackbar('dilate2', 'Canny',1, 50, nothing)#150
cv2.createTrackbar('dilateloop', 'Canny',1, 50, nothing)#150

while 1:    
    Gausskernel = cv2.getTrackbarPos('Gausskernel', 'Canny')
    Binary_TH = cv2.getTrackbarPos('Binary_TH', 'Canny')
    Rrode1 = cv2.getTrackbarPos('Rrode1', 'Canny')
    Rrode2 = cv2.getTrackbarPos('Rrode2', 'Canny')
    erodeloop = cv2.getTrackbarPos('erodeloop', 'Canny')
    dilate1 = cv2.getTrackbarPos('dilate1', 'Canny')
    dilate2 = cv2.getTrackbarPos('dilate2', 'Canny')
    dilateloop = cv2.getTrackbarPos('dilateloop', 'Canny')
    
    
    threshold3_odd = oddGauss(Gausskernel)
    Binary_TH_odd = oddGauss(Binary_TH)
    Rrode1_odd = oddGauss(Rrode1)
    Rrode2_odd = oddGauss(Rrode2)
    dilate1_odd = oddGauss(dilate1)
    dilate2_odd = oddGauss(dilate2)
    
    
    img_original = cv2.imread("D:/T02Tufft.jpg", 0)    
    #===============================================================高斯
    img_original_g = img_original 
    
    
    for _ in range(10):
        img_original1 = cv2.GaussianBlur(img_original_g, (threshold3_odd, threshold3_odd), 0)
        img_original_g = img_original1
    
    x = 14734
    y = 0
    w = 33538-14734#18804
    h = 817
    crop_img = img_original[y:y+h, x:x+w]
    
    #cv2.imshow("crop_img", crop_img)
    #img_original_RTV = cv2.resize(crop_img, (1880, 81), interpolation=cv2.INTER_AREA)
    
    x_RTV = 14734
    y_RTV = 0
    w_RTV = 33538-14734#18804
    h_RTV = 83
    crop_img_RTV = img_original[y_RTV:y_RTV+h_RTV, 14734:33538]
    
#    cv2.imshow("crop_img_RTV", crop_img_RTV)
    
    #===============================================================#RTV區域二值化(原黑-->白)
    a, crop_img_RTV_th = cv2.threshold(crop_img_RTV, Binary_TH_odd, 255, cv2.THRESH_BINARY_INV)
#    cv2.imshow("crop_img_RTV_th", crop_img_RTV_th)
    
    #=================================================================#白被侵蝕
    
    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (Rrode1_odd, Rrode2_odd))
    crop_img_RTV_th_erode = crop_img_RTV_th
    for _ in range(erodeloop):
        img_erode = cv2.erode(crop_img_RTV_th_erode, kernel1)
        crop_img_RTV_th_erode = img_erode
    #print(img_erode.shape)
    
    #=================================================================#白被膨脹  
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (dilate1_odd, dilate2_odd))
    crop_img_RTV_th_dilate = img_erode
    for _ in range(dilateloop):
        img_dilate = cv2.dilate(crop_img_RTV_th_dilate, kernel)
        crop_img_RTV_th_dilate = img_dilate
      
    #=================================================================#框選defect
    defect_point_lst = []
    a, b=cv2.findContours(img_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #print(a)
    for num in a:
        defect_point_lst.append(num)
    #print(defect_point_lst)
    RTV_result = 0
    for j in range(len(defect_point_lst)):
        x, y, w, h = cv2.boundingRect(defect_point_lst[j])
        
        RTV_result = cv2.rectangle(crop_img_RTV, (x, y), (x+w, y+h), (255, 255, 255), 3)#框選出defect
#    print(type(RTV_result))
    #RTV_result_resize = cv2.resize( RTV_result, (1880, 8), interpolation=cv2.INTER_AREA)
    
    cv2.imshow("RTV_result_1", RTV_result[0:82, 0:2001])
    cv2.imshow("RTV_result_2", RTV_result[0:82, 2001:4000])
    cv2.imshow("RTV_result_3", RTV_result[0:82, 4000:6000])
    cv2.imshow("RTV_result_4", RTV_result[0:82, 6000:8200])
    cv2.imshow("RTV_result_5", RTV_result[0:82, 10200:12200])
    cv2.imshow("RTV_result_6", RTV_result[0:82, 12200:14200])
    cv2.imshow("RTV_result_7", RTV_result[0:82, 14200:16200])
    cv2.imshow("RTV_result_8", RTV_result[0:82, 16200:18804])
    
    
    
    
    if cv2.waitKey(1)==ord('q'):
        cv2.imwrite("D:\TuffyDetect\RTV_result.jpg", RTV_result)
        break

#cv2.imwrite("D:\TuffyDetect\crop_img_RTV.jpg", crop_img_RTV)
#cv2.imwrite("D:\TuffyDetect\crop_img_RTV_th.jpg", crop_img_RTV_th)
#cv2.imwrite("D:\TuffyDetect\img_erode.jpg", img_erode)
#cv2.imwrite("D:\TuffyDetect\img_dilate.jpg", img_dilate)
#cv2.imwrite("D:\TuffyDetect\RTV_result.jpg", RTV_result)








































cv2.destroyAllWindows()
