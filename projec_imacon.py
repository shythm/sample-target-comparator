import cv2 as cv
import numpy as np

img = cv.imread("C:/Users/aaa/Desktop/projec/sample/common/commontg.png")


# HSV로 변경
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# s와 v (명도와 채도) 0 이상인 경우 h(색) 값 평균 찾기
msk = cv.inRange(hsv, (0, 20, 20), (179, 255, 255))
h_val = hsv[:,:,0]
avg = np.mean(h_val[msk > 0])

# 이미지 색 필터
lw = np.array([avg-20, 80, 80])
up = np.array([avg+20, 255, 255])
mask = cv.inRange(hsv, lw, up)
img2 = cv.bitwise_and(img, img, mask=mask)

# 이진화
gr = cv.cvtColor(img2, cv.COLOR_RGB2GRAY)
ret, bi = cv.threshold(gr, 0, 100, cv.THRESH_BINARY)

# 이미지의 픽셀 값 읽기
pixel_values = bi.tolist()

# 분석 결과 출력
print(pixel_values)
cv.imshow('grah', img2)
cv.imshow('graph', bi)
cv.waitKey(0)
cv.destryAllWindows