import yaml
from actions import AddHotspotAction, AddInventoryItemAction, AddTransitionAction, EventListener, PrintMessageAction, SetSceneFlagAction, UnsetSceneFlag
from game_state import GameState

from scene import Hotspot, InventoryItem, Scene, Transition


def load_yaml_data(filename):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)


def parse_scenes(data):
    scenes = {}
    for scene_id, scene_data in data['scenes'].items():
        transitions = [Transition(**t) for t in scene_data.get('transitions', [])]
        hotspots = [parse_hotspot(h) for h in scene_data.get('hotspots', [])]
        items = [parse_inventory_item(i) for i in scene_data.get('items', [])]
        scenes[scene_id] = Scene(scene_id, scene_data['title'], scene_data['description'], transitions, hotspots, items)
    return scenes


def parse_hotspot(hotspot_data):
    event_listeners = {}
    for event, actions in hotspot_data.get('event_listeners', {}).items():
        parsed_actions = [parse_action(action_data) for action_data in actions]
        event_listeners[event] = EventListener(actions=parsed_actions)
    return Hotspot(hotspot_data['hotspot_id'], hotspot_data['name'], hotspot_data['details'], hotspot_data.get('synonyms', []), event_listeners)


def parse_inventory_item(inv_item_data):
    event_listeners = {}
    for event, actions in inv_item_data.get('event_listeners', {}).items():
        parsed_actions = [parse_action(action_data) for action_data in actions]
        event_listeners[event] = EventListener(actions=parsed_actions)
    return InventoryItem(inv_item_data['item_id'], inv_item_data['name'], inv_item_data['details'], inv_item_data.get('synonyms', []), event_listeners)


def parse_action(action_data):
    if action_data['action_type'] == 'PrintMessage':
        return PrintMessageAction(action_data['message'])
    elif action_data['action_type'] == 'AddHotspot':
        return AddHotspotAction(parse_hotspot(action_data['hotspot']), action_data.get('target_scene_id'))
    elif action_data['action_type'] == 'AddTransition':
        return AddTransitionAction(Transition(**action_data['transition']), action_data.get('target_scene_id'))
    elif action_data['action_type'] == 'AddInventoryItem':
        return AddInventoryItemAction(parse_inventory_item(action_data['inventory_item']), action_data.get('target_scene_id'))
    elif action_data['action_type'] == 'SetSceneFlag':
        return SetSceneFlagAction(action_data['flag'], action_data.get('target_scene_id'))
    elif action_data['action_type'] == 'UnsetSceneFlag':
        return UnsetSceneFlag(action_data['flag'], action_data.get('target_scene_id'))
    # Add more action types as needed
    else:
        raise ValueError(f"Unknown action type: {action_data['action_type']}")    


def load_game_state_from_file(filename):
    game_data = load_yaml_data(filename)  # Call the function with filename
    scenes = parse_scenes(game_data)
    initial_scene_id = next(iter(scenes))  # Assuming the first scene is the starting scene
    return GameState(initial_scene=scenes[initial_scene_id], scenes=scenes)
