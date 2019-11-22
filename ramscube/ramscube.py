import warnings
warnings.filterwarnings('ignore', category=UserWarning, append=True)

RAMS_Units=dict()
# winds
RAMS_Units['UC']='m s-1'
RAMS_Units['VC']='m s-1'
RAMS_Units['WC']='m s-1'
# potential temperature
RAMS_Units['THETA']='K'
RAMS_Units['PI']='J kg-1 K-1'
RAMS_Units['DN0']='kg m-3'

# water vapour mixing ratio:
RAMS_Units['RV']='kg kg-1'

# hydrometeor mass mixing ratios:
mass_mixing_ratios=['RCP','RDP','RRP','RPP','RSP','RAP','RGP','RHP']
for variable in mass_mixing_ratios:
    RAMS_Units[variable]='kg kg-1'

# hydrometeor number mixing ratios:
mass_mixing_ratios=['CCP','CDP','CRP','CPP','CSP','CAP','CGP','CHP']
for variable in mass_mixing_ratios:
    RAMS_Units[variable]='kg-1'

#hydrometeor precipitation rates:
precipitation_rates=['PCPRR','PCPRD','PCPRS','PCPRH','PCPRP','PCPRA','PCPRG']
for variable in precipitation_rates:
    RAMS_Units[variable]='kg m-2'
    
# hydrometeor precipitation accumulated:
precipitation_accumulated=['ACCPR','ACCPD','ACCPS','ACCPH','ACCPP','ACCPA','ACCPG']
for variable in precipitation_accumulated:
    RAMS_Units[variable]='kg m-2 s-1'

# radiation:
RAMS_Units['LWUP']='W m-2'
RAMS_Units['LWDN']='W m-2'
RAMS_Units['SWUP']='W m-2'
RAMS_Units['SWDN']='W m-2'

# individual microphysics processes accumulated
RAMS_processes_mass=[
'NUCCLDRT',
'NUCICERT',
'INUCHOMRT',
'INUCCONTR',
'INUCIFNRT',
'INUCHAZRT',
'VAPCLDT',
'VAPRAINT',
'VAPPRIST',
'VAPSNOWT',
'VAPAGGRT',
'VAPGRAUT',
'VAPHAILT',
'VAPDRIZT',
'MELTSNOWT',
'MELTAGGRT',
'MELTGRAUT',
'MELTHAILT',
'RIMECLDSNOWT',
'RIMECLDAGGRT',
'RIMECLDGRAUT',
'RIMECLDHAILT',
'RAIN2PRT',
'RAIN2SNT',
'RAIN2AGT',
'RAIN2GRT',
'RAIN2HAT',
'AGGRSELFPRIST',
'AGGRSELFSNOWT',
'AGGRPRISSNOWT'
]

for variable in RAMS_processes_mass:
    RAMS_Units[variable]='kg kg-1'

# grouped microphysics processes accumulated:
RAMS_processes_mass_grouped=[
'VAPLIQT',
'VAPICET',
'MELTICET',
'CLD2RAINT',
'RIMECLDT',
'RAIN2ICET',
'ICE2RAINT',
'AGGREGATET'	
]
for variable in RAMS_processes_mass_grouped:
    RAMS_Units[variable]='kg kg-1'

# grouped microphysics processes instantaneous:
RAMS_processes_mass_grouped_instantaneous=[
'VAPLIQ',
'VAPICE',
'MELTICE',
'CLD2RAIN',
'RIMECLD',
'RAIN2ICE',
'ICE2RAIN',
'NUCCLDR',
'NUCICER'
]
for variable in RAMS_processes_mass_grouped_instantaneous:
    RAMS_Units[variable]='kg kg-1 s-1'


RAMS_standard_name=dict()

