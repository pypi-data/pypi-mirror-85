from ._picoharp_300 import PicoHarp_300


__all__ = ["read_phd"]


def read_phd(filename):
    """Read Picoharp phd file

    Parameters
    ----------
    filename : str
        Picoharp ".phd" filename.

    Returns
    -------
    PicoHarp_300 object
        A `Picoharp_300` object representing the
        picoharp phd file
    """
    return PicoHarp_300(filename)
