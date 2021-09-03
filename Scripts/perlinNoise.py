from mathlib import Vector, GraphStuff
import random

gradientVectors = [Vector([[1],[1]]), 
                    Vector([[-1],[1]]),
                    Vector([[1],[-1]]),
                    Vector([[-1],[-1]]),
                    Vector([[GraphStuff.root2],[0]]),
                    Vector([[0],[GraphStuff.root2]]),
                    Vector([[-GraphStuff.root2],[0]]),
                    Vector([[0],[-GraphStuff.root2]])]

permutationTable = [151,160,137,91,90,15,                 
    131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,    
    190, 6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,
    88,237,149,56,87,174,20,125,136,171,168, 68,175,74,165,71,134,139,48,27,166,
    77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,
    102,143,54, 65,25,63,161, 1,216,80,73,209,76,132,187,208, 89,18,169,200,196,
    135,130,116,188,159,86,164,100,109,198,173,186, 3,64,52,217,226,250,124,123,
    5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,
    223,183,170,213,119,248,152, 2,44,154,163, 70,221,153,101,155,167, 43,172,9,
    129,22,39,253, 19,98,108,110,79,113,224,232,178,185, 112,104,218,246,97,228,
    251,34,242,193,238,210,144,12,191,179,162,241, 81,51,145,235,249,14,239,107,
    49,192,214, 31,181,199,106,157,184, 84,204,176,115,121,50,45,127, 4,150,254,
    138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180]

#p = [] * 512
#for x in range(512):
#    p[x] = permutationTable[x%256]

repeat = 1

def Noise(x, y):
    #print(x)
    x0 = int(x)
    x1 = x0 + 1
    y0 = int(y)
    y1 = y0 + 1

    sx = x - x0
    sy = y - y0

    n0 = dotGridGradient(x0, y0, x, y)
    n1 = dotGridGradient(x1, y0, x, y)
    ix0 = lerp(n0, n1, sx)

    n0 = dotGridGradient(x0, y1, x, y)
    n0 = dotGridGradient(x1, y1, x, y)
    ix1 = lerp(n0, n1, sx)

    value = lerp(ix0, ix1, sy)
    #print(value)
    return value

#                 gradient , distance 
def dotGridGradient(ix, iy, x, y):
    gradientVals = randomGradient().Val()
    #print(gradientVals)

    dx = x - ix
    dy = y - iy

    value = (dx*gradientVals[0][0] + dy*gradientVals[1][0])
    #print(value)
    return value

def randomGradient():
    return Vector([[random.random()],[random.random()]])
    #return gradientVectors[random.randint(0, 7)]

def lerp(a0, a1, w):
    value = (a1 - a0) * w + a0
    #print(value)
    return value

def Fade(t):
    t * t * t * (t * (t * 6 - 15) + 10)