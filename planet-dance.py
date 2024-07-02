import matplotlib.pyplot as plt
import math
import random
import numpy as np

PERIOD = 20*math.pi
# Define a list of named colors
COLORS = ["red", "blue", "green", "yellow", "purple", "orange", "pink"]

""" Summary of User functions:



drawCorrespondence
    parameters: alpha, beta, mult
        all are integers. 
    Will draw a grid of four pictures. 
    Let the sampling rate (m) = abs(alpha - beta*mult).
    Clockwise starting from upper right corner:
        - Torus knots (alpha, beta) and (mult, 1) with intersection points highlighted.
        - Epicyloid (alpha, beta)
        - MMMT (m, mult)
        - moon dance (alpha, beta) sampled m times

drawKnots
    parameters: knots, sample
        knots is a list of 2-tuples, each giving alpha and beta for a knot
        sample is a 2-tuple. sample[0] is a integer indicating which knot to sample. 
        sample[1] is the sampling rate m
    Draws one torus with each knot in knots. Random colors are chosen. 
    The desired knot is sampled at rate sample[1].

knotAndSampleDance
    parameters: alpha, beta, sample
        all are integers, sample is positive and (generally) large
    Will draw two pictures side by side
    On the left:
        knot strands of (alpha, beta) sampled at rate 'sample'
    On the right:
        planet dance (alpha, beta) sampled at rate 'sample'

danceAndEpicycloid
    parameters: alpha, beta
        both are integers
    Will draw two pictures side by side
    On the left:
        "continuous" planet dance L(alpha, beta)
    On the right:
        Epicycloid given by alpha and beta

"""

#---------------------------------------------------------------------------------------------------------
#  Non-User Functions 
#---------------------------------------------------------------------------------------------------------

# Given values for a, b, and m, calculates the angles of endpoints of each chord in S(a, b, m)
# parameters: integers a and b, natural number m 
# returns: list of 2-item lists. Each 2-item list represents the angles of the initial and terminal endpoints of one chord.
def generatePlanetDanceChords(a, b, m):
    chords = []
    index = 0
    while index < m :
        pair = [(2*math.pi*a*index)/m, (2*math.pi*b*index)/m]
        chords.append(pair)
        index += 1
    return chords

# Given values m and a, calculates angles for each chord connecting p to a*p mod m
# parameters: natural number m and integer a
# returns: list of 2-item lists
def generateModChords(mod, mult):
    return generatePlanetDanceChords(1, mult, mod)

# Given values a and b, calculated the intersection of line ay = bx with the boundary of the unit square
# parameters: integers a and b
# returns: list of 2-tuples representing x and y coordinates of points
def knotStrandPoints(a, b):
    points = []
    index = 0
    while index <= max(abs(a),abs(b)) :
        if a >= b :
            points.append(((index/abs(a)), 0))
            points.append(((index/abs(a)), 1))
        else :
            points.append((0, (index/abs(b))))
            points.append((1, (index/abs(b))))
        index += 1
    return points


# Draws chords on plot. Stops at edge of circle or continues to form an extended line.
# parameters: - list of 2-item lists. Each 2-item lists should be a pair of angles defining the endpoints for the chord.
#                       ex: [0, pi] indicates the horizontal diameter of the circle. 
#             - boolean value `extended` indicates whether the lines extend outside of the circle
#             - graph is axes of a plot where the picture should be drawn
def drawChords(chords, extended, graph):
    graph.axis('equal')
    if extended :
        graph.set_ylim(-10,10)
        graph.set_xlim(-10,10)
    graph.axis('off')
    opacity = 1
    if len(chords) > 800 :
        opacity = 0.05  
    for pair in chords:
        if round(((pair[0]/(2*math.pi)) % 1), 8) != round(((pair[1]/(2*math.pi)) % 1), 8) :
            if extended :
                graph.axline((math.cos(pair[0]), math.sin(pair[0])), (math.cos(pair[1]), math.sin(pair[1])), color='black', alpha=opacity, linewidth=0.3)
            else :     
                graph.plot([math.cos(pair[0]), math.cos(pair[1])], [math.sin(pair[0]), math.sin(pair[1])], color='black', alpha=opacity, linewidth=0.3)

# Draws line segments representing the line ay = bx on the square torus
# parameters: - integers a and b
#             - string 'col' giving a color for the knot
#             - graph is the axes of a plot where the picture should be drawn
def drawKnotStrands(a, b, col, graph):
    if graph == plt :
        graph.xlim(0,1)
        graph.ylim(0,1)
    else :
        graph.set_ylim(0,1)
        graph.set_xlim(0,1)
        graph.set_aspect('equal')
    points = knotStrandPoints(a,b)
    for p in points:
        graph.axline(p, slope=a/b, color=col)

