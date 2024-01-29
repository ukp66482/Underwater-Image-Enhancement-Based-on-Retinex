import numpy as np

def gaussian_kernel(size, sigma):
    kernel = np.fromfunction(
        lambda x, y: (1/ (2*np.pi*sigma**2)) * 
                      np.exp(- ((x - (size-1)/2)**2 + (y - (size-1)/2)**2) / (2*sigma**2)),
        (size, size)
    )
    return kernel / np.sum(kernel)


kernel_size = 3
sigma = 0.85

gaussian_3x3 = gaussian_kernel(kernel_size, sigma)

print(gaussian_3x3)
