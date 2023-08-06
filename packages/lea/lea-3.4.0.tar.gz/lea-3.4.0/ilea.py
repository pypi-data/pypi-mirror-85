'''
--------------------------------------------------------------------------------

    ilea.py

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

from .lea import Lea, Alea
from .evidence_ctx import EvidenceCtx

from operator import and_


class Ilea(Lea):
    
    '''
    Ilea is a Lea subclass, which instance represents a probability distribution obtained
    by filtering the values Vi of a given Lea instance that verify a boolean condition C,
    which is the AND of given boolean conditions Cj(Vi).
    Beside the conditions carried by each Ilea instance, global conditions enforced by all
    Ilea instances can be specified by means of "evidence contexts" (see EvidenceCtx class).
    If used to define a conditional probability table (CPT), each Ilea instance represents
    a given distribution <Vi,p(Vi|C)>, assuming that a given condition C is verified (see
    Blea class).
    An Ilea instance is a "conditional pex", as defined in the paper on Statues algorithm
    (see http://arxiv.org/abs/1806.09997).
    '''

    __slots__ = ('_lea1','_cond_leas')

    def __init__(self,lea1,cond_leas):
        Lea.__init__(self)
        self._lea1 = lea1
        self._cond_leas = tuple(cond_leas)

    def _get_lea_children(self):
        return (self._lea1,) + self._get_cond_leas()
    
    def _clone_by_type(self,clone_table):
        return Ilea(self._lea1._clone(clone_table),
                    (cond_lea._clone(clone_table) for cond_lea in self._get_cond_leas()))

    def _get_cond_leas(self):
        return EvidenceCtx.get_active_conditions() + self._cond_leas

    @staticmethod
    def _gen_true_p(cond_leas):
        ''' generates probabilities of True for ANDing the given conditions 
            this uses short-circuit evaluation
        '''
        if len(cond_leas) == 0:
            # empty condition: evaluated as True (seed of recursion)
            yield 1
        else:
            tail_cond_leas = cond_leas[1:]
            for (cv0,p0) in cond_leas[0].gen_vp():
                if cv0 == True:
                    # the first condition is true, for some binding of variables
                    for p1 in Ilea._gen_true_p(tail_cond_leas):
                        # the full condition is true, for some binding of variables
                        yield p0*p1
                elif cv0 == False:
                    # short-circuit: do not go further since the AND is false
                    pass
                else:
                    # neither True, nor False -> error
                    raise Lea.Error("boolean expression expected")
    
    def _gen_vp(self):
        for cp in Ilea._gen_true_p(self._get_cond_leas()):
            # the AND of conditions is true, for some binding of variables
            # yield value-probability pairs of _lea1, given this binding
            for (v,p) in self._lea1.gen_vp():
                yield (v,cp*p)

    def _gen_vp_mclw(self,nb_subsamples,exact_vars_lea,nb_tries=None):
        ''' generates tuples (v,p) where v is a value of the current probability distribution
            and p is the associated probability weight; this implements the MCLW algorithm
            (Monte-Carlo Likelihood Weighting): exact inference on the conditon,
            then, for each binding found, nb_subsamples random samples for remaining unbound
            variables; nb_tries, if not None, defines the maximum number of trials in case a random
            value is incompatible with a condition; this happens only if the conditioned part
            is itself an Ilea instance x.given(e) or is referring to such instance;
            the exact_vars_lea argument may refer to other variables, which shall be used in the
            exact evaluation, beyond these already referred in the condition (see Lea.calc)
        '''
        for p0 in Ilea._gen_true_p(self._get_cond_leas()):
            # the AND of conditions is true, for some binding of variables
            # perform random sampling on _lea1, given this binding and
            # yield value-probability pairs with the probability of the binding
            for (_,p1) in exact_vars_lea.gen_vp():
                for v in self._lea1.gen_random_mc(nb_samples=nb_subsamples,nb_tries=nb_tries):
                    yield (v,p0*p1)

    def _gen_one_random_true_cond(self,cond_leas,with_exception):
        if len(cond_leas) == 0:
            # empty condition: evaluated as True (seed of recursion)
            yield None
        else:
            for cv in cond_leas[0].gen_one_random_mc():
                if cv == True:
                    for v in self._gen_one_random_true_cond(cond_leas[1:],with_exception):
                        yield v
                elif cv == False:
                    if with_exception:
                        raise Lea._FailedRandomMC()
                    yield self
                else:
                    raise Lea.Error("boolean expression expected")

    def gen_one_random_mc(self,nb_subsamples=1):
        if self._val is not self:
            # distribution already bound to a value, because gen_one_random_mc has been called already on self 
            # yield the bound value nb_subsamples times, in order to be consistent
            for _ in range(nb_subsamples):
                yield self._val
        else:        
            # distribution not yet bound
            try:
                # get nb_subsamples random values from Ilea._gen_one_random_mc method 
                # (this generator create some binding by calling gen_one_random_mc)
                for v in self._gen_one_random_mc(nb_subsamples):
                    # bind value v: this is important if an object calls gen_one_random_mc on the same
                    # instance before resuming the present generator (see above)
                    self._val = v
                    yield v
            finally:
                # unbind value, after the random values have been bound or if an exception has been raised
                self._val = self

    def _gen_one_random_mc(self,nb_subsamples=1):
        for _ in self._gen_one_random_true_cond(self._get_cond_leas(),True):
            for _ in range(nb_subsamples):
                for v in self._lea1.gen_one_random_mc():
                    yield v

    def _gen_one_random_mc_no_exc(self):
        for u in self._gen_one_random_true_cond(self._get_cond_leas(),False):
            if u is not self: 
                for v in self._lea1._gen_one_random_mc():
                    yield v

    def lr(self):
        ''' returns a float giving the likelihood ratio (LR) of an 'evidence' E,
            which is self's unconditional probability distribution, for a given
            'hypothesis' H, which is self's condition; it is calculated as 
                  P(E | H) / P(E | not H)
            both E and H must be boolean probability distributions, otherwise
            an exception is raised;
            an exception is raised also if H is certainly true or certainly false      
        '''
        lr_n = self.P
        lr_d = self._lea1.given(~Lea.reduce_all(and_,self._get_cond_leas(),False)).P
        if lr_d == 0:
            if lr_n == 0:
                raise Lea.Error("undefined likelihood ratio")
            return float('inf') 
        return lr_n / lr_d

    def _em_step(self,model_lea,cond_lea,obs_pmf_tuple,conversion_dict):
        return Ilea(self._lea1.em_step(model_lea,cond_lea,obs_pmf_tuple,conversion_dict),
                    ( cond_lea1.em_step(model_lea,cond_lea,obs_pmf_tuple,conversion_dict)
                      for cond_lea1 in self._get_cond_leas()) )

