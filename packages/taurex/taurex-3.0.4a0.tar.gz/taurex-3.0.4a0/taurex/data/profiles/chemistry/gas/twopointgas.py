from .gas import Gas
from taurex.util import molecule_texlabel
import math
import numpy as np


class TwoPointGas(Gas):
    """

    Two point gas profile.

    A gas profile with two different mixing layers at the surface of the
    planet and top of the atmosphere and interpolated between the two

    Parameters
    -----------
    molecule_name : str
        Name of molecule

    mix_ratio_surface : float
        Mixing ratio of the molecule on the planet surface

    mix_ratio_top : float
        Mixing ratio of the molecule at the top of the atmosphere


    """

    def __init__(self, molecule_name='CH4',
                 mix_ratio_surface=1e-4, mix_ratio_top=1e-8):
        super().__init__('TwoPointGas', molecule_name)
        self._mix_surface = mix_ratio_surface
        self._mix_top = mix_ratio_top
        self.add_surface_param()
        self.add_top_param()
        self._mix_profile = None

    @property
    def mixProfile(self):
        """

        Returns
        -------
        mix: :obj:`array`
            Mix ratio for molecule at each layer
        """
        return self._mix_profile

    @property
    def mixRatioSurface(self):
        """Abundance on the planets surface"""
        return self._mix_surface

    @property
    def mixRatioTop(self):
        """Abundance on the top of atmosphere"""
        return self._mix_top

    @mixRatioSurface.setter
    def mixRatioSurface(self, value):
        self._mix_surface = value

    @mixRatioTop.setter
    def mixRatioTop(self, value):
        self._mix_top = value

    def add_surface_param(self):

        param_name = self.molecule
        param_tex = molecule_texlabel(param_name)

        param_surface = '{}_surface'.format(param_name)
        param_surf_tex = '{}_surface'.format(param_tex)

        def read_surf(self):
            return self._mix_surface

        def write_surf(self, value):
            self._mix_surface = value

        fget_surf = read_surf
        fset_surf = write_surf

        bounds = [1.0e-12, 0.1]

        default_fit = False
        self.add_fittable_param(param_surface, param_surf_tex, fget_surf,
                                fset_surf, 'log', default_fit, bounds)

    def add_top_param(self):

        param_name = self.molecule
        param_tex = molecule_texlabel(param_name)

        param_top = '{}_top'.format(param_name)
        param_top_tex = '{}_top'.format(param_tex)

        def read_top(self):
            return self._mix_top

        def write_top(self, value):
            self._mix_top = value

        fget_top = read_top
        fset_top = write_top

        bounds = [1.0e-12, 0.1]

        default_fit = False
        self.add_fittable_param(param_top, param_top_tex, fget_top, fset_top,
                                'log', default_fit, bounds)

    def initialize_profile(self, nlayers=None, temperature_profile=None,
                           pressure_profile=None, altitude_profile=None):
        self._mix_profile = np.zeros(nlayers)

        chem_surf = self._mix_surface
        chem_top = self._mix_top
        p_surf = pressure_profile[0]
        p_top = pressure_profile[-1]

        a = (math.log10(chem_surf)-math.log10(chem_top)) / \
            (math.log10(p_surf)-math.log10(p_top))

        b = math.log10(chem_surf)-a*math.log10(p_surf)

        self._mix_profile[1:-1] = 10**(a * np.log10(pressure_profile[1:-1])+b)
        self._mix_profile[0] = chem_surf
        self._mix_profile[-1] = chem_top

    def write(self, output):
        gas_entry = super().write(output)
        gas_entry.write_scalar('mix_ratio_top', self.mixRatioTop)
        gas_entry.write_scalar('mix_ratio_surface', self.mixRatioSurface)
        return gas_entry
