import autofit as af
import numpy as np
from astropy import cosmology as cosmo
from autoarray.structures import grids
from autofit.text import formatter
from autogalaxy import dimensions as dim
from autogalaxy.profiles import geometry_profiles
from autogalaxy.util import cosmology_util
from scipy.integrate import quad
from scipy.special import comb
import typing


def kesi(p):
    n_list = np.arange(0, 2 * p + 1, 1)
    kesi_n = (2.0 * p * np.log(10) / 3.0 + 2.0 * np.pi * n_list * 1j) ** (0.5)
    return kesi_n


def eta(p):
    eta_list = np.zeros(int(2 * p + 1))
    kesi_list = np.zeros(int(2 * p + 1))
    kesi_list[0] = 0.5
    kesi_list[1 : p + 1] = 1.0
    kesi_list[int(2 * p)] = 1.0 / 2.0 ** p

    for i in np.arange(1, p, 1):
        kesi_list[2 * p - i] = kesi_list[2 * p - i + 1] + 2 ** (-p) * comb(p, i)

    for i in np.arange(0, 2 * p + 1, 1):
        eta_list[i] = (
            (-1) ** i * 2.0 * np.sqrt(2.0 * np.pi) * 10 ** (p / 3.0) * kesi_list[i]
        )

    return eta_list


class LightProfile:
    """Mixin class that implements functions common to all light profiles"""

    def image_from_grid_radii(self, grid_radii):
        """
        Abstract method for obtaining intensity at on a grid of radii.

        Parameters
        ----------
        grid_radii : float
            The radial distance from the centre of the profile. for each coordinate on the grid.
        """
        raise NotImplementedError("intensity_at_radius should be overridden")

    # noinspection PyMethodMayBeStatic
    def image_from_grid(self, grid, grid_radial_minimum=None):
        """
        Abstract method for obtaining intensity at a grid of Cartesian (y,x) coordinates.

        Parameters
        ----------
        grid : grid_like
            The (y, x) coordinates in the original reference frame of the grid.
        Returns
        -------
        intensity : ndarray
            The value of intensity at the given radius
        """
        raise NotImplementedError("intensity_from_grid should be overridden")

    def luminosity_within_circle_in_units(
        self,
        radius: dim.Length,
        unit_luminosity="eps",
        exposure_time=None,
        redshift_profile=None,
        cosmology=cosmo.Planck15,
        **kwargs
    ):
        raise NotImplementedError()


