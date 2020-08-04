import cv2
import shutil

filename="result.png"
filepath = "raw/result.png"

img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
# print(img)
# cv2.imshow("result",img)

area = 0

ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
height, width = thresh.shape
for i in range(height):
    for j in range(width):
        if (thresh[i, j]) == 0:
            area += 1
print("area:    ", area)

# copy图片到3个文件夹
min = 100
max = 1000
if (area < min):
    shutil.copy(filepath, "without_cave")
elif (area > max):
    print("I am here !")
    shutil.copy(filepath, "with_cave")
else:
    shutil.copy(filepath, "unknow")

print(thresh)
cv2.imshow("bin", thresh)

f = open("result.txt", "w")
f.write(filename + " " + str(area))
f.close()

cv2.imwrite("binImg.jpg", thresh)
cv2.waitKey(0)