# Draws points at m evenly spaced intervals along the linear loop on the torus ay = bx
# parameters: - integers a and b
#             - natural number m
#             - string 'col' giving the color
#             - graph is the axes of a plot where the picture should be drawn
def sampleKnot(a, b, m, col, graph):
    k = 0
    while k < m :
        graph.plot((b*(k/m) % 1), (a*(k/m) % 1), marker='.', color=col)
        k += 1

# Plots the epicycloid with given integers a and b for time t in [0, range].
# parameters: - integers a and b
#             - real number `range' (universal variable PERIOD defined at top)
#             - graph is the axes of a plot where the picture should be drawn
def plotEpicycloid(a, b, range, graph):
    graph.set_aspect('equal')
    graph.axis('equal')
    t = np.linspace(0, range, math.ceil(range/0.1))
    x = a*np.cos(t) + b*np.cos((a/b)*t)
    y = a*np.sin(t) + b*np.sin((a/b)*t)
    graph.plot(x,y)

# Draws the given continuous planet dance P(a,b) on plot `graph`
# parameters: - integers a and b
#             - graph is the axes of a plot where the picture should be drawn
def planetDance(a, b, graph):
    graph.set_aspect('equal')
    extended = False
    if a*b < 0 :
        extended = True
    drawChords(generatePlanetDanceChords(a,b,3000), extended, graph)

# Draws an m-sampling of the planet dance P(a,b) on plot `graph`
# parameters: - integers a and b
#             - natural number m
#             - graph is the axes of a plot where the picture should be drawn
def planetDanceSample(a, b, m, graph):
    graph.set_aspect('equal')
    extended = False
    if a*b < 0 :
        extended = True
    drawChords(generatePlanetDanceChords(a,b,m), extended, graph)

# Draws the modular multiplication table MMT(m,a) on plot `graph`
# parameters: - natural number m
#             - integer a
#             - graph is the axes of a plot where the picture should be drawn
def modMultTable(m,a, graph) :
    drawChords(generateModChords(m,a), False, graph)

#---------------------------------------------------------------------------------------------------------
#  User Functions 
#---------------------------------------------------------------------------------------------------------

# Will draw a grid of four pictures on plt.
# Let the sampling rate (m) = abs(alpha*mult - beta).
# Clockwise starting from upper right corner:
#         - Torus knots (alpha, beta) and (mult, 1) with intersection points highlighted.
#         - Epicyloid (alpha, beta)
#         - MMMT (m, mult)
#         - moon dance (alpha, beta) sampled m times
# parameters: alpha, beta, mult, all are integers. 
def drawCorrespondence(alpha, beta, mult):
    d = math.gcd(alpha, beta)
    a = alpha/d
    b = beta/d
    sam = abs(alpha*mult - beta)
    figure, ax = plt.subplots(2,2)
    figure.tight_layout(pad=3.0)
    planetDance(a, b, ax[0][0])
    ax[0][0].set_title('Planet Dance ' + chr(945) + ' = '+ str(alpha) + ' ' + chr(946)+ ' = ' + str(beta))
    modMultTable(sam, mult, ax[1][0])
    ax[1][0].set_title('MMT(' + str(sam) + ', ' + str(mult) + ')')
    plotEpicycloid(a, b, PERIOD, ax[1][1])
    ax[1][1].set_title('Epicycloid')

    drawKnotStrands(a, b, 'blue', ax[0][1])
    drawKnotStrands(mult, 1, 'red', ax[0][1])
    sampleKnot(mult, 1, sam, 'black', ax[0][1])
    ax[0][1].set_title('Linear Loops on Torus (' + str(alpha) + ', ' +  str(beta) + ') and (' + str(mult) + ', 1)')

    plt.show()

# Draws one torus with each knot in knots. Random colors are chosen. 
# The desired knot, indicated by the integer in sample[0], is sampled at rate sample[1].
# parameters: knots, sample
#     - knots is a list of 2-tuples, each giving alpha and beta for a knot
#     - sample is a 2-tuple. sample[0] is a integer indicating which knot to sample; sample[1] is the sampling rate m.
# Draws the picture on plt
def drawKnots(knots, sample=[0,0]) :
    for k in knots :
        if len(k) > 2 :
            color = k[2]
        else :
            color =  random.choice(COLORS)
        drawKnotStrands(k[0], k[1], color, plt)
    if sample[1] != 0 :
        sampleKnot(knots[sample[0]][0], knots[sample[0]][1], sample[1], 'black', plt)
    plt.show()

