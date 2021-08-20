from astropy.time import Time
from barycorrpy import utc_tdb
from astroquery.simbad import Simbad
import astropy.units as u
from astropy.coordinates import SkyCoord
import pandas as pd
import numpy as np
import yaml
import requests
import matplotlib.pylab as plt
config = yaml.safe_load(open("config/config.yaml"))

#check this page for the major observatories on Earth: https://en.wikipedia.org/wiki/List_of_astronomical_observatories
class BarycorrError(BaseException):
    pass

class observatory:
	lat = 1.
	longi = 1.
	alt = 1.

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




def time_conversion(file_name): #input is one particular file in our database
    print("Converting Time to BJD for "+file_name+"...")
    # get the information on the observatories
    obs_info = pd.read_csv(config['default_directory'] + '/Metadata/observ_names.csv',header = 0)
    #print(obs_info)

    #get the data to be converted
    df = pd.read_csv(file_name,header = 0)
    df['Time_BJD'] = df['Time']#np.ones(len(


    #get info on the host star
    Simbad.add_votable_fields('pmra','pmdec','plx','rv_value')
    result_table = Simbad.query_object(df['Star_Name'][0])
    c = SkyCoord(str(result_table['RA'][0])+str(result_table['DEC'][0]), unit=(u.hourangle, u.deg))

    #read in the leap second file
    leap_sec_df = pd.read_csv(config['default_directory'] + '/Metadata/leap_seconds.csv',header = 0)
    leap_sec_df['Sec'] += 32
    leap_sec_df['jd'] = np.ones(len(leap_sec_df['Sec']))
    for i in range(len(leap_sec_df['jd'])):
        tmp = Time(str(leap_sec_df['Year'][i])+'-'+str(leap_sec_df['Month'][i]).zfill(2)+'-'+str(leap_sec_df['Day'][i]).zfill(2), format = 'isot')
        leap_sec_df['jd'][i] = tmp.jd





    for i in range(len(df['Time_Convention'])):#
        match = np.where(obs_info['Observatory_Site'] == df['Observatory_Site'][i])[0]

        #find the info on the observatories
        obs = observatory()
        obs.lat = obs_info['Latitude'][match].values[0]
        obs.longi = obs_info['Longitutde'][match].values[0]
        obs.alt = obs_info['Altitude(m)'][match].values[0]#match['alt'].values[0]






        if (df['Time_Convention'][i] == 'BJD') or (df['Time_Convention'][i] == 'BJD_TDB') or (df['Time_Convention'][i] == 'BJD-TDB'):#no need to convert
            df['Time_BJD'][i] = df['Time'][i]

        if (df['Time_Convention'][i] == 'BJD-UTC'):#correct for leap seconds BJD-UTC
            tmp = abs(df['Time'][i]-leap_sec_df['jd'])
            index_tmp = np.where(tmp==np.min(tmp))[0]
            df['Time_BJD'][i] = df['Time'][i]+leap_sec_df['Sec'][index_tmp].values[0]/24/3600.

        if (df['Time_Convention'][i] == 'JD') or (df['Time_Convention'][i] == 'JD-UTC') or (df['Time_Convention'][i] == 'FCJD') or (df['Time_Convention'][i] == 'MJD'):
            JDUTC = Time(df['Time'][i], format='jd', scale='utc')
            bjd = utc_tdb.JDUTC_to_BJDTDB(JDUTC,ra=c.ra.degree, dec=c.dec.degree, pmra=result_table['PMRA'][0], pmdec=result_table['PMDEC'][0], px=result_table['PLX_VALUE'][0], rv=result_table['RV_VALUE'][0]*1e3, lat=obs.lat, longi=obs.longi, alt=obs.alt)
            df['Time_BJD'][i] = bjd[0][0]

        if (df['Time_Convention'][i] == 'HJD') or (df['Time_Convention'][i] == 'HJD-UTC'):
            df['Time_BJD'][i] = hjd2bjd(df['Time'][i], c.ra.degree, c.dec.degree, raunits='degrees')

        if (df['Time_Convention'][i] == 'HJD_TBD'):#correct for leap second before converting
            tmp = abs(df['Time'][i]-leap_sec_df['jd'])
            index_tmp = np.where(tmp==np.min(tmp))[0]
            df['Time_BJD'][i] = hjd2bjd(df['Time'][i]-leap_sec_df['Sec'][index_tmp].values[0]/24/3600., c.ra.degree, c.dec.degree, raunits='degrees')

    return df #the output data frame with BJD_TDB in df['Time_BJD']

#df = time_conversion('Database/HD 95089.csv')
#plt.scatter(df['Time'],df['Time_BJD']-df['Time'])
#plt.savefig('tmp.pdf')
