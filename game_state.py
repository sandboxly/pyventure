from commands import DebugFlagsCommand, ExamineHotspotCommand,\
                     ExamineItemCommand,\
                     InventoryCommand,\
                     LookCommand,\
                     QuitCommand,\
                     TakeItemCommand,\
                     TransitionCommand


class GameState:
    
    def __init__(self, initial_scene, scenes):
        self.initial_scene = initial_scene
        self.current_scene = initial_scene
        self.scenes = scenes
        self.inventory = {}
        self.flags = []
        self.command_context = {}
        self.debug = False

    def build_command_context(self):
        self.command_context.clear()

        # Register basic commands
        self.register_command(['quit', 'exit'], QuitCommand(self))
        self.register_command(['look', 'look around'], LookCommand(self))
        self.register_command(['inventory', 'i'], InventoryCommand(self))

        # Register debug commands
        if self.debug:
            self.register_command(['$flags'], DebugFlagsCommand(self))

        # Register transition commands
        for transition in self.current_scene.transitions.values():
            destination_id = transition.destination_id
            transition_command = TransitionCommand(self, destination_id)
            transition_name = transition.name.strip().lower()
            utterances = [transition_name, f'go {transition_name}']\
                + [s.strip().lower() for s in transition.synonyms]\
                + [f'go {s.strip().lower()}' for s in transition.synonyms]
            self.register_command(utterances, transition_command)

        # Register examine hotspot commands
        for hotspot in self.current_scene.hotspots.values():
            hotspot_id = hotspot.hotspot_id
            examine_command = ExamineHotspotCommand(self, hotspot_id)
            hotspot_name = hotspot.name.strip().lower()
            utterances = [f'examine {hotspot_name}']\
                + [f'examine {s.strip().lower()}' for s in hotspot.synonyms]
            self.register_command(utterances, examine_command)

        # Register examine and take actions for items in scene
        for inv_item in self.current_scene.items.values():
            item_id = inv_item.item_id
            examine_command = ExamineItemCommand(self, item_id)
            take_command = TakeItemCommand(self, item_id)
            item_name = inv_item.name.strip().lower()
            examine_utterances = [f'examine {item_name}']\
                + [f'examine {s.strip().lower()}' for s in inv_item.synonyms]
            self.register_command(examine_utterances, examine_command)
            take_utterances = [f'take {item_name}'] + [f'take {s.strip().lower()}' for s in inv_item.synonyms]
            self.register_command(take_utterances, take_command)

        for inv_item in self.inventory.values():
            item_id = inv_item.item_id
            examine_command = ExamineItemCommand(self, item_id)
            item_name = inv_item.name.strip().lower()
            utterances = [f'examine {item_name}']\
                + [f'examine {s.strip().lower()}' for s in inv_item.synonyms]
            self.register_command(utterances, examine_command)

    def register_command(self, utterances, command):
        for utterance in utterances:
            self.command_context[utterance] = command

    def get_scene(self, scene_id):
        return self.scenes.get(scene_id)

    def set_current_scene(self, scene_id):
        scene = self.scenes.get(scene_id)
        if scene is None:
            raise ValueError(f'Unknown scene ID {scene_id}')
        self.current_scene = scene

    def get_inventory_item(self, item_id):
        return self.inventory.get(item_id)
    
    def add_inventory_item(self, inv_item):
        self.inventory[inv_item.item_id] = inv_item

    def remove_inventory_item(self, item_id):
        del self.inventory[item_id]

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