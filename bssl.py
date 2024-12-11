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
    first_name: str
    last_name: str
    current_team: str
    off_skill: int
    def_skill: int
    num_seasons_played: int
    injury_status: InjuryStatus

    def __init__(self, first_name, last_name, team):
        self.id = gen_id()
        self.first_name = first_name
        self.last_name = last_name
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
    record: tuple[int, int, int] # (wins, losses, ties)
    average_off: int
    average_def: int

    def __init__(self, owner, name, stadium):
        self.owner = owner
        self.name = name
        self.stadium = stadium
        self.record = (0, 0, 0)
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

    def __str__(self):
        out = ""
        out += f"Team: {self.name}\nOwner: {self.owner}\nStadium: {self.stadium}\nRecord: {self.record[0]} wins, {self.record[1]} losses, {self.record[2]} ties\n\nActive roster: ({self.average_off} OFF, {self.average_def} DEF)\n"
        for player in self.active_roster:
            out += f"\t{player.first_name} {player.last_name} ({player.current_team}) - {player.off_skill} offensive rating, {player.def_skill} defensive rating - "
            out += f"season number {player.num_seasons_played} - Injured: {player.injury_status.is_injured}\n"
        out += "\nBench:\n"
        for player in self.bench:
                    out += f"\t{player.first_name} {player.last_name} ({player.current_team}) - {player.off_skill} offensive rating, {player.def_skill} defensive rating - "
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
    home_team: Team
    away_team: Team

def main():
    random.seed(time.time())

    t1 = Team(owner="Reilly", name="The Devs", stadium="Silicon Valley Field")
    t2 = Team(owner="Reilly", name="The Bugs", stadium="Errorville Stadium")
    print(t1)
    print(t2)

if __name__ == "__main__":
    main()
