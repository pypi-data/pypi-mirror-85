from learns2.constants import races
from learns2.parser import SC2ReplayParser
from collections import deque, defaultdict
from collections.abc import Iterator
from typing import List


class EventIterator(Iterator):
    """Groups game events by game loop."""

    def __init__(self, events: List, num_frames: int):
        """
        :param events: raw sequence of game events
        :param num_frames: number of frames to return
        """
        self.events = deque(events)
        self.buffer = None
        self.frame = 0
        self.num_frames = num_frames

    def __next__(self):
        """Returns a list of all game events for the current frame."""
        if self.frame == self.num_frames:
            raise StopIteration
        buf = []
        while self.events and self.events[0]['_gameloop'] == self.frame:
            buf.append(self.events.popleft())
        self.frame += 1
        if not self.events and not buf:
            raise StopIteration
        return buf


def get_all_frames(replay, num_frames=500):
    parser = SC2ReplayParser(replay)
    itr = EventIterator(parser.events(), num_frames)
    return list(itr)

def get_players(replay):
    parser = SC2ReplayParser(replay)
    return parser.players()


class SC2ReplayFeaturizer(object):
    MAX_SELECTION_SIZE = 1000

    def __init__(self, replay, user_id: int, num_frames: int = 500, num_camera_hotspots: int = 5):
        self.frames = get_all_frames(replay, num_frames)
        self.players = get_players(replay)
        self.user_id = user_id
        self.num_camera_hotspots = num_camera_hotspots

    def feature(self) -> List[List[int]]:
        f1 = self.hotkey_feature()
        f2 = self.target_feature()
        f3 = self.races_feature()
        f4 = self.selection_feature()
        f5 = self.camera_hotspots_feature()
        f6 = self.scmd_feature()
        features = []
        for (i, j, k, x, y, z) in zip(f1, f2, f3, f4, f5, f6):
            features.append(i + j + k + x + y + z)
        return features

    def scmd_feature(self):
        features = []
        for frame in self.frames:
            feature = [0]
            for event in frame:
                if event['_event'] == 'NNet.Game.SCmdEvent' \
                        and event['_userid']['m_userId'] == self.user_id:
                    feature = [1]
            features.append(feature)
        return features

    def hotkey_feature(self):
        features = []
        for frame in self.frames:
            feature = [0] * 10
            for event in frame:
                if event['_event'] == 'NNet.Game.SControlGroupUpdateEvent' \
                        and event['_userid']['m_userId'] == self.user_id:
                    idx = event['m_controlGroupIndex']
                    feature[idx] = 1
            features.append(feature)
        return features

    def target_feature(self):
        features = []
        for frame in self.frames:
            feature = [0, 0]
            for event in frame:
                if event['_userid']['m_userId'] == self.user_id:
                    if event['_event'] == 'NNet.Game.SCmdUpdateTargetPointEvent':
                        feature[0] = 1
                    elif event['_event'] == 'NNet.Game.SCmdUpdateTargetUnitEvent':
                        feature[1] = 1
            features.append(feature)
        return features

    def races_feature(self):
        feature = [0, 0, 0]
        for p in self.players:
            if p['m_userId'] == self.user_id:
                race = races[p['m_race']]
                if race == 'Protoss':
                    feature[0] = 1
                elif race == 'Terran':
                    feature[1] = 1
                elif race == 'Zerg':
                    feature[2] = 1
        return [feature for _ in self.frames]

    def selection_feature(self):
        features = []
        for frame in self.frames:
            # This potentially overwrites earlier events in the rare case where there are multiple selection delta
            # events in a single gameloop. A quick scan of my replay folder found 0 occurrences of this, so I'm going to
            # ignore that case in the interest of simplicity.
            feature = [0]
            for event in frame:
                if event['_event'] == 'NNet.Game.SSelectionDeltaEvent' and event['_userid']['m_userId'] == self.user_id:
                    num_selected = len(event['m_delta']['m_addUnitTags'])
                    feature = [num_selected / self.MAX_SELECTION_SIZE]
            features.append(feature)
        return features

    def camera_hotspots_feature(self):
        # Count the number of times the player visited each (x, y) location
        locations = defaultdict(int)
        for frame in self.frames:
            for event in frame:
                if event['_event'] == 'NNet.Game.SCameraUpdateEvent' and event['_userid']['m_userId'] == self.user_id:
                    x, y = event['m_target']['x'], event['m_target']['y']
                    locations[(x, y)] += 1

        # Select the top n visited locations
        sorted_locations = {k: v for k, v in sorted(locations.items(), key=lambda item: item[1], reverse=True)}
        hotspots = [k for k in sorted_locations][:self.num_camera_hotspots]

        # Each feature is an array of length `self.num_camera_hotspots`
        # Each value in the array represents an individual camera hotspot
        # For each gameloop, set the features value to 1 if the user's camera matches the coordinates of the hotspot
        features = []
        for frame in self.frames:
            feature = [0] * self.num_camera_hotspots
            for event in frame:
                if event['_event'] == 'NNet.Game.SCameraUpdateEvent' and event['_userid']['m_userId'] == self.user_id:
                    x, y = event['m_target']['x'], event['m_target']['y']
                    for (idx, hotspot) in enumerate(hotspots):
                        if hotspot == (x, y):
                            feature[idx] = 1
            features.append(feature)

        return features
