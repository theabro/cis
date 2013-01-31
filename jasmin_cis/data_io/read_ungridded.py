'''
Module for reading ungridded data in HDF4 format
'''
import numpy as np
from ungridded_data import UngriddedData
import hdf_vd as hdf_vd
import hdf_sd as hdf_sd

def get_file_variables(filename):
    '''
    Get all variables from a file containing ungridded data.
    Concatenate variable from both VD and SD data
    
    args:
        filename: The filename of the file to get the variables from
    
    '''
    SD_vars = hdf_sd.get_hdf_SD_file_variables(filename)
    VD_vars = hdf_vd.get_hdf_VD_file_variables(filename)
    
    return SD_vars, VD_vars


def get_file_coordinates(filename):
    '''
    Read in coordinate variables and pass back tuple of lat, lon,
    each element of tuple being a 2D numpy array
    '''

    data = hdf_vd.get_hdf4_VD_data(filename,['Latitude','Longitude'])
    lat = data['Latitude'].get()
    long = data['Longitude'].get()
    
    return (lat,long)


def get_file_coordinates_points(filename):
    '''
    Convert coordinate arrays into a list of points
    useful or colocation sampling   
    '''
    from jasmin_cis.data_io.hyperpoint import HyperPoint
    
    latitude, longitude = get_file_coordinates(filename)
    
    points = []    
    
    for (x,y), lat in np.ndenumerate(latitude):
        lon = longitude[x,y]
        points.append(HyperPoint(lat,lon))
        
    return points


def read(filenames, variables):
    '''
    Read ungridded data from a file. Just a wrapper that calls the appropriate class method based on
        whether in the inputs are lists or not
    
    args:
        filenames:    List of filenames of files to read
        variables:    List of variables to read from the files
    '''
    if isinstance(filenames,list):
        if isinstance(variables, list):
            return UngriddedData.load_ungridded_data_list(filenames, variables)
        else:
            return UngriddedData.load_ungridded_data(filenames, variables)
    else:
        if isinstance(variables, list):
            return UngriddedData.load_ungridded_data_list([filenames], variables)
        else:
            return UngriddedData.load_ungridded_data([filenames], variables)             

