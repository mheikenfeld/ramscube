import warnings
warnings.filterwarnings('ignore', category=UserWarning, append=True)

#Added for RAMS:
    
#def loadrams(filename,variable):
#    from iris import load_cube 
#    variable_cube=load_cube(filename,variable)
#    add_dim_coordinates(filename, variable,variable_cube,add_coordinates=None)
#    return  variable_cube


RAMS_Units=dict()
RAMS_Units['UC']='m s-1'
RAMS_Units['VC']='m s-1'
RAMS_Units['WC']='m s-1'
RAMS_Units['THETA']='K'	
RAMS_Units['RV']='kg kg-1'
RAMS_Units['RCP']='kg kg-1'	
RAMS_Units['RDP']='kg kg-1'
RAMS_Units['RRP']='kg kg-1'	
RAMS_Units['RPP']='kg kg-1'		
RAMS_Units['RSP']='kg kg-1'		
RAMS_Units['RAP']='kg kg-1'	
RAMS_Units['RGP']='kg kg-1'		
RAMS_Units['RHP']='kg kg-1'	
RAMS_Units['CCP']='kg-1'	
RAMS_Units['CDP']='kg-1'
RAMS_Units['CRP']='kg-1'	
RAMS_Units['CPP']='kg-1'
RAMS_Units['CSP']='kg-1'	
RAMS_Units['CAP']='kg-1'
RAMS_Units['CGP']='kg-1'	
RAMS_Units['CHP']='kg-1'
RAMS_Units['DN0']='kg m-3'

RAMS_standard_name=dict()

variable_list_derive=[
        'potential_temperature',
        'temperature'
        ]
#def variable_list(filenames):
#    from netCDF4 import Dataset
#    if type(filenames)==list:
#        filenames=filenames[0]
#    variable_list = list(Dataset(filenames).variables)
#    return variable_list
#
#
#def load(filenames,variable,mode='auto',**kwargs):
#    if mode=='auto':
#        variable_list_file=variable_list(filenames)
#        if variable in variable_list_file:
#            variable_cube=loadwrfcube(filenames,variable,**kwargs)
#        elif variable in variable_list_derive:
#            variable_cube=derivewrfcube(filenames,variable,**kwargs)
#        elif variable in variable_dict_pseudonym.keys:
#            variable_load=variable_dict_pseudonym[variable]
#            variable_cube=loadwrfcube(filenames,variable_load,**kwargs)
#    elif mode=='file':
#        variable_list_file=variable_list(filenames)
#        if variable in variable_list_file:
#            variable_cube=loadwrfcube(filenames,variable,**kwargs)
#    elif mode=='derive':
#        variable_cube=derivewrfcube(filenames,variable,**kwargs)
#    elif mode=='pseudonym':
#        variable_load=variable_dict_pseudonym[variable]
#        variable_cube=loadwrfcube(filenames,variable_load,**kwargs)
#    else:
#       print("mode=",mode)
#       raise SystemExit('unknown mode')
#
#    return variable_cube





def loadramscube(filenames,variable,**kwargs):
    if type(filenames) is list:
        variable_cube=loadramscube_mult(filenames,variable,**kwargs)
    elif type(filenames) is str:
        variable_cube=loadramscube_single(filenames,variable,**kwargs)
    else:
        print("filenames=",filenames)
        raise SystemExit('Type of input unknown: Must be str of list')
    
    return variable_cube
    
def loadramscube_single(filenames,variable,constraint=None,add_coordinates=None):
    from iris import load_cube 

    variable_cube=load_cube(filenames,variable)
    variable_cube.units=RAMS_Units[variable]

    variable_cube=addcoordinates(filenames, variable,variable_cube,add_coordinates=add_coordinates)
    return  variable_cube

        
    
