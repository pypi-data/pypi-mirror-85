#    This script is part of pymaid (http://www.github.com/schlegelp/pymaid).
#    Copyright (C) 2017 Philipp Schlegel
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

import logging
import math
import pandas as pd

from . import utils, tiles, config

__all__ = sorted(['test_connection', 'test_internet_speed'])

logger = logging.getLogger(__name__)


def test_connection(remote_instance=None, stack_id=5, verbose=True):
    """Benchmark connection to CATMAID server.

    Parameters
    ----------
    remote_instance :   CatmaidInstance, optional
                        If not passed directly, will try using global.
    stack_id :          int
                        ID of image stack to test.
    verbose :           bool, optional

    Returns
    -------
    benchmark :         pandas.DataFrame

    """
    config.logger.setLevel('WARNING')

    remote_instance = utils._eval_remote_instance(remote_instance)

    if verbose:
        logger.setLevel('INFO')
    else:
        logger.setLevel('WARNING')

    res = pd.Series()

    res['DownloadSpeed [Mbit/s]'], res['UploadSpeed [Mbit/s]'] = test_internet_speed()

    stacks = remote_instance.image_stacks
    if stack_id not in stacks.index.values:
        raise ValueError('Stack ID {} not found in stacks:\n{}'.format(stack_id,
                                                                       stacks))
    res['stack'] = stacks.loc[stack_id]


def test_image_mirror(remote_instance):
    """Test image mirror."""
    # Test server response times
    logger.info("Testing image mirrors' base response times...")

    for m in res['stack']['mirrors']:
        m['response_time'] = tiles.test_response_time(m['image_base'],
                                                      calls=2)
        logger.info('Mirror {} ({}): {:.2f} s'.format(m['title'],
                                                      m['image_base'],
                                                      m['response_time']))

    mirror = sorted(res['stack']['mirrors'],
                    key=lambda x: x['response_time'],
                    reverse=False)

    logger.info('Testing with fastest image mirror: {}'.format(mirror['title']))

    # Get stack center
    stack_center = [int(res['stack']['dimension']['x'] / 2),
                    int(res['stack']['dimension']['y'] / 2),
                    int(res['stack']['dimension']['z'] / 2)]

    # Define field of views
    for px in [1e6, 10e6, 100e6]:
        width = int(math.sqrt(px))
        bbox = tiles._bbox_helper(stack_center, width)

        job = tiles.TileLoader(bbox, stack_id, image_mirror=mirror['id'],
                               zoom_level=0, coords='PIXEL')


def test_internet_speed():
    """Test internet speed."""
    # If speedtest-cli is installed benchmark the internet connection
    try:
        import speedtest
        s = speedtest.Speedtest()
        s.get_servers([])
        s.get_best_server()
        logger.info('Testing download speed...')
        s.download(threads=None)
        logger.info('Testing upload speed...')
        s.upload(threads=None)
        dl = s.results.dict()['download'] / 1e6
        ul = s.results.dict()['upload'] / 1e6
        logger.info('Download: {} Mbit/s | Upload: Mbit/s {}'.format(dl,
                                                                     ul))
        return dl, ul
    except ImportError:
        pass
        print('To check the performance of your internet connection install '
              'speedtest-cli: pip3 install speedtest-cli')
        return 'NA', 'NA'
    except BaseException:
        raise
