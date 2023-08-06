import warnings
import numpy as np
from occamtools.occam_data import OccamData


def _check_dimension(dimension):
    if dimension is None:
        return 0
    if isinstance(dimension, str):
        if 'x' in dimension:
            return 0
        elif 'y' in dimension:
            return 1
        elif 'z' in dimension:
            return 2
    elif isinstance(dimension, int):
        if dimension >= 0 and dimension <= 2:
            return dimension
        else:
            error_str = (f'Dimension keyword must be 0 <= dimension <= 2, not '
                         f'{dimension}.')
            raise ValueError(error_str)
    error_str = (f'Dimension keyword must be of type string (value x/y/z), or '
                 f'int (value 0/1/2), not {type(dimension)}.')
    raise TypeError(error_str)


def _check_time_steps(data, time_steps):
    if time_steps is None:
        return (0, len(data))
    if (isinstance(time_steps, tuple) or isinstance(time_steps, list) or
            isinstance(time_steps, np.ndarray)):
        time_steps = list(time_steps)
        if time_steps[0] < 0:
            time_steps[0] = len(data) + time_steps[0]
        if time_steps[1] < 0:
            time_steps[1] = len(data) + time_steps[1]
        if (time_steps[0] >= 0 and time_steps[1] <= len(data) and
                time_steps[1] >= time_steps[0]):
            return list(time_steps)
    error_str = (f'Provided time_steps must be a list/tuple/np.ndarray of two '
                 f'elements, with time_steps[0] >= time_steps[1], '
                 f'time_steps[0] >= 0, time_steps[1] <= len(data), not '
                 f'{time_steps}.')
    raise ValueError(error_str)


def histogram(data, dimension=None, time_steps=None, **kwargs):
    if isinstance(data, OccamData):
        dim = _check_dimension(dimension)
        if dim == 0:
            d = data.x
        elif dim == 1:
            d = data.y
        else:
            d = data.z
    elif isinstance(data, np.ndarray):
        d = data
        if dimension is not None:
            warn_str = (f'When input to histogram is of type np.ndarray, the '
                        f'dimension keyword (dimension={dimension}) is '
                        f'ignored.')
            warnings.warn(warn_str)
    else:
        error_str = (f'Given data must be of type OccamData or np.ndarray, not'
                     f' {type(data)}.')
        raise TypeError(error_str)

    time_steps = _check_time_steps(d, time_steps)
    hist, bins = np.histogram(d[time_steps[0], :], **kwargs)
    for step in range(time_steps[0]+1, time_steps[1]):
        hist_, _ = np.histogram(d[step, :], **kwargs)
        hist = hist + hist_
    return hist, bins
