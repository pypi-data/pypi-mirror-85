def flam2millijansky(wavelength_angstrom,flam):
    """
    flam2millijansky converts spectral profile from flam (i.e., erg/s/cm**2/A) to mJy (i.e., 1e-26 erg/s/cm**2/Hz).
    #####
    + Inputs:
      - wavelength_angstrom = 1D array of wavelengths in angstrom
      - flam = 1D array of flux in flam (i.e., erg/s/cm**2/A), parallel to wavelength_angstrom
    + Output:
      - return mjy = 1D array of flux in mJy.
    """
    # wavelength * flam = frequency * fnu
    # speed_of_light = frequency * wavelength
    # 1 mJy = 1e-26 erg/s/cm**2/Hz
    speed_of_light = 299792458e10 # A/s
    fnu2mjy = 1e26
    frequency_hz = speed_of_light / wavelength_angstrom
    fnu = wavelength_angstrom * flam / frequency_hz
    mjy = fnu * fnu2mjy
    return mjy
