import os
import shutil
from contextlib import contextmanager
from timeit import default_timer
from sherlockpipe.sherlock import Sherlock
from sherlockpipe.objectinfo.InputObjectInfo import InputObjectInfo
from sherlockpipe.objectinfo.MissionFfiIdObjectInfo import MissionFfiIdObjectInfo
from sherlockpipe.objectinfo.MissionInputObjectInfo import MissionInputObjectInfo
from sherlockpipe.objectinfo.MissionObjectInfo import MissionObjectInfo
from sherlockpipe.objectinfo.ObjectInfo import ObjectInfo


@contextmanager
def elapsed_timer():
    start = default_timer()
    elapser = lambda: str(default_timer() - start)
    yield lambda: elapser()
    end = default_timer()
    elapser = lambda: str(end - start)

# tpl = tp.TransitsPipeline()
# tpl.load_tois()\
#     .filter_hj_tois()\
#     .limit_tois(0, 5)\
#     .retrieve_pfs_list()\
#     .compute_lcs()\
#     .flatten_lcs()\
#     .transit_adjusts()

# TODO bin the lightcurve so noise gets smooth?
# TODO reduce scattering: regression lightkurve (is it already done i PDCSAP?), different bitmask
    # Get max period data
    # Discard very close periods
    # Recalculate period adjust
    # Repeat until snr, sde and fap
# Promising candidates list from predictions
# TIC 31374837 - TOI 431 (2 sectors) - period 20-40
# TIC 153951307 - TOI 1238 (4 sectors) - period 1-2.5, period 4-40
# TIC 36724087 - TOI 732 (1 sector) - period 15-30
# TIC 219852882 - TOI 1346 (6 sectors) - period 2-4, period 7-20
# TIC 181804752 - TOI 736 (1 sector)- period 0.5-5
# TIC 271596225 - TOI 797 (9 sectors) - period 2-3, period 5-20
# TIC 167600516 - TOI 713 (8 sectors) - period 50-100
# TIC 243185500 - TOI 1468 (1 sector) - period 2 - 10
# TIC 318022259 - TOI 1730 (1 sector) - period 2.5-4
# TIC 307210830 - TOI 175 (7 sectors) - period 10-30
# TIC 54962195 - TOI 663 (1 sector) - period 7-13
# TIC 283722336 - TOI 1469 (1 sector) - period 4-5, period 9-20
# TIC 355867695 - TOI 1260 (1 sector)- period 4-5, period 10-20
# TIC 259377017 - TOI 270 (3 sectors) - period 15-30
# TIC 63898957 - TOI 261 (1 sector) - period 4-10
# TIC 440887364 - TOI 836 (1 sector) - period 5-7
# TIC 425997655 - TOI 174 (4 sectors) - period 5-7
# TIC 100990000 - TOI 411 (2 sectors) - period 5-7, period 11-25
# TIC 198241702 - TOI 1269 (6 sectors) - period 5-7, period 11-25
# TIC 230127302 - TOI 1246 (9 sectors) - period 7-12, period 40-90
# TIC 198390247 - TOI 1453 (5 sectors) - period 8-20
# TIC 219195044 - TOI 714 (5 sectors) - period 15-40
# TIC 233602827 - TOI 1749 (6 sectors) - period 15-45
# TIC 150030205 - TOI 286 (12 sectors) - period 40-70
# TIC 120896927 - TOI 402 (1 sector) - period 5-13
# TIC 229650439 - TOI 1438 (6 sectors) - period 10-25
# TIC 278683844 - TOI 119 (6 sectors) - period 11-25
# TIC 130181866 - TOI 1726 (1 sector) - period 8-20
# TIC 31852980 - TOI 487 (4 sectors) - period 8-23
# TIC 237928815 - TOI 703 (2 sectors) - period 9-40
# TIC 150151262 - TOI 712 (5 sectors) - period 10-50
# TIC 167415965 - TOI 214 (12 sectors) - period 19-60
# TIC 150428135 - TOI 700 (8 sectors) - period 17-37, period 39-50
# TIC 149302744 - TOI 699 (6 sectors) - period 15-33, period 35-43
# TIC 29781292 - TOI 282 (13 sector) - period 32-55, period 57-83

# TODO report next lines to TLS because of
"""Traceback (most recent call last):
  File "/usr/lib/python3.6/multiprocessing/pool.py", line 119, in worker
    result = (True, func(*args, **kwds))
  File "/home/martin/.local/lib/python3.6/site-packages/transitleastsquares/core.py", line 153, in search_period
    duration_min_in_samples = int(numpy.floor(duration_min * len(y)))
ValueError: cannot convert float NaN to integer"""
#sherlock = Sherlock([]).setup_detrend(initial_rms_threshold=2.5, initial_rms_bin_hours=5)\
    #        .setup_transit_adjust_params(snr_min=8, period_min=0.5, period_max=70, max_runs=8)\
#         .load_ois().filter_hj_ois().limit_ois(7, 8).run()
with elapsed_timer() as elapsed:
     os.listdir(".git/ref/tags")
     # sherlock = Sherlock([]).setup_detrend(initial_rms_mask=False, initial_rms_threshold=2.5, initial_rms_bin_hours=5, n_detrends=1)\
     #     .setup_transit_adjust_params(snr_min=8, period_min=0.5, period_max=70, max_runs=1)\
     #     .filter_hj_ois()\
     #     .limit_ois(0, 1).run()
     # sherlock = sherlock_class.Sherlock(object_ids=["TIC 231912935"]).setup_detrend(n_detrends=3).setup_transit_adjust_params(period_max=30).run()
     #.filter_tois(lambda tois: tois.sort_values(by=['TIC ID', 'TOI'])) \
     #.filter_tois(lambda tois: tois[tois["TIC ID"].isin([149603524])])\
     #.run()
     #.filter_tois(lambda tois: tois.sort_values(by=['TIC ID', 'TOI']))\
     #.filter_tois(lambda tois: tois[tois["TIC ID"].isin([231912935])])\
     #.run()
     # for i in range(1, 6):
     #     sherlock = sherlock_class.Sherlock([InputObjectInfo('sinteticos/hj_comp/modeled' + str(i) + '.csv')]).setup_detrend(
     #         n_detrends=3, auto_detrend_periodic_signals=False, auto_detrend_method="cosine")\
     #         .setup_transit_adjust_params(period_max=20).run()
     #     orig_fn = "INP_" + "sinteticos_hj_comp_modeled" + str(i)
     #     shutil.move(orig_fn, "sinteticos/hj_comp/filter/" + orig_fn + "_1-4")
     #     sherlock.run()
     print("Analysis took " + elapsed() + "s")
