.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_generated_gallery_instrument_degradation.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_generated_gallery_instrument_degradation.py:


========================================
Modeling Channel Degradation over Time
========================================

This example demonstrates how to model the degradation
of the AIA channels as a function of time over the entire
lifetime of the instrument.


.. code-block:: default


    import numpy as np
    import matplotlib.pyplot as plt
    import astropy.units as u
    import astropy.time
    from astropy.visualization import time_support

    from aiapy.calibrate import degradation
    from aiapy.calibrate.util import get_correction_table








The sensitivity of AIA channels degrade over time. Possible causes include
the deposition of organic molecules from the telescope structure onto the
optical elements and the decrease in detector sensitivity following (E)UV
exposure. When looking at AIA images over the lifetime of the mission, it
isimportant to understand how the degradation of the instrument impacts the
measured intensity. For monitoring brightness changes over months and years,
degradation correction is an important step in the data normalization proces.
For instance, the SDO Machine Learning Dataset
(`Galvez et al., 2019 <https://ui.adsabs.harvard.edu/abs/2019ApJS..242....7G/abstract>`_)
includes this correction.

The AIA team models the change in transmission as a function of time (see
`Boerner et al., 2012 <https://doi.org/10.1007/s11207-011-9804-8>`_) and
the table of correction parameters is publicly available via the
`Joint Science Operations Center (JSOC) <http://jsoc.stanford.edu/>`_.

First, fetch this correction table. It is not strictly necessary to do this,
but will significantly speed up the calculation by only fetching the table
once.


.. code-block:: default

    correction_table = get_correction_table()





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /Users/willbarnes/anaconda/envs/aiapy-dev/lib/python3.8/site-packages/astropy/_erfa/core.py:104: ErfaWarning: ERFA function "taiutc" yielded 1 of "dubious year (Note 4)"
      warnings.warn('ERFA function "' + func_name + '" yielded ' + wmsg, ErfaWarning)
    /Users/willbarnes/anaconda/envs/aiapy-dev/lib/python3.8/site-packages/astropy/_erfa/core.py:104: ErfaWarning: ERFA function "utctai" yielded 1 of "dubious year (Note 3)"
      warnings.warn('ERFA function "' + func_name + '" yielded ' + wmsg, ErfaWarning)
    /Users/willbarnes/anaconda/envs/aiapy-dev/lib/python3.8/site-packages/astropy/_erfa/core.py:104: ErfaWarning: ERFA function "dtf2d" yielded 82 of "dubious year (Note 6)"
      warnings.warn('ERFA function "' + func_name + '" yielded ' + wmsg, ErfaWarning)




We want to compute the degradation for each EUV channel.


.. code-block:: default

    channels = [94, 131, 171, 193, 211, 304, 335] * u.angstrom








We can use the `~astropy.time` subpackage to create an array of times
between now and the start of the mission with a cadence of one week.


.. code-block:: default

    time_0 = astropy.time.Time('2010-06-01T00:00:00', scale='utc')
    now = astropy.time.Time.now()
    time = time_0 + np.arange(0, (now - time_0).to(u.day).value, 7) * u.day








Finally, we can use the `~aiapy.calibrate.degradation` function to
compute the degradation for a particular channel and observation time.
This is modeled as the ratio of the effective area measured at a particular
calibration epoch over the uncorrected effective area with a polynomial
interpolation to the exact time.


.. code-block:: default

    deg = {c: degradation(c, time, correction_table=correction_table) for c in channels}








Plotting the different degradation curves as a function of time, we can
easily visualize how the different channels have degraded over time.


.. code-block:: default

    time_support()  # Pass astropy.time.Time directly to matplotlib
    fig = plt.figure()
    ax = fig.gca()
    for c in channels:
        ax.plot(time, deg[c], label=f'{c.value:.0f} Å')
    ax.set_xlim(time[[0, -1]])
    ax.legend(frameon=False, ncol=4, bbox_to_anchor=(0.5, 1), loc='lower center')
    ax.set_xlabel('Time')
    ax.set_ylabel('Degradation')



.. image:: /generated/gallery/images/sphx_glr_instrument_degradation_001.png
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    Text(0, 0.5, 'Degradation')




.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  17.142 seconds)


.. _sphx_glr_download_generated_gallery_instrument_degradation.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: instrument_degradation.py <instrument_degradation.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: instrument_degradation.ipynb <instrument_degradation.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
