
## Synopsis

This library provides a simple python interface to 
NASA's [Satellite Situation Center](https://sscweb.sci.gsfc.nasa.gov/)
(SSC).  This library implements the client side of the 
[SSC RESTful web services](https://sscweb.sci.gsfc.nasa.gov/WebServices/REST/)
and can return data in the 
[SpacePy data model](https://pythonhosted.org/SpacePy/datamodel.html).
For more general details about the SSC web services, see
https://sscweb.sci.gsfc.nasa.gov/WebServices/REST/.

## Code Example

This package contains example code calling most of the available web services.
To run the included example, do the following

    python -m sscws

---

The following code demonstrates ....

    import matplotlib as mpl
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt

    from sscws import SscWs

    ssc = SscWs()
    data = ssc....

## Motivation

This library hides the HTTP, JSON/XML, and CDF details of the SSC web 
services. A python developer only has to deal with python objects and 
methods (primarily the SpacePy data model object).

## Dependencies

???  rewrite this section
Accept for common, fundamental depenencies like requests, the
primary dependency is
[SpacePy](https://pythonhosted.org/SpacePy/).  And SpacePy is only 
required if you call the get_data method that returns the data in the
SpacePy data model. Refer to the SpacePy
documentation for the details of SpacePy's dependencies.  In particular, 
SpacePy's data model import capability is dependent upon
[CDF](https://cdf.sci.gsfc.nasa.gov) which is
not (at the time of this writing) automatically installed with SpacePy.  

## Installation

???  rewrite this section
As noted in the dependencies above, if you intend to call the get_data
method, you must install [SpacePy](https://pythonhosted.org/SpacePy/) and
the [CDF](https://cdf.sci.gsfc.nasa.gov) library (following the
procedures at the SpacePy and CDF web sites).

Then, to install this package

    $ pip install -U sscws


## API Reference

Refer to
[sscws package API reference](https://sscweb.sci.gsfc.nasa.gov/WebServices/REST/py/sscws/index.html)

or use the standard python help mechanism.

    from sscws import SscWs
    help(SscWs)

## Tests

The tests directory contains 
[unittest](https://docs.python.org/3/library/unittest.html)
tests.

## Contributors

Bernie Harris.  
[e-mail](mailto:gsfc-spdf-support@lists.nasa.gov) for support.

## License

This code is licensed under the 
[NASA Open Source Agreement](https://cdaweb.gsfc.nasa.gov/WebServices/NASA_Open_Source_Agreement_1.3.txt) (NOSA).