def loadramscube_mult(filenames,variable,constraint=None,add_coordinates=None):
    from iris.cube import CubeList
    cube_list=[]

    for i in range(len(filenames)):
        cube_list.append(loadramscube_single(filenames[i],variable,add_coordinates=add_coordinates) )
    for member in cube_list:
        member.attributes={}
    variable_cubes=CubeList(cube_list)
    variable_cube=variable_cubes.merge_cube()
    variable_cube=variable_cube.extract(constraint)
    return variable_cube


def readramsheader(filename):
    from numpy import array
    
    searchfile = open(filename, "r")
    coord_dict=dict()
    variable_dict=dict()

    coord_part=False
    i_variable=0
    n_variable=0

    for i,line in enumerate(searchfile):

        if (i==0):
            num_variables=int(line[:-1])
            
        if (i>0 and i<=num_variables):
            line_split=line[:-1].split()
            variable_dict[line_split[0]]=int(line_split[2])
            

        if ('__') in line:
            coord_part=True

            
            i_variable=i
            variable_name=line[2:-1]
            variable_list=[]
        if coord_part: 
            if (i==i_variable+1):
                n_variable=int(line[:-1])

            if n_variable>0:
    
                if (i>=i_variable+2 and i<=i_variable+1+n_variable):
                    try:
                        value_out=array(float(line[:-1]))
                    except:
                        value_out=line[:-1]
                    variable_list.append(value_out)

                if (i==i_variable+1+n_variable):

                    coord_dict[variable_name]=array(variable_list)
                    coord_part=False
#            else:
#                coord_part=False


    return variable_dict, coord_dict

def addcoordinates(filename, variable,variable_cube,**kwargs):
    if 'add_coordinates' in kwargs:
        add_coordinates=kwargs['add_coordinates']
    else:
        add_coordinates=None
    filename_header=filename[:-5]+'head.txt'
    variable_dict, coord_dict=readramsheader(filename_header)
    if add_coordinates==None:
        variable_cube=add_dim_coordinates(filename, variable,variable_cube,variable_dict, coord_dict,**kwargs)
    else:
        variable_cube=add_dim_coordinates(filename, variable,variable_cube,variable_dict, coord_dict,**kwargs)
        variable_cube=add_aux_coordinates(filename, variable,variable_cube,variable_dict, coord_dict,**kwargs)
    return variable_cube
 
    
def make_time_coord(coord_dict):
    from datetime import datetime,timedelta
    from iris import coords
    timestr=str(int(coord_dict['iyear1'][0]))+str(int(coord_dict['imonth1'][0])).zfill(2)+str(int(coord_dict['idate1'][0])).zfill(2)+str(int(coord_dict['itime1'][0])).zfill(4)
    timeobj = datetime.strptime(timestr,"%Y%m%d%H%M")+timedelta(seconds=1)*coord_dict['time'][0]

    if timeobj<datetime(100,1,1):
        base_date=datetime(1,1,1)
    else:
        base_date=datetime(1970,1,1)
    time_units='days since '+ base_date.strftime('%Y-%m-%d')

    time_days=(timeobj - base_date).total_seconds() / timedelta(days=1).total_seconds()
    time_coord=coords.DimCoord(time_days, standard_name='time', long_name='time', var_name='time', units=time_units, bounds=None, attributes=None, coord_system=None, circular=False)
    return time_coord              


def add_dim_coordinates(filename, variable,variable_cube,variable_dict, coord_dict,add_coordinates=None):        
    from iris import coords
#    from iris import coord_systems

