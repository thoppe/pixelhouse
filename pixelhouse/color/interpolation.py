import numpy as np
import cv2


def lerp(t, ys, xs=None):
    """
    Linear interpolation between the list of ys. If xs is not given
    points are evenly distributed between [0, 1]. Points are evaluated
    on the values of t.
    """
    if xs is None:
        xs = np.linspace(0, 1, len(ys))

    return np.interp(t, xs, ys)


def discrete_interpolation(t, alpha, cs):
    """
    No interpolation used, simply select the color on fixed intervals.
    Downweight by alpha.
    """
    cs = np.array(cs)
    n = len(cs)
    idx = np.clip(np.floor(t * n), 0, n - 1).astype(int)
    C = cs[idx, :].astype(np.float)
    C[:, 3] *= alpha
    return C


def RGBa_interpolation(t, alpha, cs):
    """
    Interpolate two colors RGB in RGB space parameterized by t. 
    Downweight by alpha.
    """
    csx = list(zip(*cs))
    R = lerp(t, csx[0])
    G = lerp(t, csx[1])
    B = lerp(t, csx[2])
    a = lerp(t, csx[3]) * alpha
    return np.vstack([R, G, B, a]).T


def LABa_interpolation(t, alpha, cs):
    """
    Interpolate two RGB colors in LAB space parameterized by t. 
    Downweight by alpha.
    """
    csx = list(zip(*cs))
    alpha_channel = csx[3]

    # Convert colors to LAB (remove alpha channel)
    C = np.array(cs).astype(np.uint8)[:, :3].reshape(-1, 1, 3)
    C = cv2.cvtColor(C, cv2.COLOR_RGB2LAB).reshape(-1, 3).T

    # Interpolate in LAB space
    L = lerp(t, C[0])
    A = lerp(t, C[1])
    B = lerp(t, C[2])

    # Convert back to RGB
    C = np.vstack([L, A, B]).T.reshape(-1, 1, 3)
    C = C.astype(np.uint8)
    C = cv2.cvtColor(C, cv2.COLOR_LAB2RGB).reshape(-1, 3)

    # Add back in the weighted alpha channel
    a = lerp(t, alpha_channel)
    a = np.clip(a * alpha, 0, 255).astype(np.uint8)

    # Stack them all together
    C = np.hstack([C, a.reshape(-1, 1)])

    return C
