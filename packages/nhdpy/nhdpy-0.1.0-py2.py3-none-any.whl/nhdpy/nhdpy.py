"""Main module."""

from shutil import copyfileobj
import requests
from requests import HTTPError
import pandas as pd
import appdirs
import os
import zipfile
import fiona
import geopandas

def key_state(state):
    key = {'sabb': ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC'], 'sname': ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New_Hampshire', 'New_Jersey', 'New_Mexico', 'New_York', 'North_Carolina', 'North_Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode_Island', 'South_Carolina', 'South_Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West_Virginia', 'Wisconsin', 'Wyoming', 'District_of_Columbia']}
    key = pd.DataFrame(data = key)

    return key[key.sabb.eq(state)]['sname'].astype('string').iloc[0]

def nhd_path():
    return appdirs.user_data_dir() + "/nhdR/"

def gdb_path(state):
    return os.path.join(nhd_path(), "NHD_H_" + key_state(state) + "_State_GDB.gdb")

# cribbed from the 'nhdnet' package (https://github.com/brendan-ward/nhdnet)
def get_if_not_exists(url, destfile, force_dl = False):
    if force_dl:
        print("Re-downloading " + url)
        with requests.get(url, stream=True) as r:
            if not r.status_code == 200:
                raise HTTPError("Could not download {}".url)
            with open(destfile, "wb") as out:
                print(
                    "Downloading: {url} ({size:.2f} MB)".format(
                        url=url, size=int(r.headers["Content-Length"]) / 1024 ** 2
                    )
                )                
                copyfileobj(r.raw, out)

    if not os.path.exists(destfile):
        print("Downloading " + url)
        with requests.get(url, stream=True) as r:
            if not r.status_code == 200:
                raise HTTPError("Could not download {}".url)
            with open(destfile, "wb") as out:
                print(
                    "Downloading: {url} ({size:.2f} MB)".format(
                        url=url, size=int(r.headers["Content-Length"]) / 1024 ** 2
                    )
                )                
                copyfileobj(r.raw, out)
    else:
        print("A local copy of " + url + " already exists on disk")  

def get_remotepath(state, baseurl):    
    filename = "NHD_H_" + state + "_State_GDB.zip"
    url = baseurl + "GDB/" + filename
    return [filename, url]

def nhd_get(state, force_dl = False):
    """Download and cache NHD data by state
    
    Parameters
    ----------
    state : str
        character state abbreviation includes "DC", "PR", and "VI"
    force_dl : boolean
        force download and allow for file overwrite
    """
        
    # state = "DC"

    baseurl = "https://prd-tnm.s3.amazonaws.com/StagedProducts/Hydrography/NHD/State/HighResolution/"

    state_name = key_state(state)
    filename, url = get_remotepath(state_name, baseurl)
    destfile = nhd_path() + filename

    get_if_not_exists(url, destfile, force_dl = force_dl)
    zipfile.ZipFile(destfile).extractall(path = os.path.dirname(destfile))

def nhd_list(state):
    return fiona.listlayers( \
        gdb_path(state))

def nhd_load(state, layer):
    # state = "DC"
    # layer = "NHDWaterbody"
    res = geopandas.read_file(gdb_path(state), layer = layer)
    return res