variable_list_derive=[
        'air_temperature',
        'air_pressure',
        'temperature',
        'air_density',
        'OLR',
        'LWC',
        'IWC',
        'LWP',
        'IWP',
        'IWV',
        'airmass',
        'airmass_path',
        'surface_precipitation',
        'surface_precipitation_average',
        'surface_precipitation_accumulated',
        'surface_precipitation_instantaneous',
        'LWup_TOA',
        'LWup_sfc',
        'LWdn_TOA',
        'LWdn_sfc',
        'SWup_TOA',
        'SWup_sfc',
        'SWdn_TOA',
        'SWdn_sfc'  
        ]

def variable_list(filenames):
    from iris import load
    cubelist=load(filenames[0])
    variable_list = [cube.name() for cube in cubelist]
    return variable_list

def load(filenames,variable,mode='auto',**kwargs):
    if variable in variable_list_derive:
        variable_cube=deriveramscube(filenames,variable,**kwargs)
    else:
        variable_cube=loadramscube(filenames,variable,**kwargs)

    # if mode=='auto':
    #     variable_list_file=variable_list(filenames)
    #     if variable in variable_list_file:
    #         variable_cube=loadramscube(filenames,variable,**kwargs)
    #     elif variable in variable_list_derive:
    #         variable_cube=deriveramscube(filenames,variable,**kwargs)
    #     elif variable in variable_dict_pseudonym.keys():
    #         variable_load=variable_dict_pseudonym[variable]
    #         variable_cube=loadramscube(filenames,variable_load,**kwargs)
    #     else:
    #         raise SystemExit('variable not found')

    # elif mode=='file':
    #     variable_list_file=variable_list(filenames)
    #     if variable in variable_list_file:
    #         variable_cube=loadramscube(filenames,variable,**kwargs)
            
    # elif mode=='derive':
    #     variable_cube=deriveramscube(filenames,variable,**kwargs)
    # elif mode=='pseudonym':
    #     variable_load=variable_dict_pseudonym[variable]
    #     variable_cube=loadramscube(filenames,variable_load,**kwargs)
    # else:
    #     print("mode=",mode)
    #     raise SystemExit('unknown mode')

    return variable_cube



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

    filename_header=filename[:-5]+'head.txt'
    domain=filename[-4]

    variable_dict, coord_dict=readramsheader(filename_header)
    variable_cube=add_dim_coordinates(filename, variable,variable_cube,variable_dict, coord_dict,domain,**kwargs)
    variable_cube=add_aux_coordinates(filename, variable,variable_cube,variable_dict, coord_dict,domain,**kwargs)
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

def make_model_level_number_coordinate(n_level):
    from iris import coords
    from numpy import arange
    MODEL_LEVEL_NUMBER=arange(0,n_level)
    model_level_number=coords.AuxCoord(MODEL_LEVEL_NUMBER, standard_name='model_level_number', units='1')
    return model_level_number          


def add_dim_coordinates(filename, variable,variable_cube,variable_dict, coord_dict,domain,add_coordinates=None):        
    from iris import coords
    import numpy as np
   
        #    from iris import coord_systems

