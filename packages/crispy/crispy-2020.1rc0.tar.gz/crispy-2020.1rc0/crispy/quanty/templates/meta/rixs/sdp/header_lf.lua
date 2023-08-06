--------------------------------------------------------------------------------
-- Quanty input file generated using Crispy. If you use this file please cite
-- the following reference: http://dx.doi.org/10.5281/zenodo.1008184.
--
-- elements: #m
-- symmetry: #symmetry
-- experiment: #experiment
-- edge: #edge
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- Set the verbosity of the calculation. For increased verbosity use the values
-- 0x00FF or 0xFFFF.
--------------------------------------------------------------------------------
Verbosity($Verbosity)

--------------------------------------------------------------------------------
-- Define the parameters of the calculation.
--------------------------------------------------------------------------------
Temperature = $Temperature -- temperature (Kelvin)

NPsis = $NPsis  -- number of states to consider in the spectra calculation
NPsisAuto = $NPsisAuto  -- determine the number of state automatically
NConfigurations = $NConfigurations  -- number of configurations

-- X-axis parameters
Emin1 = $XEmin  -- minimum value of the energy range (eV)
Emax1 = $XEmax  -- maximum value of the energy range (eV)
NPoints1 = $XNPoints  -- number of points of the spectra
ExperimentalShift1 = $XExperimentalShift  -- experimental edge energy (eV)
Gaussian1 = $XGaussian  -- Gaussian FWHM (eV)
Gamma1 = $XGamma  -- Lorentzian FWHM used in the spectra calculation (eV)

WaveVector = $XWaveVector  -- wave vector
Ev = $XFirstPolarization  -- vertical polarization
Eh = $XSecondPolarization  -- horizontal polarization

-- Y-axis parameters
Emin2 = $YEmin  -- minimum value of the energy range (eV)
Emax2 = $YEmax  -- maximum value of the energy range (eV)
NPoints2 = $YNPoints  -- number of points of the spectra
ExperimentalShift2 = $YExperimentalShift  -- experimental edge energy (eV)
Gaussian2 = $YGaussian  -- Gaussian FWHM (eV)
Gamma2 = $YGamma  -- Lorentzian FWHM used in the spectra calculation (eV)

WaveVector = $YWaveVector  -- wave vector
Ev = $YFirstPolarization  -- vertical polarization
Eh = $YSecondPolarization  -- horizontal polarization

SpectraToCalculate = $SpectraToCalculate  -- types of spectra to calculate
DenseBorder = $DenseBorder -- number of determinants where we switch from dense methods to sparse methods

Prefix = "$Prefix"  -- file name prefix

--------------------------------------------------------------------------------
-- Toggle the Hamiltonian terms.
--------------------------------------------------------------------------------
AtomicTerm = $AtomicTerm
CrystalFieldTerm = $CrystalFieldTerm
LmctLigandsHybridizationTerm = $LmctLigandsHybridizationTerm
MlctLigandsHybridizationTerm = $MlctLigandsHybridizationTerm
MagneticFieldTerm = $MagneticFieldTerm
ExchangeFieldTerm = $ExchangeFieldTerm

--------------------------------------------------------------------------------
-- Define the number of electrons, shells, etc.
--------------------------------------------------------------------------------
NBosons = 0
NFermions = 18

NElectrons_#i = 2
NElectrons_#f = 6
NElectrons_#m = $NElectrons_#m

IndexDn_#i = {0}
IndexUp_#i = {1}
IndexDn_#f = {2, 4, 6}
IndexUp_#f = {3, 5, 7}
IndexDn_#m = {8, 10, 12, 14, 16}
IndexUp_#m = {9, 11, 13, 15, 17}

if LmctLigandsHybridizationTerm then
    NFermions = 28

    NElectrons_L1 = 10

    IndexDn_L1 = {18, 20, 22, 24, 26}
    IndexUp_L1 = {19, 21, 23, 25, 27}
end

if MlctLigandsHybridizationTerm then
    NFermions = 28

    NElectrons_L2 = 0

    IndexDn_L2 = {18, 20, 22, 24, 26}
    IndexUp_L2 = {19, 21, 23, 25, 27}
end

if LmctLigandsHybridizationTerm and MlctLigandsHybridizationTerm then
    return
end

--------------------------------------------------------------------------------
-- Initialize the Hamiltonians.
--------------------------------------------------------------------------------
H_i = 0
H_m = 0
H_f = 0
