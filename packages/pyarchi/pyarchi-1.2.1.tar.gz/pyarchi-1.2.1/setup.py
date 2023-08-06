# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyarchi',
 'pyarchi.data_objects',
 'pyarchi.initial_detection',
 'pyarchi.masks_creation',
 'pyarchi.output_creation',
 'pyarchi.routines',
 'pyarchi.star_track',
 'pyarchi.utils',
 'pyarchi.utils.data_export',
 'pyarchi.utils.factors_handler',
 'pyarchi.utils.image_processing',
 'pyarchi.utils.misc',
 'pyarchi.utils.noise_metrics',
 'pyarchi.utils.optimization']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.0,<5.0',
 'imageio>=2.8.0,<3.0.0',
 'matplotlib>=3.1.2,<4.0.0',
 'opencv-python>=4.1.2,<5.0.0',
 'pyyaml>=5.3,<6.0',
 'scipy>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'pyarchi',
    'version': '1.2.1',
    'description': "Photometry for CHEOPS's background stars",
    'long_description': '[![Documentation Status](https://readthedocs.org/projects/archi/badge/?version=latest)](https://archi.readthedocs.io/en/latest/?badge=latest)  [![PyPI version fury.io](https://badge.fury.io/py/pyarchi.svg)](https://pypi.org/project/pyarchi/) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/pyarchi.svg)](https://pypi.org/project/pyarchi/) [![DOI:10.1093/mnras/staa1443](https://zenodo.org/badge/DOI/10.1007/978-3-319-76207-4_15.svg)](https://doi.org/10.1093/mnras/staa1443)\n\n# ARCHI - An expansion to the CHEOPS mission official pipeline\n\n\nHigh precision time-series photometry from space is being used for a number of scientific cases. In this context, the recently launched CHaracterizing ExOPlanet Satellite (CHEOPS) (ESA) mission promises to bring 20 ppm precision over an exposure time of 6\u2009h, when targeting nearby bright stars, having in mind the detailed characterization of exoplanetary systems through transit measurements. However, the official CHEOPS (ESA) mission pipeline only provides photometry for the main target (the central star in the field). In order to explore the potential of CHEOPS photometry for all stars in the field,  we present archi, an additional open-source pipeline module to analyse the background stars present in the image. As archi uses the official data reduction pipeline data as input, it is not meant to be used as an independent tool to process raw CHEOPS data but, instead, to be used as an add-on to the official pipeline. We test archi using CHEOPS simulated images, and show that photometry of background stars in CHEOPS images is only slightly degraded (by a factor of 2–3) with respect to the main target. This opens a potential for the use of CHEOPS to produce photometric time-series of several close-by targets at once, as well as to use different stars in the image to calibrate systematic errors. We also show one clear scientific application where the study of the companion light curve can be important for the understanding of the contamination on the main target.\n\n# ARCHI - a quick preview \n\nHere we have the masks used for the analysis of a simulated data set, for each individual image:\n\n![Alt Text](https://github.com/Kamuish/archi/blob/master/docs/archi_info/star_tracking.gif)\n\n\n# How to install archi \n\nThe pipeline is written in Python3, and most features should work on all versions. However, so far, it was only tested on python 3.6, 3.7 and 3.8\n\nTo install, simply do :\n\n    pip install pyarchi \n\nTo see bug fixes and the new functionalities of each version refer to the [official documentation](https://archi.readthedocs.io/en/latest/archi_info/release.html)\n\n# How to use the library \n\nA proper introduction to the library, alongside documentation of the multiple functions and interfaces can be found [here](https://archi.readthedocs.io/en/latest/). \n\nIf you use the pipeline, cite the article \n\n    @article{Silva_2020,\n       title={ARCHI: pipeline for light curve extraction of CHEOPS background stars},\n       ISSN={1365-2966},\n       url={http://dx.doi.org/10.1093/mnras/staa1443},\n       DOI={10.1093/mnras/staa1443},\n       journal={Monthly Notices of the Royal Astronomical Society},\n       publisher={Oxford University Press (OUP)},\n       author={Silva, André M and Sousa, Sérgio G and Santos, Nuno and Demangeon, Olivier D S and Silva, Pedro and Hoyer, S and Guterman, P and Deleuil, Magali and Ehrenreich, David},\n       year={2020},\n       month={May}\n    }\n\n# Known Problems\n\n\n [1] There is no correction for cross-contamination between stars\n \n [2] If we have data in the entire 200*200 region (not expected to happen) and using the "dynam" mask for the background stars it might "hit" one of the edges of the image. In such case, larger masks will not increase in the direction in which the edge is reached. However, the mask can still grow towards the other directions, leading to masks significantly larger than the original star. In such cases, we recommend to manually change the mask size on the "optimized factors" file.\n',
    'author': 'Kamuish',
    'author_email': 'amiguel@astro.up.pt',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kamuish/archi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
