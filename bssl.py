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
    owner: str
    active_roster: list[Player]
    bench: list[Player]
    record: tuple[int, int, int] # (wins, losses, ties)

    def __init__(self, owner, name):
        self.owner = owner
        self.name = name
        self.record = (0, 0, 0)
        self.id = gen_id()
        self.active_roster = []
        for i in range(6):
            self.active_roster.append(Player(random.choice(FIRST_NAMES), random.choice(LAST_NAMES), self.name))
        self.bench = []
        for i in range(4):
            self.bench.append(Player(random.choice(FIRST_NAMES), random.choice(LAST_NAMES), self.name))

    def __str__(self):
        out = ""
        out += f"Team: {self.name}\nOwner: {self.owner}\nRecord: {self.record[0]} wins, {self.record[1]} losses, {self.record[2]} ties\n\nActive roster:\n"
        for player in self.active_roster:
            out += f"\t{player.first_name} {player.last_name} ({player.current_team}) - {player.off_skill} offensive rating, {player.def_skill} defensive rating - "
            out += f"season number {player.num_seasons_played} - Injured: {player.injury_status.is_injured}\n"
        out += "\nBench:\n"
        for player in self.bench:
                    out += f"\t{player.first_name} {player.last_name} ({player.current_team}) - {player.off_skill} offensive rating, {player.def_skill} defensive rating - "
                    out += f"season number {player.num_seasons_played} - Injured: {player.injury_status.is_injured}\n"
        return out

def main():
    random.seed(time.time())

    t1 = Team(owner="Reilly", name="The Devs")
    t2 = Team(owner="Reilly", name="The Bugs")
    print(t1)
    print(t2)

if __name__ == "__main__":
    main()
