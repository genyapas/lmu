# Evaluate Taylor series of exp(x) to precision eps > 0
def e(x,eps):

    if ( eps<=0 ):
        raise Exception("eps must be positive")

    psum, z, k = 1, 1, 1
    while ( abs(z) > eps or abs(x)/k > 0.5 ):
        z = z * x/k
        psum += z
        k += 1

    return psum
