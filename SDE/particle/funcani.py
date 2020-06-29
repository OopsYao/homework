import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Ani:
    def __init__(self, next):
        self.next = next
        self.fig, self.ax = plt.subplots()
        self.fig.tight_layout()
        # self.scat = self.ax.scatter([], [])
        self.quiv = self.ax.quiver(np.tile(0, 405), np.tile(
            0, 405), np.tile(0, 405), np.tile(0, 405))
        self.ax.set_xlim(-3, 3)
        self.ax.set_ylim(-3, 3)

    def _update(self, t):
        x, v, c = self.next(t)
        # self.scat.set_offsets(x)
        # self.scat.set_color(c)
        self.quiv.set_offsets(x)
        self.quiv.set_UVC(*(v.T))
        self.quiv.set_color(c)

        lim = np.vstack((self.ax.get_xlim(), self.ax.get_ylim()))
        if (x < lim[:, 0]).any() or (x > lim[:, 1]).any():
            low = x.min(axis=0)
            upp = x.max(axis=0)
            gap = (upp - low).max()
            self.ax.set_xlim(low[0] - .1 * gap, low[0] + 1.2 * gap)
            self.ax.set_ylim(low[1] - .1 * gap, low[1] + 1.2 * gap)
            self.fig.canvas.resize_event()
        return self.quiv,

    def start(self):
        return FuncAnimation(self.fig, self._update, interval=0, frames=1440, blit=True)
