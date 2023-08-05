import sys

import jax.numpy as jnp
import numpy

from .. import tensor as T
from .base import jax_wrap
import jax
import jax.lax as jla


# Add the apodization windows

names = ["blackman", "bartlett", "hamming", "hanning", "kaiser"]

module = sys.modules[__name__]
for name in names:
    module.__dict__.update({name: jax_wrap(jnp.__dict__[name])})


for name in ["convolve", "convolve2d", "correlate", "correlate2d"]:
    module.__dict__.update({name: jax_wrap(jax.scipy.signal.__dict__[name])})


# Add some utility functions


def hat_1D(x, t_left, t_center, t_right):
    """hat basis function in 1-D

    Hat function, continuous piecewise linear

    Parameters
    ----------

    x: array-like
        the sampled input space

    t_left: scalar
        the position of the left knot

    t_center: scalar
        the position of the center knot

    t_right: scalar
        the position of the right knot

    Returns
    -------

    output : array
        same shape as x with applied hat function
    """
    eps = 1e-6
    slope_left = 1 / (t_center - t_left)
    slope_right = 1 / (t_right - t_center)
    output = (
        (relu(x - t_left)) * slope_left
        - relu(x - t_center) * (slope_left + slope_right)
        + relu(x - t_right) * slope_right
    )
    return output


def _extract_signal_patches(signal, window_length, hop=1, data_format="NCW"):
    if hasattr(window_length, "shape"):
        assert window_length.shape == ()
    else:
        assert not hasattr(window_length, "__len__")

    if data_format == "NCW":
        if signal.ndim == 2:
            signal_3d = signal[:, None, :]
        elif signal.ndim == 1:
            signal_3d = signal[None, None, :]
        else:
            signal_3d = signal

        N = (signal_3d.shape[2] - window_length) // hop + 1
        indices = jnp.arange(window_length) + jnp.expand_dims(jnp.arange(N) * hop, 1)
        indices = jnp.reshape(indices, [1, 1, N * window_length])
        patches = jnp.take_along_axis(signal_3d, indices, 2)
        output = jnp.reshape(patches, signal_3d.shape[:2] + (N, window_length))
        if signal.ndim == 1:
            return output[0, 0]
        elif signal.ndim == 2:
            return output[:, 0, :]
        else:
            return output
    else:
        error


extract_signal_patches = jax_wrap(_extract_signal_patches, module)


