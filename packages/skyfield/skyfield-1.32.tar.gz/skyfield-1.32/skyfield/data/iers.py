"""Parse data files from the International Earth Rotation Service.

See:
https://datacenter.iers.org/eop.php
ftp://cddis.gsfc.nasa.gov/pub/products/iers/readme.finals2000A

"""
import numpy as np
import re

from ..constants import DAY_S

inf = float('inf')
_R = re.compile(b'^......(.........) . '
                b'(.\d.......)......... '
                b'(.\d.......).........  '
                b'.(.\d........)', re.M)

def parse_dut1_x_y_from_finals_all(f):
    data = np.fromregex(f, _R, [
        ('mjd_utc', np.float32),
        ('x', np.float32),
        ('y', np.float32),
        ('dut1', np.float32),
    ])
    return data['mjd_utc'], data['x'], data['y'], data['dut1']

def _build_timescale_arrays(mjd_utc, dut1):
    big_jumps = np.diff(dut1) > 0.9
    leap_second_mask = np.concatenate([[False], big_jumps])
    tt_minus_utc = np.cumsum(leap_second_mask) + 32.184 + 12.0

    tt_jd = mjd_utc + tt_minus_utc / DAY_S + 2400000.5
    delta_t = tt_minus_utc - dut1
    delta_t_recent = np.array([tt_jd, delta_t])

    leap_dates = 2400000.5 + np.concatenate([
        [-inf], [41317.0, 41499.0, 41683.0], mjd_utc[leap_second_mask], [inf],
    ])
    leap_offsets = np.arange(8.0, len(leap_dates) + 8.0)
    leap_offsets[0] = leap_offsets[1] = 10.0

    return delta_t_recent, leap_dates, leap_offsets

# Compatibility with older Skyfield versions:

def parse_dut1_from_finals_all(f):
    v = parse_dut1_x_y_from_finals_all(f)
    return v[0], v[3]
