import cv2 as cv
import numpy as np

img = cv.imread("./samples/001.jpeg")

img_h, img_w, _ = img.shape

# HSV로 변경
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# s와 v (명도와 채도) 20 이상인 경우 h(색) 값 평균 찾기
msk = cv.inRange(hsv, (0, 20, 20), (179, 255, 255))
h_val = hsv[:,:,0]
s_val = hsv[:,:,1]
v_val = hsv[:,:,2]

avg_h = np.mean(h_val[msk > 0])
avg_s = np.mean(s_val[msk > 0])
avg_v = np.mean(v_val[msk > 0])

# 이미지 색 필터
lw = np.array([avg_h - 20, avg_s - avg_s//20, avg_v - avg_s//20]) # 범위 값 설정
up = np.array([avg_h + 20, 255, 255])                             # 범위 값 설정
mask = cv.inRange(hsv, lw, up)
img2 = cv.bitwise_and(img, img, mask=mask)

# 이진화
gr = cv.cvtColor(img2, cv.COLOR_RGB2GRAY)
ret, bi = cv.threshold(gr, 0, 100, cv.THRESH_BINARY)

# 연속성 판단 함수
def check_pixel_connectivity(image):
    _, labels, stats, _ = cv.connectedComponentsWithStats(image, connectivity=8)
    connectivity_threshold = img_w * 50                          # 범위 값 설정

    connected_images = []
    for i in range(1, len(stats)):
        if stats[i][-1] >= connectivity_threshold:
            connected_images.append(labels == i)

    return connected_images

connected_images = check_pixel_connectivity(bi)

for i, connected_image in enumerate(connected_images):
    rt_img = connected_image.astype(np.uint8) * 255


# 이미지의 픽셀 값 읽기
pixel_values = rt_img.flatten().tolist()

# 분석 결과 출력
#print(pixel_values)
#cv.imshow('grah', img2)
print(img_w)
cv.imshow('graphjh', bi)
cv.imshow('graph', rt_img)
cv.waitKey(0)
cv.destryAllWindows