import matplotlib.pyplot as plt
import math
import random
import numpy as np

PERIOD = 20*math.pi
# Define a list of named colors
DARKBLUE = '#227c9d'
LIGHTBLUE = '#17c3b2'
OCHRE = '#c67b35'
PURPLE ='#a877ba'
YELLOW = '#ffcb77'
GREEN ='#47865b'
RED ='#fe6d73'
COLORS = [DARKBLUE, LIGHTBLUE, OCHRE, PURPLE, YELLOW, GREEN, RED]

""" Summary of User functions:

drawPlanetDance(alpha, beta)
    parameters: integers alpha and beta
    Draws the planet dance P(alpha, beta) on plt

drawSampledPlanetDance(alpha, beta, m)
    integers alpha and beta, natural number m
    Draws the sampled planet dance S(alpha, beta, m) on plt

drawEpicycloid(alpha, beta) 
    parameters: integers alpha and beta, natural number m
    Draws the sampled planet dance S(alpha, beta, m) on plt

drawMMT(m, a) 
    parameters: natural number m, integer a. 
    Draws the modular multiplication table MMT(m,a)

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

    example: drawKnots([(3,2)], [0, 46])

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
            points.append(((index/abs(b)), 0))
            points.append(((index/abs(b)), 1))
        else :
            points.append((0, (index/abs(a))))
            points.append((1, (index/abs(a))))
        index += 1
    return points


# Draws chords on plot. Stops at edge of circle or continues to form an extended line.
# parameters: - list of 2-item lists. Each 2-item lists should be a pair of angles defining the endpoints for the chord.
#                       ex: [0, pi] indicates the horizontal diameter of the circle. 
#             - boolean value `extended` indicates whether the lines extend outside of the circle
#             - graph is axes of a plot where the picture should be drawn
def drawChords(chords, extended, circle, graph):
    graph.axis('equal')
    if extended :
        graph.set_ylim(-10,10)
        graph.set_xlim(-10,10)
        circle = False
    graph.axis('off')
    opacity = 1
    if len(chords) > 800 :
        opacity = 0.05
    if circle:
        # Generate theta values from 0 to 2π
        theta = np.linspace(0, 2 * np.pi, 100)
        # Parametric equations for the circle
        x = np.cos(theta)  # x = r*cos(theta), r=1
        y = np.sin(theta)  # y = r*sin(theta), r=1
        # Plot the circle boundary
        graph.plot(x, y, color='black', linewidth=0.3)
    for pair in chords:
        if round(((pair[0]/(2*math.pi)) % 1), 8) != round(((pair[1]/(2*math.pi)) % 1), 8) :
            if extended :
                graph.axline((math.cos(pair[0] + 0.5*math.pi), math.sin(pair[0] +  0.5*math.pi)), (math.cos(pair[1] +  0.5*math.pi), math.sin(pair[1] +  0.5*math.pi)), color='black', alpha=opacity, linewidth=0.3)
            else :     
                graph.plot([math.cos(pair[0] +  0.5*math.pi), math.cos(pair[1] +  0.5*math.pi)], [math.sin(pair[0] +  0.5*math.pi), math.sin(pair[1] +  0.5*math.pi)], color='black', alpha=opacity, linewidth=0.3)

# Draws line segments representing the line ay = bx on the square torus
# parameters: - integers a and b
#             - string 'col' giving a color for the knot
#             - graph is the axes of a plot where the picture should be drawn
def drawKnotStrands(a, b, col, graph):
    if graph == plt :
        graph.xlim(0,1)
        graph.ylim(0,1)
        ax = graph.gca()
        ax.axes.xaxis.set_ticks([])
        ax.axes.yaxis.set_ticks([])
    else :
        graph.set_ylim(0,1)
        graph.set_xlim(0,1)
        graph.axes.get_xaxis().set_ticks([])
        graph.axes.get_yaxis().set_ticks([])
        #graph.set_aspect('equal')
    points = knotStrandPoints(a,b)
    for p in points:
        graph.axline(p, slope=b/a, color=col)

# Draws points at m evenly spaced intervals along the linear loop on the torus ay = bx
# parameters: - integers a and b
#             - natural number m
#             - string 'col' giving the color
#             - graph is the axes of a plot where the picture should be drawn
def sampleKnot(a, b, m, col, graph):
    k = 0
    while k < m :
        graph.plot((a*(k/m) % 1), (b*(k/m) % 1), marker='.', color=col)
        k += 1

# Plots the epicycloid with given integers a and b for time t in [0, range].
# parameters: - integers a and b
#             - real number `range' (universal variable PERIOD defined at top)
#             - graph is the axes of a plot where the picture should be drawn
def plotEpicycloid(a, b, range, graph):
    #graph.set_aspect('equal')
    graph.axis('equal')
    if graph == plt :
        ax = graph.gca()
        ax.axes.xaxis.set_ticks([])
        ax.axes.yaxis.set_ticks([])
        ax.set_frame_on(False)
    else :
        graph.axes.get_xaxis().set_ticks([])
        graph.axes.get_yaxis().set_ticks([])
        graph.axes.spines['top'].set_visible(False)
        graph.axes.spines['bottom'].set_visible(False)
        graph.axes.spines['left'].set_visible(False)
        graph.axes.spines['right'].set_visible(False)
        #graph.set_aspect('equal')
    t = np.linspace(0, range, math.ceil(range/0.1))
    x = a*np.cos(t + 0.5*math.pi) + b*np.cos((a/b)*t + 0.5*math.pi)
    y = a*np.sin(t + 0.5*math.pi) + b*np.sin((a/b)*t + 0.5*math.pi)
    graph.plot(x,y)

# Draws the given continuous planet dance P(a,b) on plot `graph`
# parameters: - integers a and b
#             - graph is the axes of a plot where the picture should be drawn
def planetDance(a, b, graph):
    #graph.set_aspect('equal')
    extended = False
    if a*b < 0 :
        extended = True
    drawChords(generatePlanetDanceChords(a,b,3000), extended, True, graph)

# Draws an m-sampling of the planet dance P(a,b) on plot `graph`
# parameters: - integers a and b
#             - natural number m
#             - graph is the axes of a plot where the picture should be drawn
def planetDanceSample(a, b, m, circle, graph):
    #graph.set_aspect('equal')
    extended = False
    if a*b < 0 :
        extended = True
    drawChords(generatePlanetDanceChords(a,b,m), extended, circle, graph)

# Draws the modular multiplication table MMT(m,a) on plot `graph`
# parameters: - natural number m
#             - integer a
#             - graph is the axes of a plot where the picture should be drawn
def modMultTable(m,a, graph) :
    drawChords(generateModChords(m,a), False, True, graph)

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

    drawKnotStrands(a, b, DARKBLUE, ax[0][1])
    drawKnotStrands(1, mult, OCHRE, ax[0][1])
    sampleKnot(1, mult, sam, 'black', ax[0][1])
    ax[0][1].set_title('Linear Loops on Torus (' + str(alpha) + ', ' +  str(beta) + ') and (1, ' + str(mult) + ')')

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
    planetDanceSample(a, b, sample, True, ax[1])
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
    planetDanceSample(alpha, beta, m, True, plt)
    plt.show()

# parameters: integers alpha and beta, natural number m
# Draws the sampled planet dance S(alpha, beta, m) on plt
def drawEpicycloid(alpha, beta) :
    plotEpicycloid(alpha, beta, PERIOD, plt)
    plt.show()

# parameters: natural number m, integer a. 
# Draws the modular multiplication table MMT(m,a)
def drawMMT(m, a) :
    modMultTable(m, a, plt)
    plt.show()

#--------------------------------------------------------------------------------------------------
#    Example commands
#--------------------------------------------------------------------------------------------------

#drawKnots([(1,35, YELLOW), (3,2, DARKBLUE)], [0, 206])
# drawEpicycloid(-5,3)
# knotAndSampleDance(1,25,78)
# drawCorrespondence(4,3,31)

#danceAndEpicycloid(5,-3)

#drawKnots([(5,29, YELLOW), (1,25, DARKBLUE)], [1, 96])

# drawEpicycloid(3,2)


# knotAndSampleDance(1,115,400)
# # knotAndSampleDance(1,26,201)
# knotAndSampleDance(1,49,100)
# knotAndSampleDance(1,31,90)
# knotAndSampleDance(1,51,100)
#drawCorrespondence(2,3,100)

# knotAndSampleDance(1,25,50)
# knotAndSampleDance(1,21,200)
# knotAndSampleDance(1,25,104)

# drawMMT(512, 43)
# danceAndEpicycloid(4, 3)
# knotAndSampleDance(1, 34, 100)

drawCorrespondence(3,2,34)
