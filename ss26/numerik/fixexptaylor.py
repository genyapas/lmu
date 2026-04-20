def e(x,eps):

    if ( eps<=0 ):
        raise Exception("eps must be positive")
    
    y = abs(x)

    psum, z, k = 1, 1, 1
    while ( abs(z) > eps or abs(x)/k > 0.5 ):
        z = z * y/k
        psum += z
        k += 1
    
    if x < 0:
        return 1 / psum
    else:
        return psum