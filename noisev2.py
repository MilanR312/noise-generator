from onelinerizer import onelinerize

import numpy
import cv2
import time


itter = 500

width = heigth = 1000


numpy.random.seed(1)

noiseMap = numpy.zeros((width, heigth))
noiseMap2 = numpy.zeros((width,heigth))
printMap = numpy.zeros((width, heigth, 1), dtype='uint8')

out = cv2.VideoWriter('name.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 20, (1000, 1000), False) 

def rand():
    for ir, row in enumerate(noiseMap):
        for ic, col in enumerate(row):
            noiseMap[ic][ir] = numpy.random.random()

def cellAround(x, y, curr):
    return (noiseMap[(x-1)%width][(y-1)%heigth] + noiseMap[x][(y-1)%heigth] + noiseMap[(x+1)%width][(y-1)%heigth] +
            noiseMap[(x-1)%width][y] + noiseMap[(x+1)%width][y] +
            noiseMap[(x-1)%width][(y+1)%heigth] + noiseMap[x][(y+1)%heigth] + noiseMap[(x+1)%width][(y+1)%heigth])

def initialNoise():
    for ir, row in enumerate(noiseMap):
        for ic, col in enumerate(row):
            if noiseMap[ic][ir] > 0.999992:
                noiseMap[ic][ir] = 1
            else:
                noiseMap[ic][ir] = 0

""" def color(itt): 
    for ir, row in enumerate(noiseMap):
        for ic, col in enumerate(row):
            
 """
def timer(itt, curr):
    completed = (((time.time() - start) / curr) * (itt - curr))
    if completed > 3600:
        print(f"hours until completion: {completed/3600}")
    elif completed > 60:
        print(f"minutes until completion: {completed/60}")
    else:
        print(f"seconds until completion: {completed}")

def swap():
    global noiseMap, noiseMap2
    noiseMap, noiseMap2 = noiseMap2, noiseMap

def smooth(itt, curr):
    print(curr)
    timer(itt, curr)
    for ir, row in enumerate(noiseMap):
        for ic, col in enumerate(row):
            if noiseMap[ic][ir] != 0:
                noiseMap2[ic][ir] = noiseMap[ic][ir] + 1
            if noiseMap[ic][ir] == 0:
                if cellAround(ic,ir, curr) > numpy.random.randint(2,4):
                    noiseMap2[ic][ir] = 1
            printMap[ir][ic] = ((noiseMap[ir][ic]) * (255 / (itt + 1)))
  

    swap()
    test = cv2.resize(printMap, (1000, 1000), interpolation=cv2.INTER_AREA)
    cv2.imshow("test", test)
    cv2.waitKey(10)
    out.write(test)

    if (itt == curr):
        return
    else:
        return smooth(itt, curr + 1)

rand()
initialNoise()
start = time.time()
smooth(itter, 1)
out.release()
arr = cv2.resize(printMap, (1000, 1000), interpolation=cv2.INTER_AREA)
cv2.imshow("test", arr)

cv2.waitKey(0)

cv2.destroyAllWindows() 