# noinspection PyAbstractClass
class EllipticalLightProfile(geometry_profiles.EllipticalProfile, LightProfile):
    """Generic class for an elliptical light profiles"""

    @af.map_types
    def __init__(
        self,
        centre: dim.Position = (0.0, 0.0),
        elliptical_comps: typing.Tuple[float, float] = (0.0, 0.0),
        intensity: dim.Luminosity = 0.1,
    ):
        """  Abstract class for an elliptical light-profile.

        Parameters
        ----------
        centre : (float, float)
            The (y,x) arc-second coordinates of the profile centre.
        elliptical_comps : (float, float)
            The first and second ellipticity components of the elliptical coordinate system, where
            fac = (1 - axis_ratio) / (1 + axis_ratio), ellip_y = fac * sin(2*phi) and ellip_x = fac * cos(2*phi).
        """
        super(EllipticalLightProfile, self).__init__(
            centre=centre, elliptical_comps=elliptical_comps
        )
        self.intensity = intensity

    @property
    def light_profile_centres(self):
        return grids.GridIrregularGrouped([self.centre])

    def blurred_image_from_grid_and_psf(self, grid, psf, blurring_grid):
        """Evaluate the light profile image on an input *Grid* of coordinates and then convolve it with a PSF.

        The *Grid* may be masked, in which case values outside but near the edge of the mask will convolve light into
        the mask. A blurring grid is therefore required, which evaluates the image on pixels on the mask edge such that
        their light is blurred into it by the PSF.

        The grid and blurring_grid must be a *Grid* objects so the evaluated image can be mapped to a uniform 2D array
        and binned up for convolution. They therefore cannot be *GridIrregularGrouped* objects.

        Parameters
        ----------
        grid : Grid
            The (y, x) coordinates in the original reference frame of the grid.
        psf : aa.Kernel
            The PSF the evaluated light profile image is convolved with.
        blurring_grid : Grid
            The (y,x) coordinates neighboring the (masked) grid whose light is blurred into the image.

        """
        image = self.image_from_grid(grid=grid)

        blurring_image = self.image_from_grid(grid=blurring_grid)

        return psf.convolved_array_from_array_2d_and_mask(
            array_2d=image.in_2d_binned + blurring_image.in_2d_binned, mask=grid.mask
        )

    def blurred_image_from_grid_and_convolver(self, grid, convolver, blurring_grid):
        """Evaluate the light profile image on an input *Grid* of coordinates and then convolve it with a PSF using a
        *Convolver* object.

        The *Grid* may be masked, in which case values outside but near the edge of the mask will convolve light into
        the mask. A blurring grid is therefore required, which evaluates the image on pixels on the mask edge such that
        their light is blurred into it by the Convolver.

        The grid and blurring_grid must be a *Grid* objects so the evaluated image can be mapped to a uniform 2D array
        and binned up for convolution. They therefore cannot be *GridIrregularGrouped* objects.

        Parameters
        ----------
        grid : Grid
            The (y, x) coordinates in the original reference frame of the grid.
        Convolver : aa.Convolver
            The Convolver object used to blur the PSF.
        blurring_grid : Grid
            The (y,x) coordinates neighboring the (masked) grid whose light is blurred into the image.

        """
        image = self.image_from_grid(grid=grid)

        blurring_image = self.image_from_grid(grid=blurring_grid)

        return convolver.convolved_image_from_image_and_blurring_image(
            image=image.in_1d_binned, blurring_image=blurring_image.in_1d_binned
        )

    def profile_visibilities_from_grid_and_transformer(self, grid, transformer):

        image = self.image_from_grid(grid=grid)

        return transformer.visibilities_from_image(image=image.in_1d_binned)

    def luminosity_within_circle_in_units(
        self,
        radius: dim.Length,
        unit_luminosity="eps",
        exposure_time=None,
        redshift_object=None,
        cosmology=cosmo.Planck15,
        **kwargs
    ):
        """Integrate the light profile to compute the total luminosity within a circle of specified radius. This is \
        centred on the light profile's centre.

        The following unit_label for mass can be specified and output:

        - Electrons per second (default) - 'eps'.
        - Counts - 'counts' (multiplies the luminosity in electrons per second by the exposure time).

        Parameters
        ----------
        radius : float
            The radius of the circle to compute the dimensionless mass within.
        unit_luminosity : str
            The unit_label the luminosity is returned in {esp, counts}.
        exposure_time : float or None
            The exposure time of the observation, which converts luminosity from electrons per second unit_label to counts.
        """

        if not hasattr(radius, "unit_length"):
            radius = dim.Length(value=radius, unit_length="arcsec")

        if self.unit_length is not radius.unit_length:
            kpc_per_arcsec = cosmology_util.kpc_per_arcsec_from(
                redshift=redshift_object, cosmology=cosmology
            )

            radius = radius.convert(
                unit_length=self.unit_length, kpc_per_arcsec=kpc_per_arcsec
            )

        luminosity = dim.Luminosity(
            value=quad(self.luminosity_integral, a=0.0, b=radius)[0],
            unit_luminosity=self.unit_luminosity,
        )
        return luminosity.convert(
            unit_luminosity=unit_luminosity, exposure_time=exposure_time
        )

    def luminosity_integral(self, x):
        """Routine to integrate the luminosity of an elliptical light profile.

        The axis ratio is set to 1.0 for computing the luminosity within a circle"""
        return 2 * np.pi * x * self.image_from_grid_radii(x)


