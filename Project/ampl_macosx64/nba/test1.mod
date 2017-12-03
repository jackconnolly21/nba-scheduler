set TEAMS;

set DATES := 1..161;

param atlantic {TEAMS};
param central {TEAMS};
param southeast {TEAMS};
param northwest {TEAMS};
param pacific {TEAMS};
param southwest {TEAMS};

set ATL {i in teams atlantic[i] = 1};
set CEN {i in teams central[i] = 1};
set SE {i in teams southeast[i] = 1};
set NW {i in teams northwest[i] = 1};
set CEN {i in teams central[i] = 1};
set SW {i in teams southwest[i] = 1};

set EAST {i in TEAMS: atlantic[i] = 1 or central[i] = 1 or southeast[i] = 1}
set WEST {i in TEAMS: northwest[i] = 1 or central[i] = 1 or southwest[i] = 1}

var Game {i in TEAMS, j in TEAMS, k in DATES}, binary;

minimize objective: sum{i in TEAMS, j in TEAMS, k in DATES} Game[i,j,k];

subject to constraint1 {i in TEAMS}: sum {j in DATES} Game[i,i,j] = 0;

subject to constraint2 {i in TEAMS}: sum {j in TEAMS, k in DATES} Game[i,j,k] = 41;

subject to constraint3 {i in TEAMS}: sum {j in TEAMS, k in DATES} Game[j,i,k] = 41;

subject to constraint4 {i in TEAMS, in DATES}: 
	sum {i in TEAMS} Game[i,j,k] + Game[j,i,k] 	<=1;
