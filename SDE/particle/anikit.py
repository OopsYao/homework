import matplotlib as mpl
import matplotlib.pyplot as plt
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


class ShootPlot():
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.fig.tight_layout()

        self._ax_init()

        self._camera = Camera(self.fig)

    def quiver(self, x, v, color='black'):
        self.ax.quiver(*(x.T), *(vector_rescale(v).T),
                       color=color, scale=50)
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

        # Hide the right and top spines
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['top'].set_visible(False)

        # Only show ticks on the left and bottom spines
        self.ax.yaxis.set_ticks_position('left')
        self.ax.xaxis.set_ticks_position('bottom')

    def scatter(self, x, *args, **kwargs):
        self.ax.scatter(*(x.T), args, kwargs)
        self._ax_init()

    def clear(self):
        self.ax.cla()

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
