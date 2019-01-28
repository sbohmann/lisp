from io import open
import re


input_pattern = re.compile('(\d+) players; last marble is worth (\d+) points')


def run():
    for configuration in read_configurations():
        print(Game(configuration).highest_score)


def read_configurations():
    configurations = []
    for raw_line in open('input.txt'):
        line = raw_line.strip()
        match = input_pattern.fullmatch(line)
        num_players = int(match[1])
        highest_marble = int(match[2])
        configurations.append(Configuration(num_players, highest_marble))
    return configurations


class Configuration:
    def __init__(self, num_players, highest_marble):
        self.num_players = num_players
        self.highest_marble = highest_marble


class Game:
    def __init__(self, configuration):
        self._num_players = configuration.num_players
        self._highest_marble = configuration.highest_marble
        self.highest_score = 0
        self._run()

    def _run(self):
        self._circle = Circle()
        self._create_players()
        for value in range(0, self._highest_marble + 1):
            self._play_round(value)

    def _create_players(self):
        self._players = [Player(index) for index in range(0, self._num_players)]
        self._current_player = self._players[0]

    def _play_round(self, value):
        self._play_according_to_value(value)
        self._adjust_highest_score()
        self._advance_player()

    def _play_according_to_value(self, value):
        if value > 0 and value % 23 == 0:
            self._play_special_marble(value)
        else:
            self._play_ordinary_marble(value)

    def _play_special_marble(self, value):
        self._current_player.score += value
        removed_marble_value = self._circle.remove_after(-8)
        self._current_player.score += removed_marble_value

    def _play_ordinary_marble(self, value):
        self._circle.insert_after(1, value)

    def _adjust_highest_score(self):
        player_score = self._current_player.score
        if player_score > self.highest_score:
            self.highest_score = player_score

    def _advance_player(self):
        self._current_player = self._players[self._next_player_index()]

    def _next_player_index(self):
        return (self._current_player.index + 1) % len(self._players)


class Player:
    def __init__(self, index):
        self.index = index
        self.score = 0


class Circle:
    def __init__(self):
        self.current = None

    def insert_after(self, relpos, value):
        if self.current is None:
            self.current = Marble(value)
        else:
            marble_at_relpos, marble_after_relpos = self._marbles_at_and_after_relpos(relpos)
            new_marble = self._insert_between(marble_at_relpos, marble_after_relpos, value)
            self.current = new_marble

    def remove_after(self, relpos):
        if self.current is None:
            raise ValueError()
        else:
            marble_at_relpos, marble_after_relpos = self._marbles_at_and_after_relpos(relpos)
            removed_marble_value = self._remove_next(marble_at_relpos, marble_after_relpos)
            return removed_marble_value

    def _marbles_at_and_after_relpos(self, relpos):
        if relpos == 0:
            return self.current, self.current.next
        elif relpos > 0:
            return self._marbles_at_and_after_positive_offset(relpos)
        else:
            return self._marbles_at_and_after_negative_offset(-relpos)

    def _marbles_at_and_after_positive_offset(self, offset):
        at = self.current
        for index in range(0, offset):
            at = at.next
        return at, at.next

    def _marbles_at_and_after_negative_offset(self, offset):
        at = self.current
        for index in range(0, offset - 1):
            at = at.previous
        return at.previous, at

    def _insert_between(self, marble_at_relpos, marble_after_relpos, value):
        new_marble = Marble(value, marble_at_relpos, marble_after_relpos)
        marble_at_relpos.next = new_marble
        marble_after_relpos.previous = new_marble
        return new_marble

    def _remove_next(self, marble, next):
        if marble == next:
            raise ValueError
        removed_marble_value = next.value
        marble.next = next.next
        next.next.previous = marble
        self.current = next.next
        return removed_marble_value


class Marble:
    def __init__(self, value, previous=None, next=None):
        self.value = value
        self.previous = previous if previous is not None else self
        self.next = next if next is not None else self


run()
