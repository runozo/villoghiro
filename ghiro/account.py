#!/usr/bin/env python
#
# Copyright 2007 Ghiro.
#
# This software VilloGhiro is licensed under the GNU GPL License;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.gnu.org/licenses/gpl.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Classess related to the management of the game account datas"""
class Village:
    """Base class to store the villages datas"""
    def __init__(self, name,dorfId,stockStuff={},prodStuff={},destDorfId=None,browser=None,parser=None):
        self.dorfId = dorfId
        self.name = name
        self.dorfId = dorfId
        self.stock = stockStuff
        self.production = prodStuff
        self.scrocco = destDorfId
        self.marketId = ''
        self.browser = browser
        self.parser = parser
        self.x = None
        self.y = None
class Stuffs:
    """Base class to store the amount of stuffs"""
    def __init__(self,legno,argilla,ferro,grano):
        self.legno = legno
        self.argilla = argilla
        self.ferro = ferro
        self.grano = grano
