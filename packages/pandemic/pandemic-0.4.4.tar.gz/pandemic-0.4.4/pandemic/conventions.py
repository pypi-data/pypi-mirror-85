from collections import OrderedDict
from copy import  deepcopy

#---------------------
#    State space
# --------------------

STATE_DESCRIPTIONS     = OrderedDict( {'v':'vulnerable',
                                       'i':'infected',
                                       's':'symptomatic',
                                       'p':'positive',
                                       'r':'recovered',
                                       'd':'deceased'} )

STATES    = list(STATE_DESCRIPTIONS.keys())
VULNERABLE, INFECTED, SYMPTOMATIC, POSITIVE, RECOVERED, DECEASED = 0, 1, 2, 3, 4, 5     # FIXME adopt from STATE_DESCRIPTIONS
HOME, WORK = 0, 1

#---------------------
#    Parameter space
# --------------------



MOTION_DESCRIPTIONS    = OrderedDict({'t':'Number of time steps in a day',
                                      'k':'Fractional distance moved towards attractor per day (kappa)',
                                      'w':'Standard deviation per day (brownian motion term)'
                                      })

GEOMETRY_DESCRIPTIONS  = OrderedDict({'n':'Population count',
                                      'i':'Number initially infected',
                                      'r':'Radius',
                                      'b':'Bound on size of the world',
                                      'h':'Size of household',
                                      'c':'Commuting fraction',
                                      's':'Spawl',
                                      'e':'Sprawl quadratic term',
                                      'p':'Precision of geoahashing'} )

HEALTH_DESCRIPTIONS    = OrderedDict({ 'vi':'Infection probability if exposed',
                                       'is':'Symptom rate if infected',
                                       'ip':'Randomized testing rate',
                                       'sp':'Symptomatic testing rate',
                                       'ir':'Asymptomatic recovery rate',
                                       'sr':'Symptomatic recovery rate',
                                       'sd':'Symptomatic death rate',
                                       'id':'Asymptomatic death rate',
                                       'pd':'Positive death rate',
                                       'pr':'Positive recovery rate'})  # All rates are per day.

DESCRIPTIONS = OrderedDict({'geometry':GEOMETRY_DESCRIPTIONS,
                             'motion':MOTION_DESCRIPTIONS,
                             'health':HEALTH_DESCRIPTIONS})
CATEGORIES = list(DESCRIPTIONS.keys())
GEOMETRY   = list(GEOMETRY_DESCRIPTIONS.keys())
MOTION     = list(MOTION_DESCRIPTIONS.keys())
HEALTH     = list(HEALTH_DESCRIPTIONS.keys())


def parameter_category(name):
    for c in CATEGORIES:
        if name in DESCRIPTIONS[c].keys():
            return c

NUM_STATES, NUM_GEOMETRY, NUM_MOTION, NUM_HEALTH  = len(STATE_DESCRIPTIONS), len(GEOMETRY_DESCRIPTIONS), len(MOTION), len(HEALTH)



#--------------------------------
#   Flat dict
# -------------------------------


def flatten(params):
    flat_params = OrderedDict()
    for parent in DESCRIPTIONS.keys():
        for c in params[parent].keys():
            flat_params[parent+'_'+c] = params[parent][c]
    return dict(flat_params)

def unflatten(flat_params):
    params = dict( [ (k,dict()) for k in DESCRIPTIONS.keys() ] )
    for ky,val in flat_params.items():
        parent, c = ky.split('_')[0],ky.split('_')[1]
        params[parent][c] = val
    return dict(params)



#--------------------------------
#   Map from parameters to R^n
# -------------------------------

# Canonical flattenning of parameters. Not required for simulation but may be useful for estimation, et cetera.

def params_to_vector(d:dict):  # FIXME: Broken ... should adopt ordering from DESCRIPTIONS
    g, m, c  = OrderedDict( zip(GEOMETRY,GEOMETRY) ), OrderedDict( zip(MOTION, MOTION)), OrderedDict( zip(HEALTH, HEALTH) )
    g.update(d['geometry'] )
    m.update(d['motion'])
    c.update(d['health'])
    values = list( g.values() ) + list( m.values() ) + list( c.values() )
    return [ float(v) for v in values ]   # Just checking

def vector_to_params(v):
    return {'geometry':dict(zip(GEOMETRY,v[:NUM_GEOMETRY])),
            'motion':dict(zip(MOTION,v[NUM_GEOMETRY:NUM_GEOMETRY+NUM_MOTION])),
            'health':dict(zip(HEALTH, v[-NUM_STATES * NUM_STATES:]))
           }

