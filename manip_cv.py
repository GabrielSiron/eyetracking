import cv2 
from numpy import array

#multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml

cascadeFace = cv2.CascadeClassifier('cascadeFace.xml')
cascadeEye  = cv2.CascadeClassifier('cascadeEye.xml')

image = mask = h = 0

def detect_face(image, cascade):

    imgInGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces     = cascade.detectMultiScale(imgInGray, 1.3, 5)

    try:
        return faces[0]
    except:
        return (0, 0, 0, 0)

def detect_circle(img, pts):
    
    global image, mask, h
    
    roiBGR  = cv2.medianBlur(img[pts['y']+15:pts['yh']-10, pts['x']+10:pts['xw']-5], 5)
    roiGRAY = cv2.cvtColor(roiBGR, cv2.COLOR_BGR2GRAY)
    
    mask2 = cv2.inRange(roiBGR, array([0, 0, 0]), array([255, 255, 60]))
    
    image = cv2.resize(roiBGR, (25, 25))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    contorns, hierarquia = cv2.findContours(mask2, cv2.RETR_TREE,
                                             cv2.CHAIN_APPROX_SIMPLE)
    
    max_area = index = 0
    
    x, y, w, h = (0, 0, 0, 0)
    
    for contorn in contorns:
        
        if cv2.contourArea(contorn) > max_area:
            max_area = cv2.contourArea(contorn)
            x, y, w, h = cv2.boundingRect(contorn)
            
    else:
        for i in range(len(contorns)):
            if cv2.contourArea(contorns[i]) != max_area:
                x1, y1, w1, h1 = cv2.boundingRect(contorns[i])
                cv2.rectangle(mask2, (x1, y1), (x1+w1, y1+h1), (0), -1)
       
    mask = mask2
    
    cv2.rectangle(mask2, (x, y), (x+w, y+h), (255), 1)
    
    try:
        circles = cv2.HoughCircles(roiGRAY,cv2.HOUGH_GRADIENT,2,40,
                                param1=50,param2=30,minRadius=2,maxRadius=17)

        return circles, mask2
    
    except:
        return None, None


def img_out(frame, text, coord):
    """
    Essa funcao encapsula algumas partes necessarias
    para escrever textos numa imagem, para simplificar
    o processo.
    """
    font     = cv2.FONT_HERSHEY_COMPLEX_SMALL
    scale    = 1
    espess   = 1

    cv2.putText(frame, text, coord, font, scale, (0, 255, 0), espess)

def improve_contraste(frame):
    """
    Essa funcao aumenta o contraste entre as cores na imagem
    afim de facilitar a deteccao ocular.
    """
    frame_in_lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b      = cv2.split(frame_in_lab)

    clahe = cv2.createCLAHE(clipLimit = 4.0, tileGridSize = (8,8))
    l_out = clahe.apply(l)

    frame_out = cv2.cvtColor(cv2.merge((l_out, a, b)), cv2.COLOR_LAB2BGR)

    return frame_out