from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random

add_itens = fig1 = 0

hist_val = []
infos   = ['Figuras', 'Respostas', 'Enunciado', 'Formulas']
total   = [0, 0, 0, 0]
percent = [0, 0, 0, 0]

def __init__():
    
    global add_itens, figura
    
    fig1, add_itens = plt.subplots() 
    
def add_valores(px, py):
    
    global hist_val
    
    fat = [0.32, 13]
    
    hist_val.append((px, py))
    
    print(px, py)
    
    if len(hist_val) == 3:
              
        if hist_val[0][1] < fat[1] and hist_val[1][1] < fat[1] and hist_val[2][1] < fat[1]:
            if hist_val[0][0] < fat[0] and hist_val[1][0] < fat[0] and hist_val[2][0] < fat[0]:
                total[1] += 1
            elif hist_val[0][0] >= fat[0] and hist_val[1][0] >= fat[0] and hist_val[2][0] >= fat[0]:
                total[3] += 1
        elif hist_val[0][1] >= fat[1] and hist_val[1][1] >= fat[1] and hist_val[2][1] >= fat[1]:
            if hist_val[0][0] < fat[0] and hist_val[1][0] < fat[0] and hist_val[2][0] < fat[0]:
                total[0] += 1
            elif hist_val[0][0] >= fat[0] and hist_val[1][0] >= fat[0] and hist_val[2][0] >= fat[0]:
                total[2] += 1
                    
        for i in range(4):
            
            percent[i] = (total[i]/(1 + sum(total)))*100
            #print(int(percent[i]), end = ' ')    
    
        #print()
    
        del(hist_val[0])
        
def plot_grafico():
    
    global add_itens, infos
    
    add_itens.pie(percent, labels = infos, autopct = '%1.1f%%',
                  shadow = True, startangle = 90)
    
    add_itens.axis('equal')
    
    plt.show()    