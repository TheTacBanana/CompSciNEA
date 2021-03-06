import random, math

p = [151,160,137,91,90,15,                 
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
p = p + p

def OctaveNoise(x, y, octaves, persistence): # Sums multiple levels of perlin noise
    total = 0
    frequency = 1
    amplitude = 1
    maxValue = 0

    for i in range(octaves): # Combines Multiple octaves of perlin noise
        total += ((Noise(x * frequency, y * frequency)) * amplitude)

        maxValue += amplitude

        amplitude *= persistence
        frequency *= 2

    return total / maxValue

def Noise(x, y): # Returns a value of the perlin noise function at (x, y) coordinate
    xi = math.floor(x) % 255
    yi = math.floor(y) % 255

    g1 = p[p[xi] + yi]
    g2 = p[p[xi + 1] + yi]
    g3 = p[p[xi] + yi + 1]
    g4 = p[p[xi + 1] + yi + 1]

    xf = x - math.floor(x)
    yf = y - math.floor(y)

    d1 = Grad(g1, xf, yf)
    d2 = Grad(g2, xf - 1, yf)
    d3 = Grad(g3, xf, yf - 1)
    d4 = Grad(g4, xf - 1, yf - 1)

    u = Fade(xf)
    v = Fade(yf)

    x1Inter = Lerp(u, d1, d2)
    x2Inter = Lerp(u, d3, d4)
    yInter = Lerp(v, x1Inter, x2Inter)

    return yInter

def Grad(hash, x, y): # Gradient Function defined as part of the algorithm
    temp = hash & 3
    if temp == 0:
        return x + y
    elif temp == 1:
        return -x + y
    elif temp == 2:
        return x - y
    elif temp == 3:
        return -x - y
    else:
        return 0

def Lerp(ammount, left, right): # Linear interpolation of values
    return ((1 - ammount) * left + ammount * right)

def Fade(t): # Fade Function defined as part of the algorithm
    return t * t * t * (t * (t * 6 - 15) + 10)