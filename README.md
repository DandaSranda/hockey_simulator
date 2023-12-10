** Hockey Tournament Simulator **

** Daniel Sibor **
** 12/2023 **

-- Overview:

The Hockey Tournament Simulator is a command-line-based simulation of a Czech Extraliga.
https://en.wikipedia.org/wiki/Czech_Extraliga
It allows user to progress through multiple rounds, input match results, view upcoming matches,
and analyze team statistics. The game is designed to specified number of rounds with 14 teams
competing against each other.

-- Game Flow:

- Initialization:
  Teams are initialized from a CSV file, each represented by a unique team code, name, and initial
  statistics - more about them at the end of this file.

- User Interaction:
  Users navigate through the game using a menu system. Options include advancing to the next round,
  viewing upcoming matches, seeing results of previous rounds, and more.

- Match Simulation:
  Users input match results, providing the number of goals scored by each team. If the goal
  difference is one, the user is prompted to specify whether the match ended in overtime, shootout or none.

- Statistics Update:
  Team statistics are updated based on match results, considering wins, losses, goals scored, and
  points earned.

- End of Season:
  The game progresses through multiple rounds until the end of the season, displaying appropriate
  messages when there are no more upcoming matches.

-- CSV File Format:
The game reads team information from a CSV file with the following format:

> (team_code;team_name;matches;wins;ot_wins;so_wins;ot_losses;so_losses;losses;scored_in;scored_against;points)

    team_code: Unique code representing each team.
    team_name: Name of the team.
    matches: Total number of matches played.
    wins, ot_wins, so_wins: Wins in regular time, overtime, and shootout.
    ot_losses, so_losses, losses: Losses in overtime, shootout, and regular time.
    scored_in: Total goals scored by the team.
    scored_against: Total goals scored against the team.
    points: Total points earned by the team.

-- Game Configuration:
The game supports three difficulty levels: 13, 26, or 52 rounds in a season.

-- Game Management:
The user can choose to continue a previous game or start a new one, which will reset all statistics.
