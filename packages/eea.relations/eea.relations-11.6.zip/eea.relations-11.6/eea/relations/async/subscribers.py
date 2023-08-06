""" Subscribers
"""
import os
import logging
from plone.app.async.subscribers import set_quota
logger = logging.getLogger('eea.relations')


def getMaximumThreads(queue):
    """ Get the maximum threads per queue
    """
    size = 0
    for da in queue.dispatchers.values():
        if not da.activated:
            continue
        for _agent in da.values():
            size += 3
    return size or 1


def configureQueue(event):
    """ Configure zc.async queue for rdf async jobs
    """
    queue = event.object

    try:
        size = int(os.environ.get(
            'EEARELATIONS_ASYNC_THREADS', getMaximumThreads(queue)))
    except Exception, err:
        logger.exception(err)
        size = 1

    set_quota(queue, 'relations', size=size)
    logger.info("quota 'relations' with size %r configured in queue %r.",
                size, queue.name)