class EllipticalCoreSersic_MGE(EllipticalLightProfile):
    @af.map_types
    def __init__(
        self,
        centre: dim.Position = (0.0, 0.0),
        elliptical_comps: typing.Tuple[float, float] = (0.0, 0.0),
        effective_radius: dim.Length = 0.01,
        sersic_index: float = 0.6,
        radius_break: dim.Length = 0.01,
        intensity_break: dim.Luminosity = 0.05,
        gamma: float = 0.25,
        alpha: float = 3.0,
    ):

        """
        The MGE based Sersic profile.
        """

        super(EllipticalCoreSersic_MGE, self).__init__(
            centre=centre, elliptical_comps=elliptical_comps, intensity=intensity_break
        )
        # super(mp.EllipticalMassProfile, self).__init__(
        #    centre=centre, elliptical_comps=elliptical_comps
        # )
        # self.mass_to_light_ratio = mass_to_light_ratio

        if self.axis_ratio > 0.9999:
            self.axis_ratio = 0.9999

            #########################################################
        # Below is to decompose a gNFW into a series of Gaussians
        #########################################################

        p = int(
            28
        )  # number of terms used to approximate function "f" below. Fix it to be 28 is okay.
        n = int(
            20
        )  # number of Gaussians to use. It can vary depending on the accuracy one want to achieve.

        rmin = effective_radius / 50.0
        rmax = effective_radius * 20.0

        self.sersic_constant = (
            (2 * sersic_index)
            - (1.0 / 3.0)
            + (4.0 / (405.0 * sersic_index))
            + (46.0 / (25515.0 * sersic_index ** 2))
            + (131.0 / (1148175.0 * sersic_index ** 3))
            - (2194697.0 / (30690717750.0 * sersic_index ** 4))
        )

        self.intensity_prime = (
            intensity_break
            * (2.0 ** (-gamma / alpha))
            * np.exp(
                self.sersic_constant
                * (((2.0 ** (1.0 / alpha)) * radius_break) / effective_radius)
                ** (1.0 / sersic_index)
            )
        )

        def core_sersic_2D(r):
            return (
                self.intensity_prime
                * (1.0 + (radius_break / r) ** alpha) ** (gamma / alpha)
                * np.exp(
                    -self.sersic_constant
                    * ((r ** alpha + radius_break ** alpha) / effective_radius ** alpha)
                    ** (1.0 / (sersic_index * alpha))
                )
            )

        kesi_list = kesi(p)
        eta_list = eta(p)

        def f(sigma):
            return np.sum(eta_list * np.real(target_function(sigma * kesi_list)))

        log_sigma_list = np.linspace(np.log(rmin), np.log(rmax), n)
        d_log_sigma = log_sigma_list[1] - log_sigma_list[0]
        sigma_list = np.exp(log_sigma_list)

        a_list = np.zeros(n)

        for i in range(n):
            f_sigma = np.sum(
                eta_list * np.real(core_sersic_2D(sigma_list[i] * kesi_list))
            )
            if (i == -1) or (i == (n - 1)):
                a_list[i] = 0.5 * f_sigma * d_log_sigma / np.sqrt(2.0 * np.pi)
            else:
                a_list[i] = f_sigma * d_log_sigma / np.sqrt(2.0 * np.pi)

        self.amps = a_list
        # note this is different from the part of gNFW, since sersic_2D is a 2D profile, while gNFW_3D
        # is a 3D profile
        self.sigmas = sigma_list

    @grids.grid_like_to_structure
    @grids.transform
    @grids.relocate_to_radial_minimum
    def image_from_grid(self, grid, grid_radial_minimum=None):
        """ Calculate the projected convergence at a given set of arc-second gridded coordinates.

        Parameters
        ----------
        grid : aa.Grid
            The grid of (y,x) arc-second coordinates the convergence is computed on.

        """
        return self.image_from_grid_radii(grid_radii=self.grid_to_eccentric_radii(grid))

    def image_from_grid_radii(self, grid_radii):

        for i in range(len(self.sigmas)):
            if i == 0:
                light = self.intensity_one_gaussian(
                    grid_radii=grid_radii, sigma=self.sigmas[i], intensity=self.amps[i]
                )
            else:
                light += self.intensity_one_gaussian(
                    grid_radii=grid_radii, sigma=self.sigmas[i], intensity=self.amps[i]
                )
        return light

    def intensity_one_gaussian(self, grid_radii, sigma, intensity):
        """Calculate the intensity of the Gaussian light profile on a grid of radial coordinates.

        Parameters
        ----------
        grid_radii : float
            The radial distance from the centre of the profile. for each coordinate on the grid.
        """
        return np.multiply(
            intensity, np.exp(-0.5 * np.square(np.divide(grid_radii, sigma)))
        )


