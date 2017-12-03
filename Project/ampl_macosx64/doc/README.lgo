Solver lgo is a global nonlinear solver based on the LGO solver by

        Janos D. Pinter
        Pinter Consulting Services, Inc.
        http://www.pinterconsulting.com

For much more detail on LGO, see the accompanying lgo_guide.pdf;
for a more detailed "quick start" guide that focuses on Microsoft
Windows, as well as a collection of models called GOMODELS,
see http://www.pinterconsulting.com/ampl .

It is most convenient to invoke lgo with AMPL's solve command:

        ampl: option solver lgo;
        ampl: solve;

but lgo can also be run separately, with invocation syntax

        lgo stub [-AMPL] [keywd=[value] ...]

in which stub comes from AMPL's write command.  For example,

        > ampl -obfoo foo.mod foo.dat
        > lgo foo

demonstrates running lgo separately; the ampl invocation writes file
foo.nl (stub = "foo"), which lgo reads.

Command-line arguments to lgo have the form

        keywd=value

where keywd is one of the keywords described in the "lgo -=" output
shown below.  Alternatively, you can invoke lgo the way AMPL's solve
command does, i.e.,

        lgo stub -AMPL [keywd=value ...]

where stub was specified in

        ampl -obstub ...
or
        ampl -ogstub...

Such an invocation causes lgo to read from stub.nl and to write stub.sol.

---------------
Controlling lgo
---------------

Lgo reads keywords and values from the environment (shell) variable
lgo_options and from the command line.  Execute

        lgo -?

or (if your shell requires ? to be quoted)

        lgo '-?'

for a summary of lgo usage and

        lgo -=

(or lgo '-=') for a summary of keywords peculiar to the AMPL/LGO
driver "lgo".

------------------
Sample Invocations
------------------

  If you're using AMPL, just say

        option solver lgo;
        solve;

  If you've executed, say,

        ampl -objunk junk.model junk.data

then you could say

        lgo junk l_maxfct=20000 lbound=-1e3

to force lgo to use at most 20000 function evalutions in doing
local searches and to assume lower bound -1e3 = -1000 on variables
that are not bounded below.  With the Bourne shell, either of the
invocations

        lgo_options='l_maxfct=20000 lbound=-1e3' lgo junk
or
        lgo_options='l_maxfct=20000 lbound=-1e3'
        export lgo_options
        lgo junk

would have the same effect; within AMPL, specifying

        option lgo_options 'l_maxfct=20000 lbound=-1e3', solver lgo;
        solve;

would also have this effect.


-----------------------
solve_result_num values
=======================

Here is a table of solve_result_num values that "lgo" can return to
an AMPL session, along with the text that appears in the associated
solve_message.

        Value   Message

          0     Feasible solution from global search
        100     Feasible solution from local search
        120     Feasible solution <= l_target
        110     Feasible solution <= g_target
        200     Infeasible problem
        300     Unbounded objective
        400     Intermediate solution
        410     A partition got too small
        420     Too many MS cycles with little improvement
        510     Interrupted by control-C (SIGINT)
        520     Problem too large.

The above values may be incremented by 1, 2, 3, 4, 5, or 6:

        1       Maximum number of active partition subsets reached
        2       Function evaluation limit reached reached
        3       Maximum local-search function evaluations reached
        4       Time limit reached
        5       No objective improvement in maxnosuc global search steps
        6       Stopped by control-C.

Questions about this stuff?  Contact support@ampl.com .


--------------------------------
keyword summary: "lgo -=" output
================================

con_tol   max. constraint violation in local search; default 1e-8

fi_tol    local search merit function precision improvement target;
          default = 1e-8

flog      name of log file for function evaluations (debug option,
          default = not written)

g_maxfct  factor affecting max. merit function evals in global phase.
          The limit is often 2*g_maxfct but may be more when the starting
          point is infeasible.  Default g_maxfct = 50*(m+n+2)^2, in which
          n = _snvars (number of decision variables the solver sees)
          and m = _sncons (number of constraints the solver sees).

g_target  global search target objective function value; default -1e10

irngs     random number seed (default 0) for LGO's built-in random-number
          generator

kt_tol    local Kuhn-Tucker optimality tolerance; default 1e-8

l_maxfct  max. merit function evals in global phase; default 50*(m+n+2)^2,
          with m and n as for g_maxfct

l_target  local search target objective function value; default -1e10

lbound    lower bound imposed on variables unbounded below:
                change -Infinity <= x <= U
                to min(0,U) + lbound <= x <= U;
                default lbound = -1e4

logfile   name of log file written when outlev >= 3 (default "LGO.LOG")

maxnosuc  limit on global phase merit evals without improvement;
          default = 50*(m+n+2)^2

objno     objective number: 1 = first (default)

objrep    Whether to replace
                minimize obj: v;
          with
                minimize obj: f(x)
          when variable v appears linearly
          in exactly one constraint of the form
                s.t. c: v >= f(x);
          or
                s.t. c: v == f(x);
          Possible objrep values:
          0 = no
          1 = yes for v >= f(x)
          2 = yes for v == f(x)
          3 = yes in both cases (default)

opmode    synonym for "search" (see below)

outfile   name of file written when outlev >= 2 (default "LGO.OUT")

outlev    output level:
                0 (default) ==> no output
                1 ==> write sumfile
                2 ==> also outfile
                3 ==> also logfile

penmult   constraint penalty multiplier; default 1.0

search    search kind:
                0 = just local optimization
                1 = global branch-and-bound + local optimization
                2 = global adaptive random  + local optimization
                3 = multi-start local search (default)

sumfile   name of summary file written when outlev >= 1 (default "LGO.SUM")

timelim   time limit in seconds; default 300

timing    report I/O and solution times: 1 = stdout, 2 = stderr, 3 = both

ubound    upper bound imposed on variables unbounded above:
                change L <= x <= Infinity
                to L <= x <= max(L,0) + ubound;
                default ubound = 1e4

wantsol   solution report without -AMPL: sum of
                1 ==> write .sol file
                2 ==> print primal variable values
                4 ==> print dual variable values
                8 ==> do not print solution message
