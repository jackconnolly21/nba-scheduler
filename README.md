# nba-scheduler

This system attempts to optimize the NBA schedule, minimizing back to backs and travel distance, while fulfilling the hard constraints of the NBA season. We have implemented hill climbing and simulated annealing algorithms to do so, which generally reduce the number of back to backs per team by almost 7 per season, while keep travel distance roughly the same.

To run our program, you may need to download a few Python packages (a full list is in requirements.txt), but they are all pretty standard, especially with Anaconda. You may need to install Pickle, which we used to store our scheduler objects before and after we ran local search on them. You can install all needed dependencies (most should already be installed), using the command:

* `pip install --user -r requirements.txt`

To run a local search on a schedule in your terminal, type:

* `python localSearch.py`

This will run hill climbing on a randomly initialized schedule for the default number of 50,000 iterations. All of this is highly customizable with the use of command line arguments and flags. The result of each local search is saved in the "pickles" file. The name of each pickle file is the number of back-to-backs the schedule ended up with, followed by the algorithm used to get there (HC or SA). To choose which algorithm you want to use (simulated annealing or hill climbing) use the --method tag, or -m for short, followed by SA for simulated annealing or HC for hill climbing. Here is an example of running simulated annealing:

* `python localSearch.py -m SA`

Now to choose how many iterations you want the algorithm to run, use the --numIters or -n for short followed by a positive integer. Here is an example of running hill climbing for 500,000 iterations:

* `python localSearch.py -m HC -n 500000`

Now to choose the number of times you want to run an algorithm, use the --numTimes flag or -t for short. This will run the chosen algorithm on a new schedule initialization a given number of times and save only the schedule with the lowest cost in the form of a pickle. Here is an example of running simulated annealing for 100,000 iterations 5 times:

* `python localSearch.py -m SA -n 100000 -t 5`

Now to run local search on an already initialized schedule, you can use the --fileName flag or -f for short. This comes in handy when trying to make a good schedule even better, maybe even with both algorithms. Now the -f flag already assumes that the file is in the pickles folder so no need to add "pickles/" at the beginning. Here is an example of running hill climbing for 750,000 iterations 2 times on a file called 315SA.txt. 315SA.txt means that the schedule was created using simulated annealing and has 315 back-to-backs.

* `python localSearch.py -m HC -n 750000 -t 2 -f 315SA.txt`

Finally, you can change the number of swaps being used by each algorithm using the --numSwaps tag or -s for short. In our testing we found that this wasn't that helpful, but you can still do it! This means that for one iteration of each algorithm the given number of swaps of game dates occur and then the cost of the schedule is analyzed and the algorithm either accepts or rejects the swaps. Here is the ultimate example: simulated annealing run for 1000 iterations 4 times on 456SA.txt with 6 swaps per iteration:

* `python localSearch.py -m SA -n 1000 -t 4 -f 456SA.txt -s 6`

The most useful flags will likely be -m, -n, and -f. Now that you know how to generate nice locally searched schedules here is how you analyze them. You are going to want to run the analyze.py file followed by the --files flag or -f for short. Analyze will tell you all sorts of interesting information about the given file(s) by printing to stdout and creating a plot, and you can analyze more than one file at a time by inputting a comma separated list (no spaces) after the -f flag. For each schedule you analyze you will be able to see the name of the file, cost of the schedule, total distance travelled in that season, total back to backs, number of triples (3 games in 3 days), the standard deviations of both back to backs and travel distance between teams, the least back to backs a team has and the most back to backs a team has. In addition, a plot of the cost of the schedule on the y-axis as well as the number of iterations on the x-axis. Again, we already assume the file is coming from the pickles folder, so there is no need to add "pickles/" Here is an example of how to analyze a single schedule stored in the pickle file 399HC.txt:

* `python analyze.py -f 399HC.txt`

Now if you analyze more than one schedule at a time you can compare the costs of the schedules over time. This works best if the two schedules were formed after the same number of iterations of any algorithm. Here is an example of how to analyze multiple schedules at once:

* `python analyze.py -f 301SA.txt,295HC.txt`