import warnings

import autofit as af
import numpy as np
from autoarray.structures import arrays
from autoarray.structures import grids
from autogalaxy import dimensions as dim
from autogalaxy.profiles import mass_profiles as mp

# from pyquad import quad_grid
from scipy.special import wofz, comb
import typing
import time


class StellarProfile:
    pass


def kesi(p):
    """
        see Eq.(6) of 1906.08263
    """
    n_list = np.arange(0, 2 * p + 1, 1)
    kesi_n = (2.0 * p * np.log(10) / 3.0 + 2.0 * np.pi * n_list * 1j) ** (0.5)
    return kesi_n


def eta(p):
    """
        see Eq.(6) of 1906.00263
    """
    eta_list = np.zeros(int(2 * p + 1))
    kesi_list = np.zeros(int(2 * p + 1))
    kesi_list[0] = 0.5
    kesi_list[1 : p + 1] = 1.0
    kesi_list[int(2 * p)] = 1.0 / 2.0 ** p

    for i in np.arange(1, p, 1):
        kesi_list[2 * p - i] = kesi_list[2 * p - i + 1] + 2 ** (-p) * comb(p, i)

    for i in np.arange(0, 2 * p + 1, 1):
        eta_list[i] = (
            (-1) ** i * 2.0 * np.sqrt(2.0 * np.pi) * 10 ** (p / 3.0) * kesi_list[i]
        )

    return eta_list


def w_f_approx(z):
    """
    Compute the Faddeeva function :math:`w_{\mathrm F}(z)` using the
    approximation given in Zaghloul (2017).
    :param z: complex number
    :type z: ``complex`` or ``numpy.array(dtype=complex)``
    :return: :math:`w_\mathrm{F}(z)`
    :rtype: ``complex``

    # This function is copied from
    # "https://github.com/sibirrer/lenstronomy/tree/master/lenstronomy/LensModel/Profiles"
    # written by Anowar J. Shajib (see 1906.08263)
    """

    reg_minus_imag = z.imag < 0.0
    z[reg_minus_imag] = np.conj(z[reg_minus_imag])

    sqrt_pi = 1 / np.sqrt(np.pi)
    i_sqrt_pi = 1j * sqrt_pi

    wz = np.empty_like(z)

    z_imag2 = z.imag ** 2
    abs_z2 = z.real ** 2 + z_imag2

    reg1 = abs_z2 >= 38000.0
    if np.any(reg1):
        wz[reg1] = i_sqrt_pi / z[reg1]

    reg2 = (256.0 <= abs_z2) & (abs_z2 < 38000.0)
    if np.any(reg2):
        t = z[reg2]
        wz[reg2] = i_sqrt_pi * t / (t * t - 0.5)

    reg3 = (62.0 <= abs_z2) & (abs_z2 < 256.0)
    if np.any(reg3):
        t = z[reg3]
        wz[reg3] = (i_sqrt_pi / t) * (1 + 0.5 / (t * t - 1.5))

    reg4 = (30.0 <= abs_z2) & (abs_z2 < 62.0) & (z_imag2 >= 1e-13)
    if np.any(reg4):
        t = z[reg4]
        tt = t * t
        wz[reg4] = (i_sqrt_pi * t) * (tt - 2.5) / (tt * (tt - 3.0) + 0.75)

    reg5 = (62.0 > abs_z2) & np.logical_not(reg4) & (abs_z2 > 2.5) & (z_imag2 < 0.072)
    if np.any(reg5):
        t = z[reg5]
        u = -t * t
        f1 = sqrt_pi
        f2 = 1
        s1 = [1.320522, 35.7668, 219.031, 1540.787, 3321.99, 36183.31]
        s2 = [1.841439, 61.57037, 364.2191, 2186.181, 9022.228, 24322.84, 32066.6]

        for s in s1:
            f1 = s - f1 * u
        for s in s2:
            f2 = s - f2 * u

        wz[reg5] = np.exp(u) + 1j * t * f1 / f2

    reg6 = (30.0 > abs_z2) & np.logical_not(reg5)
    if np.any(reg6):
        t3 = -1j * z[reg6]

        f1 = sqrt_pi
        f2 = 1
        s1 = [5.9126262, 30.180142, 93.15558, 181.92853, 214.38239, 122.60793]
        s2 = [
            10.479857,
            53.992907,
            170.35400,
            348.70392,
            457.33448,
            352.73063,
            122.60793,
        ]

        for s in s1:
            f1 = f1 * t3 + s
        for s in s2:
            f2 = f2 * t3 + s

        wz[reg6] = f1 / f2

    # wz[reg_minus_imag] = np.conj(wz[reg_minus_imag])

    return wz


