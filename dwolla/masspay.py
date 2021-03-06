'''
      _               _ _
   __| |_      _____ | | | __ _
  / _` \ \ /\ / / _ \| | |/ _` |
 | (_| |\ V  V / (_) | | | (_| |
  \__,_| \_/\_/ \___/|_|_|\__,_|

  An official requests based wrapper for the Dwolla API.

  This file contains functionality for all MassPay related endpoints.
'''

from . import constants as c
from .rest import r


def create(fundssource, items, **kwargs):
    """
    Creates a MassPay job. Must pass in an array of items.

    :param fundsSource: String of funding source for jobs.
    :param items: Dictionary with items of type frozenset
    :param params: Dictionary with optional parameters

    :**kwargs: Additional parameters for API or client control. 
    If a "params" key with Dictionary value is passed all other 
    params in **kwargs will be discarded and only the values 
    in params used.

    :return: None
    """
    if not fundssource:
        raise Exception('create() requires fundssource parameter')
    if not items:
        raise Exception('create() requires items parameter')

    p = {
        'oauth_token': kwargs.pop('alternate_token', c.access_token),
        'pin': kwargs.pop('alternate_pin', c.pin),
        'fundsSource': fundssource,
        'items': items
    }

    if 'params' in kwargs:
        p = dict(list(p.items()) + list(kwargs['params'].items()))
    elif kwargs:
        p = dict(list(p.items()) + list(kwargs.items()))

    return r._post('/masspay', p, dwollaparse=p.pop('dwollaparse', 'dwolla'))


def getjob(id, **kwargs):
    """
    Check the status of an existing MassPay job and
    returns additional information.

    :param id: String with MassPay job ID

    :param kwargs: Additional parameters for client control.

    :return: Dictionary with information about the job
    """
    if not id:
        raise Exception('getjob() requires id parameter')

    return r._get('/masspay/' + id, 
                    {
                        'oauth_token': kwargs.pop('alternate_token', c.access_token)
                    }, dwollaparse=kwargs.pop('dwollaparse', 'dwolla'))


def getjobitems(id, **kwargs):
    """
    Gets all items for a created MassPay job.

    :param id: String with MassPay job ID
    :param params: Dictionary with additional parameters.

    :**kwargs: Additional parameters for API or client control. 
    If a "params" key with Dictionary value is passed all other 
    params in **kwargs will be discarded and only the values 
    in params used.

    :return: Dictionary with job items
    """
    if not id:
        raise Exception('getjobitems() requires id parameter')

    p = {'oauth_token': kwargs.pop('alternate_token', c.access_token)}

    if 'params' in kwargs:
        p = dict(list(p.items()) + list(kwargs['params'].items()))
    elif kwargs:
        p = dict(list(p.items()) + list(kwargs.items()))

    return r._get('/masspay/' + id + '/items', p, dwollaparse=p.pop('dwollaparse', 'dwolla'))


def getitem(jobid, itemid, **kwargs):
    """
    Gets an item from a created MassPay job.

    :param jobid: String with MassPay job ID
    :param itemid: String with item ID.

    :param kwargs: Additional parameters for client control.

    :return: Dictionary with information about item from job.
    """
    if not jobid:
        raise Exception('getitem() requires jobid parameter')
    if not itemid:
        raise Exception('getitem() requires itemid parameter')

    return r._get('/masspay/' + jobid + '/items/' + itemid, 
                    {
                        'oauth_token': kwargs.pop('alternate_token', c.access_token)
                    }, dwollaparse=kwargs.pop('dwollaparse', 'dwolla'))


def listjobs(**kwargs):
    """
    Lists all MassPay jobs for the user
    under the current OAuth token.

    :**kwargs: Additional parameters for API or client control. 
    If a "params" key with Dictionary value is passed all other 
    params in **kwargs will be discarded and only the values 
    in params used.

    :return: Dictionary with MassPay jobs.
    """
    p = {'oauth_token': kwargs.pop('alternate_token', c.access_token)}

    if 'params' in kwargs:
        p = dict(list(p.items()) + list(kwargs['params'].items()))
    elif kwargs:
        p = dict(list(p.items()) + list(kwargs.items()))

    return r._get('/masspay', p, dwollaparse=p.pop('dwollaparse', 'dwolla'))
