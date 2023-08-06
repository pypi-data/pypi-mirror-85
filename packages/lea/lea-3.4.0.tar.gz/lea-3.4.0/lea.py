'''
--------------------------------------------------------------------------------

    lea.py

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

import operator
import sys
from itertools import islice
import collections
from .prob_fraction import ProbFraction
from .toolbox import min2, max2, read_csv_filename, read_csv_file, dict, zip, isclose, log2

# note: see other import statements at the end of the module


class Lea(object):
    
    '''
    Lea is an abstract class representing discrete probability distributions.

    Each instance of concrete Lea's subclasses (called simply a "Lea instance" in the following)
    represents a discrete probability distribution, which associates each value of a set of
    values with the probability that such value occurs.

    A Lea instance can be defined by a sequence of (value,probability), giving the probability 
    of each value. A Lea instance can be defined also by a sequence of values, the probability
    of a given value being its frequency in the sequence.

    Lea instances can be combined in arithmetic expressions resulting in new Lea instances, by
    obeying the following rules:

    - Lea instances can be added, subtracted, multiplied and divided together,
    through +, -, *, /, // operators. The resulting distribution's values and probabilities
    are determined by combination of operand's values into sums of probability
    products (the operation known as 'convolution', for the addition case).
    - Other supported binary arithmetic operators are power (**), modulo (%) and
    divmod function.
    - Unary operators +, - and abs function are supported also.
    - The Python's operator precedence rules, with the parenthesis overrules, are fully
    respected.
    - Any object X, which is not a Lea instance, involved as argument of an
    expression containing a Lea instance, is coerced to a Lea instance
    having X has sole value, with probability 1 (i.e. occurrence of X is certain).
    - Lea instances can be compared together, through ==, !=, <, <=, >, >= operators.
    The resulting distribution is a boolean distribution, giving probability of True result
    and complementary probability of False result.
    - Boolean distributions can be combined together with AND, OR, XOR, through &, |, ^
    operators, respectively.

    WARNING: the Python's 'and', 'or' and 'not' operators shall NOT be used on Lea instances;
    this raises an exception. Replace:
           a and b    by    a & b
           a or b     by    a | b
           not a      by    ~ a

    WARNING: in boolean expression involving arithmetic comparisons, the parenthesis
    shall be used, e.g. (a < b) & (b < c)

    WARNING: the augmented comparison (a < b < c) expression shall NOT be used.; this raises
    an exception (reason: it has the same limitation as 'and' operator).

    Lea instances can be used to generate random values, respecting the given probabilities.
    There are two Lea methods for this purpose:
    - random:   calculates the exact probability distribution, then takes random values 
    - random_mc: takes random values from atomic probability distribution, then makes the 
                required calculations (Monte-Carlo algorithm)
    The random_mc is suited for complex distributions, when calculation of exact probability
    distribution is intractable. This could be used to provide an estimation of the probability
    distribution (see estimate_mc method).

    There are 13 concrete subclasses to Lea class, namely:
      Alea, Olea, Plea, Clea, Flea, Flea1, Flea2, Glea, Ilea, Rlea, Tlea, Slea and Blea.
    
    Each subclass represents a "definition" of discrete probability distribution, with its own data
    or with references to other Lea instances to be combined together through a given operation.
    Each subclass defines what are the (value,probability) pairs or how they can be generated (see
    _gen_vp method implemented in each Lea subclass). The Lea class acts as a facade, by providing
    different constructors (static methods) to instantiate these subclasses, so it is usually not
    needed to instantiate Lea subcasses explicitly. Here is an overview on these subclasses, with
    their relationships. We indicate the equivalent type of "p-expression" ("pex" for short) as
    defined in the paper on the Statues algorithm (see reference below).

    - Alea  (elementary pex) defines a probability mass function ("pmf") defined by extension,
            i.e. explicit (value,P(value)) pairs
    - Olea  (elementary pex) defines a binomial probability distribution
    - Plea  (elementary pex) defines a Poisson probability distribution
    - Clea  (tuple pex) provides the joint of a given sequence of Lea instances
    - Flea  (functional pex) applies a given n-ary function to a given sequence of n Lea instances
    - Flea1 (functional pex) applies a given 1-ary function to a given Lea instance
    - Flea2 (functional pex) applies a given 2-ary function to two given Lea instances
    - Glea  (multi-functional pex) applies n-ary functions present in a given Lea instance to a
            given sequence of n Lea instances
    - Ilea  (conditional pex) filters the values of a given Lea instance according to a given Lea
            instance representing a boolean condition (conditional probabilities)
    - Rlea  (mixture pex) embeds Lea instances as values of a parent Lea instance 
    - Tlea  (table pex) defines CPT by a dictionary associating Lea instances to given values
    - Slea  (NO pex defined yet) defines CPT by a function associating Lea instances to given values
    - Blea  (mixture+conditional pex) defines CPT by associating Lea instances to conditions

    Instances of Lea subclasses other than Alea represent prob. distributions obtained by operations
    done on existing Lea instance(s). Any such instance forms a direct acyclic graph (DAG) structure,
    having other Lea instances as nodes and Alea instances as leaves. This uses "lazy evaluation":
    actual (value,probability) pairs are calculated only at the time they are required (e.g. display,
    query probability of a given value, etc); then, these are aggregated in a new Alea instance. This 
    Alea instance is then cached, as an attribute of the queried Lea instance, for speeding up next
    queries.

    Note that Flea1 and Flea2 subclasses have more efficient implementation than Flea subclass.
    Tlea, Slea and Blea may be used to define Bayesian networks. Tlea class is the closest to CPT
    concept since it stores the table in a dictionary. Slea allows to define CPT by means of a
    function, which could be more compact to store than an explicit table; it may be useful in
    particular for noisy-or and noisy-max models.  
    
    WARNING: The following methods are called without parentheses (for the sake of ease of use):
      P, Pf, mean, mean_f, var, var_f, std, std_f, mode, entropy, rel_entropy, redundancy, information,
      support, ps, pmf_tuple, pmf_dict, cdf_tuple, cdf_dict, p_sum
    These are applicable on any Lea instance; these are implemented and documented in the Alea class.

    Short design notes:
    
    Lea uses the "template method" design pattern: the Lea base abstract class calls the following
    methods, which are implemented in each Lea's subclass:
        _get_lea_children, _clone_by_type, _gen_vp, _gen_one_random_mc and _em_step.
    Excepting the afore-mentioned estimate_mc method, Lea performs EXACT calculation of probability
    distributions.
    It implements an original algorithm, called the "Statues" algorithm, by reference to the game of the
    same name; this uses a variable binding mechanism that relies on Python's generators. To learn more,
    you may read the paper "Probabilistic inference using generators - the Statues algorithm", freely
    available on http://arxiv.org/abs/1806.09997. The heart of the algorithm is implemented in
    Lea._gen_bound_vp method (aka GENATOMS in the paper) and <X>lea._gen_vp methods implemented in Lea's
    subclasses (aka GENATOMSBYTYPE in the paper); the final collection and condensation is done by
    Lea.calc method (aka MARG in the paper), which uses Alea.pmf method.
    '''

    class Error(Exception):
        ''' exception representing any violation of requirements of Lea methods  
        '''
        pass
        
    class _FailedRandomMC(Exception):
        ''' internal exception representing a failure to get a set of random values that
            satisfy a given condition in a given number of trials (see methods having '..._mc' suffix) 
        '''
        pass

    # Lea attributes
    __slots__ = ('_alea', '_val', 'gen_vp')

    # a mutable object, which cannnot appear in Lea's values (not hashable)
    _DUMMY_VAL = []

    # constructor methods
    # -------------------

    def __init__(self):
        ''' initializes Lea instance's attributes
        '''
        # alea instance acting as a cache when actual value-probability pairs have been calculated
        self._alea = None
        # _val is the value temporarily bound to the instance, during evaluation (see _gen_bound_vp method)
        # note: self is used as a sentinel value to express that no value is currently bound; Python's
        # None is not a good sentinel value since it prevents using None as value in a distribution
        self._val = self
        # when evaluation is needed, gen_vp shall be bound on _gen_vp or _gen_bound_vp method
        # (see _init_calc method)
        self.gen_vp = None

    @staticmethod
    def binom(n,p,prob_type=None):
        ''' static method, returns an Olea instance representing a binomial
            distribution giving the number of successes among a number n of
            independent experiments, each having probability p of success;
            note: the binom method generalizes the bernoulli method:
              binom(1,p) is the same as bernoulli(p)
            prob_type argument allows converting the given probability p:
              -1: no conversion;
              None (default): default conversion, as set by Alea.set_prob_type;
              other: see doc of Alea.get_prob_type;
        '''
        return Olea(n,p,prob_type)

    @staticmethod
    def poisson(mean,precision=1e-20):
        ''' static method, returns a Plea instance representing a Poisson probability
            distribution having the given mean; the distribution is approximated by
            the finite set of values that have probability > precision
            (i.e. low/high values with too small probabilities are dropped);
            the probabilities are stored as float, whatever the current probability
            type configured
        '''
        return Plea(mean,precision)

    def _id(self):
        ''' returns a unique id, containing the concrete Lea class name as prefix
        '''
        return '%s#%s'%(self.__class__.__name__,id(self))

    def get_alea_leaves_set(self):
        ''' returns a set containing all the Alea leaves in the tree having the root self;
            this calls _get_lea_children() method implemented in Lea's subclasses;
            this method is overloaded in Alea subclass to stop the recursion
        '''
        return frozenset(alea_leaf for lea_child in self._get_lea_children()
                                   for alea_leaf in lea_child.get_alea_leaves_set())

    def gen_lea_descendants(self):
        ''' generates all the Lea instances in the tree having the root self,
            including self itself; the same instance may be yieled multiple times;
            this calls _get_lea_children() method implemented in Lea's subclasses;
        '''
        yield self
        for lea_child in self._get_lea_children():
            for lea_child_descendant in lea_child.gen_lea_descendants():
                yield lea_child_descendant

    def get_inner_lea_set(self):
        ''' returns a set containing all the Lea instances in the tree having the root self,
            including self itself;
            this calls _get_lea_children() method implemented in Lea's subclasses;
        '''
        return frozenset(self.gen_lea_descendants())

    def _gen_bound_vp(self):
        ''' generates tuple (v,p) where v is a value of the current probability distribution
            and p is the associated probability  (integer > 0);
            this obeys the "binding" mechanism, so if the same variable is referred multiple
            times in a given expression, then same value will be yielded at each occurrence;
            "Statues" algorithm:
            before yielding a value v, this value v is bound to the current instance;
            then, if the current calculation requires to get again values on the current
            instance, then the bound value is yielded with probability 1;
            the instance is rebound to a new value at each iteration, as soon as the execution
            is resumed after the yield;
            it is unbound at the end;
            the method calls the _gen_vp method implemented in Lea subclasses;
            the present Alea._gen_vp method is called by the _gen_vp methods implemented in
            other Lea subclasses; these methods are themselves called by Lea.new and,
            indirectly, by Lea.get_alea
        '''
        if self._val is not self:
            # distribution already bound to a value because gen_vp has been called already on self
            # it is yielded as a certain distribution (unique yield)
            yield (self._val,1)
        else:
            # distribution not yet bound to a value
            try:
                # browse all (v,p) tuples
                for (v,p) in self._gen_vp():
                    # bind value v: this is important if an object calls gen_vp on the same instance
                    # before resuming the present generator (see above)
                    self._val = v
                    # yield the bound value v with probability p
                    yield (v,p)
            finally:
                # unbind value v, after all values have been bound or if an exception has been raised
                self._val = self

    def _reset_gen_vp(self):
        ''' sets gen_vp = None on self and all Lea descendants
        '''
        self.gen_vp = None
        # treat children recursively, up to Alea instances
        for lea_child in self._get_lea_children():
            lea_child._reset_gen_vp()

    def _set_gen_vp(self,memoization=True):
        ''' prepares calculation of probability distribution by binding x.gen_vp to the most adequate method,
            where x is self or any of self descendents: x.gen_vp is bound
            - to x._gen_vp method, if no binding is required (single occurrence of self in expression and no
              explicit binding of x)
            - to x._gen_bound_vp method, if binding is required (multiple occurrences of self in expression
              or explicit binding of x)
            note: x._gen_bound_vp works in any case but perform unnecessary binding job if x occurrence is
            unique in the evaluated expression; hence, the method makes a preprocessing allowing to optimize
            the pmf calculation
            * memoization argument: see Lea.calc method
            requires that gen_vp = None for self and all Lea descendants
        '''
        if self.gen_vp is None:
            # first occurrence of self in the expression: 
            if self._val is self:
                # self is not bound; use the simplest _gen_vp method
                # this may be overwritten if a second occurrence is found
                self.gen_vp = self._gen_vp
            else:
                # self is explicitely bound - see observe(...) method or .calc(bindings=...);
                # use the _gen_bound_vp method to yield the bound value
                self.gen_vp = self._gen_bound_vp
        ## note: do not replace '==' by 'is' operator below                
        elif memoization and self.gen_vp == self._gen_vp:
            # second occurrence of self in the expression: use the _gen_bound_vp method
            self.gen_vp = self._gen_bound_vp
        # treat children recursively, up to Alea instances
        for lea_child in self._get_lea_children():
            lea_child._set_gen_vp(memoization)

    def is_bound(self):
        ''' returns True iff self is currently bound
        '''
        return self._val is not self

    def _init_calc(self,bindings=None,memoization=True,optimize=True,debug=False):
        ''' prepares calculation of probability distribution by binding self.gen_vp to the most adequate method;
            see _set_gen_vp method;
            if bindings is not None, then it is browsed as a dictionary: each key (Alea instance) is bound
            to the associated value - see requirements of Lea.observe;
            if optimize is true, then independent sub-DAG are searched in the DAG rooted by self; if such
            independent sub-DAG are found, then their roots are evaluated and replaced by resulting Alea
            instances; for some DAG presenting inner tree patterns, this divide-and-conquer process may save a
            lot of calculations; this is used only in the context of EXACT algorithm (see calc method); 
            all effects done by the present method are transient, for performing the calculation of self;
            these are undone by _finalize_calc method
        '''
        self._reset_gen_vp()
        # set explicit bindings, if any
        if bindings is not None:
            for (x,v) in bindings.items():
                x.observe(v)
        self._set_gen_vp(memoization)
        if optimize:
            dependent_nodes = self._get_dependent_nodes()
            # independent nodes can be evaluated one by one and replaced by an Alea instance
            self._optimize(dependent_nodes,debug=debug)

    def _optimize(self,dependent_nodes,first_level=True,debug=False):
        """ replace in the DAG rooted by self the roots of independent sub-DAG by equivalent Alea instances;
            these nodes are identified as non-Alea instances absent from the given dependent_nodes set,
            provided that first_level is false;
            the present method shall be called only in the context of EXACT algorithm (see calc method);
            warning; it updates the dependent_nodes set by adding optimized nodes in it, in order to ensure
            that these are optimized no more than once
        """
        for lea_child in self._get_lea_children():
            lea_child._optimize(dependent_nodes,first_level=False,debug=debug)
        if not (first_level or isinstance(self,Alea) or self in dependent_nodes):
            alea1 = Alea.pmf(self.gen_vp(),normalization=False)
            if debug:
                print ("optimize %s"%(self._id()))
            ## note: do not replace '==' by 'is' operator below
            if self.gen_vp == self._gen_bound_vp:
                self.gen_vp = alea1._gen_bound_vp
            else:
                self.gen_vp = alea1._gen_vp
            dependent_nodes.add(self)

    def _get_dependent_nodes(self):
        """ returns the set of all "dependent" nodes in the DAG rooted by self;
            a dependent node is, by definition, a node that cannot be evaluated individually
            without referential consistency error on an ancestor;
            (supporting method for _optimize)
        """
        ## note: do not replace '==' by 'is' operator below
        pivotal_nodes = frozenset(x for x in self.gen_lea_descendants()
                                    if x.gen_vp == x._gen_bound_vp)
        dependent_nodes = set()
        for pivotal_node in pivotal_nodes:
            antipivotal_node = self._get_antipivotal_node(pivotal_node)
            dependent_nodes.update(antipivotal_node._gen_dependent_nodes(pivotal_node))
        return dependent_nodes
  
    def _gen_dependent_nodes(self,pivotal_node,first_level=True):
        """ generates all "dependent" nodes in the DAG rooted by self on paths up to given pivotal_node;
            a dependent node is, by definition, a node that cannot be evaluated individually
            without referential consistency error on an ancestor; these are retrieved by gathering
            all nodes between self and given pivotal_node (including); self is yielded, excepted
            if it is the anti-pivotal node (first_level=True)
            (supporting method for _optimize)
        """
        for lea_child in self._get_lea_children():
            if lea_child is pivotal_node and not first_level:
                yield self
            has_found_dependent_nodes = False
            for x in lea_child._gen_dependent_nodes(pivotal_node,False):
                has_found_dependent_nodes = True
                yield x
            if has_found_dependent_nodes:
                yield lea_child
                
    def _get_antipivotal_node(self,pivotal_node):
        """ returns the anti-pivotal node corresponding to given pivotal_node in the DAG rooted by self,
            a pivotal node is a node that has more than one parent, i.e. which is referred multiple times
            in the expression under evaluation, requiring a binding mechanism to ensure referential consistency
            for each pivotal node, there exists one and only one anti-pivotal node, which is the closest
            ancestor node that is the origin of all paths leading to this pivotal node
            (supporting method for _optimize)
        """
        children_containing_pivotal_node = tuple(lea_child for lea_child in self._get_lea_children()
                                                 if any(y is pivotal_node for y in lea_child.gen_lea_descendants()))
        if len(children_containing_pivotal_node) == 1:
            return children_containing_pivotal_node[0]._get_antipivotal_node(pivotal_node)
        return self

    def _finalize_calc(self,bindings=None):
        ''' makes finalization after pmf calculation, by unbinding all instances bound in
            _init_calc, supposed to be present in given bindings dictionary
        '''
        if bindings is not None:
            for x in bindings:
                ## note: leave check=False because in case of exception _init_calc, then some instances may still be unbound
                x.free(check=False)

    def given_prob(self,cond_lea,p):
        ''' returns a new Lea instance from current distribution,
            such that given p is the probability that cond_lea is true
        '''
        cur_cond_lea = Alea.coerce(cond_lea)
        req_cond_lea = Alea.event(p)
        if req_cond_lea.is_true():
            return self.given(cur_cond_lea)
        elif not req_cond_lea.is_feasible():
            return self.given(~cur_cond_lea)
        return Lea.if_(req_cond_lea,self.given(cur_cond_lea).get_alea(sorting=False),self.given(~cur_cond_lea).get_alea(sorting=False))

    def given(self,*evidences):
        ''' returns a new Ilea instance representing the current distribution
            updated with the given evidences, which are each either a boolean or
            a Lea instance with boolean values; the values present in the returned
            distribution are those and only those compatible with the given AND of
            evidences;
            the resulting (value,probability) pairs are calculated when the
            returned Ilea instance is evaluated;
            an exception is raised if the evidences contain a non-boolean or
            if they are unfeasible
        '''
        return Ilea(self,(Alea.coerce(evidence) for evidence in evidences))

    def times(self,n,op=operator.add,normalization=False):
        ''' returns, after evaluation of the probability distribution self, a new
            Alea instance representing the current distribution operated n times
            with itself, through the given binary operator op;
            if n = 1, then a copy of self is returned;
            requires that n is strictly positive; otherwise, an exception is
            raised;
            if normalization is True (default: False), then each probability is
            divided by the sum of all probabilities
            note that the implementation uses a fast dichotomous algorithm,
            instead of a naive approach that scales up badly as n grows
        '''
        alea1 = self.new(normalization=False)
        if n <= 0:
            raise Lea.Error("times method requires a strictly positive integer")
        if n == 1:
            return alea1.new(normalization=normalization)
        (n2,r) = divmod(n,2)
        alea2 = alea1.times(n2,op,normalization=False)
        res_flea2 = Flea2(op,alea2,alea2.new(normalization=False))
        if r == 1:
            res_flea2 = Flea2(op,res_flea2,alea1)
        return res_flea2.calc(normalization=normalization)

    def times_tuple(self,n):
        ''' returns a new Alea instance with tuples of length n, containing
            the joint of self with itself repeated n times
            note: equivalent to self.draw(n,sorted=False,replacement=True)
        '''
        return self.get_alea().draw_with_replacement(n)

    def joint(self,*args):
        ''' returns a new Clea instance, representing the joint of all
            arguments, coerced to Lea instances, including self as first argument 
        '''
        return Clea(self,*args)

    @staticmethod
    def reduce_all(op,args,absorber=None):
        ''' static method, returns a new Flea2 instance that join the given args with
            the given function op, from left to right;
            requires that op is a 2-ary function, accepting self's values as arguments;
            requires that args contains at least one element
            if absorber is not None, then it is considered as a "left-absorber" value
            (i.e. op(absorber,x) = absorber); this activates a more efficient algorithm
            which prunes the tree search as soon as the absorber is met.
        '''
        args_rev_iter = iter(reversed(tuple(args)))
        res = next(args_rev_iter)
        if absorber is None:
            for arg in args_rev_iter:
                res = Flea2(op,arg,res)
        else:
            for arg in args_rev_iter:
                res = Flea2a(op,arg,res,absorber)
        return res

    def merge(self,*lea_args):
        ''' returns a new Blea instance, representing the merge of self and given lea_args, i.e.
                  P(v) = (P1(v) + ... + Pn(v)) / n
            where P(v)  is the probability of value v in the merge result 
                  Pi(v) is the probability of value v in ((self,)+lea_args)[i]
        '''
        leas = (self,) + lea_args
        lea = Alea.vals(*range(len(leas)))
        return Blea.build(*((lea==i,lea_arg) for (i,lea_arg) in enumerate(leas)))

    def map(self,f,*args):
        ''' returns a new Flea instance representing the distribution obtained
            by applying the given function f, taking values of self distribution
            as first argument and optional given args as following arguments;
            requires that f is a n-ary function with 1 <= n = len(args)+1;
            note: f can be also a Lea instance, with functions as values
        '''
        return Flea.build(f,(self,)+args)

    def map_seq(self,f,*args):
        ''' returns a new Flea instance representing the distribution obtained
            by applying the given function f on each element of each value
            of self distribution; optional given args are added as f's
            following arguments;
            requires that f is a n-ary function with 1 <= n = len(args)+1;
            requires that self's values are sequences;
            the values of returned distribution are tuples
            note: f can be also a Lea instance, with functions as values
        '''
        return self.map(lambda v: tuple(f(e,*args) for e in v))

    @staticmethod
    def func_wrapper(f):
        ''' static method, returns a wrapper function on given f function,
            mimicking f with Lea instances as arguments;
            the returned wrapper function has the same number of arguments
            as f and expects for argument #i
            - either an object of the type expected by f for argument #i
            - or a Lea instance with values of that type;
            the returned wrapper function, when called, returns a Lea instance
            having values of the type returned by f;
            note: Lea.func_wrapper can be used as a function decorator
        '''
        def wrapper(*args):
            return Flea.build(f,args)
        wrapper.__name__ = 'lea_wrapper_on__' + f.__name__
        wrapper.__doc__ = ("" if f.__doc__ is None else f.__doc__) \
                          + "\nThe present function wraps '%s' so to work with Lea instances as arguments." % (f.__name__,)
        return wrapper

    def as_joint(self,*attr_names):
        ''' returns a new Flea instance by building named tuples from self, which
            is supposed to have n-tuples as values, using the n given attr_names;
            note: this is useful to access fields of joint probability distribution
            by names instead of indices
        '''
        NTClass = collections.namedtuple('_',attr_names)
        return self.map(lambda a_tuple: NTClass(*a_tuple))

    def is_uniform(self):
        ''' returns, after evaluation of the probability distribution self,
            True  if the probability distribution is uniform,
            False otherwise
        '''
        return self.get_alea().is_uniform()

    def draw(self,n,sorted=False,replacement=False):
        ''' returns, after evaluation of the probability distribution self,
            a new Alea instance representing the probability distribution
            of drawing n elements from self;
            the returned values are tuples with n elements;
            * if sorted is True, then the order of drawing is irrelevant and
                 the tuples are arbitrarily sorted by increasing order;
                 (the efficient algorithm used is due to Paul Moore)
              otherwise, the order of elements of each tuple follows the order
                 of the drawing
            * if replacement is True, then the drawing is made WITH replacement,
                 so the same element may occur several times in each tuple
              otherwise, the drawing is made WITHOUT replacement,
                 so an element can only occur once in each tuple;
                 this last case requires that 0 <= n <= number of values of self,
                 otherwise an exception is raised
            Note: if the order of drawing is irrelevant, it is strongly advised to
             use sorted=True because the processing can be far more efficient thanks
             to a combinatorial algorithm proposed by Paul Moore; however, this
             algorithm is NOT used if replacement is False AND the probability
             distribution is NOT uniform.
            requires Python 2.7+ for the case replacement = sorted = True
        '''
        if n < 0:
            raise Lea.Error("draw method requires a positive integer")
        alea1 = self.get_alea()
        if replacement:
            if sorted:
                # draw sorted with replacement
                return alea1.draw_sorted_with_replacement(n)
            else:
                # draw sorted without replacement
                return alea1.draw_with_replacement(n)
        else:
            if len(alea1._vs) < n:
                raise Lea.Error("number of values to draw without replacement (%d) exceeds the number of possible values (%d)"%(n,len(alea1._vs)))
            if sorted:
                # draw sorted without replacement
                return alea1.draw_sorted_without_replacement(n)
            else:
                # draw unsorted without replacement
                return alea1.draw_without_replacement(n)

    def flat(self):
        ''' assuming that self's values are themselves Lea instances,
            returns a new Rlea instance representing a probability distribution of
            inner values of these Lea instances  
        '''
        return Rlea(self)

    def equiv(self,other):
        ''' returns True iff self and other represent the same probability distribution,
            i.e. they have the same probability for each of their value;
            returns False otherwise;
            the probabilities are compared strictly (see Lea.equiv_f method for
            comparisons tolerant to rounding errors)
        '''
        other = Alea.coerce(other)
        # absolute equality required
        # frozenset(...) is used to avoid any dependency on the order of values
        return frozenset(self._gen_raw_vps()) == frozenset(other._gen_raw_vps())

    def equiv_f(self,other,rel_tol=1e-09,abs_tol=0.0):
        ''' returns True iff self and other represent the same probability distribution,
            i.e. they have the same probability for each of their value;
            returns False otherwise;
            the probabilities are compared using the math.isclose function,
            in order to be tolerant to rounding errors
        '''
        other = Alea.coerce(other)
        vps1 = tuple(self._gen_raw_vps())
        vps2Dict = dict(other._gen_raw_vps())
        if len(vps1) != len(vps2Dict):
            return False
        for (v1,p1) in vps1:
            p2 = vps2Dict.get(v1)
            if p2 is None:
                return False
            if not isclose(p1,p2,rel_tol,abs_tol):
                return False
        return True

    @staticmethod
    def dist_l1(lea1,lea2):
        ''' static method, returns the L1 distance between the pmf of given (coerced)
            lea instances;
            note: assuming that Lea instances are normalized, the result is between 0
            (iff lea1 and lea2 have same pmf) and 2 (iff lea1 and lea2 have disjoint
            supports)
        '''
        lea1 = Alea.coerce(lea1)
        lea2 = Alea.coerce(lea2)        
        return sum(abs(lea1._p(v)-lea2._p(v)) for v in frozenset(lea1.support+lea2.support))

    @staticmethod
    def dist_l2(lea1,lea2):
        ''' static method, returns the L2 distance between the pmf of given (coerced)
            lea instances;
            note: assuming that Lea instances are normalized, the result is between 0
            (iff lea1 and lea2 have same pmf) and sqrt(2) (iff lea1 and lea2 have
            disjoint singleton supports)
        '''
        lea1 = Alea.coerce(lea1)
        lea2 = Alea.coerce(lea2)        
        return (sum((lea1._p(v)-lea2._p(v))**2 for v in frozenset(lea1.support+lea2.support))) ** 0.5

    def p(self,val):
        ''' returns the probability of given value val
        '''
        return Alea._downcast(self._p(val))

    def _gen_raw_vps(self):
        ''' generates, after evaluation of the probability distribution self,
            tuples (v,p) where v is a value of self
            and p is the associated probability (integer > 0);
            the sequence follows the order defined on values;
            note that there is NO binding, contrarily to _gen_vp method
        '''
        return self.get_alea()._gen_vp()
    
    def _gen_vps(self):
        ''' generates, after evaluation of the probability distribution self,
            tuples (v,p) where v is a value of self and p is the associated
            probability;
            the sequence follows the order defined on values;
            note that there is NO binding, contrarily to _gen_vp method
        '''
        return ((v,Alea._downcast(p)) for (v,p) in self._gen_raw_vps())

    def _p(self,val,check_val_type=False):
        ''' returns the probability of the given value val
            if check_val_type is True, then raises an exception if some value in the
            distribution has a type different from val's
        '''
        return self.get_alea()._p(val,check_val_type)

    def sort_by(self,*ordering_leas):
        ''' returns an Alea instance representing the same probability distribution as self
            but having values ordered according to given ordering_leas;
            requires that self doesn't contain duplicate values, otherwise an exception is
            raised; note that it is NOT required that all ordering_leas appear in self 
        '''
        # after prepending ordering_leas to self, the Alea returned by new() is sorted with ordering_leas;
        # then, extracting self (index -1) allows generating self's (v,p) pairs in the expected order;
        # these shall be used to create a new Alea, keeping the values in that order (no sort)
        sorted_lea = Lea.joint(*ordering_leas).joint(self).new()[-1]
        sorted_lea._init_calc()
        return Alea._pmf_ordered(sorted_lea.gen_vp())

    def is_any_of(self,*values):
        ''' returns a boolean probability distribution
            indicating the probability that a value is any of the values passed as arguments
        '''
        return Flea1(lambda v: v in values,self)

    def is_none_of(self,*values):
        ''' returns a boolean probability distribution
            indicating the probability that a value is none of the given values passed as arguments 
        '''
        return Flea1(lambda v: v not in values,self)

    def subs(self,*args):
        ''' returns a new Alea instance, equivalent to self, where probabilities have been converted
            by applying subs(*args) on them;
            this is useful for substituting variables when probabilities are expressed as sympy
            expressions (see doc of sympy.Expression.subs method);
            requires that all self's probabilities have a 'subs' method available
        '''
        return Alea(*zip(*((v,p.subs(*args)) for (v,p) in self._gen_raw_vps())),normalization=False)

    @staticmethod
    def if_(cond_lea,then_lea,else_lea=_DUMMY_VAL,prior_lea=_DUMMY_VAL):
        ''' static method, returns an instance of Tlea representing the
            conditional probability table
            giving then_lea  if cond_lea is true
                   else_lea  otherwise
            if else_lea is defined this method is equivalent to 
              cond_lea.switch({True:then_lea,False:else_lea})
            if else_lea is undefined then prior_lea provides the Lea
            instance representing the prior (unconditional) probabilities;
            this is used then to calculate the missing else_lea
            requires: either else_lea or prior_lea argument shall be provided
            requires: if prior_lea is provided, a solution shall exist for else_lea
        '''
        if (else_lea is Lea._DUMMY_VAL and prior_lea is Lea._DUMMY_VAL) \
           or (else_lea is not Lea._DUMMY_VAL and prior_lea is not Lea._DUMMY_VAL):
            raise Lea.Error("if_ method requires either else_lea or prior_lea argument")
        lea_dict = dict(((True,then_lea),))
        if else_lea is not Lea._DUMMY_VAL:
            lea_dict[False] = else_lea
        return Tlea.build(cond_lea,lea_dict,prior_lea=prior_lea)

    def switch(self,lea_dict,default_lea=_DUMMY_VAL,prior_lea=_DUMMY_VAL):
        ''' returns an instance of Tlea representing a conditional probability table (CPT)
            defined by the given dictionary lea_dict associating each value of self to a
            specific Lea instance;
            if default_lea is given, then it provides the Lea instance associated to the
            value(s) of self missing in lea_dict;
            if prior_lea is given, then it provides the Lea instance representing the prior
            (unconditional) probabilities; this is used to define the Lea instance associated
            to the value(s) of self missing in lea_dict (as default_lea)
            all dictionary's values and default_lea (if defined) are coerced to Alea instances
            requires: default_lea and prior_lea shall not defined together
            requires: if prior_lea is provided, a solution shall exist for default_lea
        '''        
        return Tlea.build(self,lea_dict,default_lea,prior_lea)

    def switch_func(self,f):
        ''' returns an instance of Slea representing a conditional probability table (CPT)
            defined by the given function f associating each value of self to a
            specific Alea instance, if returned value is not a Lea instance, then it is
            coerced to an Alea instance
            requires: the f function shall return Alea instances only or non-Lea instances
            (coerced automatically to Alea instances)
        '''
        return Slea(self,f)

    ## note: in PY3, could use:
    ## def cpt(*clauses,prior_lea=None,auto_else=False,check=True):
    @staticmethod
    def cpt(*clauses,**kwargs):
        ''' static method, returns an instance of Blea representing the conditional
            probability table (e.g. a node in a Bayes network) from the given clauses;
            each clause is a tuple (condition,result)
            where condition is a boolean or a Lea boolean distribution
              and result is a value or Lea distribution representing the result
                   assuming that condition is true
            the conditions from all clauses shall be mutually exclusive
            if a clause contains None as condition, then it is considered as a 'else'
            condition;
            the method supports three optional named arguments:
             'prior_lea', 'auto_else', 'check' and 'ctx_type';
            'prior_lea' and 'auto_else' are mutually exclusive, they require the absence
            of an 'else' clause (otherwise, an exception is raised); 
            * if prior_lea argument is specified, then the 'else' clause is calculated
            so that the prior_lea is returned for the unconditional case
            * if auto_else argument is specified as True, then the 'else' clause is
            calculated so that a uniform probability distribution is returned for
            the condition cases not covered in given clauses (principle of indifference);
            the values are retrieved from the results found in given clauses
            * if check argument is specified as False, then NO checks are made on the given
            clauses (see below); this can significantly increase performances, as the 
            set of clauses or variables become large; 
            by default (check arg absent or set to True), checks are made on clause
            conditions to ensure that they form a partition:
              1) the clause conditions shall be mutually disjoint, i.e. no subset
                 of conditions shall be true together;
              2) if 'else' is missing and not calculated through 'prior_lea' nor 'auto_else',
                 then the clause conditions shall cover all possible cases, i.e. ORing
                 them shall be certainly true;
            an exception is raised if any of such conditions is not verified;
        '''
        return Blea.build(*clauses,**kwargs)

    def revised_with_cpt(self,*clauses):
        ''' returns an instance of Blea representing the conditional probability table
            (e.g. a node in a Bayes network) from the given clauses;
            each clause is a tuple (condition,result)
            where condition is a boolean or a Lea boolean distribution
              and result is a value or Lea distribution representing the result
                   assuming that condition is true
            the conditions from all clauses shall be mutually exclusive
            no clause can contain None as condition
            the 'else' clause is calculated so that the returned Blea if no condition is
            given is self
        ''' 
        return Blea.build(*clauses,prior_lea=self)

    def build_bn_from_joint(self,*bn_definition):
        ''' returns a named tuple of Lea instances (Alea or Tlea) representing a Bayes
            network with variables stored in attributes A1, ... , An, assuming that self
            is a Lea joint probability distribution having, as values, named tuples
            with the same set of attributes A1, ... , An (such Lea instance is
            returned by as_joint method, for example);
            each argument of given bn_definition represents a dependency relationship
            from a set of given variables to one given variable; this is expressed as
            a tuple (src_var_names, tgt_var_name) where src_var_names is a sequence of
            attribute names (strings) identifying 'from' variables and tgt_name is the
            attribute name (string) identifying the 'to' variable;
            the method builds up the 'to' variable of the BN as a CPT calculated from
            each combination of 'from' variables in the joint probability distribution:
            for each such combination C, the distribution of 'to' variable is calculated
            by marginalization on the joint probability distribution given the C condition;
            possible missing combinations are covered in an 'else' clause on the CPT
            that is defined as a uniform distribution of the values of 'to' variable,
            which are found in the other clauses (principle of indifference);
            the variables that are never referred as 'to' variable are considered
            as independent in the BN and are calculated by unconditional marginalization
            on the joint probability distribution;
            if a variable appears in more than one 'to' variable, then an exception is
            raised (error)
        '''
        joint_alea = self.get_alea()
        # retrieve the named tuple class from the first value of the joint distribution,
        NamedTuple = joint_alea._vs[0].__class__
        vars_dict = dict((var_name,self.__getattribute__(var_name)) for var_name in NamedTuple._fields)
        # all BN variables initialized as independent (maybe overwritten below, according to given relationships)
        vars_bn_dict = dict((var_name,var.get_alea(sorting=False)) for (var_name,var) in vars_dict.items())
        for (src_var_names,tgt_var_name) in bn_definition:
            if not isinstance(vars_bn_dict[tgt_var_name],Alea):
                raise Lea.Error("'%s' is defined as target in more than one BN relationship"%(tgt_var_name,))
            tgt_var = vars_dict[tgt_var_name]
            joint_src_vars = Lea.joint(*(vars_dict[src_var_name] for src_var_name in src_var_names))
            joint_src_vars_bn = Lea.joint(*(vars_bn_dict[src_var_name] for src_var_name in src_var_names))
            # build CPT clauses (condition,result) from the joint probability distribution
            joint_src_vals = joint_src_vars.support
            clauses = tuple((joint_src_val,tgt_var.given(joint_src_vars==joint_src_val).get_alea(sorting=False)) \
                             for joint_src_val in joint_src_vals)
            # determine missing conditions in the CPT, if any
            all_vals = Lea.joint(*(vars_dict[src_var_name].get_alea(sorting=False) for src_var_name in src_var_names)).support
            missing_vals = frozenset(all_vals) - frozenset(joint_src_vals)
            if len(missing_vals) > 0:
                # there are missing conditions: add clauses with each of these conditions associating
                # them with a uniform distribution built on the values found in results of other clauses
                # (principle of indifference)
                else_result = Alea.vals(*frozenset(val for (cond,result) in clauses for val in result.support))
                clauses += tuple((missing_val,else_result) for missing_val in missing_vals)
            # overwrite the target BN variable (currently independent Alea instance), with a CPT built
            # up from the clauses determined from the joint probability distribution
            # the check is deactivated for the sake of performance; this is safe since, by construction,
            # the clauses conditions verify the "truth partioning" rules
            # the ctx_type is 2 for the sake of performance; this is safe since, by construction, the
            # clauses results are Alea instances and clause conditions refer to the same variable,
            # namely joint_src_vars_bn
            vars_bn_dict[tgt_var_name] = joint_src_vars_bn.switch(dict(clauses))
        # return the BN variables as attributes of a new named tuple having the same attributes as the
        # values found in self
        return NamedTuple(**vars_bn_dict)

    def em_step(self,model_lea,cond_lea,obs_pmf_tuple,conversion_dict):
        ''' returns a revised version of self, with parameters tuned to match a given observed
            sample; this executes one step of the Expectation-Maximization (EM) algorithm;
            the arguments are:
            - model_lea:  model in which self occurs, it shall match the observed data
              (see obs_pmf_tuple below);
            - cond_lea: condition involving variables of model_lea, to be verified in the
              returned instance;
            - obs_pmf_tuple: tuple containing the frequencies of the observed data in the form of
              tuples (vi,f(vi)); the set of vi values shall be a subset of the support of
              model_lea; in case of multiple variables observed, the vi could be tuples giving
              the values jointly observed;
            - conversion_dict: dictionary associating the variables of model_lea already
              converted by the present function, with their conversion; if self is not yet
              present in it as a key, then it is added, with the instance to be returned 
            the object returned has same type and same DAG structure as self, only the internal
            parameters may be different; if self is in conversion_dict, then the associated
            instance is returned without any further treatment;
            the method calls _em_step defined on each Lea subclass, this implements the
            required treatments for EM step for the specifc instance, possibly calling
            recursively em_step on self's child nodes;
        '''
        lea2 = conversion_dict.get(self)
        if lea2 is None:
            lea2 = self._em_step(model_lea,cond_lea,obs_pmf_tuple,conversion_dict)
            conversion_dict[self] = lea2
        return lea2

    def _em_step(self,model_lea,cond_lea,obs_pmf_tuple,conversion_dict):
        ''' returns a revised version of self, with parameters tuned to match a given observed
            sample; this executes one step of the Expectation-Maximization (EM) algorithm;
            the arguments are:
            - model_lea: model in which self occurs, and which matches the observed data (see
              obs_pmf_tuple below);
            - cond_lea: condition involving variables of model_lea, to be verified in the
              returned instance;
            - obs_pmf_tuple: tuple containing the frequencies of the observed data in the form of
              tuples (vi,f(vi)); the set of vi values shall be a subset of the support of
              model_lea; in case of multiple variables observed, the vi could be tuples giving
              the values jointly observed;
            - conversion_dict: dictionary associating the variables of model_lea already
              converted by the present function, with their conversion; if self is not yet
              present in it as a key, then it is added, with the instance to be returned 
            the object returned has same type and same DAG structure as self, only the internal
            parameters may be different;
            the method is defined on each Lea subclass, this implements the required treatments
            for EM step for the specifc instance, possibly calling recursively em_step on self's
            child nodes;
        '''
        raise NotImplementedError("missing method '%s._em_step(...)'"%(self.__class__.__name__))

    def gen_em_steps(self,obs_lea,fixed_vars=()):
        ''' generates an infinite sequence of steps of Expectation-Maximization (EM) algorithm,
            yielding revised versions of a probabilistic model, with parameters tuned to match
            a given observed sample; this algorithm allows hidden variables in the model (i.e.
            absent from observed sample);
            the arguments are:
            - obs_lea: Lea instance giving the frequencies of the observed data; the support of
              obs_lea shall be a subset of the support of self; in case of n variables observed,
              self and obs_lea can be defined as joint tables, having tuples of size n as support;
            - fixed_vars (default: empty tuple): an iterable giving the variables that shall NOT
              be revised by the algorithm; in the returned model, these variables shall keep their
              initial parameters unchanged;
            the object yielded is a dictionary md associating self and inner self variables to the
            revised variables after each EM step, for any variable v present in self, md[v] has same
            type and same DAG structure as v, only the internal parameters may be different;
            the EM algorithm is iterative, supposingly converging to a Lea instance maximizing
            the likelihood of obs_lea; the caller is expected to stop iterations when some criteria
            are satisfied (see Lea.learn_by_em method for an example)
        '''
        obs_pmf_tuple = obs_lea.pmf_tuple
        new_model_lea = self
        conversion_dict = None
        while True:
            conversion_dict2 = dict((fv,fv) for fv in fixed_vars)
            new_model_lea = new_model_lea.em_step(new_model_lea,True,obs_pmf_tuple,conversion_dict2)
            if conversion_dict is None:
                conversion_dict = conversion_dict2
            else:
                conversion_dict = dict((var0,conversion_dict2[var1]) for (var0,var1) in conversion_dict.items())
            yield conversion_dict

    def learn_by_em(self,obs_lea,fixed_vars=(),nb_steps=None,max_kld=None,max_delta_kld=None):
        ''' returns a revised version of a probabilistic model, with parameters tuned to match a
            given observed sample; this uses the Expectation-Maximization (EM) algorithm, which
            allows hidden variables in the model (i.e. absent from observed sample);
            the first two arguments are:
            - obs_lea: Lea instance giving the frequencies of the observed data; the support of
              obs_lea shall be a subset of the support of self; in case of n variables observed,
              self and obs_lea can be defined as joint tables, having tuples of size n as support;
            - fixed_vars (default: empty tuple): an iterable giving the variables that shall NOT
              be revised by the algorithm, if any; in the returned model, these variables shall
              keep their initial parameters unchanged;
            the object returned is a dictionary md associating self and inner self variables to the
            revised variables after each EM step, for any variable v present in self, md[v] has same
            type and same DAG structure as v, only the internal parameters may be different;
            the algorithm is iterative, supposingly converging to a Lea instance maximizing
            the likelihood of obs_lea; this is equivalently stated as maximizing log-likelihood,  
            minimizing the cross-entropy or minimizing the Kullback-Leibler divergence;
            the exit condition can be specified in three different ways, defined by the last
            three arguments (at least one of them shall be not None):
            - nb_steps (int): the maximum number of iterations of EM algorithm
            - max_kld (float): the EM algorithm halts as soon as the Kullback-Leibler
              divergence is lower or equal to this number; this indicates the degree of fit
              required; the smallest, the longest the execution;
            - max_delta_kld (float): the EM algorithm halts as soon as the difference in
              absolute value between cross entropy calculated on two consecutive iterations
              is equal or lower to this number; this is a convergence criterium;
              the smallest, the longest the execution;
            if more than one argument is not None, then any fulfilled halting conditions makes
            the EM algorithm halts
        '''
        if nb_steps is None and max_kld is None and max_delta_kld is None:
            raise Lea.Error("learn_by_em method requires providing at least one halt condition (nb_steps,"
                            " max_delta_kld or max_kld argument)")
        obs_lea_entropy = obs_lea.entropy
        nb_steps_done = 0
        learn_by_em_generator = self.gen_em_steps(obs_lea,fixed_vars)
        new_model_lea = self
        while True:
            nb_steps_done += 1
            # calculation of cross_entropy will raise an exception if some value of obs_lea
            # support is absent from model_lea
            ## kl_divergence method is not used here, to avoid multiple calculation
            ## of obs_lea.entropy, which is constant
            kld = obs_lea.cross_entropy(new_model_lea) - obs_lea_entropy
            if nb_steps is not None and nb_steps_done > nb_steps:
                break
            if max_kld is not None and kld <= max_kld:
                break
            if max_delta_kld is not None:
                if nb_steps_done >= 2 and abs(kld-prev_kld) <= max_delta_kld:
                    break
                prev_kld = kld
            model_lea_dict = next(learn_by_em_generator)
            new_model_lea = model_lea_dict[self]
        return model_lea_dict

    @staticmethod
    def make_vars(obj,tgt_dict,prefix='',suffix=''):
        ''' static method, retrieves attributes names A1, ... , An of obj and
            put associations {V1 : obj.A1, ... , Vn : obj.An} in tgt_dict dictionary
            where Vi is a variable name string built as prefix + Ai + suffix;
            obj is
            (a) either a named tuple with attributes A1, ... , An (as returned
            by build_bn_from_joint, for example)
            (b) or a Lea instances representing a joint probability distribution
            with the attributes A1, ... , An (such Lea instance is returned by
            as_joint method, for example);
            note: if the caller passes globals() as tgt_dict, then the variables
            named Vi, referring to obj.Ai, shall be created in its scope, as
            a side-effect (this is the purpose of the method);
            warning: the method may silently overwrite caller's variables
        '''
        if isinstance(obj,Lea):
            # case (b)
            # retrieve the named tuple class from the first value of the joint distribution
            NamedTuple = obj.get_alea()._vs[0].__class__
        else:
            # case (a)
            NamedTuple = obj.__class__
        tgt_dict.update((prefix+var_name+suffix,obj.__getattribute__(var_name)) for var_name in NamedTuple._fields)       
    
    def __call__(self,*args):
        ''' returns a new Glea instance representing the probability distribution
            of values returned by invoking functions of current distribution on 
            given arguments (assuming that the values of current distribution are
            functions);
            called on evaluation of "self(*args)"
        '''
        return Glea.build(self,args)

    def __iter__(self):
        ''' raises en error exception
            called on evaluation of "iter(self)", "tuple(self)", "list(self)"
                or on "for x in self"
        '''
        raise Lea.Error("cannot iterate on a Lea instance")

    def __getattribute__(self,attr_name):
        ''' returns the attribute with the given name in the current Lea instance;
            if the attribute name is a distribution indicator, then the distribution
            is evaluated and the indicator method is called; 
            if the attribute name is unknown as a Lea instance's attribute,
            then returns a Flea instance that shall retrieve the attribute in the
            values of current distribution; 
            called on evaluation of "self.attr_name"
            WARNING: the following methods are called without parentheses:
                         P, Pf, mean, mean_f, var, var_f, std, std_f, mode,
                         entropy, rel_entropy, redundancy, information,
                         support, p_sum, ps, pmf_tuple, pmf_dict, cdf_tuple,
                         cdf_dict
                     these are applicable on any Lea instance
                     and these are documented in the Alea class
        '''
        try:
            if attr_name in Alea.indicator_method_names:
                # indicator methods are called implicitely
                return object.__getattribute__(self.get_alea(),attr_name)()
            # return Lea's instance attribute
            return object.__getattribute__(self,attr_name)
        except AttributeError:
            # return new Lea made up of attributes of inner values
            return Flea2(getattr,self,attr_name)

    ## in PY3, could use
    ## def max_of(*args,fast=False):
    @staticmethod
    def max_of(*args,**kwargs):
        ''' static method, returns a Lea instance giving the probabilities to have
            the maximum value of each combination of the given args;
            if some elements of args are not Lea instances, then these are coerced
            to a Lea instance with probability 1;
            if optional arg fast is False (default), then
                returns a Flea2 instance or, if there is only one argument in args,
                this argument unchanged; 
                the returned distribution keeps dependencies with args but the 
                calculation could be prohibitively slow (exponential complexity);
            if optional arg fast is True,
                returns an Alea instance;
                the method uses an efficient algorithm (linear complexity), which is
                due to Nicky van Foreest;
                however, unlike most of Lea methods, the distribution returned loses
                any dependency with given args; this could be important if some args
                appear in the same expression as Lea.max(...) but outside it, e.g.
                conditional probability expressions
            requires at least one argument in args
        '''        
        fast = kwargs.get('fast',False)
        if fast:
            alea_args = (Alea.coerce(arg).get_alea() for arg in args)
            return Alea.fast_extremum(Alea.p_cumul,*alea_args)
        args_iter = iter(args)
        max_lea = next(args_iter)
        for arg in args_iter:
            max_lea = Flea2(max2,max_lea,arg)
        return max_lea

    ## in PY3, could use
    ## def min_of(*args,fast=False):
    @staticmethod
    def min_of(*args,**kwargs):
        ''' static method, returns a Lea instance giving the probabilities to have
            the minimum value of each combination of the given args;
            if some elements of args are not Lea instances, then these are coerced
            to a Lea instance with probability 1;
            if optional arg fast is False (default), then
                returns a Flea2 instance or, if there is only one argument in args,
                this argument unchanged; 
                the returned distribution keeps dependencies with args but the 
                calculation could be prohibitively slow (exponential complexity);
            if optional arg fast is True,
                returns an Alea instance;
                the method uses an efficient algorithm (linear complexity), which is
                due to Nicky van Foreest;
                however, unlike most of Lea methods, the distribution returned loses
                any dependency with given args; this could be important if some args
                appear in the same expression as Lea.max(...) but outside it, e.g.
                conditional probability expressions
            requires at least one argument in args
        '''
        fast = kwargs.get('fast',False)
        if fast:
            alea_args = (Alea.coerce(arg).get_alea() for arg in args)
            return Alea.fast_extremum(Alea.p_inv_cumul,*alea_args)
        args_iter = iter(args)
        min_lea = next(args_iter)
        for arg in args_iter:
            min_lea = Flea2(min2,min_lea,arg)
        return min_lea

    def _get_lea_children(self):
        ''' returns a tuple containing all the Lea instances children of the current Lea;
            Lea._get_lea_children method is abstract: it is implemented in all Lea's subclasses;
            it shall contain one entry per occurrence, NOT per instance (duplicates shall not
            be removed)
        '''
        raise NotImplementedError("missing method '%s._get_lea_children(self)'"%(self.__class__.__name__))

    def _clone_by_type(self,clone_table):
        ''' returns a deep copy of current Lea, without any value binding;
            all Lea instances are copied, excepting the instances k referred in (k,v) associations
            of given clone_table dictionary, in such case the instance referred by v is used instead
            of instance referred by k; otherwise, a new entry (k,v) is put in clone_table, where u
            is a reference to the newly created clone of k; so, if the Lea tree contains multiple
            references to the same Lea instance, then this instance is cloned only once and its
            references are copied in the cloned DAG;
            Lea._clone method is abstract: it is implemented in all Lea's subclasses
        '''
        raise NotImplementedError("missing method '%s._clone(self,clone_table)'"%(self.__class__.__name__))
        
    def _gen_vp(self):
        ''' generates tuples (v,p) where v is a value of the current probability distribution
            and p is a probability such that the sum of all probabilities yielded for v is the
            probability that self equals v;
            this obeys the "binding" mechanism, so if the same variable is referred multiple times in
            a given expression, then same value will be yielded at each occurrence;
            Lea._gen_vp method is abstract: it is implemented in all Lea's subclasses
        '''
        raise NotImplementedError("missing method '%s._gen_vp(self)'"%(self.__class__.__name__))

    def _gen_one_random_mc(self):
        ''' generates one random value from the current probability distribution,
            WITHOUT precalculating the exact probability distribution (contrarily to 'random' method);
            Lea._gen_one_random_mc method is abstract: it is implemented in all Lea's subclasses;
            see Lea.gen_one_random_mc method
        '''
        raise NotImplementedError("missing method '%s._gen_one_random_mc(self)'"%(self.__class__.__name__))

    def gen_one_random_mc(self,nb_subsamples=1):
        ''' generates one random value from the current probability distribution,
            WITHOUT precalculating the exact probability distribution (contrarily to 'random' method);
            this obeys the "binding" mechanism, so if the same variable is referred multiple times in
            a given expression, then same value will be yielded at each occurrence; 
            before yielding the random value v, this value v is bound to the current instance;
            if the current calculation requires to get again a random value on the current instance,
            then the bound value is yielded;
            the instance is rebound to a new value at each iteration, as soon as the execution
            is resumed after the yield;
            the instance is unbound at the end;
            the actual random value is yielded by _gen_one_random_mc method, which is implemented in
            each Lea subclass;
            nb_subsamples is not used in present Lea.gen_one_random_mc method; it is used in the
            overloaded Ilea.gen_one_random_mc method
        '''
        if self._val is not self:
            # distribution already bound to a value, because gen_one_random_mc has been called already on self;
            # yield the bound value, to ensure referential consistency 
            yield self._val
        else:
            # distribution not yet bound
            try:
                # get random value from _gen_one_random_mc method defined in Lea subclass
                # (this generator create some binding by calling gen_one_random_mc)
                for v in self._gen_one_random_mc():
                    # bind value v: this is important if an object calls gen_one_random_mc on the same
                    # instance before resuming the present generator (see above)
                    self._val = v
                    yield v
            finally:
                # unbind value, after the random value has been bound or if an exception has been raised
                self._val = self

    def gen_random_mc(self,nb_samples,nb_subsamples=1,nb_tries=None):
        ''' generates nb_samples random values from the current probability distribution,
            without precalculating the exact probability distribution (contrarily to 'random' method);
            nb_tries, if not None, defines the maximum number of trials in case a random
            value is incompatible with a condition; this happens only if the conditioned part
            is itself an Ilea instance x.given(e) or is referring to such instance;
            nb_subsamples (default: 1) may greater than 1 only if self is an Ilea instance, i.e. a
            conditional probability x.given(e); it specifies the number of random samples made on x
            for each binding verifying the condition e; nb_subsamples shall be a divisor of nb_samples; 
        '''
        if nb_subsamples == 1:
            act_nb_samples = nb_samples
        else:
            if not isinstance(self,Ilea):
                raise Lea.Error("nb_subsamples argument can only be specified for sampling expressions under condition, i.e. x.given(...) constructs")
            (act_nb_samples,residue) = divmod(nb_samples,nb_subsamples)
            if residue > 0:
                raise Lea.Error("nb_subsamples argument (%s) shall be a divisor of nb_samples argument (%s)"%(nb_subsamples,nb_samples))
        for _ in range(act_nb_samples):
            remaining_nb_tries = 1 if nb_tries is None else nb_tries
            v = self
            while remaining_nb_tries > 0:
                try:
                    for v in self.gen_one_random_mc(nb_subsamples):
                        yield v
                    remaining_nb_tries = 0
                except Lea._FailedRandomMC:
                    if nb_tries is not None:
                        remaining_nb_tries -= 1        
            if v is self:
                raise Lea.Error("impossible to validate given condition(s), after %d random trials"%(nb_tries,)) 
    
    def random_mc(self,nb_samples=None,nb_tries=None):
        ''' if nb_samples is None, returns a random value with the probability given by the distribution
            without precalculating the exact probability distribution (contrarily to 'random' method);
            otherwise, returns a tuple of nb_samples such random values;
            nb_tries, if not None, defines the maximum number of trials in case a random value
            is incompatible with a condition; this happens only if the current Lea instance
            is (referring to) an Ilea or Blea instance, i.e. 'given' or 'cpt' methods;
            WARNING: if nb_tries is None, any infeasible condition shall cause an infinite loop
        '''
        act_nb_samples = 1 if nb_samples is None else nb_samples
        random_mc_tuple = tuple(self.gen_random_mc(act_nb_samples,nb_tries=nb_tries))
        if nb_samples is None:
            return random_mc_tuple[0]
        return random_mc_tuple

    def estimate_mc(self,nb_samples,nb_tries=None): 
        ''' convenience method equivalent to
              calc(algo=MCRS,nb_samples=nb_samples,nb_tries=nb_tries)
            returns an Alea instance, which is an approximate probability distribution
            following the MC rejection sampling algorithm on nb_samples random samples;
            the method is suited for complex distributions, when calculation of exact probability
            distribution is intractable; the larger the value of nb_samples, the better the
            returned estimation;
            nb_tries (default: None): if not None, defines the maximum number of trials in case a random
            value is incompatible with a condition; this happens only if the current Lea instance is an Ilea
            instance x.given(e) or is referring to such instance;
            if a condition cannot be satisfied after nb_tries tries, then an error exception is raised; 
            WARNING: if nb_tries is None, any infeasible condition shall cause an infinite loop;
        '''
        return self.calc(algo=Lea.MCRS,nb_samples=nb_samples,nb_tries=nb_tries)
    
    def nb_cases(self,bindings=None,memoization=True):
        ''' returns the number of atomic cases evaluated to build the exact probability distribution;
            this provides a measure of the complexity of the probability distribution
            * bindings argument: see Lea.calc method
            * memoization argument: see Lea.calc method
        '''
        try:
            self._init_calc(bindings,memoization,optimize=False)
            return sum(1 for vp in self.gen_vp())
        finally:
            self._finalize_calc(bindings)

    def is_certain_value(self):
        ''' returns True iff there is only one possible value, having probability 1
                    False otherwise
        '''
        return len(tuple(None for (_,p) in self._gen_raw_vps() if p > 0)) == 1 

    def get_certain_value(self):
        ''' returns the value having probability 1
            requires that such value exists (i.e. self.is_certain_value() returns True)
        '''
        vs = tuple(v for (v,p) in self._gen_raw_vps() if p > 0)
        if len(vs) != 1:
            raise Lea.Error("multiple values have a non-null probability")
        return vs[0]

    def is_true(self):
        ''' returns True iff the value True has probability 1;
                    False otherwise;
            raises exception if some value is not boolean
        '''
        return self._p(True,check_val_type=True) == 1

    def is_feasible(self):
        ''' returns True iff the value True has a non-null probability;
                    False otherwise;
            raises exception if some value is not boolean
        '''
        return self._p(True,check_val_type=True) > 0

    def as_string(self,kind=None,nb_decimals=6,chart_size=100,tabular=True):
        ''' returns, after evaluation of the probability distribution self, a string
            representation of it;
            it contains one line per distinct value, separated by a newline character;
            each line contains the string representation of a value with its
            probability in a format depending of given kind, which is either None
            (default) or a string among
                '/', '.', '%', '-', '/-', '.-', '%-';
            the probabilities are displayed as
            - if kind is None   : as they are stored
            - if kind[0] is '/' : rational numbers "n/d" or "0" or "1"
            - if kind[0] is '.' : decimals with given nb_decimals digits
            - if kind[0] is '%' : percentage decimals with given nb_decimals digits
            - if kind[0] is '-' : histogram bar made up of repeated '-', such that
                                  a bar length of histo_size represents a probability 1 
            if kind[1] is '-', the histogram bars with '-' are appended after 
                               numerical representation of probabilities
            if an order relationship is defined on values, then the values are sorted by 
            increasing order; otherwise, an arbitrary order is used;
            if tabular is True (default), then if values are tuples of same length, then
            these are represented in a tabular format (fixed column width); in the
            specific cases of named tuple, a header line is prepended with the field names
        '''
        return self.get_alea().as_string(kind,nb_decimals,chart_size,tabular)

    def __str__(self):
        ''' returns, after evaluation of the probability distribution self, a string
            representation of it;
            it contains one line per distinct value, separated by a newline character;
            each line contains the string representation of a value  with its
            probability expressed as a rational number "n/d" or "0" or "1";
            if an order relationship is defined on values, then the values are sorted by 
            increasing order; otherwise, an arbitrary order is used;
            called on evaluation of "str(self)" and "repr(self)"
        '''        
        return self.get_alea().__str__()

    __repr__ = __str__

    def as_float(self,nb_decimals=6):
        ''' returns, after evaluation of the probability distribution self, a string
            representation of it;
            it contains one line per distinct value, separated by a newline character;
            each line contains the string representation of a value with its
            probability expressed as decimal with given nb_decimals digits;
            if an order relationship is defined on values, then the values are sorted by 
            increasing order; otherwise, an arbitrary order is used;
        '''
        return self.get_alea().as_float(nb_decimals)

    def as_pct(self,nb_decimals=1):
        ''' returns, after evaluation of the probability distribution self, a string
            representation of it;
            it contains one line per distinct value, separated by a newline character;
            each line contains the string representation of a value with its
            probability expressed as percentage with given nb_decimals digits;
            if an order relationship is defined on values, then the values are sorted by 
            increasing order; otherwise, an arbitrary order is used;
        '''
        return self.get_alea().as_pct(nb_decimals)
    
    def histo(self,size=100):
        ''' returns, after evaluation of the probability distribution self, a string
            representation of it;
            it contains one line per distinct value, separated by a newline character;
            each line contains the string representation of a value with its
            probability expressed as a histogram bar made up of repeated '-',
            such that a bar length of given size represents a probability 1
            if an order relationship is defined on values, then the values are sorted by 
            increasing order; otherwise, an arbitrary order is used;
        '''
        return self.get_alea().histo(size)

    def plot(self,title=None,fname=None,savefig_args=dict(),**bar_args):
        ''' produces, after evaluation of the probability distribution self,
            a matplotlib bar chart representing it with the given title (if not None);
            the bar chart may be customized by using named arguments bar_args, which are
            relayed to matplotlib.pyplot.bar function
            (see doc in http://matplotlib.org/api/pyplot_api.html)
            * if fname is None, then the chart is displayed on screen, in a matplotlib window;
              the previous chart, if any, is erased
            * otherwise, the chart is saved in a file specified by given fname as specified
              by matplotlib.pyplot.savefig; the file format may be customized by using
              savefig_args argument, which is a dictionary relayed to matplotlib.pyplot.savefig
              function and containing named arguments expected by this function;
              example:
               flip.plot(fname='flip.png',savefig_args=dict(bbox_inches='tight'),color='green')
            the method requires matplotlib package; an exception is raised if it is not installed
        '''
        self.get_alea().plot(title,fname,savefig_args,**bar_args)

    def get_alea(self,sorting=True):
        ''' returns an Alea instance representing the distribution after it has been evaluated
            considering, if any, explicit bindings and evidence contexts;
            the sorting argument (default True) allows sorting the value of the returned Alea
            instance (see Alea.pmf method);
            in most simple cases, the newly created Alea is cached: the evaluation occurs only
            for the first call
        '''
        has_explicit_bindings = any((a._val is not a) for a in self.get_alea_leaves_set())
        is_not_cacheable = has_explicit_bindings or EvidenceCtx.has_evidence()
        if self._alea is None or is_not_cacheable:
            new_alea = self.new(sorting=sorting)
            if is_not_cacheable:
                self_alea = None
                return new_alea
            self._alea = new_alea
        return self._alea

    def reset(self):
        ''' erases the Alea cache, so to force the recalculation at next call to get_alea();
            note: there is no need to call this method, except for freeing memory or for making
            cleanup after hacking private attributes of Lea instances assumed immutable
        ''' 
        self._alea = None

    def is_bindable(self,v):
        ''' returns True iff self is bindable to given value v,
            i.e. self is an Alea instance (i.e. not dependent of other Lea instances);
            and v is present in the domain of self
        '''
        return False

    def observe(self,v):
        ''' (re)binds self with given value v;
            requires that self is an Alea instance (i.e. not dependent of other Lea instances);
            requires that v is present in the domain of self
        '''
        raise Lea.Error("impossible to bind %s because it depends of other instances"%(self._id(),))

    def free(self,check=True):
        ''' unbinds self;
            requires that self is an Alea instance (i.e. not dependent of other Lea instances);
            if check is True, then requires that self is bound
        '''
        if check:
            raise Lea.Error("impossible to unbind %s because it depends of other instances"%(self._id(),))

    def clone(self,shared=(),n=None):
        ''' returns a deep copy of current Lea, without any value binding;
            if n is not None, then a tuple containing n new instances is returned;
            all Lea instances are cloned, excepting the instances present in given iterable shared,
            these instances are shared between the cloned and the original instances; 
            if the Lea tree contains multiple references to the same Lea instance, then this instance
            is cloned only once and its references are copied in the cloned tree
        '''
        clone_table = dict((lea1,lea1) for lea1 in shared)
        if n is not None:
            return tuple(self._clone(clone_table.copy()) for _ in range(n))
        return self._clone(clone_table)

    def _clone(self,clone_table):
        ''' returns a deep copy of current Lea, without any value binding;
            all Lea instances are copied, excepting the instances k referred in (k,v) associations
            of given clone_table dictionary, in such case the instance referred by v is used instead
            of instance referred by k; otherwise, a new entry (k,v) is put in clone_table, where u
            is a reference to the newly created clone of k; so, if the Lea tree contains multiple
            references to the same Lea instance, then this instance is cloned only once and its
            references are copied in the cloned DAG;
            the method calls the _clone_by_type() method implemented in Lea's subclasses
        '''
        cloned_lea = clone_table.get(self)
        if cloned_lea is None:
            cloned_lea = self._clone_by_type(clone_table)
            clone_table[self] = cloned_lea
            if self._alea is not None:
                cloned_lea._alea = self._alea
        return cloned_lea

    def new(self,n=None,prob_type=-1,sorting=True,normalization=True):
        ''' returns a new Alea instance representing the distribution after it has been evaluated;
            if self is an Alea, then it returns a copy of itself representing an independent event;
            the probability type used in the returned instance depends on given prob_type:
            * if n is not None, then a tuple containing n new independent Alea instances is returned
            * if prob_type is -1, then the probability type is the same as self's
              otherwise, the probability type is defined using prob_type (see doc of Alea.set_prob_type);
            * sorting allows sorting the value of the returned Alea instance (see Alea.pmf method);
            * normalization (default: True): if True, then each probability is divided by the sum of
              all probabilities
            note that the present method is overloaded in Alea class, to be more efficient
        '''
        new_alea = self.calc(prob_type=prob_type,sorting=sorting,normalization=normalization)
        if n is not None:
            return tuple(new_alea.new(normalization=False) for _ in range(n))
        return new_alea

    EXACT = 'EXACT'
    MCRS = 'MCRS'
    MCLW = 'MCLW'
    MCEV = 'MCEV'

    def _check_calc_arg(self,algo,nb_samples,nb_subsamples,nb_tries,exact_vars):
        ''' checks consistency of calc method's arguments;
            see calc method;
            raises an exception if arguments are inconsistent
        '''
        if algo == Lea.EXACT:
            if nb_samples is not None:
                raise Lea.Error("nb_samples argument incompatible with EXACT algorithm")        
            if nb_subsamples is not None:
                raise Lea.Error("nb_subsamples argument incompatible with EXACT algorithm")        
            if nb_tries is not None:
                raise Lea.Error("nb_tries argument incompatible with EXACT algorithm")        
            if exact_vars is not None:
                raise Lea.Error("exact_vars argument incompatible with EXACT algorithm")        
            if nb_samples is not None or nb_subsamples is not None or nb_tries is not None:
                raise Lea.Error("nb_samples, nb_subsamples and nb_tries arguments incompatible with EXACT algorithm")        
        elif algo == Lea.MCRS:
            if not isinstance(self,Ilea) and nb_subsamples is not None:
                raise Lea.Error("nb_subsamples argument incompatible with MCRS algorithm, unless for expressions under condition, i.e. x.given(...) constructs")
            if nb_samples is None:
                raise Lea.Error("nb_samples argument is required for MCRS algorithm")
            if exact_vars is not None:
                raise Lea.Error("exact_vars argument incompatible with MCRS algorithm")        
        elif algo == Lea.MCLW:
            if not isinstance(self,Ilea):
                raise Lea.Error("MCLW algorithm can only be used for expressions under condition, i.e. x.given(e)")
            if exact_vars is not None and any(isinstance(inner_lea,Ilea) for inner_lea in self._lea1.get_inner_lea_set()):
                raise Lea.Error("MCLW algorithm with exact_vars cannot handle embedded conditions, e.g x.given(e1).given(e2); use factorized conditions insted, e.g. x.given(e1,e2)")
            if nb_samples is not None:
                raise Lea.Error("nb_samples argument incompatible with MCLW algorithm")
            if nb_subsamples is None:
                raise Lea.Error("MCLW algorithm requires a nb_subsamples argument")
        elif algo == Lea.MCEV:
            if any(isinstance(inner_lea,Ilea) for inner_lea in self.get_inner_lea_set()):
                raise Lea.Error("MCEV algorithm cannot handle expressions under condition, i.e. x.given(e); use MCLW instead")
            if nb_samples is not None:
                raise Lea.Error("nb_samples argument incompatible with MCEV algorithm")
            if nb_subsamples is None:
                raise Lea.Error("MCEV algorithm requires a nb_subsamples argument")
            if exact_vars is None:
                raise Lea.Error("MCEV algorithm requires an exact_vars argument")
        else:
            raise Lea.Error("algo argument shall be %s, %s, %s or %s"%(Lea.EXACT,Lea.MCRS,Lea.MCLW,Lea.MCEV))

    def calc(self,prob_type=-1,sorting=True,normalization=True,bindings=None,memoization=True,
             algo=EXACT,optimize=True,nb_samples=None,nb_subsamples=None,nb_tries=None,exact_vars=None,debug=False):
        ''' returns a new Alea instance representing the distribution after it has been evaluated;
            the first three arguments allow customizing the Alea instance returned:
            * prob_type (default: -1): if -1, then the probability type is the same as self's,
              otherwise, the probability type is defined using prob_type (see doc of Alea.set_prob_type);
            * sorting (default: True): allows sorting the value of the returned Alea instance (see Alea.pmf method);
            * normalization (default: True): if True, then each probability is divided
              by the sum of all probabilities before being stored; this division is essential to
              get correct results in case of conditional probabilities;
              setting normalization=False is useful,
              - to speed up if the caller guarantees that the probabilities sum is 1
              - or to get non-normalized probabilities of a subset of a given probability distribution
            the two following arguments change the problem statement:
            * bindings (default: None): if not None, it required to be a dictionary {a1:v1, a2:v2 ,... }
              associating some Alea instances a1, a2, ... to specific values v1, v2, ... of their
              respective domains; these Alea instances are then temporarily bound for calculating
              the resulting pmf; this offers an optimization over the self.given(a1==v1, a2==v2, ...)
              construct: this last gives the same result but requires browsing the whole v1, v2, ...
              domains, evaluating the given equalities; specifying the bindings argument requires that
              keys are all unbound Alea instances and that the bindings values are in the expected
              domains of associated keys;
            * memoization (default: True): if False, then no binding is performed by the algorithm,
              hence reference consistency is no more respected; this option returns WRONG results in all
              construction referring multiple times to the same instances (e.g. conditional probability
              and Bayesian reasoning); this option has no real use, excepting demonstrating by absurd the
              importance of memoization and referential consistency in the Statues algorithm; note that
              this option offers NO speedup when evaluating expressions not requiring referential
              consistency: such cases are already detected and optimized by the calculation preprocessing
              (see Lea._init_calc);
            the last arguments specify the evaluation algorithm and related options: 
            * algo (default: EXACT): four algorithms are available:
              - EXACT: calculates the exact probability distribution using the Statues algorithm;
                for such choice, the remaining arguments shall not be used; 
              - MCRS (Monte-Carlo Rejection Sampling): calculates an approximate probability distribution
                following the MC rejection sampling algorithm on nb_samples random samples;
                if self is an Ilea instance, i.e. evaluating a conditional probability x.given(e), then the
                algorithm may be speed up by specifying the nb_subsamples argument, which shall be a divisor
                of nb_samples; each time the condition e is satisfied, nb_subsamples random samples are taken
                on the conditioned part x instead of a single one; specifying nb_subsamples is especially
                valuable if the condition has a small probability;
              - MCLW (Monte-Carlo Likelihood Weighting): this requires that self is an Ilea instance,
                i.e. a conditional probability x.given(e); this algorithm calculates an approximate
                probability distribution by making first an exact evaluation of the condition e using the
                Statues algorithm; then, for each binding that verifies the condition with some probability p,
                it makes nb_subsamples random samples on the conditioned part x, assigning a weight p to these
                samples; this algorithm is especially valuable if the condition has a small probability while
                its exact evaluation is tractable; this algorithm accepts also an optional exact_vars argument,
                to include given variables in the exact evaluation, beyond these already referred in the
                condition (see MCEV);
              - MCEV (Monte-Carlo Exact Variables): calculates an approximate probability distribution
                by making first an exact evaluation of the variables given in exact_vars using the Statues
                algorithm; for each binding found with some probability p, it makes nb_subsamples random
                samples on remaining (unbound) variables, assigning a weight p to these samples;
                MCEV algorithm cannot handle expressions under condition, i.e. x.given(e); MCLW shall be
                used instead;
            * optimize (default: true), considered only if algo=EXACT, if true then independent sub-DAG are
               searched in the DAG rooted by self; if such independent sub-DAG are found, then their roots
               are evaluated using EXACT algorithm and replaced by resulting Alea instances; for some DAG
               presenting inner tree patterns, this divide-and-conquer process may save a lot of calculations;
               putting optimize=False allows getting the behavior of Lea versions prior to 3.4.0. and
               highlighting the effect of optimization
            * nb_samples (default: None): number of random samples made for MCRS algorithm;
            * nb_subsamples (default: None): only for MCRS and MCLW algorithms and if self is
              an Ilea instance, i.e. a conditional probability x.given(e); it specifies the number of random
              samples made on x for each binding verifying the condition e;
              for MCRS, nb_subsamples is optional, if specified it shall be a divisor of nb_samples; 
              for MCLW, nb_subsamples is mandatory;
            * nb_tries (default: None): if not None, defines the maximum number of trials in case a random
              value is incompatible with a condition; this happens only if the current Lea instance is an Ilea
              instance x.given(e) or is referring to such instance;
              for MCLW algorithm on x.given(e), it only applies on x, should it refers to Ilea instances,
              since e is evaluated using the exact algorithm;
              if a condition cannot be satisfied after nb_tries tries, then an error exception is raised; 
              WARNING: if nb_tries is None, any infeasible condition shall cause an infinite loop;
            * exact_vars (default: None): only for MCEV algorithm: an iterable giving the variables
              referred in self that shall be evaluated by using the exact algorithm, the other ones being
              subject to random sampling;
            * debug (default: False): displays debug trace on standard output
            On choosing the right algorithm and options...
            EXACT is the default algorithm; it is the recommended algorithm for all tractable problems;
            it allows in particular to work with probability fractions and symbols;
            for untractable problems, the three other algorithms offer fallback options;
            MCRS algorithm with sole nb_samples argument is the easiest option; choosing the value for
            nb_samples is a matter of trade-off between result accuracy and execution time;
            if the evaluated expression contains conditions having low probabilities, then the MCRS
            algorithm may be inefficient: as a rejection sampling algorithm, it may use most of processing
            time to find bindings satisfying the condition; for improving the efficiency, the nb_subsamples
            argument can be used: this allows making multiple random samples each time the condition is met,
            instead of a single one; the samples are generated until the condition has been satisfied n times,
            with n = nb_samples/nb_subsamples. For a given nb_samples, increasing nb_subsamples shall speed up
            the calculation; however, the result accuracy may tend to decrease if the condition is not visited
            enough (e.g. choosing nb_subsamples=nb_samples will satisfy the condition with only one binding).
            MCLW algorithm with mandatory nb_subsamples argument is the best choice if the evaluation
            of the conditioned part is untractable meanwhile the condition is tractable (whatever its
            probability); every binding verifying the condition is covered and, for each one, nb_subsamples
            random samples are generated, weighted by the binding's probability;
            MCEV algorithm is suited for untractable problems, from which a set of variables v1, ..., vn
            can be evaluated in a reasonable time or, in other words, if joint(v1,...,vn) is tractable;
            if this set of variables is specified in exact_vars argument, then all their value combinations are
            browsed systematically by the exact algorithm while random sampling is done for other variables.
        '''
        if EvidenceCtx.has_evidence():
            lea1 = Ilea(self,())
        else:
            lea1 = self
        lea1._check_calc_arg(algo,nb_samples,nb_subsamples,nb_tries,exact_vars)
        if algo == Lea.MCEV or algo == Lea.MCLW:
            if exact_vars is None:
                exact_vars_lea = Alea.coerce(None)
            else:
                exact_vars_lea = Clea(*exact_vars)
            lea_scope = Clea(lea1,exact_vars_lea)
        else:
            lea_scope = lea1
        try:
            if algo != Lea.EXACT:
                optimize = False
            lea_scope._init_calc(bindings,memoization,optimize,debug)
            if algo == Lea.EXACT:
                vps = lea1.gen_vp()
            elif algo == Lea.MCRS:
                if nb_subsamples is None:
                    nb_subsamples = 1
                vps = ((v,1) for v in lea1.gen_random_mc(nb_samples,nb_subsamples,nb_tries))
            elif algo == Lea.MCLW:
                vps = lea1._gen_vp_mclw(nb_subsamples,exact_vars_lea,nb_tries)
            elif algo == Lea.MCEV:
                vps = lea1._gen_vp_mcev(nb_subsamples,exact_vars_lea,nb_tries)
            return Alea.pmf(vps,prob_type=prob_type,sorting=sorting,normalization=normalization)
        finally:
            lea_scope._finalize_calc(bindings)
        
    def _gen_vp_mcev(self,nb_subsamples,exact_vars_lea,nb_tries=None):
        ''' generates tuple (v,p) where v is a value of the current probability distribution
            and p is the associated probability weight; this implements the MCEV algorithm
            (Monte-Carlo Exact Variables): exact inference on given exact_vars_lea,
            then, for each binding found, nb_subsamples random samples for remaining (unbound)
            variables; nb_tries, if not None, defines the maximum number of trials in case a random
            value is incompatible with a condition; this happens only if the current Lea instance
            is an Ilea instance x.given(e) or is referring to such instance;
        '''
        for (_,p) in exact_vars_lea.gen_vp():
            for v in self.gen_random_mc(nb_samples=nb_subsamples,nb_tries=nb_tries):
                yield (v,p)

    def cumul(self):
        ''' evaluates the distribution, then,
            returns a tuple with probabilities p that self <= value ;
            the sequence follows the order defined on values (if an order relationship is defined
            on values, then the tuples follows their increasing order; otherwise, an arbitrary
            order is used, fixed from call to call
            Note : the returned value is cached
        '''
        return tuple(Alea._downcast(p) for p in self.get_alea().cumul())
        
    def inv_cumul(self):
        ''' evaluates the distribution, then,
            returns a tuple with the probabilities p that self >= value ;
            the sequence follows the order defined on values (if an order relationship is defined
            on values, then the tuples follows their increasing order; otherwise, an arbitrary
            order is used, fixed from call to call
            Note : the returned value is cached
        '''
        return tuple(Alea._downcast(p) for p in self.get_alea().inv_cumul())
        
    def random_iter(self):
        ''' evaluates the distribution, then,
            generates an infinite sequence of random values among the values of self,
            according to their probabilities
        '''
        return self.get_alea()._random_iter
        
    def random(self,n=None):
        ''' evaluates the distribution, then, 
            if n is None, returns a random value with the probability given by the distribution
            otherwise, returns a tuple of n such random values
        '''
        if n is None:
            return self.get_alea().random_val()
        return tuple(islice(self.random_iter(),int(n)))

    def random_draw(self,n=None,sorted=False):
        ''' evaluates the distribution, then,
            if n=None, then returns a tuple with all the values of the distribution, in a random order
                       respecting the probabilities (the higher probability of a value, the most likely
                       the value will be in the beginning of the sequence)
            if n > 0,  then returns only n different drawn values
            if sorted is True, then the returned tuple is sorted
        '''
        return self.get_alea().random_draw(n,sorted)
  
    def cross_entropy(self,lea1,entropy_ceiling=True):
        ''' static method, returns the cross-entropy between self and given lea1;
            the logarithm base is 2;
            requires that all values of lea1's support have a non-null probability in self;
            notes:
            - the cross-entropy is non-commutative;
            - the cross-entropy should always be greater than the entropy of first argument,
              the equality being reached if both arguments have same pmf; if argument
              entropy_ceiling is True (default), then this is guaranteed by the implementation,
              even in case of rounding errors;
            - if self is interpreted as frequencies of observed data having N as total number
              of samples, then the cross-entropy is linked to (negative) log-likelihood by
                log-likelihood = - N * cross-entropy
              using logarithm in base 2 (for other base, use the right factor)
        '''
        lea1_pmf_dict = lea1.pmf_dict
        try:
            ce = -sum(px*log2(lea1_pmf_dict[vx]) for (vx,px) in self._gen_vps() if px > 0)
        except KeyError as key_error:
            raise Lea.Error("observed value '%s' is not produced by given model"%(key_error.args[0],))
        except ValueError:
            raise Lea.Error("some observed value has null probability in given model")
        if entropy_ceiling:
            ce = max(ce,self.entropy)
        return ce

    def kl_divergence(self,lea1,zero_ceiling=True):
        ''' returns the Kullback-Leibler divergence between self and given lea1;
            the logarithim base is 2;
            requires that all values of lea1's support have a non-null probability in self;
            notes:
            - the KL divergence is also known as "relative entropy";
            - the KL divergence is non-commutative;
            - the KL divergence should always be positive; it is null if both arguments have
              same pmf; if argument zero_ceiling is True (default), then this is guaranteed
              by the implementation, even in case of rounding errors
        '''
        kld = self.cross_entropy(lea1,entropy_ceiling=False) - self.entropy
        if zero_ceiling:
            kld = max(kld,0.0)
        return kld

    @staticmethod
    def joint_entropy(*args):
        ''' static method, returns the joint entropy of arguments, expressed in bits;
            the returned type is a float or a sympy expression (see doc of Alea.entropy)
        '''
        return Clea(*args).entropy

    def cond_entropy(self,other):
        ''' returns the conditional entropy of self given other, expressed in
            bits; note that this value is also known as the equivocation of
            self about other;
            the returned type is a float or a sympy expression (see doc of
            Alea.entropy)
        '''
        other = Alea.coerce(other)
        ce = Clea(self,other).entropy - other.entropy
        try:
            return max(0.0,ce)
        except:
            return ce

    def _cov(self,lea1):
        ''' same as cov method but without conversion nor simplification
        '''
        return ((self-self.get_alea()._mean())*(lea1-lea1.get_alea()._mean())).get_alea()._mean()

    def cov(self,lea1):
        ''' returns the covariance between self and given lea1 probability distributions;
            requires that, for self and lea1,
            1 - the requirements of the mean() method are met,
            2 - the values can be subtracted to the mean value,
            3 - the differences between values and the mean value can be multiplied together;
            if any of these conditions is not met, then the result depends of the
            value implementation (likely, raised exception)
        '''            
        return Alea._downcast(Alea._simplify(self._cov(lea1),False))

    def cov_f(self,lea1):
        ''' same as cov method but with conversion to float or simplification
            of symbolic expression;
        '''
        return Alea._simplify(self._cov(lea1),True)
    
    @staticmethod
    def mutual_information(lea1,lea2):
        ''' static method, returns the mutual information between given arguments,
            expressed in bits;
            the returned type is a float or a sympy expression (see doc of
            Alea.entropy)
        '''
        lea1 = Alea.coerce(lea1)
        lea2 = Alea.coerce(lea2)
        mi = lea1.entropy + lea2.entropy - Clea(lea1,lea2).entropy
        try:
            return max(0.0,mi)
        except:
            return mi

    def information_of(self,val):
        ''' returns, after evaluation of the probability distribution self,
            the information of given val, expressed in bits;
            the returned type is a float or a sympy expression (see doc of
            Alea.entropy);
            raises an exception if given val has a null probability
        '''
        return self.get_alea().information_of(val)

    def lr(self,*hyp_leas):
        ''' returns a float giving the likelihood ratio (LR) of an 'evidence' E,
            which is self, for a given 'hypothesis' H, which is the AND of given
            hyp_leas arguments; it is calculated as 
                  P(E | H) / P(E | not H)
            both E and H must be boolean probability distributions, otherwise
            an exception is raised;
            an exception is raised also if H is certainly true or certainly false      
        '''
        return self.given(*hyp_leas).lr()

    def internal(self,full=False,_indent='',_refs=None):
        ''' returns a string representing the inner definition of self, with
            children leas recursively up to Alea leaves; if the same lea child
            appears multiple times, then it is expanded only on the first
            occurrence, the other ones being marked with reference id;
            if full is False (default), then only the first element of Alea
            instances is displayed, otherwise all elements are displayed;
            the other arguments are used only for recursive calls, they can
            be ignored for a normal usage;
            note: this method is overloaded in Alea class
        '''
        if _refs is None:
            _refs = set()
        if self in _refs:
            args = [self._id()+'*']
        else:
            _refs.add(self)
            args = [self._id()]
            for attr_name in self.__slots__:
                attr_val = getattr(self,attr_name)
                if isinstance(attr_val,Lea):
                    args.append(attr_val.internal(full,_indent+'  ',_refs))
                elif isinstance(attr_val,tuple):
                    args1 = [lea1.internal(full,_indent+'    ',_refs) for lea1 in attr_val]
                    args1[0] = '( ' + args1[0]
                    args.append(('\n'+_indent+'    ').join(args1)+'\n'+_indent+'  )')
                elif isinstance(attr_val,dict):
                    args1 = ["'%s': %s"%(k,v.internal(full,_indent+'    ',_refs) if isinstance(v,Lea) else v)
                             for (k,v) in attr_val.items()]
                    args1[0] = '{ ' + args1[0]
                    args.append(('\n'+_indent+'    ').join(args1)+'\n'+_indent+'  }')
                elif hasattr(attr_val,'__call__'):
                    args.append(attr_val.__module__+'.'+attr_val.__name__)
        return ('\n'+_indent+'  ').join(args)

    def __hash__(self):
        return id(self)

    def __bool__(self):
        ''' raises an exception telling that Lea instance cannot be evaluated as a boolean
            called on evaluation of "bool(self)", "if self:", "while self:", etc
        '''
        raise Lea.Error("Lea instance cannot be evaluated as a boolean")

    # Python 2 compatibility
    __nonzero__ = __bool__
    
    @staticmethod
    def _check_booleans(op_msg,*vals):
        ''' static method, raises an exception if any of vals arguments is not boolean;
            the exception message refers to the name of a logical operation given in the op_msg argument
        '''
        for val in vals:
            if val != True and val != False:
                raise Lea.Error("non-boolean object involved in %s logical operation (maybe due to a lack of parentheses)"%(op_msg,)) 

    # create helper functions for defining magic methods,
    # these are used only at class creation; these are unbound below
    
    def __safe_and(a,b):
        ''' static method, returns a boolean, which is the logical AND of the given boolean arguments; 
            raises an exception if any of arguments is not boolean
        '''
        Lea._check_booleans('AND',a,b)
        return operator.and_(a,b)

    def __safe_or(a,b):
        ''' static method, returns a boolean, which is the logical OR of the given boolean arguments; 
            raises an exception if any of arguments is not boolean
        '''
        Lea._check_booleans('OR',a,b)
        return operator.or_(a,b)

    def __safe_xor(a,b):
        ''' static method, returns a boolean, which is the logical XOR of the given boolean arguments; 
            raises an exception if any of arguments is not boolean
        '''
        Lea._check_booleans('XOR',a,b)
        return operator.xor(a,b)

    def __safe_not(a):
        ''' static method, returns a boolean, which is the logical NOT of the given boolean argument; 
            raises an exception if the argument is not boolean
        '''
        Lea._check_booleans('NOT',a)
        return operator.not_(a)    

    def __make_flea1_n(f):
        ''' returns a method M with one Lea instance argument (self), where M returns a Flea1 applying
            given function f to self
            (helper function used internally to do operator overloading of magic methods for unary
            operators __xxx__)
        '''
        def func(self):            
            return Flea1(f,self)
        func.__doc__ = "returns Flea1 instance applying %s function on (self), for function/operator overloading" % (f.__name__,)
        return func

    def __make_flea2_n(f):
        ''' returns a method M with two Lea instance arguments (self,other), where M returns a Flea2
            applying given function f to (self,other)
            (helper function used internally to do operator overloading of magic methods for binary
            operators __xxx__)
        '''
        def func(self,other):
            return Flea2(f,self,other)
        func.__doc__ = "returns Flea2 instance applying %s function on (self,other), for function/operator overloading" % (f.__name__,)
        return func

    def __make_flea2_r(f):
        ''' returns a method M with two Lea instance arguments (self,other), where M returns a Flea2
            applying given function f to (other,self)
            (helper function used internally to do operator overloading of magic methods for binary
            operators __rxxx__)
        '''
        def func(self,other):            
            return Flea2(f,other,self)
        func.__doc__ = "returns Flea2 instance applying %s function on (other,self), for function/operator overloading" % (f.__name__,)
        return func
  
    # overloading of arithmetic operators and mathematical functions
    __pos__       = __make_flea1_n(operator.pos)
    __neg__       = __make_flea1_n(operator.neg)
    __abs__       = __make_flea1_n(abs)
    __add__       = __make_flea2_n(operator.add)
    __radd__      = __make_flea2_r(operator.add)
    __sub__       = __make_flea2_n(operator.sub)
    __rsub__      = __make_flea2_r(operator.sub)
    __mul__       = __make_flea2_n(operator.mul)
    __rmul__      = __make_flea2_r(operator.mul)
    __truediv__   = __make_flea2_n(operator.truediv)
    __rtruediv__  = __make_flea2_r(operator.truediv)
    __floordiv__  = __make_flea2_n(operator.floordiv)
    __rfloordiv__ = __make_flea2_r(operator.floordiv)
    __mod__       = __make_flea2_n(operator.mod)
    __rmod__      = __make_flea2_r(operator.mod)
    __divmod__    = __make_flea2_n(divmod)
    __rdivmod__   = __make_flea2_r(divmod)
    __pow__       = __make_flea2_n(operator.pow)
    __rpow__      = __make_flea2_r(operator.pow)
    # Python 2 compatibility
    __div__       = __truediv__
    __rdiv__      = __rtruediv__

    # overloading of comparison operators
    __lt__        = __make_flea2_n(operator.lt)
    __le__        = __make_flea2_n(operator.le)
    __eq__        = __make_flea2_n(operator.eq)
    __ne__        = __make_flea2_n(operator.ne)
    __gt__        = __make_flea2_n(operator.gt)
    __ge__        = __make_flea2_n(operator.ge)

    # overloading of bitwise operators to emulate boolean operators
    __invert__    = __make_flea1_n(__safe_not)
    __and__       = __make_flea2_n(__safe_and)
    __rand__      = __make_flea2_r(__safe_and)
    __or__        = __make_flea2_n(__safe_or)
    __ror__       = __make_flea2_r(__safe_or)
    __xor__       = __make_flea2_n(__safe_xor)
    __rxor__      = __make_flea2_r(__safe_xor)

    # overloading of slicing operator
    __getitem__   = __make_flea2_n(operator.getitem)

    # delete helper functions (used only at class creation)
    del __make_flea1_n, __make_flea2_n, __make_flea2_r


# import modules with Lea subclasses
# these must be placed here to avoid cycles (these import lea module)
from .alea import Alea
from .olea import Olea
from .plea import Plea
from .clea import Clea
from .ilea import Ilea
from .rlea import Rlea
from .blea import Blea
from .flea import Flea
from .flea1 import Flea1
from .flea2 import Flea2
from .flea2a import Flea2a
from .glea import Glea
from .tlea import Tlea
from .slea import Slea
from .evidence_ctx import EvidenceCtx

# init Alea class with default 'x' type code: if a probability is expressed as
# a string, then the target type is determined from its content
# - see Alea.prob_any method
Alea.set_prob_type('x')

# convenience functions

def P(lea1):
    ''' returns the probability that given lea1 is True;
        the probability is expressed in the probability type used in lea1,
        possibly downcasted for convenience (Fraction -> ProbFraction,
        Decimal -> ProbDecimal);
        raises an exception if some value in the distribution is not boolean
        (note that this is NOT the case with lea1.p(True));
        this is a convenience function equivalent to lea1.P
    '''
    return lea1.P

def Pf(lea1):
    ''' returns the probability that given lea1 is True;
        the probability is expressed as a float between 0.0 and 1.0;
        raises an exception if the probability type is no convertible to float
        raises an exception if some value in the distribution is not boolean
        (note this is NOT the case with lea1.p(True));
        this is a convenience function equivalent to lea1.Pf
    '''
    return lea1.Pf
