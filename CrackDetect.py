import cv2
import math
import numpy as np
import scipy.ndimage

def orientated_non_max_suppression(mag, ang):
    ang_quant = np.round(ang / (np.pi/4)) % 4
    winE = np.array([[0, 0, 0],[1, 1, 1], [0, 0, 0]])
    winSE = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    winS = np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]])
    winSW = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]])

    magE = non_max_suppression(mag, winE)
    magSE = non_max_suppression(mag, winSE)
    magS = non_max_suppression(mag, winS)
    magSW = non_max_suppression(mag, winSW)

    mag[ang_quant == 0] = magE[ang_quant == 0]
    mag[ang_quant == 1] = magSE[ang_quant == 1]
    mag[ang_quant == 2] = magS[ang_quant == 2]
    mag[ang_quant == 3] = magSW[ang_quant == 3]
    return mag

def non_max_suppression(data, win):
    data_max = scipy.ndimage.filters.maximum_filter(data, footprint=win, mode='constant')
    data_max[data != data_max] = 0
    return data_max

def crackDetect(f):
    # start calulcation
    gray_image = cv2.imdecode(np.fromfile(f,dtype=np.uint8),cv2.IMREAD_GRAYSCALE)

    #cv2.imshow(gray_image)

    with_nmsup = True  # apply non-maximal suppression
    fudgefactor = 1.3  # with this threshold you can play a little bit
    sigma = 21  # for Gaussian Kernel
    kernel = 2 * math.ceil(2 * sigma) + 1  # Kernel size


    print("gray_image:")
    print(gray_image)

    gray_image = gray_image / 255.0
    blur = cv2.GaussianBlur(gray_image, (kernel, kernel), sigma)
    gray_image = cv2.subtract(gray_image, blur)

    # compute sobel response
    sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
    mag = np.hypot(sobelx, sobely)
    ang = np.arctan2(sobely, sobelx)

    # threshold
    threshold = 4 * fudgefactor * np.mean(mag)
    mag[mag < threshold] = 0

    # either get edges directly
    if with_nmsup is False:
        mag = cv2.normalize(mag, 0, 255, cv2.NORM_MINMAX)
        kernel = np.ones((5, 5), np.uint8)
        result = cv2.morphologyEx(mag, cv2.MORPH_CLOSE, kernel)
        cv2.imshow('im', result)

        print("result")
        print(result)

        cv2.waitKey(3)

        sum = 0

        height = result.shape[0]  # 将tuple中的元素取出，赋值给height，width，channels
        width = result.shape[1]

        for row in range(height):  # 遍历每一行
            for col in range(width):  # 遍历每一列
                sum += result[row][col]

        return (sum)


    # or apply a non-maximal suppression
    else:

        # non-maximal suppression
        mag = orientated_non_max_suppression(mag, ang)
        # create mask
        mag[mag > 0] = 255
        mag = mag.astype(np.uint8)

        kernel = np.ones((5, 5), np.uint8)
        result = cv2.morphologyEx(mag, cv2.MORPH_CLOSE, kernel)

        cv2.imshow('im', result)

        print("result")
        print(result)

        cv2.waitKey(3)

        sum = 0

        height = result.shape[0]  # 将tuple中的元素取出，赋值给height，width，channels
        width = result.shape[1]

        for row in range(height):  # 遍历每一行
            for col in range(width):  # 遍历每一列
                sum += result[row][col]

        return (sum)


if __name__ == '__main__':
    f='F:/crackDetect.jpg'  #"C:/Users/10942/Desktop/路面图片/表面微裂纹/PS1_586.jpg" #
    main=crackDetect(f)
    print("main:    "+main.__str__())