#    coord_system=coord_systems.LambertConformal(central_lat=MOAD_CEN_LAT, central_lon=CEN_LON, false_easting=0.0, false_northing=0.0, secant_latitudes=(TRUELAT1, TRUELAT2))
    coord_system=None
    if (variable_dict[variable]==3):
        time_coord=make_time_coord(coord_dict)
        variable_cube.add_aux_coord(time_coord)
        z_coord=coords.DimCoord(coord_dict['ztn01'], standard_name='geopotential_height', long_name='z', var_name='z', units='m', bounds=None, attributes=None, coord_system=coord_system)
        variable_cube.add_dim_coord(z_coord,0)
        model_level_number_coord=make_model_level_number_coordinate(len(z_coord.points))
        variable_cube.add_aux_coord(model_level_number_coord,0)
        x_coord=coords.DimCoord(np.arange(len(coord_dict['xtn0'+domain])), long_name='x', units='1', bounds=None, attributes=None, coord_system=coord_system)
        variable_cube.add_dim_coord(x_coord,2)
        y_coord=coords.DimCoord(np.arange(len(coord_dict['ytn0'+domain])), long_name='y', units='1', bounds=None, attributes=None, coord_system=coord_system)
        variable_cube.add_dim_coord(y_coord,1)
        projection_x_coord=coords.DimCoord(coord_dict['xtn0'+domain], standard_name='projection_x_coordinate', long_name='x', var_name='x', units='m', bounds=None, attributes=None, coord_system=coord_system)
        variable_cube.add_aux_coord(projection_x_coord,(2))
        projection_y_coord=coords.DimCoord(coord_dict['ytn0'+domain], standard_name='projection_y_coordinate', long_name='y', var_name='y', units='m', bounds=None, attributes=None, coord_system=coord_system)
        variable_cube.add_aux_coord(projection_y_coord,(1))



    elif (variable_dict[variable]==2):
        x_coord=coords.DimCoord(np.arange(len(coord_dict['xtn0'+domain])), long_name='x', units='1', bounds=None, attributes=None, coord_system=coord_system)
        variable_cube.add_dim_coord(x_coord,1)
        y_coord=coords.DimCoord(np.arange(len(coord_dict['ytn0'+domain])), long_name='y', units='1', bounds=None, attributes=None, coord_system=coord_system)
        variable_cube.add_dim_coord(y_coord,0)
        projection_x_coord=coords.DimCoord(coord_dict['xtn0'+domain], standard_name='projection_x_coordinate', long_name='x', var_name='x', units='m', bounds=None, attributes=None, coord_system=coord_system)
        variable_cube.add_aux_coord(projection_x_coord,(1))
        projection_y_coord=coords.DimCoord(coord_dict['ytn0'+domain], standard_name='projection_y_coordinate', long_name='y', var_name='y', units='m', bounds=None, attributes=None, coord_system=coord_system)
        variable_cube.add_aux_coord(projection_y_coord,(0))
        time_coord=make_time_coord(coord_dict)
        variable_cube.add_aux_coord(time_coord)
    return variable_cube


def add_aux_coordinates(filename,variable,variable_cube,variable_dict, coord_dict,domain,**kwargs):
    from iris import load_cube,coords
    coord_system=None


    latitude=load_cube(filename,'GLAT').core_data()
    longitude=load_cube(filename,'GLON').core_data()
    lat_coord=coords.AuxCoord(latitude, standard_name='latitude', long_name='latitude', var_name='latitude', units='degrees', bounds=None, attributes=None, coord_system=coord_system)
    lon_coord=coords.AuxCoord(longitude, standard_name='longitude', long_name='longitude', var_name='longitude', units='degrees', bounds=None, attributes=None, coord_system=coord_system)

    if (variable_dict[variable]==3):                
         variable_cube.add_aux_coord(lon_coord,(1,2))
         variable_cube.add_aux_coord(lat_coord,(1,2))
    elif (variable_dict[variable]==2):
            variable_cube.add_aux_coord(lon_coord,(0,1))                
            variable_cube.add_aux_coord(lat_coord,(0,1))

    # add_coordinates=kwargs.pop('add_coordinates')
    # if type(add_coordinates)!=list:
    #     add_coordinates1=add_coordinates
    #     add_coordinates=[]
    #     add_coordinates.append(add_coordinates1)
    # for coordinate in add_coordinates:
    #     if coordinate=='latlon': 
    #         latitude=load_cube(filename,'GLAT').data
    #         longitude=load_cube(filename,'GLON').data
    #         lat_coord=coords.AuxCoord(latitude, standard_name='latitude', long_name='latitude', var_name='latitude', units='degrees', bounds=None, attributes=None, coord_system=coord_system)
    #         lon_coord=coords.AuxCoord(longitude, standard_name='longitude', long_name='longitude', var_name='longitude', units='degrees', bounds=None, attributes=None, coord_system=coord_system)

    #         if (variable_dict[variable]==3):                
    #             variable_cube.add_aux_coord(lon_coord,(1,2))
    #             variable_cube.add_aux_coord(lat_coord,(1,2))
    #         elif (variable_dict[variable]==2):
    #             variable_cube.add_aux_coord(lon_coord,(0,1))                
    #             variable_cube.add_aux_coord(lat_coord,(0,1))

    return variable_cube

