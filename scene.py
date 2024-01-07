class Transition:

    def __init__(self, name, destination_id, synonyms=[]):
        self.name = name
        self.destination_id = destination_id
        self.synonyms = synonyms


class Scene:

    def __init__(self, scene_id, title, description, transitions=[], hotspots=[], items=[]):
        self.scene_id = scene_id
        self.title = title
        self.description = description
        self.transitions = { t.name: t for t in transitions }
        self.items = { i.item_id: i for i in items }
        self.hotspots = { h.hotspot_id: h for h in hotspots }
        self.flags = []

    def get_transition(self, transition_id):
        return self.transitions.get(transition_id)
    
    def add_transition(self, transition):
        self.transitions[transition.name] = transition

    def remove_transition(self, transition_name):
        del self.transitions[transition_name]
    
    def get_hotspot(self, hotspot_id):
        return self.hotspots.get(hotspot_id)
    
    def add_hotspot(self, hotspot):
        self.hotspots[hotspot.hotspot_id] = hotspot

    def remove_hotspot(self, hotspot_id):
        del self.hotspots[hotspot_id]
    
    def get_item(self, item_id):
        return self.items.get(item_id)
    
    def add_item(self, item):
        self.items[item.item_id] = item
    
    def remove_item(self, item_id):
        del self.items[item_id]

    def set_flag(self, flag):
        if flag not in self.flags:
            self.flags.append(flag)

    def unset_flag(self, flag):
        self.flags = [f for f in self.flags if f != flag]

    def check_flag(self, flag):
        return flag in self.flags
    
    def toggle_flag(self, flag):
        if self.check_flag(flag):
            self.unset_flag(flag)
        else:
            self.set_flag(flag)
    
    def describe(self):
        print('\n')
        print(self.title)
        print('******************************************')
        print(self.description)
    

class Hotspot:

    def __init__(self, hotspot_id, name, details, synonyms=[], event_listeners={}):
        self.hotspot_id = hotspot_id
        self.name = name
        self.details = details
        self.synonyms = synonyms
        self.event_listeners = event_listeners

    def describe(self):
        print(self.details)

    def register_event_listener(self, event_name, event_listener):
        self.event_listeners[event_name] = event_listener

    def get_event_listener(self, event_name):
        return self.event_listeners.get(event_name)


class InventoryItem:

    def __init__(self, item_id, name, details, synonyms=[], event_listeners={}):
        self.item_id = item_id
        self.name = name
        self.details = details
        self.synonyms = synonyms
        self.event_listeners = event_listeners

    def register_event_listener(self, event_name, event_listener):
        self.event_listeners[event_name] = event_listener

    def get_event_listener(self, event_name):
        return self.event_listeners.get(event_name)