# parameters: alpha, beta, sample
#     all are integers, sample is positive and (generally) large
# Will draw two pictures side by side
# On the left:
#     knot strands of (alpha, beta) sampled at rate 'sample'
# On the right:
#     planet dance (alpha, beta) sampled at rate 'sample'
def knotAndSampleDance(alpha, beta, sample) :
    d = math.gcd(alpha, beta)
    a = alpha/d
    b = beta/d
    figure, ax = plt.subplots(1,2)
    figure.tight_layout(pad=3.0)
    drawKnotStrands(a, b, random.choice(COLORS), ax[0])
    sampleKnot(a, b, sample, 'black', ax[0])
    planetDanceSample(a, b, sample, ax[1])
    plt.show()

# parameters: alpha, beta
#     both are integers
# Will draw two pictures side by side
# On the left:
#     "continuous" planet dance P(alpha, beta)
# On the right:
#     Epicycloid given by alpha and beta
def danceAndEpicycloid(alpha, beta) :
    d = math.gcd(alpha, beta)
    a = alpha/d
    b = beta/d
    figure, ax = plt.subplots(1,2)
    figure.tight_layout(pad=3.0)
    planetDance(a, b, ax[0])
    plotEpicycloid(a, b, PERIOD, ax[1])
    plt.show()

# parameters: integers alpha and beta
# Draws the planet dance P(alpha, beta) on plt
def drawPlanetDance(alpha, beta) :
    planetDance(alpha, beta, plt)
    plt.show()

# parameters: integers alpha and beta, natural number m
# Draws the sampled planet dance S(alpha, beta, m) on plt
def drawSampledPlanetDance(alpha, beta, m) :
    planetDanceSample(alpha, beta, m, plt)
    plt.show()

# parameters: natural number m, integer a. 
# Draws the modular multiplication table MMT(m,a)
def drawMMT(m, a) :
    modMultTable(m, a, plt)
    plt.show()

#--------------------------------------------------------------------------------------------------
#    Example commands
#--------------------------------------------------------------------------------------------------

""" To do:
    - fix drawCorrespondence because it is drawing too many dots """

#figure, axis = plt.subplot(2,2)

#drawExtendedChords(generatePlanetDanceChords(ALPHA, BETA, SAMPLE))
#drawChords(generateModChords(abs(ALPHA - BETA*50), 50))
#drawKnotStrands(3, 2, 'blue')
#drawKnotStrands(20, 1, 'red')
#sampleKnot(3,2,37,'black')
#sampleKnot(20,1,74,'black')
#plt.show()

#drawKnotStrands(5, 2, 'blue', plt)
#drawKnotStrands(2, 1, 'red', plt)
#plt.show()

#drawKnotStrands(65, 1, 'blue', plt)
#sampleKnot(65, 1, 189, 'black', plt)
#plt.show()

#planetDanceSample(5, 2, 189, plt)
#plt.show()


# planetDance(-3, 2)
# planetDanceSample(3,2,37)

# drawChords(generateModChords(194,50))
# plt.show()


# plotEpicycloid(2, 3, 8*math.pi, plt)
# plt.show()

# Displaying the plot
# plt.show()

# drawCorrespondence(-4,3,50)
# drawCorrespondence(4,2,50)
# 
# drawCorrespondence(6,3,50)


#modMultTable(100,34,plt)
#plt.show()


#-----------------------------------------------------------------


#knotAndSampleDance(51, 1, 100)
#knotAndSampleDance(21, 1, 140)
#knotAndSampleDance(21, 1, 200)
#knotAndSampleDance(51, 1, 550)
#knotAndSampleDance(26, 1, 100)
#

drawMMT(512, 43)
danceAndEpicycloid(4, 3)
knotAndSampleDance(34, 1, 100)
drawCorrespondence(5,2,41)

# danceAndEpicycloid(-3, 2)
# 
# danceAndEpicycloid(3, 4)
# danceAndEpicycloid(-3, 4)
# danceAndEpicycloid(4, -3)
# danceAndEpicycloid(3, -4)
# danceAndEpicycloid(-4, 3)
#danceAndEpicycloid(-3, -4)
#danceAndEpicycloid(3, 4)
#danceAndEpicycloid(3,2)
#danceAndEpicycloid(5,-3)

#drawCorrespondence(2,3,34)

#
#drawChords(generatePlanetDanceChords(34,1,138), True , ax)
#plt.show()

#figure, ax = plt.subplots(1)
#plotEpicycloid(5, -3, PERIOD, ax)
#plt.show()

#knots = [[1, 1, 'gray'], [1, 3, 'blue'], [41, 1, 'orange']]
#drawKnots(knots, [2, 366])

# knotAndSampleDance(30, 1, 60)
# knotAndSampleDance(31, 1, 60)
# knotAndSampleDance(29, 1, 60)
# knotAndSampleDance(33, 1, 99)
# knotAndSampleDance(34, 1, 99)
# knotAndSampleDance(32, 1, 99)
# knotAndSampleDance(25, 1, 100)
# knotAndSampleDance(24, 1, 100)
# knotAndSampleDance(26, 1, 100)