def calculate_rams_LWC(filenames,**kwargs):
    RCP=loadramscube(filenames, 'RCP',**kwargs)
    RDP=loadramscube(filenames, 'RDP',**kwargs)
    RRP=loadramscube(filenames, 'RRP',**kwargs)
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
    from iris.coords import AuxCoord
    from numpy import diff
    rho=loadramscube(filenames,'DN0',**kwargs)
    z=rho.coord('geopotential_height')    
    z_dim=rho.coord_dims('geopotential_height')
    z_diff=AuxCoord(mydiff(z.points),var_name='z_diff')
    rho.add_aux_coord(z_diff,data_dims=z_dim)
    dx=diff(rho.coord('projection_x_coordinate').points[0:2])
    dy=diff(rho.coord('projection_y_coordinate').points[0:2])
    Airmass=rho*rho.coord('z_diff')*dx*dy
    Airmass.remove_coord('z_diff')
    Airmass.rename('mass_of_air')
    Airmass.units='kg'
    return Airmass

def calculate_rams_airmass_path(filenames,**kwargs):
    from iris.coords import AuxCoord
    rho=loadramscube(filenames,'DN0',**kwargs)
    z=rho.coord('geopotential_height')    
    z_dim=rho.coord_dims('geopotential_height')
    z_diff=AuxCoord(mydiff(z.points),var_name='z_diff')
    rho.add_aux_coord(z_diff,data_dims=z_dim)    
    Airmass=rho*rho.coord('z_diff') 
    Airmass.remove_coord('z_diff')
    Airmass.rename('airmass_path')
    Airmass.units='kg m-2'
    return Airmass



def calculate_rams_air_temperature(filenames,**kwargs):
    from iris.coords import AuxCoord
    theta=loadramscube(filenames,'THETA',**kwargs)
    pi=loadramscube(filenames,'PI',**kwargs)
    cp=AuxCoord(1004,long_name='cp',units='J kg-1 K-1')
    t=theta*pi/cp
    t.rename('air_temperature')
    return t

def calculate_rams_air_pressure(filenames,**kwargs):
    from iris.coords import AuxCoord
    pi=loadramscube(filenames,'PI',**kwargs)
    cp=AuxCoord(1004,long_name='cp',units='J kg-1 K-1')
    rd=AuxCoord(287,long_name='rd',units='J kg-1 K-1')
    p = 100000 * (pi/cp)**(cp.points/rd.points) # Pressure in Pa
    p.rename('air_pressure')
    p.units='Pa'
    return p

def calculate_rams_density(filenames,**kwargs):
    rho=loadramscube(filenames,'DN0',**kwargs)
    rho.rename('air_density')
    rho.units='kg m-3'
    return rho
        
def calculate_rams_LWP(filenames,**kwargs):
    from iris.analysis import SUM
    LWC=deriveramscube(filenames,'LWC',**kwargs)
    Airmass=deriveramscube(filenames,'airmass_path',**kwargs)
    LWP=(LWC*Airmass).collapsed(('geopotential_height'),SUM)
    LWP.rename('liquid water path')
    #LWP.rename('atmosphere_mass_content_of_cloud_liquid_water')
    return LWP   
#    
def calculate_rams_IWP(filenames,**kwargs):    
    from iris.analysis import SUM
    IWC=deriveramscube(filenames,'IWC',**kwargs)
    Airmass=deriveramscube(filenames,'airmass_path',**kwargs)
    IWP=(IWC*Airmass).collapsed(('geopotential_height'),SUM)
    IWP.rename('ice water path')
    #IWP.rename('atmosphere_mass_content_of_cloud_ice_water')
    return IWP

