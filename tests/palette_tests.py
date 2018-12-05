from nose.tools import *
import pixelhouse as ph


class Palette_Test:

    """ Ensuring Palettes work
    """

    def load_palette_test(self):
        """ load_palette_test:
            Load up a fixed palette and check the colors
        """

        pal = ph.palette(5)

        known_color = [232, 221, 203, 255]
        assert_true(all([c0 == c1 for c0, c1 in zip(pal[0], known_color)]))

    def check_len_test(self):
        """ check_len_test:
            Make sure that we load at least one color palette. Pull a color
            first to fix lazy loading.
        """
        ph.palette(5)
        assert_true(len(ph.palette) > 5)

    @raises(KeyError)
    def out_of_bounds_test(self):
        """ out_of_bounds_test:
            Try to access a palette that doesn't exist.
        """
        ph.palette(100000)


class Color_Test:

    """ Ensuring named colors work
    """

    def check_len_test(self):
        """ check_len_test:
            Make sure that we load at least one color palette. Pull a color
            first to fix lazy loading.
        """
        colors = ph.color.NamedColors()
        colors("k")
        assert_true(len(colors) > 5)

    @raises(KeyError)
    def check_unknown_color_name_test(self):
        """ check_unknown_color_name:
            Try to load a color name that doesn't exist.
        """
        canvas = ph.Canvas()
        canvas += ph.circle(color="this_color_does_not_exist")
