# run with powershell command > py -m poetry run python bssl.py

import sys, os

import random
import time

FIRST_NAMES: list[str] = ["John", "Luigi", "Ol'", "Wutzit", "Pajama", "Douglas", "Adam", "Jean", "Patrick", "Who"]
LAST_NAMES: list[str] = ["Doe", "de Italia", "Reliable", "Tooya", "Sam", "Douglas", "Parkzer", "Valjean", "O'Patrick", "Asked"]

def gen_id() -> str:
    id: str = ""
    for i in range(8):
        id += str(random.randint(0,9))
    return id

class InjuryStatus:
    is_injured: bool
    description: str
    skill_decrease: int
    weeks_to_heal: int

    def __init__(self):
        self.is_injured = False
        self.description = "No injury"
        self.skill_decrease = 0
        self.weeks_to_heal = 0

class Player:
    id: str
    name: str
    current_team: str
    off_skill: int
    def_skill: int
    num_seasons_played: int
    injury_status: InjuryStatus

    def __init__(self, first_name: str, last_name:str, team: str):
        self.id = gen_id()
        self.name = first_name + " " + last_name
        self.current_team = team
        self.off_skill = random.randint(0, 100)
        self.def_skill = random.randint(0, 100)
        self.num_seasons_played = 0
        self.injury_status = InjuryStatus()

class Team:
    id: str
    name: str
    stadium: str
    owner: str
    active_roster: list[Player]
    bench: list[Player]
    wins: int
    losses: int
    ties: int
    average_off: int
    average_def: int

    def __init__(self, owner: str, name: str, stadium: str):
        self.owner = owner
        self.name = name
        self.stadium = stadium
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.id = gen_id()
        self.active_roster = []
        total_off: int = 0
        total_def: int = 0
        for i in range(6):
            p = Player(random.choice(FIRST_NAMES), random.choice(LAST_NAMES), self.name)
            total_off += p.off_skill
            total_def += p.def_skill
            self.active_roster.append(p)
        self.average_off = (total_off / 6.0).__floor__()
        self.average_def = (total_def / 6.0).__floor__()
        self.bench = []
        for i in range(4):
            self.bench.append(Player(random.choice(FIRST_NAMES), random.choice(LAST_NAMES), self.name))

    def print(self):
        out = ""
        out += f"Team: {self.name}\nOwner: {self.owner}\nStadium: {self.stadium}\nRecord: {self.wins} wins, {self.losses} losses, {self.ties} ties\n\nActive roster: ({self.average_off} OFF, {self.average_def} DEF)\n"
        for player in self.active_roster:
            out += f"\t{player.name} ({player.current_team}) - {player.off_skill} offensive rating, {player.def_skill} defensive rating - "
            out += f"season number {player.num_seasons_played} - Injured: {player.injury_status.is_injured}\n"
        out += "\nBench:\n"
        for player in self.bench:
                    out += f"\t{player.name} ({player.current_team}) - {player.off_skill} offensive rating, {player.def_skill} defensive rating - "
                    out += f"season number {player.num_seasons_played} - Injured: {player.injury_status.is_injured}\n"
        return out

    def update_active_average_skill(self):
        total_off: float = 0
        total_def: float = 0
        for p in self.active_roster:
            total_off += p.off_skill
            total_def += p.def_skill
        self.average_off = (total_off / 6.0).__floor__()
        self.average_def = (total_def / 6.0).__floor__()

