set TEAMS;
set DATES := 1..161;

param atlantic {TEAMS};
param central {TEAMS};
param southeast {TEAMS};
param northwest {TEAMS};
param pacific {TEAMS};
param southwest {TEAMS};
param tdistance {TEAMS, TEAMS};

set ATL {i in TEAMS: atlantic[i] = 1};
set CENT {i in TEAMS: central[i] = 1};
set SE {i in TEAMS: southeast[i] = 1};
set NW {i in TEAMS: northwest[i] = 1};
set PAC {i in TEAMS: pacific[i] = 1};
set SW {i in TEAMS: southwest[i] = 1};

set EAST {i in TEAMS: atlantic[i] = 1 or central[i] = 1 or southeast[i] = 1};
set WEST {i in TEAMS: northwest[i] = 1 or pacific[i] = 1 or southwest[i] = 1};

# set EAST := ATL union CENT union SE;
# set WEST := NW union PAC union SW;

var Game {i in TEAMS, j in TEAMS, k in DATES}, binary;


minimize objective: sum {i in TEAMS, j in TEAMS, k in DATES} Game[i,j,k];

subject to cannotplayself {i in TEAMS}: sum {k in DATES} Game[i,i,k] = 0;

subject to 41homegames {i in TEAMS}: sum {j in TEAMS, k in DATES} Game[i,j,k] = 41;

subject to 41awaygames {i in TEAMS}: sum {j in TEAMS, k in DATES} Game[j,i,k] = 41;

subject to only1gameperday {i in TEAMS, k in DATES}: sum {j in TEAMS} (Game[i,j,k] + Game[j,i,k]) <= 1;

# subject to atlanticdiv {i in ATL, j in ATL}: sum {k in DATES} Game[i,j,k] = 2;

# subject to centraldiv {i in CENT, j in CENT}: sum {k in DATES} Game[i,j,k] = 2;

# subject to southeastdiv {i in SE, j in SE}: sum {k in DATES} Game[i,j,k] = 2;

# subject to northwestdiv {i in NW, j in NW}: sum {k in DATES} Game[i,j,k] = 2;

# subject to pacificdiv {i in PAC, j in PAC}: sum {k in DATES} Game[i,j,k] = 2;

# subject to southwestdiv {i in SW, j in SW}: sum {k in DATES} Game[i,j,k] = 2;
