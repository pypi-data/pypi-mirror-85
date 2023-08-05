import cv2
from mss import mss
import numpy as np

__all__ = [ 
            '讀取圖片灰階', '讀取圖片彩色', '顯示圖片', '等待按鍵',
            '關閉所有圖片', '儲存圖片', '開啟影像擷取', '擷取單張影像',
            '彩色轉灰階', '灰階轉彩色', '左右翻轉', '上下翻轉', '上下左右翻轉',
            '擷取螢幕灰階', '畫灰階矩形',
            ]





### Custom Exceptions
class ImageReadError(Exception):
    def __init__(self, value):
        message = f"無法讀取圖片檔 (檔名:{value})"
        super().__init__(message)

class ImageWriteError(Exception):
    def __init__(self, value):
        message = f"無法儲存圖片檔 (檔名:{value})"
        super().__init__(message)

class CameraOpenError(Exception):
    def __init__(self, value=''):
        message = f"攝影機開啟錯誤 {value}"
        super().__init__(message)     

class CameraReadError(Exception):
    def __init__(self, value=''):
        message = f"攝影機讀取錯誤 {value}"
        super().__init__(message)    


### wrapper functions

def 讀取圖片灰階(filename):
    ret = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    if ret is None:
        raise ImageReadError(filename)
    else:
        return ret

def 讀取圖片彩色(filename):
    ret = cv2.imread(filename, cv2.IMREAD_COLOR)
    if ret is None:
        raise ImageReadError(filename)
    else:
        return ret


def 儲存圖片(filename, image):
    ret = cv2.imwrite(filename, image)
    if ret is False:
        ImageWriteError(filename)

def 彩色轉灰階(image):
    if image.ndim == 2:
        return image
    elif image.ndim == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def 灰階轉彩色(image):
    if image.ndim == 3:
        return image
    elif image.ndim == 2:
        return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

def 左右翻轉(image):
    return cv2.flip(image, 1)

def 上下翻轉(image):
    return cv2.flip(image, 0)

def 上下左右翻轉(image):
    return cv2.flip(image, -1)


def 開啟影像擷取(id=0):
    cap = cv2.VideoCapture(id)
    if not cap.isOpened():
        CameraOpenError()
    return cap

def 擷取單張影像(cap):
    ret, image = cap.read()
    if ret is False:
        CameraReadError()
    return image

# for screenshot
sct = mss()

def 擷取螢幕灰階(row1, row2, col1, col2):
    global sct

    monitor = {}
    monitor['top']= row1
    monitor['left']= col1
    monitor['width']= col2 - col1
    monitor['height']= row2 - row1
    
    img = np.array(sct.grab(monitor))
    
    return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)


win_name_prefix = '圖片'
win_name_counter = 0

def 顯示圖片(image, 標題=None, 新視窗=False):
    global win_name_prefix, win_name_counter    
    
    if 標題 is not None:
        cv2.imshow(標題,image)
        cv2.waitKey(1)
    else:
        if 新視窗:
            win_name_counter += 1
        win_name = win_name_prefix + str(win_name_counter)
        cv2.imshow(win_name,image)
        cv2.waitKey(1)

def 等待按鍵(延遲=0):
    ret = cv2.waitKey(延遲)
    if ret == -1:
        return None
    else:
        return chr(ret)

def 關閉所有圖片():
    cv2.destroyAllWindows()


def 畫灰階矩形(image, row1, row2, col1, col2, color=0):
    return cv2.rectangle(image, (col1, row1), (col2,row2), color)


if __name__ == '__main__' :
    pass
    
