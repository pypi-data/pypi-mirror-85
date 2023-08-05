# -*- coding: utf-8 -*-

# Copyright 2015 Fanficdownloader team, 2018 FanFicFare team
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import absolute_import

try: # just a way to switch between CLI and PI
    import calibre.constants
except:
    import sys
    if sys.version_info >= (2, 7):
        import logging
        logger = logging.getLogger(__name__)
        loghandler=logging.StreamHandler()
        loghandler.setFormatter(logging.Formatter("FFF: %(levelname)s: %(asctime)s: %(filename)s(%(lineno)d): %(message)s"))
        logger.addHandler(loghandler)
        loghandler.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
