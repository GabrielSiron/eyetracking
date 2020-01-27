import cv2
import numpy as np
import cv_add
from matplotlib import pyplot
import manip_grafico
import rede_neural
import threading

imagem = confirm = verif = 0

manip_grafico.__init__()

def pega_imagem():
    
    global imagem, confirm, verif
    
    camera = cv2.VideoCapture(1)
    
    while True:
        
        if verif != 1:
                                
            confirm, imagem = camera.read()
            
            if confirm:
                
                cv2.imshow('imagem', imagem)

                if cv2.waitKey(1) & 0xFF == 27:
                    camera.release()
                    break
        else:
            verif = 1
            break
        
def trata_imagem():
    
    global imagem, confirm, lista, verif
    
    while True:
            
        if confirm:
            
            questao = cv2.imread('Figura 1.png')
            cv2.imshow('Questao', questao)
            
            (x, y, w, h) = cv_add.detecta_face(imagem, cv_add.cascataFace)
            
            if x != 0:
                   
                regiaoOcularBGR  = imagem[y:y+int(h/2), x:x+w]
                
                regiaoOcularGRAY = cv2.cvtColor(regiaoOcularBGR, cv2.COLOR_BGR2GRAY)
                
                eyes = cv_add.cascataOlho.detectMultiScale(regiaoOcularGRAY)
                
                for (ex,ey,ew,eh) in eyes:
                    
                    #print(ew*ex, ew*eh)
                    
                    if ew*eh > 2000 and ew*eh < 5000:
                        
                        coordenadas = {'x':ex,'y':ey,'xw':ex+ew,'yh':ey+eh}
                        
                        circulos = cv_add.detecta_circulo(regiaoOcularBGR, coordenadas)
                        
                        cont_principal, _ = cv2.findContours(cv_add.mask,
                                                             cv2.RETR_TREE,
                                                             cv2.CHAIN_APPROX_SIMPLE)
                        
                        if cont_principal:
                            
                            momento = cv2.moments(cv_add.mask)
                        
                            cx = int(momento['m10']/momento['m00'])
                        
                        #print(cx/ew)
                        
                        manip_grafico.add_valores(cx/ew, cv_add.h)
                        
                        cv2.imshow('outra', cv_add.mask)
                        
                        if cv2.waitKey(1) & 0xFF == 27:
                            verif = 1
                            break    
        
        if verif == 1:
            cv2.destroyAllWindows()  
            break

if __name__ == '__main__':
    
    acao1 = threading.Thread(target = pega_imagem)
    acao1.start()
    acao2 = threading.Thread(target = trata_imagem)
    acao2.start()    
    
    while verif == 0:
        pass
        
    acao1.join()
    acao2.join()
      
    manip_grafico.plot_grafico()