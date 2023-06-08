import img2vect
import cv2 as cv
import numpy as np

target = img2vect.load_binary_image('./images/target_a.png')
x, y, w, h, _ = img2vect.get_graph_roi(target, connectivity=8)
target_crop = target[y : y + h, x : x + w]
target_w = target_crop.shape[0]
target_h = target_crop.shape[1]

sample = img2vect.load_binary_image('./images/sample_a_01.jpeg')
x, y, w, h, _ = img2vect.get_graph_roi(sample, connectivity=8)
sample_crop = sample[y : y + h, x : x + w]
sample_crop = cv.resize(sample_crop, (target_h, target_w))
# k = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
# sample_crop = cv.erode(sample_crop, k)

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

print(target_crop)
vec1 = img2vect.image_to_vector(target_crop)
print(vec1, len(vec1))
print(sample_crop)
vec2 = img2vect.image_to_vector(sample_crop)
print(vec2, len(vec2))
print(calc_error(vec1, vec2, method='rmse'))

cv.imshow('img1', target_crop)
cv.imshow('img2', sample_crop)
cv.waitKey()
cv.destroyAllWindows()
