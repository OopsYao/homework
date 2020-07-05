import time
import progressbar
from math import ceil


def snap_iter(shot_list, system_iterator, dt=None):
    """ For the `system_iterator`, we do not want all the generated frames
        but some we specified by `shot_list`, and `dt` here
        which aims to estimate the max time, is the dt of dynamic system 
        actually. """
    gen = iter(shot_list)
    if dt == None:
        max_value = progressbar.UnknownLength
    else:
        max_value = 1 + ceil(shot_list[-1] / dt)
    with progressbar.ProgressBar(max_value=max_value) as bar:
        try:
            s = next(gen)
            f = 0
            for item in system_iterator:
                while s <= item[0]:
                    yield s, *item[1:]
                    s = next(gen)
                f += 1
                bar.update(f)
        except StopIteration:
            pass


if __name__ == '__main__':
    dt = .013

    def infinite_gen(dt):
        v = 0
        x = 0
        t = 0
        i = 0
        while i < 10:
            time.sleep(.11)
            i += 1
            yield t, v, x
            v += .1
            x += v * dt
            t += dt

    for s, x, v in snap_iter([0, .1, .2], infinite_gen(dt), dt):
        time.sleep(1)
        pass
