import numpy as np
import numpy.fft as fft


class GravitationalField:
    def __init__(self, mass_distribution_grid, g: float):
        """
        Initializes the gravitational field with the given mass distribution grid.
        The mass distribution grid is a 2D list of floats from 0 to 1, where 0 represents no mass and 1 represents the maximum mass.
        """
        self.g = g
        self.mass_distribution = np.array(mass_distribution_grid, dtype=float)
        self.gravitational_field_vectors = self._compute_gravitational_field()

    def _compute_gravitational_field(self):
        G = self.g  # Gravitational constant, adjust as needed
        N, M = self.mass_distribution.shape

        # Fourier transform of the mass distribution
        rho_hat = fft.fft2(self.mass_distribution)

        # Generate k values for the computation in the frequency domain
        kx = np.fft.fftfreq(N).reshape(-1, 1)  # Column vector
        ky = np.fft.fftfreq(M).reshape(1, -1)  # Row vector
        k_squared = kx**2 + ky**2
        k_squared[0, 0] = 1  # Prevent division by zero

        # Solve for potential in frequency domain
        phi_hat = -4 * np.pi * G * rho_hat / k_squared

        # Inverse FFT to spatial domain for potential
        phi = fft.ifft2(phi_hat).real

        # Compute gradients (forces) in spatial domain
        force_x = np.real(fft.ifft2(1j * kx * phi_hat))
        force_y = np.real(fft.ifft2(1j * ky * phi_hat))

        return force_x, force_y

    def get_vector_at_point(self, x, y):
        """
        Returns the gravitational field vector at the given point (x, y).
        """
        fx, fy = self.gravitational_field_vectors
        return fx[x, y], fy[x, y]
