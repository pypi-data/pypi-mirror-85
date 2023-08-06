import glob
import os
import requests
import time
import sys

import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame

from geocoding_api_extract.utils.progress import Progress


def create_geocoding_api_request_str(street, city, state,
                                     benchmark='Public_AR_Census2010',
                                     vintage='Census2010_Census2010',
                                     layers='14',
                                     format='json') -> str:
    """Create geocoding api request str

    Args:
        street (str): street address
        city (str): city
        state (str): state as 2 digit initial
        benchmark (str, optional): Defaults to 'Public_AR_Census2010'.
        vintage (str, optional): Defaults to 'Census2010_Census2010'.
        layers (str, optional): Defaults to '14'.
        format (str, optional): Defaults to 'json'.

    Returns:
        str: geocoding api request string.
    """

    return 'https://geocoding.geo.census.gov/geocoder/geographies/address?street=' + \
        street + '&city=' + city + '&state=' + state + '&benchmark=' + benchmark + \
        '&vintage=' + vintage + '&layers=' + layers + '&format=' + format


def extract_address_batch(address_batch, city, state, retries=5):
    """Extract one address batch

    Args:
        address_batch (list(str)): list of addresses 
        city (str): City 
        state (str): 2-digit state code 
        retries (int, optional): Number of time to retry the api request. Defaults to 5.

    Returns:
        DataFrame: result table from api extract 
    """    

    result = {'address': address_batch,
              'state': [],
              'county': [],
              'tract': [],
              'cent_lat': [],
              'cent_lon': [],
              'us_zip': []}
    exception = ""
    for address in address_batch:
        request = requests.get(
            create_geocoding_api_request_str(address, city, state))
        for attempt in range(retries):
            try:
                if request.status_code == 200 and request.json()['result']['addressMatches'] != []:
                    result['state'].append(request.json()['result']['addressMatches']
                                           [0]['geographies']['Census Blocks'][0]['STATE'])
                    result['county'].append(request.json()['result']['addressMatches']
                                            [0]['geographies']['Census Blocks'][0]['COUNTY'])
                    result['tract'].append(request.json()['result']['addressMatches']
                                           [0]['geographies']['Census Blocks'][0]['TRACT'])
                    result['cent_lat'].append(request.json()['result']['addressMatches']
                                              [0]['geographies']['Census Blocks'][0]['CENTLAT'])
                    result['cent_lon'].append(request.json()['result']['addressMatches']
                                              [0]['geographies']['Census Blocks'][0]['CENTLON'])
                    result['us_zip'].append(request.json()['result']['addressMatches']
                                            [0]['addressComponents']['zip'])
                else:
                    result['state'].append("not found")
                    result['county'].append("not found")
                    result['tract'].append("not found")
                    result['cent_lat'].append("not found")
                    result['cent_lon'].append("not found")
                    result['us_zip'].append("not found")
            except Exception as x:
                print(f'BAD REQUEST: {type(x)} {x} {request}')
                exception = x
                # wait incrementally longer each retry
                wait_time = 30 * (attempt+1)**2
                print(f'Waiting {wait_time} seconds.')
                time.sleep(wait_time)
            else:
                break
        else:
            # all attempts failed, log this
            print(
                f'API REQUEST FAILED AFTER {retries} ATTEMPTS WITH EXCEPTION: {exception} :: {request}')
            empty_result = pd.DataFrame()
            return empty_result

    results = pd.DataFrame(result)
    return results


def extract_address_batches(address_batches, city, state, progress):
    """Wrapper function to yeild results of each address batch extraction.

    Args:
        address_batches (list[list[str]]): list of address batches
        city (str): City
        state (str): 2 digit state code
        progress (Progress): Object for keeping track of progress

    Yields:
        DataFrame: resulting DataFrame from address extraction
    """    
    for i in range(progress.value, len(address_batches)):
        print('Processing address batch:', i)
        result = extract_address_batch(
            address_batches[i], city, state)
        yield result