def calculate_rams_IWV(filenames,**kwargs):    
    from iris.analysis import SUM
    RV=loadramscube(filenames,'RV',**kwargs)
    Airmass=deriveramscube(filenames,'airmass_path',**kwargs)
    IWV=(RV*Airmass).collapsed(('geopotential_height'),SUM)
    IWV.rename('integrated water vapor')
    #IWP.rename('atmosphere_mass_content_of_cloud_ice_water')
    return IWV

# Radiation fluxed at the top of the atmospere and at the surface
def calculate_rams_LWup_TOA(filenames,**kwargs):
    from iris import Constraint
    LWUP=loadramscube(filenames,'LWUP',**kwargs)
    LWup_TOA=LWUP.extract(Constraint(model_level_number=LWUP.coord('model_level_number').points[-1]))
    LWup_TOA.rename('LWup_TOA')
    return LWup_TOA

def calculate_rams_LWup_sfc(filenames,**kwargs):
    from iris import Constraint
    LWUP=loadramscube(filenames,'LWUP',**kwargs)
    LWup_sfc=LWUP.extract(Constraint(model_level_number=0))
    LWup_sfc.rename('LWup_sfc')
    return LWup_sfc

def calculate_rams_LWdn_TOA(filenames,**kwargs):
    from iris import Constraint
    LWDN=loadramscube(filenames,'LWDN',**kwargs)
    LWdn_TOA=LWDN.extract(Constraint(model_level_number=LWDN.coord('model_level_number').points[-1]))
    LWdn_TOA.rename('LWdn_TOA')
    return LWdn_TOA

def calculate_rams_LWdn_sfc(filenames,**kwargs):
    from iris import Constraint
    LWDN=loadramscube(filenames,'LWDN',**kwargs)
    LWdn_sfc=LWDN.extract(Constraint(model_level_number=0))
    LWdn_sfc.rename('LWdn_sfc')
    return LWdn_sfc

def calculate_rams_SWup_TOA(filenames,**kwargs):
    from iris import Constraint
    SWUP=loadramscube(filenames,'SWUP',**kwargs)
    SWup_TOA=SWUP.extract(Constraint(model_level_number=SWUP.coord('model_level_number').points[-1]))
    SWup_TOA.rename('SWup_TOA')
    return SWup_TOA

def calculate_rams_SWup_sfc(filenames,**kwargs):
    from iris import Constraint
    SWUP=loadramscube(filenames,'SWUP',**kwargs)
    SWup_sfc=SWUP.extract(Constraint(model_level_number=0))
    SWup_sfc.rename('SWup_sfc')
    return SWup_sfc

def calculate_rams_SWdn_TOA(filenames,**kwargs):
    from iris import Constraint
    SWDN=loadramscube(filenames,'SWDN',**kwargs)
    SWdn_TOA=SWDN.extract(Constraint(model_level_number=SWDN.coord('model_level_number').points[-1]))
    SWdn_TOA.rename('SWdn_TOA')
    return SWdn_TOA

def calculate_rams_SWdn_sfc(filenames,**kwargs):
    from iris import Constraint
    SWDN=loadramscube(filenames,'SWDN',**kwargs)
    SWdn_sfc=SWDN.extract(Constraint(model_level_number=0))
    SWdn_sfc.rename('SWdn_sfc')
    return SWdn_sfc







def calculate_rams_surface_precipitation_instantaneous(filenames,**kwargs):
    PCPRR=loadramscube(filenames,'PCPRR',**kwargs)    
    PCPRD=loadramscube(filenames,'PCPRD',**kwargs)
    PCPRS=loadramscube(filenames,'PCPRS',**kwargs)
    PCPRP=loadramscube(filenames,'PCPRP',**kwargs)
    PCPRA=loadramscube(filenames,'PCPRA',**kwargs)
    PCPRH=loadramscube(filenames,'PCPRH',**kwargs)
    PCPRG=loadramscube(filenames,'PCPRG',**kwargs)
    
    surface_precip=PCPRR+PCPRD+PCPRS+PCPRP+PCPRA+PCPRG+PCPRH
    surface_precip.rename('surface_precipitation_instantaneous')
    return surface_precip

