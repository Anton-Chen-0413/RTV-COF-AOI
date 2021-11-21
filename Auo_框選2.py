import cv2
import numpy as np


img1 = cv2.imread("C:/Users/USER/Sublime Text 3 (3211)/python/image/test3.png", 0)
img1_1 = cv2.imread("C:/Users/USER/Sublime Text 3 (3211)/python/image/test3.png", 0)
cv2.imshow("m1_1原圖", img1_1)#原圖
print(type(img1_1))

img2 = cv2.Canny(img1_1, 50, 10) #偵測邊緣後
cv2.imshow("m2偵測邊緣後", img2)

a, b = cv2.findContours(img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) 
print(a, b)
print("========================")
print(len(a))
print(a[0])
print(len(a[0]))
n = 0
value_set = 30
for i in range(0, len(a)):
	for j in range(0, len(a[0]) - len(a[0]) % value_set, value_set):
		#x, y, w, h = cv2.boundingRect(a[i])
		#print(x, y, w, h)
		x = a[i][j][0][0]
		y = a[i][j][0][1]
		n += 1		
		color_lst = []
		for py in range(y-15, y+16):
			color_lst1 = []
			for px in range(x-15, x+16):
				color_lst1.append(img1[py, px])
			color_lst.append(color_lst1)
		defect_img = np.array(color_lst)
		cv2.imwrite("C:/Users/USER/Sublime Text 3 (3211)/python/image/Auotest/{}.png".format(n), defect_img)
		img3 = cv2.rectangle(img1_1, (x-15, y-15), (x+15, y+15), (0, 0, 255), 1)

cv2.imshow("m3框選後", img3)#框選後
print("==============")
print(defect_img)
cv2.imshow("defect_img", defect_img)
print(n)

cv2.waitKey(0)
cv2.destroyAllWindows()
