import numpy as np
import pixelhouse as ph


def logo_animation(logo_text):
    pal = ph.palette(3)

    A = ph.Animation(fps=24, duration=1.5, width=800, height=800, bg=pal[2])

    lg = ph.gradient.linear([pal[0], pal[1]], theta=-np.pi / 4)

    A += ph.rectangle(-400, -400, 400, 400, color=pal[-1])
    
    A += ph.circle(color=pal[3])
    A += ph.filters.gaussian_blur()
    A += ph.circle(color=pal[3])

    y = ph.motion.easeInOutQuad(0, 1, flip=True)

    for i in np.arange(-6, 6, 1.0):
        A += ph.text(logo_text, y=i * y, gradient=lg, font_size=1.0)

    return A


if __name__ == '__main__':
    logo_text = "pixelhouse"
    save_name = "figures/logo_pixelhouse_animated.gif"
    ph.canvas2gif(logo_animation(logo_text), save_name, gifsicle=True)
