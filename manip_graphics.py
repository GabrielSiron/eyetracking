from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random

insert_itens = fig1 = 0

story_val = []
infos   = ['Figures', 'Answers', 'Statement', 'Formulas']
total   = [0, 0, 0, 0]
percent = [0, 0, 0, 0]
    
def __init__():
    
    global insert_itens, fig1

    fig1, insert_itens = plt.subplots() 
    
def insert_values(px, py):
    
    global story_val
    
    fat = [0.32, 13]
    
    story_val.append((px, py))
    
    if len(story_val) == 3:
                    
        if story_val[0][1] < fat[1] and story_val[1][1] < fat[1] and story_val[2][1] < fat[1]:
            if story_val[0][0] < fat[0] and story_val[1][0] < fat[0] and story_val[2][0] < fat[0]:
                total[1] += 1
            elif story_val[0][0] >= fat[0] and story_val[1][0] >= fat[0] and story_val[2][0] >= fat[0]:
                total[3] += 1
        elif story_val[0][1] >= fat[1] and story_val[1][1] >= fat[1] and story_val[2][1] >= fat[1]:
            if story_val[0][0] < fat[0] and story_val[1][0] < fat[0] and story_val[2][0] < fat[0]:
                total[0] += 1
            elif story_val[0][0] >= fat[0] and story_val[1][0] >= fat[0] and story_val[2][0] >= fat[0]:
                total[2] += 1
                    
        for i in range(4):
            
            percent[i] = (total[i]/(1 + sum(total)))*100
            #print(int(percent[i]), end = ' ')    
    
        #print()
    
        del(story_val[0])
        
def plot_graphics():
    
    global insert_itens, infos
    
    insert_itens.pie(percent, labels = infos, autopct = '%1.1f%%',
                  shadow = True, startangle = 90)
    
    insert_itens.axis('equal')
    
    plt.show()    