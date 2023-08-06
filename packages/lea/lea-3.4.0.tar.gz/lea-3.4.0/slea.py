'''
--------------------------------------------------------------------------------

    slea.py

--------------------------------------------------------------------------------
Copyright 2013-2020 Pierre Denis

This file is part of Lea.

Lea is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lea is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with Lea.  If not, see <http://www.gnu.org/licenses/>.
--------------------------------------------------------------------------------
'''

from .lea import Lea
from .alea import Alea
from .toolbox import dict, defaultdict

class Slea(Lea):
    
    '''
    Slea is a Lea subclass, which instance represents a conditional probability
    table (CPT) giving a Lea instance C and a function associating each
    possible value of C to a specific Lea instance.
    A Slea instance is similar to a "table pex", as defined in the paper on
    Statues algorithm (see http://arxiv.org/abs/1806.09997), if we replace
    the explicit CPT lookup table by a function. 
    '''

    __slots__ = ('_lea_c','_f')

    def __init__(self,lea_c,f):
        Lea.__init__(self)
        self._lea_c = Alea.coerce(lea_c)
        self._f = f

    def _get_lea_children(self):
        return (self._lea_c,)

    def _clone_by_type(self,clone_table):
        return Slea(self._lea_c._clone(clone_table),self._f)

    def _gen_vp(self):
        f = self._f
        for (vc,pc) in self._lea_c.gen_vp():
            lea_v = Alea.coerce(f(vc))
            if not isinstance(lea_v,Alea):
                raise Lea.Error("the function passed to switch_func shall return Alea instances only, e.g. lea.pmf(...) or lea.vals(...)")
            for (vd,pd) in lea_v._gen_vp():
                yield (vd,pc*pd)

    def _gen_one_random_mc(self):
        f = self._f
        for vc in self._lea_c.gen_one_random_mc():
            lea_v = Alea.coerce(f(vc))
            if not isinstance(lea_v,Alea):
                raise Lea.Error("the function passed to switch_func shall return Alea instances only, e.g. lea.pmf(...) or lea.vals(...)")
            for vd in lea_v.gen_one_random_mc():
                yield vd

    def _em_step(self,model_lea,cond_lea,obs_pmf_tuple,conversion_dict):
        return Slea(self._lea_c.em_step(model_lea,cond_lea,obs_pmf_tuple,conversion_dict),self._f)

