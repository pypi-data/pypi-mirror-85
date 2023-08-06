from s2protocol import versions
from mpyq import MPQArchive
from typing import List
import os


class SC2ReplayParser(object):
    def __init__(self, replay: str):
        self.archive = MPQArchive(replay)
        self.protocol = self.read_protocol(self.archive)
        self._initdata = None
        self._details = None
        self._events = None

    @staticmethod
    def read_protocol(archive: MPQArchive):
        content = archive.header['user_data_header']['content']
        header = versions.latest().decode_replay_header(content)
        base_build = header['m_version']['m_baseBuild']
        try:
            return versions.build(base_build)
        # https://github.com/Blizzard/s2protocol/issues/99
        # If the protocol is not defined, the previous protocol often works anyway
        except ImportError as e:
            print(f'Unable to import protocol{base_build}.py. Module does not exist')
            base_path = os.path.dirname(versions.__file__)
            protocols = set([p for p in os.listdir(base_path)])
            while base_build > 0:
                base_build -= 1
                candidate = f'protocol{base_build}.py'
                if candidate in protocols:
                    print(f'Falling back to {candidate}')
                    return versions.build(base_build)
            raise e

    @staticmethod
    def read_initdata(protocol, archive: MPQArchive) -> dict:
        init_file = archive.read_file('replay.initData')
        return protocol.decode_replay_initdata(init_file)

    @staticmethod
    def read_details(protocol, archive: MPQArchive) -> dict:
        detail_file = archive.read_file('replay.details')
        return protocol.decode_replay_details(detail_file)

    @staticmethod
    def read_game_events(protocol, archive: MPQArchive) -> dict:
        game_event_file = archive.read_file('replay.game.events')
        return protocol.decode_replay_game_events(game_event_file)

    def initdata(self) -> dict:
        if self._initdata is None:
            self._initdata = self.read_initdata(self.protocol, self.archive)
        return self._initdata

    def details(self) -> dict:
        """https://github.com/Blizzard/s2protocol/blob/master/docs/flags/details.md"""
        if self._details is None:
            self._details = self.read_details(self.protocol, self.archive)
        return self._details

    def events(self):
        if self._events is None:
            self._events = list(self.read_game_events(self.protocol, self.archive))
        return self._events

    def players(self) -> List[dict]:
        slots = self.initdata()['m_syncLobbyState']['m_lobbyState']['m_slots']
        slot_id_to_user_id = {}
        for slot in slots:
            if slot['m_observe'] == 0:
                slot_id, user_id = slot['m_workingSetSlotId'], slot['m_userId']
                slot_id_to_user_id[slot_id] = user_id
        player_list = self.details()['m_playerList']
        player_objects = []
        for player in player_list:
            slot_id = player['m_workingSetSlotId']
            if slot_id in slot_id_to_user_id:
                userid = slot_id_to_user_id[slot_id]
                player['m_userId'] = userid
                player['m_userInitialData'] = self.initdata()['m_syncLobbyState']['m_userInitialData'][userid]
                player['m_localizedId'] = '{}/{}/{}'.format(player['m_toon']['m_region'], player['m_toon']['m_realm'],
                                                            player['m_toon']['m_id'])
                player_objects.append(player)
        return [decode_utf8(obj) for obj in player_objects]

    def small_details(self):
        details = self.details()
        description = self.initdata()['m_syncLobbyState']['m_gameDescription']
        return {
            'm_title': details['m_title'],
            'm_isBlizzardMap': details['m_isBlizzardMap'],
            'm_timeUTC': details['m_timeUTC'],
            'm_timeLocalOffset': details['m_timeLocalOffset'],
            'm_mapSizeX': description['m_mapSizeX'],
            'm_mapSizeY': description['m_mapSizeY']
        }

    def to_dict(self):
        num_events = len(self.events())
        payload = {
            'isLabeled': False,
            'labels': {},
            'details': self.small_details(),
            'players': self.players(),
            'numEvents': num_events
        }
        return decode_utf8(payload)


# Slightly modified from:
# https://stackoverflow.com/questions/57014259/json-dumps-on-dictionary-with-bytes-for-keys
def decode_utf8(d: dict) -> dict:
    result = {}
    for key, value in d.items():
        try:
            if isinstance(key, bytes):
                key = key.decode()
            if isinstance(value, bytes):
                value = value.decode()
            elif isinstance(value, dict):
                value = decode_utf8(value)
            elif isinstance(value, list):
                decoded = [decode_utf8(v) for v in value]
                value = decoded
        except:
            value = ''
        result.update({key: value})
    return result