#    coord_system=coord_systems.LambertConformal(central_lat=MOAD_CEN_LAT, central_lon=CEN_LON, false_easting=0.0, false_northing=0.0, secant_latitudes=(TRUELAT1, TRUELAT2))
    coord_system=None
    if (variable_dict[variable]==3):
    
        x_coord=coords.DimCoord(coord_dict['xtn03'], standard_name='projection_x_coordinate', long_name='x', var_name='x', units='m', bounds=None, attributes=None, coord_system=coord_system)
        variable_cube.add_dim_coord(x_coord,1)
        y_coord=coords.DimCoord(coord_dict['ytn03'], standard_name='projection_y_coordinate', long_name='y', var_name='y', units='m', bounds=None, attributes=None, coord_system=coord_system)
        variable_cube.add_dim_coord(y_coord,2)
        z_coord=coords.DimCoord(coord_dict['ztn03'], standard_name='geopotential_height', long_name='z', var_name='z', units='m', bounds=None, attributes=None, coord_system=coord_system)
        variable_cube.add_dim_coord(z_coord,0)
        time_coord=make_time_coord(coord_dict)
        variable_cube.add_aux_coord(time_coord)


    elif (variable_dict[variable]==2):
        x_coord=coords.DimCoord(coord_dict['xtn03'], standard_name='projection_x_coordinate', long_name='x', var_name='x', units='m', bounds=None, attributes=None, coord_system=coord_system)
        variable_cube.add_dim_coord(x_coord,0)
        y_coord=coords.DimCoord(coord_dict['ytn03'], standard_name='projection_y_coordinate', long_name='y', var_name='y', units='m', bounds=None, attributes=None, coord_system=coord_system)
        variable_cube.add_dim_coord(y_coord,1)
        time_coord=make_time_coord(coord_dict)
        variable_cube.add_aux_coord(time_coord)
    return variable_cube


def add_aux_coordinates(filename,variable,variable_cube,variable_dict, coord_dict,**kwargs):
    from iris import load_cube,coords
    coord_system=None

    add_coordinates=kwargs.pop('add_coordinates')
    if type(add_coordinates)!=list:
        add_coordinates1=add_coordinates
        add_coordinates=[]
        add_coordinates.append(add_coordinates1)
    for coordinate in add_coordinates:
        if coordinate=='latlon': 
            latitude=load_cube(filename,'GLAT').data
            longitude=load_cube(filename,'GLON').data
            lat_coord=coords.AuxCoord(latitude, standard_name='latitude', long_name='latitude', var_name='latitude', units='degrees', bounds=None, attributes=None, coord_system=coord_system)
            lon_coord=coords.AuxCoord(longitude, standard_name='longitude', long_name='longitude', var_name='longitude', units='degrees', bounds=None, attributes=None, coord_system=coord_system)

            if (variable_dict[variable]==3):                
                variable_cube.add_aux_coord(lon_coord,(1,2))
                variable_cube.add_aux_coord(lat_coord,(1,2))
            elif (variable_dict[variable]==2):
                variable_cube.add_aux_coord(lon_coord,(0,1))                
                variable_cube.add_aux_coord(lat_coord,(0,1))

    return variable_cube

def calculate_rams_LWC(filenames,**kwargs):
    RCP=loadramscube(filenames, 'RCP',**kwargs)
    RDP=loadramscube(filenames, 'RDP',**kwargs)
    RRP=loadramscube(filenames, 'RDP',**kwargs)
    LWC=RCP+RDP+RRP
    LWC.rename('liquid water content')
    #LWC.rename('mass_concentration_of_liquid_water_in_air')
    return LWC   
#    
def calculate_rams_IWC(filenames,**kwargs):    
    RPP=loadramscube(filenames, 'RPP',**kwargs)
    RSP=loadramscube(filenames, 'RSP',**kwargs)
    RAP=loadramscube(filenames, 'RAP',**kwargs)
    RGP=loadramscube(filenames, 'RGP',**kwargs)
    RHP=loadramscube(filenames, 'RHP',**kwargs)

    IWC=RPP+RSP+RAP+RGP+RHP
    IWC.rename('ice water content')
    #IWC.rename('mass_concentration_of_ice_water_in_air')
    return IWC   

    
def calculate_rams_airmass(filenames,**kwargs):
    from iris.cube import Cube
    from iris.coords import AuxCoord
    from iris.util import as_compatible_shape
    rho=loadramscube(filenames,'DN0',**kwargs)
    z=rho.coord('geopotential_height')    
    z_dim=rho.coord_dims('geopotential_height')
    z_diff=AuxCoord(mydiff(z.points),var_name='z_diff')
    rho.add_aux_coord(z_diff,data_dims=z_dim)    
    Airmass=rho*rho.coord('z_diff') 
    Airmass.remove_coord('z_diff')
    Airmass.rename('mass of air')
    Airmass.units='kg m-2'
    return Airmass