def calculate_rams_surface_precipitation_accumulated(filenames,**kwargs):
    ACCPR=loadramscube(filenames,'ACCPR',**kwargs)    
    ACCPD=loadramscube(filenames,'ACCPD',**kwargs)
    ACCPS=loadramscube(filenames,'ACCPS',**kwargs)
    ACCPP=loadramscube(filenames,'ACCPP',**kwargs)
    ACCPA=loadramscube(filenames,'ACCPA',**kwargs)
    ACCPH=loadramscube(filenames,'ACCPH',**kwargs)
    ACCPG=loadramscube(filenames,'ACCPG',**kwargs)
    
    surface_precip_acc=ACCPR+ACCPD+ACCPS+ACCPP+ACCPA+ACCPG+ACCPH

    surface_precip_acc.rename('surface_precipitation_accumulated')
    #IWP.rename('atmosphere_mass_content_of_cloud_ice_water')
    return surface_precip_acc

def calculate_rams_surface_precipitation_average(filenames,**kwargs):
    from dask.array import concatenate
    surface_precip_accum=calculate_rams_surface_precipitation_accumulated(filenames,**kwargs)
    #caclulate timestep in hours
    time_coord=surface_precip_accum.coord('time')
    dt=(time_coord.units.num2date(time_coord.points[1])-time_coord.units.num2date(time_coord.points[0])).total_seconds()/3600.
    #divide difference in precip between timesteps (in mm/h) by timestep (in h):
    surface_precip=surface_precip_accum
    surface_precip.data=concatenate((0*surface_precip.core_data()[[1],:,:],surface_precip.core_data()[1:,:,:]-surface_precip.core_data()[:-1:,:,:]),axis=0)/dt
    surface_precip.rename('surface_precipitation_average')
    surface_precip.units= 'mm/h'
    return surface_precip

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
    elif variable == 'air_temperature':    
        variable_cube=calculate_rams_air_temperature(filenames,**kwargs)
    elif variable=='air_pressure':
        variable_cube=calculate_rams_air_pressure(filenames,**kwargs)
    elif variable == 'air_density':    
        variable_cube=calculate_rams_density(filenames,**kwargs)
    elif variable == 'airmass_path':    
        variable_cube=calculate_rams_airmass_path(filenames,**kwargs)
    elif variable == 'surface_precipitation_average':
        variable_cube=calculate_rams_surface_precipitation_average(filenames,**kwargs)
    elif variable == 'surface_precipitation_accumulated':
        variable_cube=calculate_rams_surface_precipitation_accumulated(filenames,**kwargs)
    elif (variable == 'surface_precipitation_instantaneous') or (variable == 'surface_precipitation'):
        variable_cube=calculate_rams_surface_precipitation_instantaneous(filenames,**kwargs)
    elif (variable == 'LWup_TOA'):
        variable_cube=calculate_rams_LWup_TOA(filenames,**kwargs)
    elif (variable == 'LWup_sfc'):
        variable_cube=calculate_rams_LWup_sfc(filenames,**kwargs)
    elif (variable == 'LWdn_TOA'):
        variable_cube=calculate_rams_LWdn_TOA(filenames,**kwargs)
    elif (variable == 'LWdn_sfc'):
        variable_cube=calculate_rams_LWdn_sfc(filenames,**kwargs)
    elif (variable == 'SWup_TOA'):
        variable_cube=calculate_rams_SWup_TOA(filenames,**kwargs)
    elif (variable == 'SWup_sfc'):
        variable_cube=calculate_rams_SWup_sfc(filenames,**kwargs)
    elif (variable == 'SWdn_TOA'):
        variable_cube=calculate_rams_SWdn_TOA(filenames,**kwargs)
    elif (variable == 'SWdn_sfc'):
        variable_cube=calculate_rams_SWdn_sfc(filenames,**kwargs)

    else:
        raise NameError(variable, 'is not a known variable') 
    return variable_cube
