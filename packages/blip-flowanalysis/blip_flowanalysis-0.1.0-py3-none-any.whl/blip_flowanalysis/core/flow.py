from __future__ import nested_scopes
import typing as tp
import json


class Flow:
    """Represents chatbot flow structure.
    
    Attributes:
        * structure (dict) - flow structure
    
    Methods:
        * get_states_list - Return the flow state list
        * get_tracks_id - Return track identification information
    """
    
    def __init__(self, json_obj: str) -> None:
        super().__init__()
        self.structure = json.loads(json_obj)

    def __str__(self):
        """Return str(self.structure)."""
        return str(self.structure)
    
    def __len__(self):
        """Return len(self.structure)."""
        return len(self.structure)
        
    def get_states_list(self) -> list:
        """Return the flow state list."""
        return self.structure["settings"]["flow"]["states"]

    def get_tracks_id(self) -> tp.Dict[str, tp.List[tp.Dict[str, str]]]:
        """Return track identification information.
         
         Tracking is recommended for analytics reports in Blip portal - (source)[https://docs.blip.ai/#analytics].
         The identification information are: `state-id`, `input_type` and `action`
         
         :return: For every `track_name` a list of info for id.
         :rtype: ``tp.Dict[str, tp.List[tp.Dict[str, str]]]``
         """
        def __insert_action(type: str, id: str) -> None:
            """Internal method to filter track info"""
            if action["type"] == "TrackEvent":
                key = action["settings"]["category"]
                
                track_filter = {
                    "state-id": id,
                    "input_type": type,
                    "action": action["settings"].get("action")
                }
                if tracking_dict.get(key):
                    tracking_dict[key].append(track_filter)
                else: tracking_dict[key] = [track_filter]
            
        state_list = self.get_states_list()
        tracking_dict = dict()
        for state in state_list:
            for action in state["inputActions"]:
                __insert_action(type="inputActions", id=state["id"])

            for action in state["outputActions"]:
                __insert_action(type="outputActions", id=state["id"])

        return tracking_dict
