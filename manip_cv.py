import cv2 
from numpy import array

#multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml

cascataFace = cv2.CascadeClassifier('cascataFace.xml')
cascataOlho = cv2.CascadeClassifier('cascataOlho.xml')

imagem = mask = h = 0

def detecta_face(imagem, cascata):

    imgInGray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    faces     = cascata.detectMultiScale(imgInGray, 1.3, 5)

    try:
        return faces[0]
    except:
        return (0, 0, 0, 0)

def detecta_circulo(img, pts):
    
    global imagem, mask, h
    
    regiaoOcularBGR  = cv2.medianBlur(img[pts['y']+15:pts['yh']-10, pts['x']+10:pts['xw']-5], 5)
    
    regiaoOcularGRAY = cv2.cvtColor(regiaoOcularBGR, cv2.COLOR_BGR2GRAY)
    
    mascara = cv2.inRange(regiaoOcularBGR, array([0, 0, 0]), array([255, 255, 60]))
    
    cv2.imshow('que', regiaoOcularBGR)
    
    imagem = cv2.resize(regiaoOcularBGR, (25, 25))
    imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    
    contornos, hierarquia = cv2.findContours(mascara, cv2.RETR_TREE,
                                             cv2.CHAIN_APPROX_SIMPLE)
    
    area_max = indice = 0
    
    x, y, w, h = (0, 0, 0, 0)
    
    for contorno in contornos:
        
        if cv2.contourArea(contorno) > area_max:
            area_max = cv2.contourArea(contorno)
            x, y, w, h = cv2.boundingRect(contorno)
            
    else:
        for i in range(len(contornos)):
            if cv2.contourArea(contornos[i]) != area_max:
                x1, y1, w1, h1 = cv2.boundingRect(contornos[i])
                cv2.rectangle(mascara, (x1, y1), (x1+w1, y1+h1), (0), -1)
       
    mask = mascara
    
    cv2.rectangle(mascara, (x, y), (x+w, y+h), (255), 1)
    
    try:
        circulos = cv2.HoughCircles(regiaoOcularGRAY,cv2.HOUGH_GRADIENT,2,40,
                                param1=50,param2=30,minRadius=2,maxRadius=17)

        return circulos, mascara
    
    except:
        return None, None


def img_out(frame, texto, coordenadas):
    """
    Essa funcao encapsula algumas partes necessarias
    para escrever textos numa imagem, para simplificar
    o processo.
    """
    fonte     = cv2.FONT_HERSHEY_COMPLEX_SMALL
    escala    = 1
    espessura = 1

    cv2.putText(frame, texto, coordenadas, fonte, escala, (0, 255, 0), espessura)

def aumenta_contraste(frame):
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