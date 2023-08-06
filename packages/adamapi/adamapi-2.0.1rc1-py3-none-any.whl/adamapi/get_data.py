"""
Copyright (c) 2020 MEEO s.r.l.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from datetime import timedelta, datetime, timezone
import os
from osgeo import ogr
import imageio
import json
import requests
import errno
import csv

import logging
logger=logging.getLogger('adamapi')

from . import AdamApiError

class GetData(object):
    def __init__(self,client):
        self.LOG=logger
        self.client=client

    def getData(self, datasetId, productId, outputFname=None ):
        """
        Method to retrive original tif data
        @datasetId datasetId, required
        @productid productId, required
        @outputFname
        """
        if outputFname is None:
            fname = productId
        else:
            fname = outputFname

        errorResponse=None
        params = {}
        url = os.path.join("apis","v2","opensearch",datasetId.split(":",1)[0],"records/",productId+"/","download")
        try:
            response=self.client.client(url,params,"GET", force_raise = True )
            self._checkDirFile(fname)
            with open( fname+".tif", 'wb' ) as f:
                f.write( response.content )
        except requests.exceptions.HTTPError as er:
            errorResponse=er
            self.LOG.error(er.response.json()['message'])
            raise AdamApiError( errorResponse.response.json()['title'])

        return fname

    def _checkDirFile(self,filename):
        dirname = os.path.dirname( filename )
        if dirname.strip():
            try:
                os.makedirs( dirname )
            except OSError as ose:
                if ose.errno!=errno.EEXIST:
                    raise AdamApiError( ose )
