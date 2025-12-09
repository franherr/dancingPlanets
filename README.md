# dancingPlanets
Code to draw pictures of modular stitch graphs, planet dances, and corresponding linear paths on the torus.

For an explanation of these ideas and how these objects connect, see https://link.springer.com/article/10.1007/s00283-025-10474-2

To get started, open planet-dance.py. Instructions and method descriptions are given at the beginning of the file. Sample calls are given at the end.

_note: the code uses an older term "modular multiplication table" instead of "modular stitch graph"._

# list of functions

Here is a list of all user-facing fucntions available in planet-dance.py.

**drawPlanetDance(alpha, beta)**
    * parameters: integers alpha and beta
    * Draws the planet dance P(alpha, beta) on plt

**drawSampledPlanetDance(alpha, beta, m)**
    - integers alpha and beta, natural number m
    - Draws the sampled planet dance S(alpha, beta, m) on plt

**drawEpicycloid(alpha, beta)**
    + parameters: integers alpha and beta, natural number m
    + Draws the sampled planet dance S(alpha, beta, m) on plt

**drawMMT(m, a)**
    -parameters: natural number m, integer a. 
    -Draws the modular multiplication table MMT(m,a)

**drawCorrespondence**
    -parameters: alpha, beta, mult
        -all are integers. 
    -Will draw a grid of four pictures. 
    -Let the sampling rate (m) = abs(alpha - beta*mult).
    -Clockwise starting from upper right corner:
        - Torus knots (alpha, beta) and (mult, 1) with intersection points highlighted.
        - Epicyloid (alpha, beta)
        - MMMT (m, mult)
        - moon dance (alpha, beta) sampled m times

**drawKnots**
    -parameters: knots, sample
        -knots is a list of 2-tuples, each giving alpha and beta for a knot
        -sample is a 2-tuple. sample[0] is a integer indicating which knot to sample. 
        -sample[1] is the sampling rate m
    -Draws one torus with each knot in knots. Random colors are chosen. 
    -The desired knot is sampled at rate sample[1].

    example: drawKnots([(3,2)], [0, 46])

**knotAndSampleDance**
    -parameters: alpha, beta, sample
        -all are integers, sample is positive and (generally) large
    -Will draw two pictures side by side
    -On the left:
        -knot strands of (alpha, beta) sampled at rate 'sample'
    -On the right:
        -planet dance (alpha, beta) sampled at rate 'sample'

**danceAndEpicycloid**
    -parameters: alpha, beta
        -both are integers
    -Will draw two pictures side by side
    -On the left:
        -"continuous" planet dance L(alpha, beta)
    -On the right:
        -Epicycloid given by alpha and beta
