Solver "loqo" is a version of Prof. Robert Vanderbei's LP solver LOQO,
which uses an interior-point algorithm to find local solutions to
smooth constrained optimization problems involving continuous
variables; loqo can be used stand-alone or with AMPL's solve command.

Stand-alone invocations have the form

	loqo stub [-AMPL] [keywd=value ...]

where stub was specified in

	ampl -obstub ...
or
	ampl -ogstub ...

Such an invocation causes loqo to read from stub.nl and, if -AMPL or
or "wantsol=..." with suitlble ... appears on the command line, to
write stub.sol.

You can use AMPL's solve command to invoke loqo and have the solution
loqo computes made available to your AMPL session.  To do this, in the
AMPL session set AMPL's solver option to loqo by giving the command

	option solver loqo;

sometime before the relevant "solve;".

----------------
Controlling loqo
----------------

Loqo reads key words and values from the environment (shell) variable
loqo_options and from the command line (in which case each key word
must be followed immediately by an = sign).  Execute

	loqo -=

for a summary of the keywords loqo recognizes.

------------------
Sample Invocations
------------------

  If you're using AMPL, just say

	option solver loqo;
	solve;

  If you've executed, say,

	ampl -objunk junk.model junk.data

then you could say

	loqo junk iterlim=30 dual=

to force loqo to solve the dual problem and to have it run for
at most 30 iterations.  Either of the invocations

	loqo_options='iterlim 30 dual' loqo junk
or
	loqo_options='iterlim 30 dual'
	export loqo_options
	loqo junk

would have the same effect; within AMPL, specifying

	option loqo_options 'iterlim 30 dual', solver loqo;
	solve;

would also have this effect.

-----------------------
solve_result_num values
=======================

Here is a table of solve_result_num values that "loqo" can return
to an AMPL session, along with the text that appears in the associated
solve_message.

	Value	Message

	0	optimal solution
	100	suboptimal solution
	201	primal infeasible
	202	dual infeasible
	203	primal and/or dual infeasible
	210	primal infeasible -- inconsistent equations
	301	primal unbounded
	302	dual unbounded
	400	iteration limit
	500	resource limit
	510	??? LOQO bug

-----------------------

If you have questions about using loqo, please E-mail support@ampl.com .