class Game:
    week_number: int
    home_team: Team
    away_team: Team
    stadium: str
    remaining_first_half_ticks: int = 22
    remaining_second_half_ticks: int = 23
    score: list[int] = [0, 0] # (home, away)
    # home_lineup: list[Player] = []
    # away_lineup: list[Player] = []
    current_offense: Team
    current_defense: Team
    current_offense_position: int = 2
    halftime_starting_offense: Team
    halftime_starting_defense: Team
    current_tick: int = 1

    def __init__(self, home_team: Team, away_team: Team):
        self.home_team = home_team
        self.away_team = away_team
        self.home_team.update_active_average_skill()
        self.away_team.update_active_average_skill()
        self.week_number = 1
        self.stadium = self.home_team.stadium
        random.shuffle(self.home_team.active_roster)
        random.shuffle(self.away_team.active_roster)
        if random.randint(0,1) == 1:
            self.current_offense = self.home_team
            self.current_defense = self.away_team
            self.halftime_starting_offense = self.away_team
            self.halftime_starting_defense = self.home_team
        else:
            self.current_offense = self.away_team
            self.current_defense = self.home_team
            self.halftime_starting_offense = self.home_team
            self.halftime_starting_defense = self.away_team

    def run_game(self):
        print(f"Welcome to week {self.week_number} of the BSSL. Today's match is {self.home_team.name} at home ({self.home_team.stadium}) against {self.away_team.name}!")
        print(f"{self.current_offense.name} have won the coin toss and will begin the game on offense. BEGIN!")
        while self.remaining_first_half_ticks > 0:
            self.tick()
            self.remaining_first_half_ticks -= 1
        print(f"FIRST HALF COMPLETE:\n{self.home_team.name} {self.score[0]} - {self.score[1]} {self.away_team.name}\n")
        self.current_offense = self.halftime_starting_offense
        self.current_defense = self.halftime_starting_defense
        self.current_offense_position = 2
        print(f"{self.current_offense.name} will start the 2nd half on offense. BEGIN!")
        while self.remaining_second_half_ticks > 0:
            self.tick()
            self.remaining_second_half_ticks -= 1
        print(f"GAME COMPLETE:\n{self.home_team.name} {self.score[0]} - {self.score[1]} {self.away_team.name}\n")
        if self.score[0] > self.score[1]:
            self.home_team.wins += 1
            self.away_team.losses += 1
            print(f"{self.home_team.name.upper()} WIN!")
        elif self.score[0] == self.score[1]:
            self.home_team.ties += 1
            self.away_team.ties += 1
            print(f"TIE GAME!")
        else:
            self.away_team.wins += 1
            self.home_team.losses += 1
            print(f"{self.away_team.name.upper()} WIN!")

    def tick(self):
        tick_update: str = f"Minute {self.current_tick * 2}: "
        offense_roll: int = random.randint(0, self.current_offense.average_off)
        defense_roll: int = random.randint(0, self.current_defense.average_def)
        score_update_index: int = 0 if self.current_offense == self.home_team else 1
        if self.current_offense_position == 5:
            tick_update += f"{self.current_offense.name} on offense at the goal. {self.current_offense.active_roster[self.current_offense_position].name} shoots... "
            if offense_roll >= defense_roll:
                self.score[score_update_index] += 1
                self.current_offense, self.current_defense = self.current_defense, self.current_offense # swap off and def after scoring
                self.current_offense_position = 2 # reset to middle of field
                tick_update += "AND SCORES!"
            else:
                self.current_offense, self.current_defense = self.current_defense, self.current_offense # swap off and def after block
                self.current_offense_position = 0 # goalie is offense position 0
                tick_update += f"BUT IS SAVED BY {self.current_defense.active_roster[5-self.current_offense_position].name}!" # index simplified from len(def_active_roster) (ALWAYS 6) - current_pos - 1
        else:
            tick_update += f"{self.current_offense.name} on offense. {self.current_offense.active_roster[self.current_offense_position].name} passes up to {self.current_offense.active_roster[self.current_offense_position + 1].name}... "
            if offense_roll >= defense_roll:
                self.current_offense_position += 1
                tick_update += "SUCCESSFULLY!"
            else:
                self.current_offense_position = 5 - self.current_offense_position # update new team's offensive position, mirrored across field
                self.current_offense, self.current_defense = self.current_defense, self.current_offense # swap off and def after scoring
                tick_update += f"BUT IS INTERCEPTED BY {self.current_offense.active_roster[self.current_offense_position].name}"
        print(tick_update)
        self.current_tick += 1

def main():
    random.seed(time.time())

    t1 = Team(owner="Reilly", name="The Devs", stadium="Silicon Valley Field")
    t2 = Team(owner="Reilly", name="The Bugs", stadium="Errorville Stadium")
    g = Game(t1, t2)
    g.run_game()
    t1.print()
    t2.print()

if __name__ == "__main__":
    main()