def _extract_image_patches(
    image, window_shape, hop=1, data_format="NCHW", mode="valid"
):
    if mode == "same":
        p1 = window_shape[0] - 1
        p2 = window_shape[1] - 1
        image = jnp.pad(
            image,
            [(0, 0), (0, 0), (p1 // 2, p1 - p1 // 2), (p2 // 2, p2 - p2 // 2)],
        )
    if not hasattr(hop, "__len__"):
        hop = (hop, hop)
    if data_format == "NCHW":

        # compute the number of windows in both dimensions
        N = (
            (image.shape[2] - window_shape[0]) // hop[0] + 1,
            (image.shape[3] - window_shape[1]) // hop[1] + 1,
        )

        # compute the base indices of a 2d patch
        patch = jnp.arange(numpy.prod(window_shape)).reshape(window_shape)
        offset = jnp.expand_dims(jnp.arange(window_shape[0]), 1)
        patch_indices = patch + offset * (image.shape[3] - window_shape[1])

        # create all the shifted versions of it
        ver_shifts = jnp.reshape(
            jnp.arange(N[0]) * hop[0] * image.shape[3], (-1, 1, 1, 1)
        )
        hor_shifts = jnp.reshape(jnp.arange(N[1]) * hop[1], (-1, 1, 1))
        all_cols = patch_indices + jnp.reshape(jnp.arange(N[1]) * hop[1], (-1, 1, 1))
        indices = patch_indices + ver_shifts + hor_shifts

        # now extract shape (1, 1, H'W'a'b')
        flat_indices = jnp.reshape(indices, [1, 1, -1])
        # shape is now (N, C, W*H)
        flat_image = jnp.reshape(image, (image.shape[0], image.shape[1], -1))
        # shape is now (N, C)
        patches = jnp.take_along_axis(flat_image, flat_indices, 2)
        return jnp.reshape(patches, image.shape[:2] + N + tuple(window_shape))
    else:
        error


extract_image_patches = jax_wrap(_extract_image_patches)


def fourier_complex_morlet(bandwidths, centers, N):
    """Complex Morlet wavelet in Fourier

    Parameters
    ----------

    bandwidths: array
        the bandwidth of the wavelet

    centers: array
        the centers of the wavelet

    freqs: array (optional)
        the frequency sampling in radion going from 0 to pi and back to 0
        :param N:

    """

    freqs = T.linspace(0, 2 * numpy.pi, N)
    envelop = T.exp(-0.25 * (freqs - centers) ** 2 * bandwidths ** 2)
    H = (freqs <= numpy.pi).astype("float32")
    return envelop * H


def complex_morlet(bandwidths, centers, time=None):
    """Complex Morlet wavelet

    It corresponds to with (B, C)::

        \phi(t) = \frac{1}{\pi B} e^{-\frac{t^2}{B}}e^{j2\pi C t}

    For a filter bank do

    J = 8
    Q = 1
    scales = T.power(2,T.linspace(0, J, J*Q))
    scales = scales[:, None]
    complex_morlet(scales, 1/scales)

    Parameters
    ----------

    bandwidths: array
        the bandwidth of the wavelet

    centers: array
        the centers of the wavelet

    time: array (optional)
        the time sampling

    Returns
    -------

    wavelet: array like
        the wavelet centered at 0

    """
    if time is None:
        B = 6 * bandwidths.max() + 1
        time = T.linspace(-(B // 2), B // 2, int(T.get(B)))
    envelop = T.exp(-((time / bandwidths) ** 2))
    wave = T.exp(1j * centers * time)
    return envelop * wave


def littewood_paley_normalization(filter_bank, down=None, up=None):
    lp = T.abs(filter_bank).sum(0)
    freq = T.linspace(0, 2 * numpy.pi, lp.shape[0])
    down = 0 if down is None else down
    up = numpy.pi or up
    lp = T.where(T.logical_and(freq >= down, freq <= up), lp, 1)
    return filter_bank / lp


def tukey(M, alpha=0.5):
    """Return a Tukey window, also known as a tapered cosine window.
    Parameters
    ----------
    M : int
        Number of points in the output window. If zero or less, an empty
        array is returned.
    alpha : float, optional
        Shape parameter of the Tukey window, representing the fraction of the
        window inside the cosine tapered region.
        If zero, the Tukey window is equivalent to a rectangular window.
        If one, the Tukey window is equivalent to a Hann window.
    Returns
    -------
    w : ndarray
        The window, with the maximum value normalized to 1 (though the value 1
        does not appear if `M` is even and `sym` is True).
    References
    ----------
    .. [1] Harris, Fredric J. (Jan 1978). "On the use of Windows for Harmonic
           Analysis with the Discrete Fourier Transform". Proceedings of the
           IEEE 66 (1): 51-83. :doi:`10.1109/PROC.1978.10837`
    .. [2] Wikipedia, "Window function",
           https://en.wikipedia.org/wiki/Window_function#Tukey_window
    """
    n = T.arange(0, M)
    width = int(numpy.floor(alpha * (M - 1) / 2.0))
    n1 = n[0 : width + 1]
    n2 = n[width + 1 : M - width - 1]
    n3 = n[M - width - 1 :]

    w1 = 0.5 * (1 + T.cos(numpy.pi * (-1 + 2.0 * n1 / alpha / (M - 1))))
    w2 = T.ones(n2.shape)
    w3 = 0.5 * (1 + T.cos(numpy.pi * (-2.0 / alpha + 1 + 2.0 * n3 / alpha / (M - 1))))

    w = T.concatenate((w1, w2, w3))

    return w


def morlet(M, s, w=5):
    """
    Complex Morlet wavelet.
    Parameters
    ----------
    M : int
        Length of the wavelet.

    s : float, optional
        Scaling factor, windowed from ``-s*2*pi`` to ``+s*2*pi``. Default is 1.
    w : float, optional
        Omega0. Default is 5
    complete : bool, optional
        Whether to use the complete or the standard version.
    Returns
    -------
    morlet : (M,) ndarray
    See Also
    --------
    morlet2 : Implementation of Morlet wavelet, compatible with `cwt`.
    scipy.signal.gausspulse
    Notes
    -----
    The standard version::
        pi**-0.25 * exp(1j*w*x) * exp(-0.5*(x**2))
    This commonly used wavelet is often referred to simply as the
    Morlet wavelet.  Note that this simplified version can cause
    admissibility problems at low values of `w`.
    The complete version::
        pi**-0.25 * (exp(1j*w*x) - exp(-0.5*(w**2))) * exp(-0.5*(x**2))
    This version has a correction
    term to improve admissibility. For `w` greater than 5, the
    correction term is negligible.
    Note that the energy of the return wavelet is not normalised
    according to `s`.
    The fundamental frequency of this wavelet in Hz is given
    by ``f = 2*s*w*r / M`` where `r` is the sampling rate.
    """
    limit = 2 * numpy.pi
    x = T.linspace(-limit, limit, M) * s
    sine = T.cos(w * x) + 1j * T.sin(w * x)
    envelop = T.exp(-0.5 * (x ** 2))

    # apply correction term for admissibility
    wave = sine - T.exp(-0.5 * (w ** 2))

    # now localize the wave to obtain a wavelet
    wavelet = wave * envelop * numpy.pi ** (-0.25)

    return wavelet


def bin_to_freq(bins, max_f):
    return (bins / bins.max()) * max_f


def freq_to_bin(freq, n_bins, fmin, fmax):
    unit = (fmax - fmin) / n_bins
    return (freq / unit).astype("int32")


def mel_to_freq(m, option="linear"):
    # convert mel to frequency with
    if option == "linear":
        # Fill in the linear scale
        f_sp = 200.0 / 3

        # And now the nonlinear scale
        # beginning of log region (Hz)
        min_log_hz = 1000.0
        min_log_mel = min_log_hz / f_sp  # same (Mels)
        # step size for log region
        logstep = numpy.log(6.4) / 27.0

        # If we have vector data, vectorize
        freq = min_log_hz * T.exp(logstep * (m - min_log_mel))
        return T.where(m >= min_log_mel, freq, f_sp * m)
    else:
        return 700 * (T.power(10.0, (m / 2595)) - 1)


def freq_to_mel(f, option="linear"):
    # convert frequency to mel with
    if option == "linear":

        # linear part slope
        f_sp = 200.0 / 3

        # Fill in the log-scale part
        min_log_hz = 1000.0  # beginning of log region (Hz)
        min_log_mel = min_log_hz / f_sp  # same (Mels)
        logstep = numpy.log(6.4) / 27.0  # step size for log region
        mel = min_log_mel + T.log(f / min_log_hz) / logstep
        return T.where(f >= min_log_hz, mel, f / f_sp)
    else:
        return 2595 * T.log10(1 + f / 700)


def power_to_db(S, ref=1.0, amin=1e-10, top_db=80.0):
    """Convert a power spectrogram (amplitude squared) to decibel (dB) units.

    https://librosa.github.io/librosa/_modules/librosa/core/spectrum.html#power_to_db.
    This computes the scaling ``10 * log10(S / ref)`` in a numerically
    stable way.

    Parameters
    ----------
    S : numpy.ndarray
        inumpy.t power

    ref : scalar or callable
        If scalar, the amplitude `abs(S)` is scaled relative to `ref`:
        `10 * log10(S / ref)`.
        Zeros in the output correspond to positions where `S == ref`.

        If callable, the reference value is computed as `ref(S)`.

    amin : float > 0 [scalar]
        minimum threshold for `abs(S)` and `ref`

    top_db : float >= 0 [scalar]
        threshold the output at `top_db` below the peak:
        ``max(10 * log10(S)) - top_db``

    Returns
    -------
    S_db : numpy.ndarray
        ``S_db ~= 10 * log10(S) - 10 * log10(ref)``

    See Also
    --------
    perceptual_weighting
    db_to_power
    amplitude_to_db
    db_to_amplitude
    """
    ref_value = numpy.abs(ref)
    log_spec = 10.0 * T.log10(T.maximum(amin, S) / T.maximum(amin, ref))
    if top_db is not None:
        if top_db < 0:
            error
        return T.maximum(log_spec, log_spec.max() - top_db)
    else:
        return log_spec


# Now some filter-bank and additional Time-Frequency Repr.


def sinc_bandpass(time, f0, f1):
    """
    ensure that f0<f1 and f0>0, f1<1
    whenever time is ..., -1, 0, 1, ...
    """
    high = f0 * T.sinc(time * f0)
    low = f1 * T.sinc(time * f1)
    return high - low


def mel_filterbank(length, n_filter, low, high, nyquist):
    # convert the low and high frequency into mel scale
    low_freq_mel = freq_to_mel(low)
    high_freq_mel = freq_to_mel(high)

    # generate center frequencies uniformly spaced in Mel scale.
    mel_points = T.linspace(low_freq_mel, high_freq_mel, n_filter + 2)
    # turn them into frequency and thus becoming in log scale
    freq_points = freq_to_bin(mel_to_freq(mel_points), length, 0, nyquist)
    peaks = T.expand_dims(freq_points, 1)
    freqs = T.range(length)
    filter_bank = T.hat_1D(freqs, peaks[:-2], peaks[1:-1], peaks[2:])
    return filter_bank


def stft(signal, window, hop, apod=T.ones, nfft=None, mode="valid"):
    """
    Compute the Shoft-Time-Fourier-Transform of a
    signal given the window length, hop and additional
    parameters.

    Parameters
    ----------

        signal: array
            the signal (possibly stacked of signals)

        window: int
            the window length to be considered for the fft

        hop: int
            the amount by which the window is moved

        apod: func
            a function that takes an integer as inumpy.t and return
            the apodization window of the same length

        nfft: int (optional)
            the number of bin that the fft on the window will use.
            If not given it is set the same as window.

        mode: 'valid', 'same' or 'full'
            the padding of the inumpy.t signals

    Returns
    -------

        output: complex array
            the complex stft
    """
    assert signal.ndim == 3
    if nfft is None:
        nfft = window
    if mode == "same":
        left = (window + 1) // 2
        psignal = T.pad(signal, [[0, 0], [0, 0], [left, window + 1 - left]])
    elif mode == "full":
        left = (window + 1) // 2
        psignal = T.pad(signal, [[0, 0], [0, 0], [window - 1, window - 1]])
    else:
        psignal = signal

    apodization = apod(window).reshape((1, 1, -1))

    p = extract_signal_patches(psignal, window, hop) * apodization
    assert nfft >= window
    pp = T.pad(p, [[0, 0], [0, 0], [0, 0], [0, nfft - window]])
    S = T.fft.fft(pp)
    return S[..., : int(numpy.ceil(nfft / 2))].transpose([0, 1, 3, 2])


def spectrogram(signal, window, hop, apod=hanning, nfft=None, mode="valid"):
    return T.abs(stft(signal, window, hop, apod, nfft, mode))


def melspectrogram(
    signal,
    window,
    hop,
    n_filter,
    low_freq,
    high_freq,
    nyquist,
    nfft=None,
    mode="valid",
    apod=hanning,
):
    spec = spectrogram(signal, window, hop, apod, nfft, mode)
    filterbank = mel_filterbank(spec.shape[-2], n_filter, low_freq, high_freq, nyquist)
    flip_filterbank = filterbank.expand_dims(-1)
    output = (T.expand_dims(spec, -3) * flip_filterbank).sum(-2)
    return output


def mfcc(
    signal,
    window,
    hop,
    n_filter,
    low_freq,
    high_freq,
    nyquist,
    n_mfcc,
    nfft=None,
    mode="valid",
    apod=hanning,
):
    """
    https://librosa.github.io/librosa/_modules/librosa/feature/spectral.html#mfcc
    """
    tf = melspectrogram(
        signal,
        window,
        hop,
        n_filter,
        low_freq,
        high_freq,
        nyquist,
        nfft,
        mode,
        apod,
    )
    tf_db = power_to_db(tf)
    M = dct(tf_db, axes=(2,))
    return M


def wvd(signal, window, hop, L, apod=hanning, mode="valid"):
    # define the following constant for clarity
    PI = 2 * 3.14159

    # compute the stft with 2 times bigger window to interp.
    s = stft(signal, window, hop, apod, nfft=2 * window, mode=mode)
    # remodulate the stft prior the spectral correlation for simplicity
    # with the following mask
    step = 1 / window
    freq = T.linspace(-step * L, step * L, 2 * L + 1)
    time = T.range(s.shape[-1]).reshape((-1, 1))
    mask = T.complex(T.cos(PI * time * freq), T.sin(PI * time * freq)) * hanning(
        2 * L + 1
    )

    # extract vertical (freq) partches to perform auto correlation
    patches = extract_image_patches(s, (2 * L + 1, 1), (2, 1), mode="same")[
        ..., 0
    ]  # (N C F' T L)
    output = (patches * T.conj(T.flip(patches, -1)) * mask).sum(-1)
    return T.real(output)


def dct(signal, axes=(-1,)):
    """
    https://dsp.stackexchange.com/questions/2807/fast-cosine-transform-via-fft
    """
    if len(axes) > 1:
        raise NotImplemented("not yet implemented more than 1D")
    to_pad = [
        (0, 0) if ax not in axes else (0, signal.shape[ax]) for ax in range(signal.ndim)
    ]
    pad_signal = T.pad(signal, to_pad)
    exp = 2 * T.exp(-1j * 3.14159 * T.linspace(0, 0.5, signal.shape[axes[0]]))
    y = fft(pad_signal, axes=axes)
    cropped_y = T.dynamic_slice_in_dim(y, 0, signal.shape[axes[0]], axes[0])
    return T.real(cropped_y * exp.expand_dims(-1))


def phase_vocoder(D, rate, hop_length=None):
    """Phase vocoder.  Given an STFT matrix D, speed up by a factor of `rate`

     Based on the implementation provided by [1]_.

     .. note:: This is a simplified implementation, intended primarily for
              reference and pedagogical purposes.  It makes no attempt to
              handle transients, and is likely to produce many audible
              artifacts.  For a higher quality implementation, we recommend
              the RubberBand library [2]_ and its Python wrapper `pyrubberband`.

     .. [1] Ellis, D. P. W. "A phase vocoder in Matlab."
         Columbia University, 2002.
         http://www.ee.columbia.edu/~dpwe/resources/matlab/pvoc/

     .. [2] https://breakfastquay.com/rubberband/

     Examples
    --------
     >>> # Play at double speed
     >>> y, sr   = librosa.load(librosa.util.example_audio_file())
     >>> D       = librosa.stft(y, n_fft=2048, hop_length=512)
     >>> D_fast  = librosa.phase_vocoder(D, 2.0, hop_length=512)
     >>> y_fast  = librosa.istft(D_fast, hop_length=512)

     >>> # Or play at 1/3 speed
     >>> y, sr   = librosa.load(librosa.util.example_audio_file())
     >>> D       = librosa.stft(y, n_fft=2048, hop_length=512)
     >>> D_slow  = librosa.phase_vocoder(D, 1./3, hop_length=512)
     >>> y_slow  = librosa.istft(D_slow, hop_length=512)

     Parameters
     ----------
     D : numpy.ndarray [shape=(d, t), dtype=complex]
         STFT matrix

     rate :  float > 0 [scalar]
         Speed-up factor: `rate > 1` is faster, `rate < 1` is slower.

     hop_length : int > 0 [scalar] or None
         The number of samples between successive columns of `D`.

         If None, defaults to `n_fft/4 = (D.shape[0]-1)/2`

     Returns
     -------
     D_stretched : numpy.ndarray [shape=(d, t / rate), dtype=complex]
         time-stretched STFT

    """
    n_fft = 2 * (D.shape[0] - 1)
    if hop_length is None:
        hop_length = int(n_fft // 4)

    time_steps = numpy.arange(0, D.shape[1], rate, "float32")

    # Create an empty output array
    d_stretch = T.zeros((D.shape[0], len(time_steps)), D.dtype)

    # Expected phase advance in each bin
    phi_advance = T.linspace(0, numpy.pi * hop_length, D.shape[0])

    # Pad 0 columns to simplify boundary logic
    D = T.pad(D, [(0, 0), (0, 2)], mode="constant")
    D = D[:, time_steps.astype("int32")]

    alpha = numpy.mod(time_steps, 1.0)

    mag = (1.0 - alpha) * numpy.abs(D[:, :-1]) + alpha * numpy.abs(D[:, 1:])

    # Compute phase advance
    dphase = numpy.angle(D[:, 1:]) - numpy.angle(D[:, :-1]) - phi_advance[:, None]
    # Wrap to -pi:pi range
    dphase = dphase - 2.0 * numpy.pi * numpy.round(dphase / (2.0 * numpy.pi))

    # Phase accumulator; initialize to the first sample
    phase_acc = T.concatenate(
        [numpy.angle(D[:, [0]]), T.cumsum(phi_advance + dphase, 1)], 1
    )

    d_stretch = mag * T.complex(T.cos(phase_acc), T.sin(phase_acc))

    return d_stretch


def istft(
    stft_matrix,
    hop_length=None,
    win_length=None,
    window="hann",
    center=True,
    dtype=numpy.float32,
    length=None,
):
    """
    Inverse short-time Fourier transform (ISTFT).

    Converts a complex-valued spectrogram `stft_matrix` to time-series `y`
    by minimizing the mean squared error between `stft_matrix` and STFT of
    `y` as described in [1]_ up to Section 2 (reconstruction from MSTFT).

    In general, window function, hop length and other parameters should be same
    as in stft, which mostly leads to perfect reconstruction of a signal from
    unmodified `stft_matrix`.

    .. [1] D. W. Griffin and J. S. Lim,
        "Signal estimation from modified short-time Fourier transform,"
        IEEE Trans. ASSP, vol.32, no.2, pp.236–243, Apr. 1984.

    Parameters
    ----------
    stft_matrix : numpy.ndarray [shape=(1 + n_fft/2, t)]
        STFT matrix from `stft`

    hop_length : int > 0 [scalar]
        Number of frames between STFT columns.
        If unspecified, defaults to `win_length / 4`.

    win_length : int <= n_fft = 2 * (stft_matrix.shape[0] - 1)
        When reconstructing the time series, each frame is windowed
        and each sample is normalized by the sum of squared window
        according to the `window` function (see below).

        If unspecified, defaults to `n_fft`.

    window : string, tuple, number, function, numpy.ndarray [shape=(n_fft,)]
        - a window specification (string, tuple, or number);
          see `scipy.signal.get_window`
        - a window function, such as `scipy.signal.hanning`
        - a user-specified window vector of length `n_fft`

        .. see also:: `filters.get_window`

    center : boolean
        - If `True`, `D` is assumed to have centered frames.
        - If `False`, `D` is assumed to have left-aligned frames.

    dtype : numeric type
        Real numeric type for `y`.  Default is 32-bit float.

    length : int > 0, optional
        If provided, the output `y` is zero-padded or clipped to exactly
        `length` samples.

    Returns
    -------
    y : numpy.ndarray [shape=(n,)]
        time domain signal reconstructed from `stft_matrix`

    See Also
    --------
    stft : Short-time Fourier Transform

    Notes
    -----
    This function caches at level 30.

    Examples
    --------
    >>> y, sr = librosa.load(librosa.util.example_audio_file())
    >>> D = librosa.stft(y)
    >>> y_hat = librosa.istft(D)
    >>> y_hat
    array([ -4.812e-06,  -4.267e-06, ...,   6.271e-06,   2.827e-07], dtype=float32)

    Exactly preserving length of the inumpy.t signal requires explicit padding.
    Otherwise, a partial frame at the end of `y` will not be represented.

    >>> n = len(y)
    >>> n_fft = 2048
    >>> y_pad = librosa.util.fix_length(y, n + n_fft // 2)
    >>> D = librosa.stft(y_pad, n_fft=n_fft)
    >>> y_out = librosa.istft(D, length=n)
    >>> numpy.max(numpy.abs(y - y_out))
    1.4901161e-07
    """

    n_fft = 2 * (stft_matrix.shape[0] - 1)

    # By default, use the entire frame
    if win_length is None:
        win_length = n_fft

    # Set the default hop, if it's not already specified
    if hop_length is None:
        hop_length = int(win_length // 4)

    ifft_window = get_window(window, win_length, fftbins=True)

    # Pad out to match n_fft, and add a broadcasting axis
    ifft_window = util.pad_center(ifft_window, n_fft)[:, numpy.newaxis]

    # For efficiency, trim STFT frames according to signal length if available
    if length:
        if center:
            padded_length = length + int(n_fft)
        else:
            padded_length = length
        n_frames = min(
            stft_matrix.shape[1], int(numpy.ceil(padded_length / hop_length))
        )
    else:
        n_frames = stft_matrix.shape[1]

    expected_signal_len = n_fft + hop_length * (n_frames - 1)
    y = numpy.zeros(expected_signal_len, dtype=dtype)

    n_columns = int(util.MAX_MEM_BLOCK // (stft_matrix.shape[0] * stft_matrix.itemsize))

    fft = get_fftlib()

    frame = 0
    for bl_s in range(0, n_frames, n_columns):
        bl_t = min(bl_s + n_columns, n_frames)

        # invert the block and apply the window function
        ytmp = ifft_window * fft.irfft(stft_matrix[:, bl_s:bl_t], axis=0)

        # Overlap-add the istft block starting at the i'th frame
        __overlap_add(y[frame * hop_length :], ytmp, hop_length)

        frame += bl_t - bl_s

    # Normalize by sum of squared window
    ifft_window_sum = window_sumsquare(
        window,
        n_frames,
        win_length=win_length,
        n_fft=n_fft,
        hop_length=hop_length,
        dtype=dtype,
    )

    approx_nonzero_indices = ifft_window_sum > util.tiny(ifft_window_sum)
    y[approx_nonzero_indices] /= ifft_window_sum[approx_nonzero_indices]

    if length is None:
        # If we don't need to control length, just do the usual center trimming
        # to eliminate padded data
        if center:
            y = y[int(n_fft // 2) : -int(n_fft // 2)]
    else:
        if center:
            # If we're centering, crop off the first n_fft//2 samples
            # and then trim/pad to the target length.
            # We don't trim the end here, so that if the signal is zero-padded
            # to a longer duration, the decay is smooth by windowing
            start = int(n_fft // 2)
        else:
            # If we're not centering, start at 0 and trim/pad as necessary
            start = 0

        y = util.fix_length(y[start:], length)

    return y


def hilbert_transform(signal):
    """
    the time should be the last dimension
    return the analytical signal
    """
    M = signal.shape[-1]
    heavyside = T.array([1, 0], dtype="float32").repeat(M // 2)
    mask = T.index_add(T.ones(M), T.index[..., 1 : M // 2], 1)
    return T.signal.ifft(T.signal.fft(signal) * mask * heavyside)


@jax_wrap
def batch_convolve(
    input,
    filter,
    strides=1,
    padding="VALID",
    input_format=None,
    filter_format=None,
    output_format=None,
    input_dilation=None,
    filter_dilation=None,
):
    """General n-dimensional batch convolution with dilations.

    Wraps Jax's conv_general_dilated functin, and thus also the XLA's `Conv
    <https://www.tensorflow.org/xla/operation_semantics#conv_convolution>`_
    operator.

    Args:
        input (Tensor): a rank `n+2` dimensional input array.
        filter (Tensor): a rank `n+2` dimensional array of kernel weights.
        strides (int, sequence of int, optional): a (sequence) of `n` integers,
            representing the inter-window strides. If a scalar is given, it is
            used `n` times. Defaults to `1`.
        padding (sequence of couple, `'SAME'`, `'VALID'`, optional): a sequence of
            `n` `(low, high)` integer pairs that give the padding to apply
            before and after each spatial dimension. For  `'VALID'`, those are
            `0`. For `'SAME'`, they are the `input length - filter length + 1`
            for each dim. Defaults to `'Valid'`.
        input_format (`None` or str, optional): a string of same length as the
            number of dimensions in `input` which specify their role
            (see below). Defaults to `'NCW'` for 1d conv, `'NCHW'` for 2d conv,
             and `'NDCHW'` for 3d conv.
        input_dilation (`None`, int or sequence of int, optional): giving the
            dilation factor to apply in each spatial dimension of `input`.
            Inumpy.t dilation is also known as transposed convolution as it allows
            to increase the output spatial dimension by inserting in the input
            any number of `0`s between each spatial value.
        filter_dilation (`None`, int or sequence of int): giving the dilation
            factor to apply in each spatial dimension of `filter`. Filter
            dilation is also known as atrous convolution as it corresponds to
            inserting any number of `0`s in between the filter values, similar
            to performing the non-dilated filter convolution with a subsample
            version of the input across the spatial dimensions.

    Returns:
        Tensor: An array containing the convolution result.

    Format of `input`, `filter` and `output`:
    For example, to indicate dimension numbers consistent with the `conv` function
    with two spatial dimensions, one could use `('NCHW', 'OIHW', 'NCHW')`. As
    another example, to indicate dimension numbers consistent with the TensorFlow
    Conv2D operation, one could use `('NHWC', 'HWIO', 'NHWC')`. When using the
    latter form of convolution dimension specification, window strides are
    associated with spatial dimension character labels according to the order in
    which the labels appear in the `rhs_spec` string, so that `window_strides[0]`
    is matched with the dimension corresponding to the first character
    appearing in rhs_spec that is not `'I'` or `'O'`.
    :param filter_format:
    :param output_format:
    """
    # setting up the strides
    if numpy.isscalar(strides):
        strides = (strides,) * (input.ndim - 2)
    elif len(strides) != (input.ndim - 2):
        msg = "given strides: {} should match the number".format(
            strides
        ) + "of spatial dim. in input: {}".format(input.ndim - 2)
        raise ValueError(msg)

    # setting up the padding
    if type(padding) != str:
        strides = (strides,) * (input.ndim - 2)
        if len(padding) != (input.ndim - 2):
            msg = "given padding: {} should match the ".format(
                padding
            ) + "number of spatial dim. in input: {}".format(input.ndim - 2)
            raise ValueError(msg)

    # setting up the filter_format
    if filter_format is None:
        if filter.ndim == 3:
            filter_format = "OIW"
        elif filter.ndim == 4:
            filter_format = "OIHW"
        elif filter.ndim == 5:
            filter_format = "OIDHW"
        else:
            msg = "filter_format should be given for >5 dimensions."
            raise ValueError(msg)
    elif len(filter_format) != filter.ndim:
        msg = "given filter_format: {} should".format(
            len(filter_format)
        ) + "match the number of dimension in filter: {}".format(filter.ndim)
        raise ValueError(msg)

    # setting up the input format
    if input_format is None:
        if len(filter.shape) == 3:
            input_format = "NCW"
        elif len(filter.shape) == 4:
            input_format = "NCHW"
        elif len(filter.shape) == 5:
            input_format = "NCDHW"
        else:
            msg = "input_format should be given for >5 dimensions."
            raise ValueError(msg)
    elif len(input_format) != input.ndim:
        msg = "given input_format: {} should".format(
            len(input_format)
        ) + "match the number of dimension in input: {}".format(input.ndim)
        raise ValueError(msg)

    # setting up the output format
    if output_format is None:
        if len(filter.shape) == 3:
            output_format = "NCW"
        elif len(filter.shape) == 4:
            output_format = "NCHW"
        elif len(filter.shape) == 5:
            output_format = "NCDHW"
        else:
            msg = "output_format should be given for >5 dimensions."
            raise ValueError(msg)
    elif len(output_format) != input.ndim:
        msg = "given output_format: {} should".format(
            len(output_format)
        ) + "match the number of dimension in output: {}".format(input.ndim)
        raise ValueError(msg)

    # setting up dilations
    if numpy.isscalar(input_dilation):
        input_dilation = (input_dilation,) * 2
    if numpy.isscalar(filter_dilation):
        filter_dilation = (filter_dilation,) * 2

    specs = (input_format, filter_format, output_format)
    return jla.conv_general_dilated(
        lhs=input,
        rhs=filter,
        window_strides=strides,
        padding=padding,
        lhs_dilation=input_dilation,
        rhs_dilation=filter_dilation,
        dimension_numbers=specs,
        precision=None,
    )


@jax_wrap
def batch_convolve_transpose(
    input,
    filter,
    strides=1,
    padding="VALID",
    input_format=None,
    filter_format=None,
    output_format=None,
    input_dilation=None,
    filter_dilation=None,
    transpose_kernel=False,
):
    """General n-dimensional convolution operator, with optional dilation.

    Wraps Jax's conv_general_dilated functin, and thus also the XLA's `Conv
    <https://www.tensorflow.org/xla/operation_semantics#conv_convolution>`_
    operator.

    Args:
        input (Tensor): a rank `n+2` dimensional input array.
        filter (Tensor): a rank `n+2` dimensional array of kernel weights.
        strides (int, sequence of int, optional): a (sequence) of `n` integers,
            representing the inter-window strides. If a scalar is given, it is
            used `n` times. Defaults to `1`.
        padding (sequence of couple, `'SAME'`, `'VALID'`, optional): a sequence of
            `n` `(low, high)` integer pairs that give the padding to apply
            before and after each spatial dimension. For  `'VALID'`, those are
            `0`. For `'SAME'`, they are the `input length - filter length + 1`
            for each dim. Defaults to `'Valid'`.
        input_format (`None` or str, optional): a string of same length as the
            number of dimensions in `input` which specify their role
            (see below). Defaults to `'NCW'` for 1d conv, `'NCHW'` for 2d conv,
             and `'NDCHW'` for 3d conv.
        input_dilation (`None`, int or sequence of int, optional): giving the
            dilation factor to apply in each spatial dimension of `input`.
            Inumpy.t dilation is also known as transposed convolution as it allows
            to increase the output spatial dimension by inserting in the input
            any number of `0`s between each spatial value.
        filter_dilation (`None`, int or sequence of int): giving the dilation
            factor to apply in each spatial dimension of `filter`. Filter
            dilation is also known as atrous convolution as it corresponds to
            inserting any number of `0`s in between the filter values, similar
            to performing the non-dilated filter convolution with a subsample
            version of the input across the spatial dimensions.

    Returns:
        Tensor: An array containing the convolution result.

    Format of `input`, `filter` and `output`:
    For example, to indicate dimension numbers consistent with the `conv` function
    with two spatial dimensions, one could use `('NCHW', 'OIHW', 'NCHW')`. As
    another example, to indicate dimension numbers consistent with the TensorFlow
    Conv2D operation, one could use `('NHWC', 'HWIO', 'NHWC')`. When using the
    latter form of convolution dimension specification, window strides are
    associated with spatial dimension character labels according to the order in
    which the labels appear in the `rhs_spec` string, so that `window_strides[0]`
    is matched with the dimension corresponding to the first character
    appearing in rhs_spec that is not `'I'` or `'O'`.
    :param filter_format:
    :param output_format:
    :param transpose_kernel:
    """

    # setting up the strides
    if numpy.isscalar(strides):
        strides = (strides,) * (input.ndim - 2)
    elif len(strides) != (input.ndim - 2):
        msg = "given strides: {} should match the number".format(
            strides
        ) + "of spatial dim. in input: {}".format(input.ndim - 2)
        raise ValueError(msg)

    # setting up the padding
    if type(padding) != str:
        strides = (strides,) * (input.ndim - 2)
        if len(padding) != (input.ndim - 2):
            msg = "given padding: {} should match the ".format(
                padding
            ) + "number of spatial dim. in input: {}".format(input.ndim - 2)
            raise ValueError(msg)

    # setting up the filter_format
    if filter_format is None:
        if filter.ndim == 3:
            filter_format = "OIW"
        elif filter.ndim == 4:
            filter_format = "OIHW"
        elif filter.ndim == 5:
            filter_format = "OIDHW"
        else:
            msg = "filter_format should be given for >5 dimensions."
            raise ValueError(msg)
    elif len(filter_format) != filter.ndim:
        msg = "given filter_format: {} should".format(
            len(filter_format)
        ) + "match the number of dimension in filter: {}".format(filter.ndim)
        raise ValueError(msg)

    # setting up the input format
    if input_format is None:
        if len(filter.shape) == 3:
            input_format = "NCW"
        elif len(filter.shape) == 4:
            input_format = "NCHW"
        elif len(filter.shape) == 5:
            input_format = "NCDHW"
        else:
            msg = "input_format should be given for >5 dimensions."
            raise ValueError(msg)
    elif len(input_format) != input.ndim:
        msg = "given input_format: {} should".format(
            len(input_format)
        ) + "match the number of dimension in input: {}".format(input.ndim)
        raise ValueError(msg)

    # setting up the output format
    if output_format is None:
        if len(filter.shape) == 3:
            output_format = "NCW"
        elif len(filter.shape) == 4:
            output_format = "NCHW"
        elif len(filter.shape) == 5:
            output_format = "NCDHW"
        else:
            msg = "output_format should be given for >5 dimensions."
            raise ValueError(msg)
    elif len(output_format) != input.ndim:
        msg = "given output_format: {} should".format(
            len(output_format)
        ) + "match the number of dimension in output: {}".format(input.ndim)
        raise ValueError(msg)

    # setting up dilations
    if numpy.isscalar(input_dilation):
        input_dilation = (input_dilation,) * 2
    if numpy.isscalar(filter_dilation):
        filter_dilation = (filter_dilation,) * 2

    specs = (input_format, filter_format, output_format)
    return jla.conv_transpose(
        lhs=input,
        rhs=filter,
        strides=strides,
        padding=padding,
        rhs_dilation=filter_dilation,
        dimension_numbers=specs,
        precision=None,
        transpose_kernel=transpose_kernel,
    )


@jax_wrap
def pool(
    input,
    window_shape,
    reducer="MAX",
    strides=None,
    padding="VALID",
    base_dilation=None,
    window_dilation=None,
):
    """apply arbitrary pooling on a Tensor.

    Parameters
    ----------

    input: Tensor
        the input to pool over

    window_shape: tuple of int
        the shape of the pooling operator, it must have same length than the
        number of dimension in `input`

    reducer: str
        the type of pooling to apply, must be one of `MAX`, `AVG`, `SUM`

    strides: tuple of int
        the stride of the pooling operator

    padding: str
        the type of padding, must be `VALID`, `SAME` or `FULL`

    base_dilation: tuple (optional)
        dilations of the input. This corresponds to the number of `0` inserted
        in between the values in the input

    window_dilation: tuple (optional)
        dilations of the window, this corresponds to the number
        of `0`s inserted in the window

    Returns
    -------

    pooled Tensor

    """

    # set up the reducer
    if reducer == "MAX":
        reduce = jla.max
        init_val = -jnp.inf
    elif reducer == "SUM" or reducer == "AVG":
        reduce = jla.add
        init_val = 0.0
    # set up the window_shape
    if len(window_shape) != input.ndim:
        msg = "Given window_shape {} not the same length ".format(
            strides
        ) + "as input shape {}".format(input.ndim)
        raise ValueError(msg)

    # set up the strides
    if strides is None:
        strides = window_shape
    elif len(strides) != len(window_shape):
        msg = "Given strides {} not the same length ".format(
            strides
        ) + "as window_shape {}".format(window_shape)
        raise ValueError(msg)

    if reducer == "AVG":
        input = input / numpy.prod(window_shape)

    out = jla.reduce_window(
        operand=input,
        init_value=init_val,
        computation=reduce,
        window_dimensions=window_shape,
        window_strides=strides,
        padding=padding,
        base_dilation=base_dilation,
        window_dilation=window_dilation,
    )

    return out
