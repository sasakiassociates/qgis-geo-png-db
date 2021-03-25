import math
from collections import namedtuple

# can't figure out how to get QGIS plugins working with dependencies, so just pulling the code we need in here from mercantile

Tile = namedtuple("Tile", ["x", "y", "z"])
LngLat = namedtuple("LngLat", ["lng", "lat"])

class MercantileError(Exception):
    """Base exception"""


class InvalidLatitudeError(MercantileError):
    """Raised when math errors occur beyond ~85 degrees N or S"""


class InvalidZoomError(MercantileError):
    """Raised when a zoom level is invalid"""


class ParentTileError(MercantileError):
    """Raised when a parent tile cannot be determined"""


class QuadKeyError(MercantileError):
    """Raised when errors occur in computing or parsing quad keys"""


class TileArgParsingError(MercantileError):
    """Raised when errors occur in parsing a function's tile arg(s)"""

"""A longitude and latitude pair

Attributes
----------
lng, lat : float
    Longitude and latitude in decimal degrees east or north.
"""

def truncate_lnglat(lng, lat):
    if lng > 180.0:
        lng = 180.0
    elif lng < -180.0:
        lng = -180.0
    if lat > 90.0:
        lat = 90.0
    elif lat < -90.0:
        lat = -90.0
    return lng, lat

def _tile(lng, lat, zoom, truncate=False):
    if truncate:
        lng, lat = truncate_lnglat(lng, lat)
    lat = math.radians(lat)
    n = 2.0 ** zoom
    xtile = (lng + 180.0) / 360.0 * n

    try:
        ytile = (
            (1.0 - math.log(math.tan(lat) + (1.0 / math.cos(lat))) / math.pi) / 2.0 * n
        )
    except ValueError:
        raise InvalidLatitudeError(
            "Y can not be computed for latitude {} radians".format(lat)
        )
    else:
        return xtile, ytile, zoom

def ul(xtile, ytile, zoom):
    """Returns the upper left longitude and latitude of a tile

    Parameters
    ----------
    tile : Tile or sequence of int
        May be be either an instance of Tile or 3 ints, X, Y, Z.

    Returns
    -------
    LngLat

    """

    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return LngLat(lon_deg, lat_deg)

def tile_plus(lng, lat, zoom, truncate=False):
    t = tile(lng, lat, zoom, truncate)
    return Tile(t.x+1, t.y+1, zoom)

def tile(lng, lat, zoom, truncate=False):
    """Get the tile containing a longitude and latitude

    Parameters
    ----------
    lng, lat : float
        A longitude and latitude pair in decimal degrees.
    zoom : int
        The web mercator zoom level.
    truncate : bool, optional
        Whether or not to truncate inputs to limits of web mercator.

    Returns
    -------
    Tile

    """
    xtile, ytile, zoom = _tile(lng, lat, zoom, truncate=truncate)
    xtile = int(math.floor(xtile))
    ytile = int(math.floor(ytile))
    return Tile(xtile, ytile, zoom)