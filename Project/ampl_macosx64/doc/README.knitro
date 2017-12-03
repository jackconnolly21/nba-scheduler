The solver "knitro" uses KNITRO (a solver by Ziena Optimization LLC;
see http://www.ziena.com/) to solve nonlinear programming problems
involving continuous or integer variables.  It also handles
complementarity constraints and complementarity problems.  Normally
knitro is invoked by AMPL's solve command, which gives the invocation

     knitro stub -AMPL

in which stub.nl is an AMPL generic output file (possibly written
by "ampl -obstub" or "ampl -ogstub").  After solving the problem,
knitro writes a stub.sol file for use by ampl's solve and solution
commands.  When you run ampl, this all happens automatically if you
give the AMPL commands

     option solver knitro;
     solve;

You can control knitro by setting the environment variable knitro_options
appropriately (either by using ampl's option command, or by using the
shell's set and export commands before you invoke ampl).  You can put
one or more (white-space separated) phrases in $knitro_options.  To see
the possibilities, invoke

        knitro '-='

-----------------------
solve_result_num values
=======================

Here is a table of solve_result_num values that knitro can return
to an AMPL session, along with an indication of the text that appears
in the associated solve_message.

        Value   Message

          0     Locally optimal solution.
	100	Current feasible solution estimate cannot be improved. Nearly optimal.
	101	Relative change in feasible solution estimate < xtol.
	102	Current feasible solution estimate cannot be improved.
	200	Convergence to an infeasible point. Problem may be locally infeasible.
	201	Relative change in infeasible solution estimate < xtol.
	202	Current infeasible solution estimate cannot be improved.
	203	Multistart: No primal feasible point found.
	204	Problem determined to be infeasible.
	205	Problem determined to be infeasible.
	300	Problem appears to be unbounded.
	400	Iteration limit reached. Current point is feasible.
	401	Time limit reached. Current point is feasible.
	403	MIP: All nodes have been explored. Integer feasible point found.
	404	MIP: Integer feasible point found.
	405	MIP: Subproblem solve limit reached. Integer feasible point found.
	406	MIP: Node limit reached. Integer feasible point found.
	410	Iteration limit reached. Current point is infeasible.
	411	Time limit reached. Current point is infeasible.
	413	MIP: All nodes have been explored. No integer feasible point found.
	415	MIP: Subproblem solve limit reached. No integer feasible point found.
	416	MIP: Node limit reached. No integer feasible point found.
	501	LP solver error.
	502	Evaluation error.
	503	Not enough memory.
	504	Terminated by user.
	505	Input or other API error.
	506	Internal KNITRO error.
	507	Unknown termination.
	508	Illegal objno value.
