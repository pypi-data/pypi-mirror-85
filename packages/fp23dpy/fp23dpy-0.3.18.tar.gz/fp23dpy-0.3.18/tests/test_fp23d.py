import numpy as np


from fp23dpy import fp23d
import example_drop

calibration = example_drop.calibration
d_grid = example_drop.drop_projection_map()
signal = 255 / 2 * example_drop.render_drop()
signal.data[signal.mask] = 0

def rms(x):
    return np.sqrt(np.mean(np.square(x)))

def test_fp23d():
    reconstruction_grid = fp23d(signal, calibration, same=True)
    rmse = rms(reconstruction_grid - d_grid) / np.max(d_grid[2])
    print(rmse)
    assert rmse < 0.15
