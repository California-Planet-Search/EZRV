from astropy.time import Time
from barycorrpy import utc_tdb
from astroquery.simbad import Simbad
import astropy.units as u
from astropy.coordinates import SkyCoord
import pandas as pd
import numpy as np
import requests

#check this page for the major observatories on Earth: https://en.wikipedia.org/wiki/List_of_astronomical_observatories
class BarycorrError(BaseException):
    pass

def _query_webserver(server_url, params, expected_length):
    """
    Query server_url with params and return results if length matches
    expected_length (internal function).
    """

    # Fire the HTTP request
    try:
        r = requests.get(server_url, params=params)
    except:
        raise BarycorrError(
            'Could not connect to web server ({})'.format(server_url)
        )

    # Convert multiline string output to numpy float array
    try:
        result = [float(x) for x in r.text.splitlines() if len(x) > 0]
        if len(result) != expected_length:
            raise BarycorrError(
                'Unexpected length of result\n{}'.format(r.url)
            )
        if expected_length == 1:
            return result[0]
        else:
            return array(result)
    except:
        raise BarycorrError(
            'Could not parse output from web server:\n{}'.format(r.url)
        )

def hjd2bjd(hjd_utc, ra, dec, raunits='degrees'):
    """
    Query the web interface for hjd2bjd.pro and compute the barycentric
    Julian Date for each value in hjd_utc.
    See also: http://astroutils.astronomy.ohio-state.edu/time/hjd2bjd.html
    :param jd_utc: Julian date (UTC)
    :param ra: RA (J2000) [deg/hours]
    :param dec: Dec (J2000) [deg]
    :param raunits: Unit of the RA value: 'degrees' (default) or 'hours'
    :return: BJD(TDB) at ~20 ms accuracy (observer at geocenter)
    """

    # Check if there are multiple values of jd_utc
    if not isinstance(hjd_utc, (list, np.ndarray)):
        hjd_utc = [hjd_utc]


    # Prepare GET parameters
    params = {
        'JDS': ','.join(map(repr, hjd_utc)),
        'RA': ra,
        'DEC': dec,
        'RAUNITS': raunits,
        'FUNCTION': 'hjd2bjd',
    }


    # Query the web server
    return _query_webserver(
        'http://astroutils.astronomy.ohio-state.edu/time/convert.php',
        params,
        len(hjd_utc)
    )

print(hjd2bjd(2454833.0132, 312.321124, -32.1312, raunits='degrees'))
'''


class observatory:
	lat = 1.
	longi = 1.
	alt = 1.

obs_list = pd.read_csv('observatory_library.csv',header = 0)
match = obs_list[obs_list['obs']=='harps']
print(match)

obs = observatory()
obs.lat = match['lat'].values[0]
obs.longi = match['longi'].values[0]
obs.alt = match['alt'].values[0]
print(obs.lat,obs.longi,obs.alt)


print(Simbad.list_votable_fields())
Simbad.add_votable_fields('pmra','pmdec','plx','rv_value')

result_table = Simbad.query_object("HD 189733")

c = SkyCoord(str(result_table['RA'][0])+str(result_table['DEC'][0]), unit=(u.hourangle, u.deg))

print(result_table['PMRA'][0])


JDUTC = Time(2458000, format='jd', scale='utc')
bjd = utc_tdb.JDUTC_to_BJDTDB(JDUTC,ra=c.ra.degree, dec=c.dec.degree, pmra=result_table['PMRA'][0], pmdec=result_table['PMDEC'][0], px=result_table['PLX_VALUE'][0], rv=result_table['RV_VALUE'][0]*1e3, lat=obs.lat, longi=obs.longi, alt=obs.alt)
print(bjd)

bjd = utc_tdb.JDUTC_to_BJDTDB(JDUTC,hip_id = 98505, lat=-29.25, longi=-70.73, alt=2400.)
print(bjd)
'''
