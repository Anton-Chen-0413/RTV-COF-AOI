import cv2

#threshold1=129 threshold2=129 Gauss_pram=1
#cv2.imshow('blurred', blurred)
#cv2.imshow('Input', image)
#cv2.moveWindow('Input', 1000, 100)#移動視窗位置(左上角X,Y+)
#cv2.imshow('blurred', blurred)
#cv2.moveWindow('blurred', 400, 100)#移動視窗位置(左上角X,Y+)

label_lst = []#輪廓的點位塞再list
rec_size = 20
rec_count = 5
Gauss_Rangelow,Gauss_Rangehigh = 1, 10
img_dir = 'C:/Users/USER/Sublime Text 3 (3211)/python/image/test3.png'

 
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

   

cv2.namedWindow('Result',0)
cv2.namedWindow('Canny',0)
cv2.createTrackbar('threshold1', 'Canny',50, 400, nothing)#30
cv2.createTrackbar('threshold2', 'Canny',100, 400, nothing)#150
cv2.createTrackbar('Gauss_pram', 'Canny',Gauss_Rangelow, Gauss_Rangehigh, nothing)#150

 
while (1):
    label_lst = []
    threshold1 = cv2.getTrackbarPos('threshold1', 'Canny')
    threshold2 = cv2.getTrackbarPos('threshold2', 'Canny')
    threshold3 = cv2.getTrackbarPos('Gauss_pram', 'Canny')
    image = cv2.imread(img_dir)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold3_odd = oddGauss(threshold3)
    blurred = cv2.GaussianBlur(gray, (threshold3_odd, threshold3_odd), 0)
    cv2.imshow('blurred', blurred)
    canny = cv2.Canny(blurred, threshold1, threshold2)
    contours, hierachy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#   print(len(contours[0]))
#   print(contours)
#   print(contours[0][1])


    for i in range(0, len(contours)):#取幾團偵測點位
#       print(contours[i])
        for j in range(0, len(contours[i]), rec_count):#取X，y點位                      
            label = contours[i][j][0]
            label_lst.append(label)
       
    for i in label_lst:#取點位框框
#       print(i[0])
        x1 = i[0]+rec_size
        y1 = i[1]+rec_size
        x2 = i[0]-rec_size
        y2 = i[1]-rec_size      
        Result = cv2.rectangle(blurred, (x2,y2), (x1,y1), (0,0,255), 1) # text background

 
    cv2.imshow('Result', Result)    
#   cv2.drawContours(img, contours,-1,(0,0,255), 3)
    cv2.imshow('Canny', canny)
    
    cv2.moveWindow('Canny', 100, 100)#移動視窗位置(左上角X,Y+)
    del image
    del blurred   
    if cv2.waitKey(1)==ord('q'):
        break

 
 

cv2.destroyAllWindows()

del cv2