def calculate_rams_density(filenames,**kwargs):
    rho=loadramscube(filenames,'DN0',**kwargs)
    rho.rename('mass of air')
    rho.units='kg m-3'
    return rho

        
def calculate_rams_LWP(filenames,**kwargs):
    from iris.analysis import SUM
    LWC=deriveramscube(filenames,'LWC',**kwargs)
    Airmass=deriveramscube(filenames,'airmass',**kwargs)
    LWP=(LWC*Airmass).collapsed(('altitude'),SUM)
    LWP.rename('liquid water path')
    #LWP.rename('atmosphere_mass_content_of_cloud_liquid_water')
    return LWP   
#    
def calculate_rams_IWP(filenames,**kwargs):    
    from iris.analysis import SUM
    IWC=deriveramscube(filenames,'IWC',**kwargs)
    Airmass=deriveramscube(filenames,'airmass',**kwargs)
    IWP=(IWC*Airmass).collapsed(('altitude'),SUM)
    IWP.rename('ice water path')
    #IWP.rename('atmosphere_mass_content_of_cloud_ice_water')
    return IWP

def calculate_rams_IWV(filenames,**kwargs):    
    from iris.analysis import SUM
    RV=loadramscube(filenames,'RV',**kwargs)
    Airmass=deriveramscube(filenames,'airmass',**kwargs)
    IWV=(RV*Airmass).collapsed(('altitude'),SUM)
    IWV.rename('integrated water vapor')
    #IWP.rename('atmosphere_mass_content_of_cloud_ice_water')
    return IWV


def mydiff(A):
    import numpy as np
    d1=np.diff(A)
    d=np.zeros(A.shape)
    d[0]=d1[0]
    d[1:-1]=0.5*(d1[0:-1]+d1[1:])
    d[-1]=d1[-1]
    return d



def deriveramscube(filenames,variable,**kwargs):
#    if variable in ['temperature','air_temperature']:
#        variable_cube=calculate_rams_temperature(filenames,**kwargs)
#        #variable_cube_out=addcoordinates(filenames, 'T',variable_cube,add_coordinates)
#    elif variable == 'density':
#        variable_cube=calculate_rams_density(filenames,**kwargs)

    if variable == 'LWC':    
        variable_cube=calculate_rams_LWC(filenames,**kwargs)
    elif variable == 'IWC':    
        variable_cube=calculate_rams_IWC(filenames,**kwargs)
    elif variable == 'LWP':    
        variable_cube=calculate_rams_LWP(filenames,**kwargs)
    elif variable == 'IWP':    
        variable_cube=calculate_rams_IWP(filenames,**kwargs)
    elif variable == 'IWV':    
        variable_cube=calculate_rams_IWV(filenames,**kwargs)
    elif variable == 'airmass':    
        variable_cube=calculate_rams_airmass(filenames,**kwargs)

    
