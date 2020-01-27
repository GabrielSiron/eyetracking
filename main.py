import cv2
import numpy as np
import manip_cv
from matplotlib import pyplot
import manip_graphics
import threading

image = confirm = verify = 0

manip_graphics.__init__()

def get_image():
    
    global image, confirm, verify
    
    camera = cv2.VideoCapture(1)
    
    while True:
        
        if verify != 1:
                                
            confirm, image = camera.read()
            
            if confirm:
                
                cv2.imshow('image', image)

                if cv2.waitKey(1) & 0xFF == 27:
                    camera.release()
                    break
        else:
            verif = 1
            break
        
def treat_image():
    
    global image, confirm, lists, verify
    
    while True:
            
        if confirm:
            
            question = cv2.imread('Figure 1.png')
            cv2.imshow('Question', question)
            
            (x, y, w, h) = manip_cv.detect_face(image, manip_cv.cascadeFace)
            
            if x != 0:
                   
                roiBGR  = image[y:y+int(h/2), x:x+w]
                
                roiGRAY = cv2.cvtColor(roiBGR, cv2.COLOR_BGR2GRAY)
                
                eyes = manip_cv.cascadeEye.detectMultiScale(roiGRAY)
                
                for (ex,ey,ew,eh) in eyes:
                    
                    if ew*eh > 2000 and ew*eh < 5000:
                        
                        coordin = {'x':ex,'y':ey,'xw':ex+ew,'yh':ey+eh}
                        
                        circles = manip_cv.detect_circle(roiBGR, coordin)
                        
                        std_cont, _ = cv2.findContours(manip_cv.mask,
                                                             cv2.RETR_TREE,
                                                             cv2.CHAIN_APPROX_SIMPLE)
                        
                        if std_cont:
                            
                            moment = cv2.moments(manip_cv.mask)
                        
                            cx = int(moment['m10']/moment['m00'])
                        
                        manip_graphics.insert_values(cx/ew, manip_cv.h)
                        
                        cv2.imshow('other', manip_cv.mask)
                        
                        if cv2.waitKey(1) & 0xFF == 27:
                            verify = 1
                            break    
        
        if verify == 1:
            cv2.destroyAllWindows()  
            break

if __name__ == '__main__':
    
    action1 = threading.Thread(target = get_image)
    action1.start()
    action2 = threading.Thread(target = treat_image)
    action2.start()    
    
    while verify == 0:
        pass
        
    action1.join()
    action2.join()
      
    manip_graphics.plot_graphics()