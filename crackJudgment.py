import cv2

img = cv2.imread("result.png", cv2.IMREAD_GRAYSCALE)
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

print(thresh)
cv2.imshow("bin", thresh)

cv2.waitKey(0)
