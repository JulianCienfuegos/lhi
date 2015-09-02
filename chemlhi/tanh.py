import math

def func(x):
    # Function to be integrated, with singular points set = 0
    if x == 1 or x == -1 :
        return 0
    else:
        return 1 / math.sqrt(1 - x ** 2)

# Input number of evaluations
N = 2100

# Set step size
h = 2.0 / (N - 1)
print "h =", h

# k ranges from -(N-1)/2 to +(N-1)/2
k = -1 * ((N - 1) / 2.0)
k_max  = ((N - 1) / 2.0)
sum = 0

# Loop across integration interval
while k < k_max + 1:

    # Compute abscissa
    x_k = math.tanh(math.pi * 0.5 * math.sinh(k * h))

    # Compute weight
    numerator = 0.5 * h * math.pi * math.cosh(k * h)
    denominator = math.pow(math.cosh(0.5 * math.pi * math.sinh(k * h)),2)
    w_k =  numerator / denominator

    sum += w_k * func(x_k)

    k += 1

print "Integral =", sum