#    if variable == 'potential temperature':
#        variable_cube=calculate_rams_potential_temperature(filenames,**kwargs)
#        #variable_cube_out=addcoordinates(filenames, 'T',variable_cube,add_coordinates)
#    elif variable in ['temperature','air_temperature']:
#        variable_cube=calculate_rams_temperature(filenames,**kwargs)
#        #variable_cube_out=addcoordinates(filenames, 'T',variable_cube,add_coordinates)
#    elif variable == 'density':
#        variable_cube=calculate_rams_density(filenames,**kwargs)
#        #variable_cube_out=addcoordinates(filenames, 'T',variable_cube,add_coordinates)
#    elif variable == 'LWC':    
#        variable_cube=calculate_rams_LWC(filenames,**kwargs)
#        #variable_cube=addcoordinates(filenames, 'QCLOUD',variable_cube,add_coordinates)
#    elif variable == 'IWC':    
#        variable_cube=calculate_rams_IWC(filenames,**kwargs)
#        #variable_cube=addcoordinates(filenames, 'QICE',variable_cube,add_coordinates)    
#    elif variable == 'LWP':    
#        variable_cube=calculate_rams_LWP(filenames,**kwargs)
#        #variable_cube=addcoordinates(filenames, 'OLR',variable_cube,add_coordinates)
#    elif variable == 'IWP':    
#        variable_cube=calculate_rams_IWP(filenames,**kwargs)
#        #variable_cube=addcoordinates(filenames, 'OLR',variable_cube,add_coordinates)
#    elif variable == 'IWV':    
#        variable_cube=calculate_rams_IWV(filenames,**kwargs)
#        #variable_cube=addcoordinates(filenames, 'OLR',variable_cube,add_coordinates)
#    elif variable == 'airmass':    
#        variable_cube=calculate_rams_airmass(filenames,**kwargs)
#    elif variable == 'layer_height':    
#        variable_cube=calculate_rams_layerheight(filenames,**kwargs)
#    elif variable == 'area':    
#        variable_cube=calculate_rams_area(filenames,**kwargs)        
#    elif variable == 'geopotential_height':    
#        variable_cube=calculate_rams_geopotential_height(filenames,**kwargs)
#        replace_cube=loadramscube(filenames,'T',**kwargs)
#        variable_cube=replacecoordinates(variable_cube,replace_cube)  
#    
#    elif variable == 'geopotential_height_stag':    
#        variable_cube=calculate_rams_geopotential_height_stag(filenames,**kwargs)
#
##    elif variable == 'geopotential_height_xstag':    
##        variable_cube=calculate_rams_geopotential_height_xstag(filenames,**kwargs)
##        replace_cube=loadramscube(filenames,'U',**kwargs)
##        variable_cube=replacecoordinates(variable_cube,replace_cube)  
##
##    elif variable == 'geopotential_height_ystag':    
##        variable_cube=calculate_rams_geopotential_height_ystag(filenames,**kwargs)
##        replace_cube=loadramscube(filenames,'V',**kwargs)
##        variable_cube=replacecoordinates(variable_cube,replace_cube)  
#
#    elif variable == 'pressure':    
#        variable_cube=calculate_rams_pressure(filenames,**kwargs)
#        
#    elif variable == 'geopotential':    
#        variable_cube=calculate_rams_geopotential(filenames,**kwargs)
#
#    elif variable == 'pressure_xstag':    
#        variable_cube=calculate_rams_pressure(filenames,**kwargs)
#        replace_cube=loadramscube(filenames,'U',**kwargs)
#        variable_cube=replacecoordinates(variable_cube,replace_cube)  
#
#    elif variable == 'pressure_ystag':    
#        variable_cube=calculate_rams_pressure(filenames,**kwargs)
#        replace_cube=loadramscube(filenames,'V',**kwargs)
#        variable_cube=replacecoordinates(variable_cube,replace_cube)  
#
#    elif variable == 'relative_humidity':    
#        variable_cube=calculate_rams_relativehumidity(filenames,**kwargs)
#        #variable_cube_out=addcoordinates(filenames, 'T',variable_cube,add_coordinates)
#    elif variable == 'w_at_T':    
#        variable_cube=calculate_rams_w_at_T(filenames,**kwargs)
#        replace_cube=loadramscube(filenames,'T',**kwargs)
#        variable_cube=replacecoordinates(variable_cube,replace_cube)        
#    elif variable == 'surface_precipitation':
#        variable_cube=calculate_rams_surface_precipitation(filenames,**kwargs)
#        #variable_cube_out=addcoordinates(filenames, 'T',variable_cube,add_coordinates)
#    elif variable == 'maximum reflectivity':    
#        variable_cube=calculate_rams_maximum_reflectivity(filenames,**kwargs)
#    else:
#        raise NameError(variable, 'is not a known variable') 
    return variable_cube