#!/usr/bin/env python3
"""
********************
*** Daniel Sibor ***
****** 12/2023 *****
********************
"""

ATTRIBUTES = [
    "matches",
    "wins",
    "ot_wins",
    "so_wins",
    "ot_losses",
    "so_losses",
    "losses",
    "scored_in",
    "scored_against",
    "points",
]


ERR_MSG = {
    -1: "\n>>> Invalid input!\n",
    -3: "\n>>> Teams can't score the same number of goals!\n>>> Enter the final result and then choose if \n>>> it ended in Overtime(o) or Shootout(s).\n",
    -4: "\n>>> Enter value again.\n",
}


class Team:
    def __init__(self, team_code, team_name, *other):
        self.code = team_code
        self.name = team_name
        for attribute, value in zip(ATTRIBUTES, other):
            setattr(self, attribute, value)

    def update(self, tup):
        for attribute, value in zip(ATTRIBUTES, tup[1:]):
            atr = int(getattr(self, attribute, value))
            setattr(self, attribute, atr + value)


def err_output(msg):
    print(msg)


def generate_matches(teams, n_rounds):
    """
    Generates match pairs for each round
    """
    matches = {}
    for round in range(1, n_rounds + 1):
        matches[round] = [
            (teams[i], teams[j])
            for i, j in zip(
                range(len(teams) // 2), range(len(teams) - 1, len(teams) // 2 - 1, -1)
            )
        ]
        teams.insert(1, teams.pop())
    return matches


def read_csv():
    """
    Return all records as lists
    """
    with open("stats.csv", "r", encoding="utf-8") as file:
        record = []
        for line in file:
            record.append(line.strip().split(";"))
        return record


def longest_name(teams):
    return len(max(teams.values(), key=len))


def create_team_dict(teams_full_record):
    """
    Returns dictionary in format of {"team_code" : "team_name"}
    """
    teams = {}
    for record in teams_full_record:
        team_code = record[0]
        team_name = record[1]
        teams[team_code] = team_name
    return teams


def create_team_objects(teams_full_record):
    """
    Creates dictionary in format of {"team_code" : "team_object"}, so each team can be accessed as object
    """
    team_objects = {}
    for record in teams_full_record:
        code, name, *other = record
        team_class = type(name, (Team,), {"__doc__": f"A class for the {name} team"})
        globals()[code] = team_class(code, name, *other)
        team_object = team_class(code, name, *other)
        team_objects[code] = team_object
    return team_objects


def statistics_table(teams, codes, LONGEST_NAME_LEN):
    """
    Prints out table of statistics sorted by priority of: 1) most points, 2) most goals scored in, 3) least goals scored against
    """
    print()
    pnts = []
    for code in codes:
        pnts.append(
            (
                code,
                teams[code].points,
                teams[code].scored_in,
                teams[code].scored_against,
            )
        )

    srted_table = sorted(pnts, key=lambda x: (-int(x[1]), -int(x[2]), int(x[3])))
    print(" " * 4 + "|", end=" ")
    print(f"Team".center(LONGEST_NAME_LEN + 6), end=" | ")
    for name in [
        "Games",
        "Wins",
        "OT Wins",
        "SO Wins",
        "OT Loss",
        "SO Loss",
        "Losses",
        "G In",
        "G Ag",
        "Points",
    ]:
        val = name.center(7, " ")
        print(val, end=" | ")
    print()

    for i, row in enumerate(srted_table):
        team = teams[row[0]]
        print(f"{i+1}.".ljust(3), end=" | ")
        print(
            f"{team.name} ({team.code})".ljust(LONGEST_NAME_LEN + 6),
            end=" | ",
        )
        for attribute in ATTRIBUTES:
            attr = f"{getattr(team, attribute)}".center(7, " ")
            print(attr, end=" | ")
        print()
    print()


def match_teams(first_team_name, second_team_name, round_n, LONGEST_NAME_LEN):
    """
    Prints out table of the played match in a concrete round.
    """
    round_out = f"Round {round_n}"
    print(round_out.center(LONGEST_NAME_LEN * 2 + len("   :   "), "-"))
    print(
        first_team_name.rjust(LONGEST_NAME_LEN)
        + "   :   "
        + second_team_name.ljust(LONGEST_NAME_LEN)
    )
    print("-" * (len(round_out) + 2 * LONGEST_NAME_LEN))


def check_input(first, second):
    if not first.isdigit() or not second.isdigit():
        return -1
    if first == second:
        return -3
    return 0


def scores_input(team_objects, match, round_n, LONGEST_NAME_LEN):
    """
    User enters goals scored by each team, then if the difference of scored goals is 1, is asked to enter if the match ended after 60 minutes or was prolonged.
    """
    print()
    first_team_name = team_objects[match[0]].name
    second_team_name = team_objects[match[1]].name

    while True:
        match_teams(first_team_name, second_team_name, round_n, LONGEST_NAME_LEN)
        first = input(f"{first_team_name}: ")
        second = input(f"{second_team_name}: ")
        check = check_input(first, second)
        if check == 0:
            break
        err_output(ERR_MSG[check])

    first = int(first)
    second = int(second)

    overtime, shootout = 0, 0
    if abs(first - second) == 1:
        while True:
            is_over_time = input("No overtime (-), Overtime (o), Shootout (s): ")
            if is_over_time.lower() == "o":
                overtime = 1
                break
            elif is_over_time.lower() == "s":
                shootout = 1
                break
            elif is_over_time.lower() == "-":
                break
            else:
                err_output(ERR_MSG[-4])

    first_team_tup = (team_objects[match[0]].code, first)
    second_team_tup = (team_objects[match[1]].code, second)

    return [first_team_tup, second_team_tup, overtime, shootout]


def update_stats(team_objects, results):
    """
    Iterates through all teams and updates its statistics retrieved from evaluate_winner() returned tuple.
    """
    for match in results:
        first_team = team_objects[match[0][0]]
        second_team = team_objects[match[1][0]]
        first_team.update(match[0])
        second_team.update(match[1])


def evaluate_winner(result):
    """
    Evaluates who is the winner and calculates points earned for both teams, returns as tuple.
    """
    first, second, overtime, shootout = result
    first_code, first_goals = first
    second_code, second_goals = second

    if first_goals > second_goals:
        winner_code = first_code
        winner_goals = first_goals
        loser_code = second_code
        loser_goals = second_goals
    else:
        winner_code = second_code
        winner_goals = second_goals
        loser_code = first_code
        loser_goals = first_goals

    winner = (
        winner_code,
        1,
        1 - overtime - shootout,
        overtime,
        shootout,
        0,
        0,
        0,
        winner_goals,
        loser_goals,
        3 - overtime - shootout,
    )
    loser = (
        loser_code,
        1,
        0,
        0,
        0,
        overtime,
        shootout,
        1 - overtime - shootout,
        loser_goals,
        winner_goals,
        0 + overtime + shootout,
    )
    return winner, loser


def upcoming_matches(team_objects, matches, LONGEST_NAME_LEN, round_n, finish):
    """
    Prints either all upcoming matches or only the first upcoming, decided on user input
    """
    print()
    if finish + 1 == round_n:
        print(">>> No more matches.")
    else:
        for rnd in range(round_n, finish + 1):
            print(f"Round {rnd}".center(LONGEST_NAME_LEN * 2 + len("   :   "), "-"))
            for match in matches[rnd]:
                first = team_objects[match[0]].name
                second = team_objects[match[1]].name
                print(
                    first.rjust(LONGEST_NAME_LEN)
                    + "   :   "
                    + second.ljust(LONGEST_NAME_LEN)
                )
    print()


def previous_matches():
    with open("past_matches.csv", "r", encoding="utf-8") as file:
        print(file.read())


def previous_round(matches):
    """
    Prints last finished round.
    """
    print()
    with open("past_matches.csv", "r", encoding="utf-8") as file:
        lines = []
        for line in file:
            lines.append(line.rstrip("\n"))
        for match in lines[-matches - 1 :]:
            print(match)
    print()


def write_results(team_objects, results, round, LONGEST_NAME_LEN):
    """
    Writes all results to file after each finished round.
    """
    with open("past_matches.csv", "a", encoding="utf-8") as file:
        file.write(f"Round {round}".center(LONGEST_NAME_LEN * 2 + 9, "-"))
        file.write("\n")
        for res in results:
            first = team_objects[res[0][0]].name
            f_goals = res[0][1]
            second = team_objects[res[1][0]].name
            s_goals = res[1][1]
            overtime, shootout = res[2:]
            if overtime:
                extended = "(OT)"
            elif shootout:
                extended = "(SO)"
            else:
                extended = ""
            file.write(
                f"{first.rjust(LONGEST_NAME_LEN)}  {f_goals} : {s_goals}  {second.ljust(LONGEST_NAME_LEN)} {extended}"
            )
            file.write("\n")


def update_csv(team_objects, team_codes):
    with open("stats.csv", "w", encoding="utf-8") as file:
        attrs = ["code", "name"]
        attrs.extend(ATTRIBUTES)
        for team in team_codes:
            team_o = team_objects[team]
            for atr in attrs:
                file.write(str(getattr(team_o, atr)))
                if atr != "points":
                    file.write(";")
            file.write("\n")


def clear_past_matches():
    with open("past_matches.csv", "w", encoding="utf-8") as f:
        return


def reset_csv():
    with open("stats.csv", "r", encoding="utf-8") as file:
        record = []
        for line in file:
            record.append(line.strip().split(";"))

    with open("stats.csv", "w", encoding="utf-8") as file:
        for rec in record:
            for i in range(len(rec)):
                if i == 0 or i == 1:
                    file.write(rec[i])
                else:
                    file.write("0")
                if i < len(rec) - 1:
                    file.write(";")
            file.write("\n")


def restart():
    clear_past_matches()
    reset_csv()


def get_dificulty():
    while True:
        rounds = input("\n> Choose difficulty - (13|26|52) rounds:\n>>> ")
        if rounds in ["13", "26", "52"]:
            return int(rounds)
        else:
            err_output(ERR_MSG[-1])


def display_menu():
    while True:
        action = input(
            f"> Advance to next round (n)\n> See upcoming matches of next round (u)\n> See results of previous round (p)\n> See all upcoming matches (a)\
                    \n> See all results (r)\n> See table of statistics (s)\n> Exit (e)\n>>> "
        ).lower()
        if action in ["n", "u", "p", "a", "r", "s", "e"]:
            return action
        else:
            err_output(ERR_MSG[-1])


def main():
    n_rounds = 13
    while True:
        game_status = input(
            "> Do you wish to continue in the previous game (p) or start new game (n)?\n>>> "
        )
        if game_status == "p":
            print()
            break
        elif game_status == "n":
            sure = input("> Are you sure? (y|n)\n>>> ")
            if sure == "y":
                n_rounds = get_dificulty()
                restart()
                break
            elif sure == "n":
                continue
            else:
                err_output(ERR_MSG[-1])
        else:
            err_output(ERR_MSG[-1])

    """****************Init****************"""
    teams_full_record = read_csv()

    teams = create_team_dict(teams_full_record)

    LONGEST_NAME_LEN = longest_name(teams)

    team_codes = [key for key in teams]

    team_objects = create_team_objects(teams_full_record)

    matches = generate_matches(team_codes, n_rounds)
    """************************************"""
    while True:
        round_n = int(team_objects[team_codes[0]].matches) + 1

        action = display_menu()
        if action == "n":
            if round_n <= n_rounds:
                results = []
                results_to_file = []
                for match in matches[round_n]:
                    result = scores_input(
                        team_objects, match, round_n, LONGEST_NAME_LEN
                    )
                    results_to_file.append(result)

                    teams_stats = evaluate_winner(result)
                    results.append(teams_stats)

                update_stats(team_objects, results)
                write_results(team_objects, results_to_file, round_n, LONGEST_NAME_LEN)
                update_csv(team_objects, team_codes)
            else:
                print("\n> End of season. No more upcoming matches.\n")
        elif action == "u":
            if round_n <= n_rounds:
                upcoming_matches(
                    team_objects, matches, LONGEST_NAME_LEN, round_n, round_n
                )
            else:
                print("\n> End of season. No more upcoming matches.\n")
        elif action == "a":
            if round_n < n_rounds:
                upcoming_matches(
                    team_objects, matches, LONGEST_NAME_LEN, round_n, n_rounds
                )
            else:
                print("\n> End of season. No more upcoming matches.\n")
        elif action == "p":
            previous_round(len(teams) // 2)
        elif action == "r":
            previous_matches()
        elif action == "s":
            statistics_table(team_objects, team_codes, LONGEST_NAME_LEN)
        elif action == "e":
            return
        else:
            err_output(ERR_MSG[-1])


if __name__ == "__main__":
    main()
