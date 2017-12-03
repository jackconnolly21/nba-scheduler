CONOPT is a nonlinear solver written by Arne Drud.
It is based on the reduced gradient method.

Command-line arguments to conopt either have the form

        keywd=
or
        keywd=value

where keywd is one of the keywords described below, or is the name
of a CONOPT "CR-Cell" (as described in separate CONOPT documentation).
Alternatively, you can invoke conopt the way AMPL's solve command does,
i.e.,

        conopt stub -AMPL [keywd=value ...]

where stub was specified in

        ampl -obstub ...
or
        ampl -ogstub...

Such an invocation causes conopt to read from stub.nl and to write stub.sol.

------------------
Controlling conopt
------------------

Conopt reads keywords and values from the environment (shell) variable
conopt_options and from the command line.  Case is ignored.  For logical
CR-Cells, use 0 for FALSE and 1 for TRUE.  Here are the non-CR-Cell
keywords that conopt understands; fp indicates a floating-point value
and none indicates a keyword that appears by itself, without a value.

        Keyword         Value           Meaning

        debug           integer         When to use finite differences to
                                        check derivatives:
                                                 0  ==> never (default);
                                                -1  ==> only at the starting point;
                                                > 0 ==> every that many iterations.

        debug2d         integer         When to use finite differences to check the
                                        Lagrangian Hessian:
                                                 0  (default) ==> never;
                                                -1  ==> only at the starting point;
                                                > 0 ==> every that many iterations.

        errlim          integer         Evaluation-error limit (default 500).
                                        If the objective or constraints cannot be
                                        evaluated at a proposed next iterate, CONOPT
                                        will try a shorter step at most errlim times.

        hess            integer         whether to use the Lagrangian Hessian:
                                                0 = no;
                                                1 = yes: just the explicit Hessian;
                                                2 = yes: just Hessian-vector products;
                                                3 = yes (default): use both explicit
                                                        and Hessian-vector products;
                                                -1 = no, but evaluate gradients as for
                                                        Hessian computations
                                                        (debug option).

        iterlim         integer         iteration limit (default 1000000).

        logfreq         integer         For outlev=3, print one summary
                                        line for every logfreq iterations.
                                        Default = 1.

        maxftime        fp              Limit on cpu seconds; default 999999.

        maxfwd          integer         Use forward automatic diff. for
                                        defined variables that depend on
                                        at most maxfwd other variables.
                                        Default = 5.

        maximize        none            Maximize the objective (even if
                                        the model says to minimize it).

        maxiter         integer         Maximum iterations; default 999999.

        minimize        none            Minimize the objective (even if
                                        the model says to maximize it).

        objno           integer         Which objective to optimize:
                                        1 = first objective (default),
                                        2 = second objectve, etc.
                                        0 = just satisfy the constraints.

        outlev          integer         0 = no options echoed on stdout.
                                        1 (default) = options but no
                                                iteration log.
                                        2 = CONOPT "SCREEN" output on stdout.
                                        3 = log line every logfreq iterations.

        superbasics     integer         limit on number of superbasic variables
                                        (default >= 500).

        timing          integer         0 = no timing report.
                                        1 = timing report on stdout.
                                        2 = timing report on stderr.
                                        3 = timing report on both.

        version         none            Show version and CONOPT banner.

        workmeg         fp              0 = let CONOPT decide how much
                                                memory to allocate.
                                        > 0 means allocate workmeg
                                                megabytes of memory.


------------------
Sample Invocations
------------------

  If you're using AMPL, just say

        option solver conopt;
        solve;

  If you've executed, say,

        ampl -objunk junk.model junk.data

then you could say

        conopt junk maxiter=300 rtmaxj=1e20

to force conopt to run for at most 300 iterations with CR-Cell rtmaxj
set to 1e20.  Either of the invocations

        conopt_options='maxiter=300 rtmaxj=1e20' conopt junk

or (using Bourne-shell notation)

        conopt_options='iterations=300 rtmaxj=1e20'
        export conopt_options
        conopt junk

would have the same effect; within AMPL, specifying

        option conopt_options 'iterations=300 rtmaxj=1e20', solver conopt;
        solve;

would also have this effect.


-----------------------
solve_result_num values
-----------------------

Here is a table of solve_result_num values that "conopt" can return
to an AMPL session, along with the text that appears in the associated
solve_message.  Values >= 510 indicate a bug of some kind.

        Value   Message

        0       Optimal.
        100     Locally optimal.
        101     Bogus "Termination by solver" (CONOPT bug).
        200     Infeasible.
        201     Locally infeasible.
        202     Intermediate infeasible.
        300     Unbounded.
        400     Iteration limit.
        401     Time limit.
        500     CONOPT bug: unknown MODSTA value.
        501     Intermediate non-optimal.
        504     Unknown type of error.
        505     Error no solution.
        506     Evaluation error.
        507     Evaluation error limit.
        508     objno = nnn is not >= 0 and <= nnn.

        510     CONOPT bug: unknown SOLSTA value.
        511     "User interrupt" = CONOPT bug.
        511     Setup failure.
        512     Solver failure.
        513     Internal solver error.
        520     Surprise: coi_solve did not call Solution.
        521     Not enough memory for CONOPT's initial allocations.
        522     Too many constraints.
        523     Too many variables.
        524     Too many variables and constraints.
        525     Too many nonzeros.
        526     Size permitted by demo license exceeded.
        527     Objective index out of range.
        528     Too many nonlinear nonzeros: more than all nonzeros.
        529     CONOPT ran out of memory.
        530     Internal CONOPT error.
        531     CONOPT error: Status not called.
        532     ReadMatrix not registered.
        533     FDEval not registered.
        534     ErrMsg not registered.
        535     Message not registered.
        536     Status not registered.
        537     Solution not registered.
        538     COIDEF_Base not called.
        539     Unexpected return nnn from coi_solve.

*************************

If you have questions about or find errors in the above text,
please contact:

     David M. Gay
     dmg@ampl.com
