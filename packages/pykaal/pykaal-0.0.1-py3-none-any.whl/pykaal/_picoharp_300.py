import matplotlib.pyplot as plt
import numpy as np

from ._picoharp_parser import PicoharpParser


class PicoHarp_300(object):
    """
    Picoharp object that represents the Picoharp phd file format
    in python.
    """

    def __init__(self, filename):
        self.filname = filename

        self.parser = PicoharpParser(filename)
        self._curves = self.parser.get_all_curves()

    def __repr__(self):
        return self.parser.info()

    def __len__(self):
        return len(self._curves)

    def curve(self, n):
        """Get histogram for a given curve number

        Parameters
        ----------
        n : int
            Curve number

        Returns
        -------
        numpy.ndarray
            Curve as a numpy array for a given array
        """
        time_window = self._time_window(n)
        curve = self._curves[n][1][0:time_window]
        return curve

    def res(self, n):
        """Get curve resolution

        Parameters
        ----------
        n : int
            Curve number
        """
        return self._curves[n][0]

    def _time_window(self, n):
        return int(np.floor(self.parser.get_time_window_in_ns(n)))

    def _time_axis(self, n):
        """Get time axis accounting for resolution

        Parameters
        ----------
        n : int
            Curve number

        Returns
        -------
        `numpy.ndarray`
            Time axis as numpy array
        """
        res = self.res(n)
        size = self._time_window(n)
        t = np.arange(0, size * res, res, np.float)
        return t

    def t(self, n):
        """Short hand for generating time axis for a given curve number

        Parameters
        ----------
        n : int
            Curve number

        Returns
        -------
        `numpy.ndarray`
            Time axis as numpy array
        """
        return self._time_axis(n)

    def intensity(self, n):
        """Get integrated intensity for a given curve number

        Parameters
        ----------
        n : int
            Curve number

        Returns
        -------
        int
            Integrated intensity under a curve
        """
        return self.parser.get_integral_counts(n)

    # TODO - Move this to utils with fitting
    # TODO - Option to apply to all traces
    def smooth(self, n, boxwidth=3, mode="same"):
        curve = self.curve(n)
        sm_curve = np.convolve(curve, np.ones(boxwidth) / boxwidth, mode=mode)
        return sm_curve

    def plot(self, n, ax=None, norm=True, smooth=False, boxwidth=3, mode="same"):
        """Plot the given curve number

        Parameters
        ----------
        n : int
            Curve number
        ax : `matplotlib.axes.Axes`, optional
            Matplotlib figure axes to plot the data, by default None.
            If None, figure and axes are generated.
        norm : bool, optional
            Normalize the intensity to maximum value, by default True
        smooth : bool, optional
            Smoothen curve, by default False
        boxwidth : int, optional
            boxwidth, by default 3
            Refer to `numpy.convolve` for more details
        mode : str, optional
            mode, by default "same"
            Refer to `numpy.convolve` for more details
        """
        t = self.t(n)

        if smooth:
            curve = self.smooth(n, boxwidth=boxwidth, mode=mode)
        else:
            curve = self.curve(n)

        if norm:
            curve = curve / np.max(curve)

        # plot
        if ax is None:
            fig, ax = plt.subplots()
        ax.plot(t, curve)
        ax.set_xlabel("Time (ns)")
        if norm:
            ax.set_ylabel("Intensity (norm.)")
        else:
            ax.set_ylabel("Intensity (a.u.)")
        ax.set_yscale("log")
