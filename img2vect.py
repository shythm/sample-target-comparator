import cv2 as cv
import numpy as np

def load_binary_image(path: str):
    img = cv.imread(path)

    # HSV로 변경
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # 명도(S)와 채도(V)가 20이상인 경우 색상(H) 값 평균 찾기
    msk = cv.inRange(hsv, (0, 20, 20), (179, 255, 255))

    h_val = hsv[:, :, 0]
    s_val = hsv[:, :, 1]
    v_val = hsv[:, :, 2]

    avg_h = np.mean(h_val[msk > 0])
    avg_s = np.mean(s_val[msk > 0])
    avg_v = np.mean(v_val[msk > 0])

    # 이미지 색 필터
    lw = (avg_h - 20, avg_s - avg_s // 20, avg_v - avg_s // 20) # 범위 값 설정
    up = (avg_h + 20, 255, 255)                                 # 범위 값 설정
    mask = cv.inRange(hsv, lw, up)
    img2 = cv.bitwise_and(img, img, mask=mask)

    # 이진화
    gr = cv.cvtColor(img2, cv.COLOR_RGB2GRAY)
    _, bi = cv.threshold(gr, 0, 100, cv.THRESH_BINARY)

    return bi

def get_graph_roi(img, connectivity=8):
    # stats: 추출된 객체의 위치(x, y), 가로세로 길이(w, h), 면적(area)
    cnt, _, stats, _ = cv.connectedComponentsWithStats(img, connectivity)

    # 가장 큰 면적을 가지는 객체 추출
    max_area = 0
    max_object = None

    for i in range(1, cnt): # 0번째는 원본 이미지
        x, y, w, h, area = stats[i]

        if area > max_area:
            max_object = stats[i]
            max_area = area

    return max_object

def image_to_vector(img):
    ret = []

    for i in range(img.shape[0]):
        # 픽셀이 보이는 위치(y)들을 구한 후, 해당 위치를 평균내어 리스트에 하나씩 추가
        ret.append(np.average(np.argwhere(img[:, i] > 0).reshape(-1)))

    return ret

def calc_error(arr1: list, arr2: list, method: str = 'mse'):
    vec1 = np.array(arr1)
    vec2 = np.array(arr2)

    if vec1.shape != vec2.shape:
        raise ValueError("두 배열의 차원이 같아야 합니다.")
    
    ret = None
    if method == 'mse':
        ret = np.mean((vec1 - vec2) ** 2)
    elif method == 'mae':
        ret = np.mean(np.abs(vec1 - vec2))
    elif method == 'rmse':
        ret = np.sqrt(np.mean(vec1 - vec2) ** 2)
    else:
        raise ValueError("지원되지 않는 방법입니다.")

    return ret