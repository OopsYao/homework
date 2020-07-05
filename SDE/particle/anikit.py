import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.offsetbox
from matplotlib.lines import Line2D
import numpy as np
import unittest
from utils import vector_rescale
from celluloid import Camera

# mpl.rcParams['figure.figsize'] = [6.0, 6.0]
mpl.rcParams['lines.markersize'] = np.sqrt(5)

REAL_TIME = 6
FPS = 144
FRAMES = REAL_TIME * FPS


class FrameKit:
    def __init__(self, T, realtime=None, FPS=None):
        realtime_setted = realtime != None
        FPS_setted = FPS != None

        DEFAULT_REALTIME = 6
        DEFAULT_FPS = 144
        DEFAULT_DT = 0.02

        if not realtime_setted:
            realtime = DEFAULT_REALTIME
        if not FPS_setted:
            FPS = DEFAULT_FPS

        self.FPS = FPS
        self.frames = int(FPS * realtime)
        self.dt = T / (realtime * FPS)

        if not FPS_setted:
            # FPS not specified
            if self.dt > DEFAULT_DT:
                self.dt = DEFAULT_DT
                self.frames = int(T / self.dt)
                self.FPS = T / self.dt / realtime
        elif not realtime_setted:
            # Realtime not specified but FPS specified
            if self.dt > DEFAULT_DT:
                self.dt = DEFAULT_DT
                self.frames = int(T / self.dt)


# From https://stackoverflow.com/questions/43258638/is-there-a-convenient-way-to-add-a-scale-indicator-to-a-plot-in-matplotlib
class AnchoredHScaleBar(matplotlib.offsetbox.AnchoredOffsetbox):
    """ size: length of bar in data units
        extent : height of bar ends in axes units """

    def __init__(self, size=1, extent=0.03, label="", loc=2, ax=None,
                 pad=0.4, borderpad=0.5, ppad=0, sep=2, prop=None,
                 frameon=True, linekw={}, **kwargs):
        if not ax:
            ax = plt.gca()
        trans = ax.get_xaxis_transform()
        size_bar = matplotlib.offsetbox.AuxTransformBox(trans)
        line = Line2D([0, size], [0, 0], **linekw)
        vline1 = Line2D([0, 0], [-extent/2., extent/2.], **linekw)
        vline2 = Line2D([size, size], [-extent/2., extent/2.], **linekw)
        size_bar.add_artist(line)
        size_bar.add_artist(vline1)
        size_bar.add_artist(vline2)
        txt = matplotlib.offsetbox.TextArea(label, minimumdescent=False)
        self.vpac = matplotlib.offsetbox.VPacker(children=[size_bar, txt],
                                                 align="center", pad=ppad, sep=sep)
        matplotlib.offsetbox.AnchoredOffsetbox.__init__(self, loc, pad=pad,
                                                        borderpad=borderpad, child=self.vpac, prop=prop, frameon=frameon,
                                                        **kwargs)


class ShootPlot():
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.fig.tight_layout(pad=0)

        self._ax_init()

        self._camera = Camera(self.fig)

    def quiver(self, x, v, **kwargs):
        self.ax.quiver(*(x.T), *(vector_rescale(v).T),
                       scale=50, **kwargs)
        self._ax_init()

    def text(self, str):
        self.ax.text(.1, .9, str,
                     horizontalalignment='center',
                     verticalalignment='center',
                     transform=self.ax.transAxes,
                     bbox=dict(boxstyle="round",
                               ec=(0, 0, 0, 0),
                               fc=(.9, .9, .9, .7)))

    def _ax_init(self):
        # self.ax.axis('equal')
        self.ax.axis('off')
        self.ax.set_aspect('equal', 'box')

        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)

        ob = AnchoredHScaleBar(size=1/4, label="1/4 unit", loc=1, frameon=True,
                               pad=0.6, sep=2, linekw=dict(color="blue"),)
        self.ax.add_artist(ob)

    def scatter(self, x, color='black', *args, **kwargs):
        self.ax.scatter((x.T)[0], (x.T)[1], color=color)
        self._ax_init()

    def clear(self):
        self.ax.cla()

    def save(self, path):
        self.fig.savefig(path, bbox_inches='tight', pad_inches=0)

    def snap(self):
        self._camera.snap()

    def animate(self):
        return self._camera.animate()


class TestSuite(unittest.TestCase):
    def test_FrameKit(self):
        kit_non = FrameKit(10)
        self.assertEqual(kit_non.FPS, 144)
        self.assertEqual(kit_non.frames, 144 * 6)
        self.assertLessEqual(kit_non.dt, .02)

        kit_non = FrameKit(20)
        self.assertAlmostEqual(kit_non.FPS, 20 / .02 / 6)
        self.assertEqual(kit_non.frames, 20 / .02)
        self.assertLessEqual(kit_non.dt, .02)

        kit_fps = FrameKit(10, FPS=60)
        self.assertAlmostEqual(kit_fps.FPS, 60)
        self.assertEqual(kit_fps.frames, 10 / .02)
        self.assertLessEqual(kit_fps.dt, .02)

        kit_fps = FrameKit(5, FPS=60)
        self.assertAlmostEqual(kit_fps.FPS, 60)
        self.assertEqual(kit_fps.frames, 60 * 6)
        self.assertLessEqual(kit_fps.dt, .02)

        kit_rlt = FrameKit(10, realtime=5)
        self.assertAlmostEqual(kit_rlt.FPS, 144)
        self.assertEqual(kit_rlt.frames, 144 * 5)
        self.assertLessEqual(kit_rlt.dt, .02)

        kit_rlt = FrameKit(20, realtime=5)
        self.assertAlmostEqual(kit_rlt.FPS, 20 / .02 / 5)
        self.assertEqual(kit_rlt.frames, 20 / .02)
        self.assertLessEqual(kit_rlt.dt, .02)

        kit_all = FrameKit(10, 5, 60)
        self.assertAlmostEqual(kit_all.FPS, 60)
        self.assertEqual(kit_all.frames, 60 * 5)


if __name__ == "__main__":
    unittest.main()