class EllipticalCoreSersic_MGE(mp.EllipticalMassProfile, StellarProfile):
    @af.map_types
    def __init__(
        self,
        centre: dim.Position = (0.0, 0.0),
        elliptical_comps: typing.Tuple[float, float] = (0.0, 0.0),
        effective_radius: dim.Length = 0.01,
        sersic_index: float = 0.6,
        radius_break: dim.Length = 0.01,
        intensity_break: dim.Luminosity = 0.05,
        gamma: float = 0.25,
        alpha: float = 3.0,
        mass_to_light_ratio: dim.MassOverLuminosity = 1.0,
    ):

        """
        The MGE based Sersic profile.
        """

        super(EllipticalCoreSersic_MGE, self).__init__(
            centre=centre, elliptical_comps=elliptical_comps
        )
        super(mp.EllipticalMassProfile, self).__init__(
            centre=centre, elliptical_comps=elliptical_comps
        )
        self.mass_to_light_ratio = mass_to_light_ratio

        if self.axis_ratio > 0.9999:
            self.axis_ratio = 0.9999

            #########################################################
        # Below is to decompose a gNFW into a series of Gaussians
        #########################################################

        p = int(
            28
        )  # number of terms used to approximate function "f" below. Fix it to be 28 is okay.
        # n = int(60) # number of Gaussians to use. It can vary depending on the accuracy one want to achieve.
        n = int(
            20
        )  # number of Gaussians to use. It can vary depending on the accuracy one want to achieve.

        self.sersic_constant = (
            (2 * sersic_index)
            - (1.0 / 3.0)
            + (4.0 / (405.0 * sersic_index))
            + (46.0 / (25515.0 * sersic_index ** 2))
            + (131.0 / (1148175.0 * sersic_index ** 3))
            - (2194697.0 / (30690717750.0 * sersic_index ** 4))
        )

        self.intensity_prime = (
            intensity_break
            * (2.0 ** (-gamma / alpha))
            * np.exp(
                self.sersic_constant
                * (((2.0 ** (1.0 / alpha)) * radius_break) / effective_radius)
                ** (1.0 / sersic_index)
            )
        )

        def core_sersic_2D(r):
            return (
                self.intensity_prime
                * (1.0 + (radius_break / r) ** alpha) ** (gamma / alpha)
                * np.exp(
                    -self.sersic_constant
                    * ((r ** alpha + radius_break ** alpha) / effective_radius ** alpha)
                    ** (1.0 / (sersic_index * alpha))
                )
            )

        kesi_list = kesi(p)
        eta_list = eta(p)

        def f(sigma):
            return np.sum(eta_list * np.real(target_function(sigma * kesi_list)))

        rmin = effective_radius / 100.0
        rmax = effective_radius * 20.0
        # rmin = effective_radius / 500.0
        # rmax = effective_radius * 50.0

        log_sigma_list = np.linspace(np.log(rmin), np.log(rmax), n)
        d_log_sigma = log_sigma_list[1] - log_sigma_list[0]
        sigma_list = np.exp(log_sigma_list)

        a_list = np.zeros(n)

        for i in range(n):
            f_sigma = np.sum(
                eta_list * np.real(core_sersic_2D(sigma_list[i] * kesi_list))
            )
            if (i == -1) or (i == (n - 1)):
                a_list[i] = 0.5 * f_sigma * d_log_sigma / np.sqrt(2.0 * np.pi)
            else:
                a_list[i] = f_sigma * d_log_sigma / np.sqrt(2.0 * np.pi)

        self.amps = a_list
        # note this is different from the part of gNFW, since sersic_2D is a 2D profile, while gNFW_3D
        # is a 3D profile
        self.sigmas = sigma_list
        self.sigmas_for_defl = sigma_list * np.sqrt(self.axis_ratio)
        # Note this part is also different from the one in gNFW.

    def zeta_from_grid(self, grid, sigma):

        """
        The key part to compute the deflection angle of each Gaussian.
        Because of my optimization, there are blocks looking weird and indirect. What I'm doing here
        is trying to avoid big matrix operation to save time.
        I think there are still spaces we can optimize.

        It seems when using w_f_approx, it gives some errors if y < 0. So when computing for places
        where y < 0, we first compute the value at - y, and then change its sign.
        """

        q2 = self.axis_ratio ** 2.0

        if self.count == 0:
            scale_factor = self.axis_ratio / (sigma * np.sqrt(2.0 * (1.0 - q2)))
            self.sigma = sigma
            self.xs = (grid[:, 1] * scale_factor).copy()
            self.ys = (grid[:, 0] * scale_factor).copy()
            self.ys_minus = self.ys < 0.0
            self.ys[self.ys_minus] *= -1
            self.z = self.xs + 1j * self.ys
            self.zq = self.axis_ratio * self.xs + 1j * self.ys / self.axis_ratio
            self.expv = -self.xs ** 2.0 * (1.0 - q2) - self.ys ** 2.0 * (1.0 / q2 - 1.0)
        else:
            self.z /= sigma / self.sigma
            self.zq /= sigma / self.sigma
            self.expv /= (sigma / self.sigma) ** 2.0
            self.sigma = sigma

        output_grid = -1j * (
            w_f_approx(self.z) - np.exp(self.expv) * w_f_approx(self.zq)
        )

        self.count += 1

        output_grid[self.ys_minus] = np.conj(output_grid[self.ys_minus])

        return output_grid

    @grids.grid_like_to_structure
    @grids.transform
    @grids.relocate_to_radial_minimum
    def deflections_from_grid(self, grid):

        self.count = 0

        for i in range(len(self.sigmas)):
            if i == 0:
                angle = (self.amps[i] * self.sigmas_for_defl[i]) * self.zeta_from_grid(
                    grid=grid, sigma=self.sigmas_for_defl[i]
                )
            else:
                angle += (self.amps[i] * self.sigmas_for_defl[i]) * self.zeta_from_grid(
                    grid=grid, sigma=self.sigmas_for_defl[i]
                )

        angle *= np.sqrt((2.0 * np.pi) / (1.0 - self.axis_ratio ** 2.0))

        return np.multiply(
            self.mass_to_light_ratio,
            self.rotate_grid_from_profile(np.vstack((-angle.imag, angle.real)).T),
        )

    @grids.grid_like_to_structure
    @grids.transform
    @grids.relocate_to_radial_minimum
    def convergence_from_grid(self, grid):
        """ Calculate the projected convergence at a given set of arc-second gridded coordinates.

        Parameters
        ----------
        grid : aa.Grid
            The grid of (y,x) arc-second coordinates the convergence is computed on.

        """

        eccentric_radii = self.grid_to_eccentric_radii(grid)

        # Note here is eccentric radius to be consistent with the EllipticalSersic

        light = self.intensity_at_radius(radius=eccentric_radii)

        return np.multiply(self.mass_to_light_ratio, light)

    def intensity_at_radius(self, radius):

        for i in range(len(self.sigmas)):
            if i == 0:
                light = self.intensity_one_gaussian(
                    grid_radii=radius, sigma=self.sigmas[i], intensity=self.amps[i]
                )
            else:
                light += self.intensity_one_gaussian(
                    grid_radii=radius, sigma=self.sigmas[i], intensity=self.amps[i]
                )
        return light

    def intensity_one_gaussian(self, grid_radii, sigma, intensity):
        """Calculate the intensity of the Gaussian light profile on a grid of radial coordinates.

        Parameters
        ----------
        grid_radii : float
            The radial distance from the centre of the profile. for each coordinate on the grid.
        """
        return np.multiply(
            intensity, np.exp(-0.5 * np.square(np.divide(grid_radii, sigma)))
        )
