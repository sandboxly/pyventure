from textutils import preprocess_text


class Command():

    def __init__(self, game_state):
        self.game_state = game_state

    def execute(self):
        pass


class QuitCommand(Command):

    def __init__(self, game_state):
        super().__init__(game_state)

    def execute(self):
        print('See you later!')
        exit()


class LookCommand(Command):

    def __init__(self, game_state):
        super().__init__(game_state)

    def execute(self):
        description = preprocess_text(self.game_state.current_scene.description, self.game_state)
        print(description)
        

class TransitionCommand(Command):

    def __init__(self, game_state, destination_id):
        super().__init__(game_state)
        self.destination_id = destination_id

    def execute(self):
        self.game_state.set_current_scene(self.destination_id)
        description = preprocess_text(self.game_state.current_scene.description, self.game_state)
        print(description)


class ExamineHotspotCommand(Command):

    def __init__(self, game_state, hotspot_id):
        super().__init__(game_state)
        self.hotspot_id = hotspot_id

    def execute(self):
        hotspot = self.game_state.current_scene.get_hotspot(self.hotspot_id)
        if hotspot is None:
            raise ValueError(f'Unknown hotspot ID {self.hotspot_id}.')
        description = hotspot.details
        description = preprocess_text(description, self.game_state)
        print(description)
        event_listener = hotspot.get_event_listener('examine')
        if event_listener:
            event_listener.fire(self.game_state)


class ExamineItemCommand(Command):

    def __init__(self, game_state, item_id):
        super().__init__(game_state)
        self.item_id = item_id

    def execute(self):
        inv_item = self.game_state.get_inventory_item(self.item_id)
        if inv_item is None:
            raise ValueError(f'Unknown item ID {self.item_id}.')
        description = preprocess_text(inv_item.details, self.game_state)
        print(description)
        event_listener = inv_item.get_event_listener('examine')
        if event_listener:
            event_listener.fire(self.game_state)


class TakeItemCommand(Command):

    def __init__(self, game_state, item_id):
        super().__init__(game_state)
        self.item_id = item_id

    def execute(self):
        inv_item = self.game_state.current_scene.get_item(self.item_id)
        if inv_item is None:
            raise ValueError(f'Unknown item ID {self.item_id}')
        self.game_state.current_scene.remove_item(self.item_id)
        self.game_state.add_inventory_item(inv_item)
        print(f'{inv_item.name} has been added to your inventory.')
        event_listener = inv_item.get_event_listener('take')
        if event_listener:
            event_listener.fire(self.game_state)


class InventoryCommand(Command):

    def __init__(self, game_state):
        super().__init__(game_state)

    def execute(self):
        if not (self.game_state.inventory):
            print('You do not carry anything with you.')
        else:
            print('Your inventory contains the following items:')
            for inv_item in self.game_state.inventory.values():
                print(f'* {inv_item.name}')


class DebugFlagsCommand(Command):

    def __init__(self, game_state):
        super().__init__(game_state)

    def execute(self):
        print('**********************************')
        print('Global Flags:')
        for flag in self.game_state.flags:
            print(f'* {flag}')
        print('**********************************')
        print('Current Scene Flags:')
        for flag in self.game_state.current_scene.flags:
            print(f'* {flag}')
