import numpy as np
import cv2


def lerp(t, y0, y1, x0=0, x1=1):
    # Linear interpolation
    return np.interp(t, [x0, x1], [y0, y1])


def RGBa_interpolation(t, c0, c1, alpha):
    """
    Interpolate two colors RGB in RGB space parameterized by y. 
    Downweight by alpha.
    """

    R = lerp(t, c0[0], c1[0])
    G = lerp(t, c0[1], c1[1])
    B = lerp(t, c0[2], c1[2])
    a = lerp(t, c0[3], c1[3]) * alpha
    return np.vstack([R, G, B, a]).T


def LABa_interpolation(t, c0, c1, alpha):
    """
    Interpolate two RGB colors in LAB space parameterized by y. 
    Downweight by alpha.
    """

    # Slice off the alpha channel
    a_start, c0 = c0[3], c0[:3]
    a_final, c1 = c1[3], c1[:3]

    # Convert colors to LAB
    C = np.array([c0, c1]).astype(np.uint8).reshape((2, 1, 3))
    c0, c1 = cv2.cvtColor(C, cv2.COLOR_RGB2LAB).reshape(2, 3)

    # Interpolate in LAB space
    L = lerp(t, c0[0], c1[0])
    A = lerp(t, c0[1], c1[1])
    B = lerp(t, c0[2], c1[2])

    # Convert back to RGB
    C = np.vstack([L, A, B]).T.reshape(-1, 1, 3)
    C = C.astype(np.uint8)
    C = cv2.cvtColor(C, cv2.COLOR_LAB2RGB).reshape(-1, 3)

    # Add back in the weighted alpha channel
    a = lerp(t, a_start, a_final)
    a = np.clip(a * alpha, 0, 255).astype(np.uint8)

    # Stack them all together
    C = np.hstack([C, a.reshape(-1, 1)])

    return C