def extract_address_details(addresses, city, state, 
                            tmp_folder, tmp_filename_prefix='', 
                            reset=False, clean_result=True) -> DataFrame:
    """Extract address details from geocoding api

    Args:
        addresses (list[str]): a list of addresses
        city (str): the city where the addresses reside
        state (str): 2-digit state abbreviation
        tmp_folder (str): the folder to put partial data extracts in
        tmp_filename_prefix (str, optional): export filename suffix for temp result chunks
        reset (bool, optional): if True, the extraction will reset
            which will delete all temp files and reset progress
        

    Returns:
        DataFrame: A table showing each address and the following extra columns:
            ['address','state'(id),'county'(id),'tract'(id),'cent_lat','cent_lon','us_zip']
    """
    if type(addresses) != list:
        print("Type mismatch: 'addresses' needs to be a list of strings")
        return pd.DataFrame()
     
    if (type(city) != str):
        print("Type mismatch: 'city' needs to be a string")
        return pd.DataFrame()
    
    if (type(state) != str):
        print("Type mismatch: 'state' needs to be a string")
        return pd.DataFrame()
    
    if (type(tmp_folder) != str):
        print("Type mismatch: 'tmp_folder' needs to be a string")
        return pd.DataFrame()

    
    # batch addresses into manageable chunks
    parts = len(addresses)//50
    if parts > 1:
        address_batches = np.array_split(addresses, parts)
    else:
        address_batches = [addresses]

    path = tmp_folder + tmp_filename_prefix + state + '_' + city + '/'
    
    try:
        if os.path.isdir(path):
            print("Directory already exists")
        else:
            os.mkdir(path)
    except OSError as e:
        print("Returning empty DataFrame:  There is a problem with the tmp_folder path: %s." % path)
        return pd.DataFrame()
    else:
        print("Successfully created the directory %s " % path)
    
    export_tmp_fp = path + 'geocoding_api_extract'
    
    # initialize progress tracker
    # TODO: add 'home' directory in a project config file and use that as the root for
    # this progress filepath
    progress = Progress('GEOCODING_API', path + 'geocoding_api_progress.cfg')

    # reset progress
    if reset:
        progress.reset()
        filepaths = glob.glob(export_tmp_fp + "_part*.parquet.gzip")
        for fp in filepaths:
            os.remove(fp)

    # extract and export each batch
    for result in extract_address_batches(address_batches, city, state, progress):
        # export batch DataFrame
        fp = export_tmp_fp + '_part' + str(progress.value) + '.parquet.gzip'
        result.to_parquet(fp)

        # record progress
        progress.increment()

    # combine all the batch files into a DataFrame
    filepaths = glob.glob(export_tmp_fp + "_part*.gzip")
    result_dfs = [pd.read_parquet(filepath) for filepath in filepaths]
    results = pd.concat(result_dfs, ignore_index=True)
    
    if clean_result:
        results = results[results['tract'] != 'not found']
    
    print("Geocoding api address extract is complete.")

    return results


def remove_tmp_files(city, state, tmp_folder, tmp_filename_prefix='') -> None:
    """Remove temp files created during an extract

    Args:
        city (str): the city where the addresses reside
        state (str): 2-digit state abbreviation
        tmp_filename_prefix (str, optional): export filename suffix for temp result chunks
    """    
    
    path = tmp_folder + tmp_filename_prefix + state + '_' + city + '/'
    if not os.path.isdir(path):
        return
    
    export_tmp_fp = path + 'geocoding_api_extract'
    
    filepaths = glob.glob(export_tmp_fp + "_part*.parquet.gzip")
    for fp in filepaths:
        os.remove(fp)
        
    if os.path.isfile(path + 'geocoding_api_progress.cfg'):
        os.remove(path + 'geocoding_api_progress.cfg')
    
    if os.path.isdir(path):
        os.rmdir(path)
    


    
