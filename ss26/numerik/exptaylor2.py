import numpy as np

def test_precision(x, dtype):
    x = dtype(x)
    psum = dtype(1.0)
    z = dtype(1.0)
    eps = dtype(1e-15)
    k = 1
    while (abs(z) > eps or abs(x)/k > 0.5):
        # Erzwinge den dtype in jedem Schritt!
        z = dtype(z * x / k)
        psum = dtype(psum + z)
        k += 1
    return psum

x_val = -16
print(f"Exakt:   {np.exp(x_val):.5e}")
print(f"float32: {test_precision(x_val, np.float32):.5e}")
print(f"float64: {test_precision(x_val, np.float64):.5e}")
