# set TEAMS;
# set ATL;
set DATES := 1..161;
set DIVS;
set TEAMS {DIVS};

# param atlantic {TEAMS};
# param central {TEAMS};
# param southeast {TEAMS};
# param northwest {TEAMS};
# param pacific {TEAMS};
# param southwest {TEAMS};

# param tdistance {i in DIVS, j in DIVS, TEAMS[i], TEAMS[j]};

# set ATL {i in TEAMS: atlantic[i] = 1};
# set CENT {i in TEAMS: central[i] = 1};
# set SE {i in TEAMS: southeast[i] = 1};
# set NW {i in TEAMS: northwest[i] = 1};
# set PAC {i in TEAMS: pacific[i] = 1};
# set SW {i in TEAMS: southwest[i] = 1};





# set EAST {i in TEAMS: atlantic[i] = 1 or central[i] = 1 or southeast[i] = 1};
# set WEST {i in TEAMS: northwest[i] = 1 or pacific[i] = 1 or southwest[i] = 1};

var Game {a in DIVS, b in DIVS, i in TEAMS[a], j in TEAMS[b], k in DATES}, binary;

minimize objective: sum {a in DIVS, b in DIVS, i in TEAMS[a], j in TEAMS[b], k in DATES} Game[a,b,i,j,k];

subject to cannotplayself {a in DIVS, i in TEAMS[a]}: sum {k in DATES} Game[a,a,i,i,k] = 0;

subject to 41homegames {a in DIVS, i in TEAMS[a]}: sum {b in DIVS, j in TEAMS[b], k in DATES} Game[a,b,i,j,k] = 41;

subject to 41awaygames {a in DIVS, i in TEAMS[a]}: sum {b in DIVS, j in TEAMS[b], k in DATES} Game[b,a,j,i,k] = 41;

# subject to only1gameperday {a in DIVS, i in TEAMS[a], k in DATES}: sum {b in DIVS, j in TEAMS[b]} (Game[a,b,i,j,k] + Game[b,a,j,i,k]) <= 1;

# param consumo{a in AEREI, z in ALT[a], v in SPEED[a]} >= 0;
subject to atlanticdiv {a in DIVS, i in TEAMS[a], j in TEAMS[a]}: sum {k in DATES} Game[a,a,i,j,k] = 2;

# subject to centraldiv {i in CENT, j in CENT}: sum {k in DATES} Game[i,j,k] = 2;

# subject to southeastdiv {i in SE, j in SE}: sum {k in DATES} Game[i,j,k] = 2;

# subject to northwestdiv {i in NW, j in NW}: sum {k in DATES} Game[i,j,k] = 2;

# subject to pacificdiv {i in PAC, j in PAC}: sum {k in DATES} Game[i,j,k] = 2;

# subject to southwestdiv {i in SW, j in SW}: sum {k in DATES} Game[i,j,k] = 2;
