.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_generated_gallery_update_header_keywords.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_generated_gallery_update_header_keywords.py:


==========================================================
Updating Pointing and Observer Keywords in the FITS Header
==========================================================

This example demonstrates how to update the metadata in
an AIA FITS file to ensure that it has the most accurate
information regarding the spacecraft pointing and observer
position.


.. code-block:: default


    import astropy.units as u
    from sunpy.net import Fido, attrs
    import sunpy.map

    from aiapy.calibrate import update_pointing, fix_observer_location








An AIA FITS header contains various pieces of
`standard <https://fits.gsfc.nasa.gov/fits_standard.html>`_.
metadata that are critical to the physical interpretation of the data.
These include the pointing of the spacecraft, necessary for connecting
positions on the pixel grid to physical locations on the Sun, as well as
the observer (i.e. satellite) location.

While this metadata is recorded in the FITS header, some values in
the headers exported by data providers (e.g.
`Joint Science Operations Center (JSOC) <http://jsoc.stanford.edu/>`_ and
the `Virtual Solar Observatory <https://sdac.virtualsolar.org/cgi/search>`_
may not always be the most accurate. In the case of the spacecraft
pointing, a more accurate 3-hourly pointing table is available from the
JSOC.

As an example, let's first query the VSO for a single 171 Å AIA observation
on 1 January 2019, download it, and create a `~sunpy.map.Map`


.. code-block:: default

    q = Fido.search(
        attrs.Time('2019-01-01T00:00:00', '2019-01-01T01:00:00'),
        attrs.Sample(1*u.h),
        attrs.Instrument('AIA'),
        attrs.Wavelength(171*u.angstrom),
    )
    file = Fido.fetch(q)
    m = sunpy.map.Map(file)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Files Downloaded:   0%|          | 0/1 [00:00<?, ?file/s]    Files Downloaded: 100%|##########| 1/1 [00:01<00:00,  1.02s/file]    Files Downloaded: 100%|##########| 1/1 [00:01<00:00,  1.02s/file]




To update the pointing keywords, we can pass our `~sunpy.map.Map` to the
`~aiapy.calibrate.update_pointing` function. This function will query the
JSOC, using `~sunpy`, for the most recent pointing information, update
the metadata, and then return a new `~sunpy.map.Map` with this updated
metadata.


.. code-block:: default

    m_updated_pointing = update_pointing(m)








If we inspect the reference pixel and rotation matrix of the original map


.. code-block:: default

    print(m.reference_pixel)
    print(m.rotation_matrix)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    PixelPair(x=<Quantity 2055.310059 pix>, y=<Quantity 2045.709961 pix>)
    [[ 9.99999944e-01 -3.34562158e-04]
     [ 3.34562158e-04  9.99999944e-01]]




and the map with the updated pointing information


.. code-block:: default

    print(m_updated_pointing.reference_pixel)
    print(m_updated_pointing.rotation_matrix)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    PixelPair(x=<Quantity 2054.501465 pix>, y=<Quantity 2045.018311 pix>)
    [[ 9.99999944e-01 -3.34562158e-04]
     [ 3.34562158e-04  9.99999944e-01]]




we find that the relevant keywords, `CRPIX1`, `CRPIX2`, `CDELT1`, `CDELT2`,
and `CROTA2`, have been updated.

Similarly, the Heliographic Stonyhurst (HGS) coordinates of the observer
location in the header are inaccurate. If we check the HGS longitude keyword
in the header, we find that it is 0 degrees which is not the HGS longitude
coordinate of SDO.


.. code-block:: default

    print(m_updated_pointing.meta['hgln_obs'])
    print(m_updated_pointing.meta['hglt_obs'])





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    0.0
    -2.976075




To update the HGS observer coordinates, we can use the
`~aiapy.calibrate.fix_observer_location` function. This function reads the
correct observer location from Heliocentric Aries Ecliptic (HAE) coordinates
in the header, converts them to HGS, and replaces the inaccurate HGS
keywords.


.. code-block:: default

    m_observer_fixed = fix_observer_location(m_updated_pointing)








Looking again at the HGS longitude and latitude keywords, we can see that
they have been updated.


.. code-block:: default

    print(m_observer_fixed.meta['hgln_obs'])
    print(m_observer_fixed.meta['hglt_obs'])





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    -0.01480900749072589
    -2.976118447285847




Note that in `~sunpy.map.AIAMap`, the `~sunpy.map.Map.observer_coordinate`
attribute is already derived from the HAE coordinates such that it is not
strictly necessary to apply `~aiapy.calibrate.fix_observer_location`. For
example, the unfixed `~sunpy.map.Map` will still have an accurate derived
observer position


.. code-block:: default

    print(m_updated_pointing.observer_coordinate)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    <SkyCoord (HeliographicStonyhurst: obstime=2019-01-01T00:00:09.350): (lon, lat, radius) in (deg, deg, m)
        (-0.01480901, -2.97611845, 1.47085021e+11)>




However, we suggest that users apply this fix such that the information
stored in `~sunpy.map.Map.meta` is accurate and consistent.

Plot the fixed map


.. code-block:: default

    m_observer_fixed.peek()



.. image:: /generated/gallery/images/sphx_glr_update_header_keywords_001.png
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /Users/willbarnes/anaconda/envs/aiapy-dev/lib/python3.8/site-packages/sunpy/visualization/visualization.py:22: UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.
      plt.show()





.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  8.605 seconds)


.. _sphx_glr_download_generated_gallery_update_header_keywords.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: update_header_keywords.py <update_header_keywords.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: update_header_keywords.ipynb <update_header_keywords.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
