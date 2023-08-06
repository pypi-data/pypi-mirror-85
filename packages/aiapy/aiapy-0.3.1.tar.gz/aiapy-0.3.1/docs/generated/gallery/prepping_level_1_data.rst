.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_generated_gallery_prepping_level_1_data.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_generated_gallery_prepping_level_1_data.py:


=======================================
Registering and Aligning Level 1 Data
=======================================

This example demonstrates how to convert AIA images to a common pointing,
rescale them to a common plate scale , and remove the roll angle. This process
is often referred to as "aia_prep" and the resulting data are typically
referred to as level 1.5 data. In this example, we will demonstrate how to do
this with `aiapy`. This corresponds to the `aia_prep.pro` procedure as
described in the `SDO Analysis Guide <https://www.lmsal.com/sdodocs/doc/dcur/SDOD0060.zip/zip/entry/index.html>`_.


.. code-block:: default


    import astropy.units as u
    from sunpy.net import Fido, attrs
    import sunpy.map

    from aiapy.calibrate import register, update_pointing, normalize_exposure








Performing multi-wavelength analysis on level 1 data can be problematic as
each of the AIA channels have slightly different spatial scales and roll
angles. Furthermore, the estimates of the pointing keywords (`CDELT1`, `CDELT2`, `CRPIX1`,
`CRPIX2`, `CROTA2`) may have been improved due to limb fitting procedures. The
`Joint Science Operations Center (JSOC) <http://jsoc.stanford.edu/>`_ stores
AIA image data and metadata separately; when users download AIA data, these
two data types are combined to produce a FITS file. While metadata are
continuously updated at JSOC, previously downloaded FITS files will not
contain the most recent information.

Thus, before performing any multi-wavelength analyses, level 1 data
should be updated to the most recent and accurate pointing and interpolated
to a common grid in which the y-axis of the image is aligned
with solar North.

First, let's fetch level 1 AIA images from the
`Virtual Solar Observatory <https://sdac.virtualsolar.org/cgi/search>`_
from 1 January 2019 for the 94 Å channel and create a `~sunpy.map.Map`
object.


.. code-block:: default

    q = Fido.search(
        attrs.Time('2019-01-01T00:00:00', '2019-01-01T00:00:11'),
        attrs.Instrument('AIA'),
        attrs.Wavelength(wavemin=94*u.angstrom, wavemax=94*u.angstrom),
    )
    m = sunpy.map.Map(Fido.fetch(q))





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Files Downloaded:   0%|          | 0/1 [00:00<?, ?file/s]    Files Downloaded: 100%|##########| 1/1 [00:01<00:00,  1.22s/file]    Files Downloaded: 100%|##########| 1/1 [00:01<00:00,  1.22s/file]




The first step in this process is to update the metadata of the map to the
most recent pointing using  the `~aiapy.calibrate.update_pointing` function.
This function queries the JSOC for the most recent pointing information,
updates the metadata, and returns a `~sunpy.map.Map` with updated metadata.


.. code-block:: default

    m_updated_pointing = update_pointing(m)








If we take a look at the plate scale and rotation matrix of the map, we
find that the scale is slightly off from the expected value of 0.6" per
pixel and that the rotation matrix has off-diagonal entries.


.. code-block:: default

    print(m_updated_pointing.scale)
    print(m_updated_pointing.rotation_matrix)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    SpatialPair(axis1=<Quantity 0.600109 arcsec / pix>, axis2=<Quantity 0.600109 arcsec / pix>)
    [[ 0.99999712  0.0024018 ]
     [-0.0024018   0.99999712]]




We can use the `~aiapy.calibrate.register` function to scale the image to
the 0.6" per pixel and derotate the image such that the y-axis is aligned
with solar North.


.. code-block:: default

    m_registered = register(m_updated_pointing)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /Users/willbarnes/anaconda/envs/aiapy-dev/lib/python3.8/site-packages/sunpy/image/transform.py:118: SunpyUserWarning: Input data has been cast to float64.
      warnings.warn("Input data has been cast to float64.", SunpyUserWarning)




If we look again at the plate scale and rotation matrix, we
should find that the plate scale in each direction is 0.6 arcseconds
per pixel and that the rotation matrix is diagonalized.
The image in `m_registered` is now a level 1.5 data product.


.. code-block:: default

    print(m_registered.scale)
    print(m_registered.rotation_matrix)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    SpatialPair(axis1=<Quantity 0.6 arcsec / pix>, axis2=<Quantity 0.6 arcsec / pix>)
    [[ 1.00000000e+00 -2.84754216e-20]
     [-4.62156291e-19  1.00000000e+00]]




Though it is not typically part of the level 1.5 "prep" data pipeline,
it is also common to normalize the image to the exposure time such that
the units of the image are DN / pixel / s.


.. code-block:: default

    m_normalized = normalize_exposure(m_registered)








Plot the exposure-normalized map
Note: Small negative pixel values are possible because
CCD images were taken with a pedestal set at ~ 100 DN.
This pedestal is then subtracted when the JSOC pipeline
performs dark (+pedestal) subtraction and flatfielding
to generate level 1 files.


.. code-block:: default

    m_normalized.peek(vmin=0)



.. image:: /generated/gallery/images/sphx_glr_prepping_level_1_data_001.png
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /Users/willbarnes/anaconda/envs/aiapy-dev/lib/python3.8/site-packages/sunpy/visualization/visualization.py:22: UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.
      plt.show()





.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  16.216 seconds)


.. _sphx_glr_download_generated_gallery_prepping_level_1_data.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: prepping_level_1_data.py <prepping_level_1_data.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: prepping_level_1_data.ipynb <prepping_level_1_data.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
