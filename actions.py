class EventListener:

    def __init__(self, actions=[]):
        self.actions = actions

    def fire(self, game_state):
        for action in self.actions:
            action.execute(game_state)


class Action:

    def __init__(self):
        pass

    def execute(self, game_state):
        pass


class PrintMessageAction(Action):

    def __init__(self, message):
        super().__init__()
        self.message = message

    def execute(self, game_state):
        print(self.message)


class AddHotspotAction(Action):

    def __init__(self, hotspot, target_scene_id=None):
        super().__init__()
        self.hotspot = hotspot
        self.target_scene_id = target_scene_id

    def execute(self, game_state):
        target_scene = game_state.get_scene(self.target_scene_id) or game_state.current_scene
        target_scene.add_hotspot(self.hotspot)


class AddTransitionAction(Action):

    def __init__(self, transition, target_scene_id=None):
        super().__init__()
        self.transition = transition
        self.target_scene_id = target_scene_id

    def execute(self, game_state):
        target_scene = game_state.get_scene(self.target_scene_id) or game_state.current_scene
        target_scene.add_transition(self.transition)


class AddInventoryItemAction(Action):

    def __init__(self, inventory_item, target_scene_id=None):
        super().__init__()
        self.inventory_item = inventory_item
        self.target_scene_id = target_scene_id

    def execute(self, game_state):
        target_scene = game_state.get_scene(self.target_scene_id) or game_state.current_scene
        target_scene.add_item(self.inventory_item)


class SetSceneFlagAction(Action):

    def __init__(self, flag, target_scene_id=None):
        super().__init__()
        self.flag = flag
        self.target_scene_id = target_scene_id
    
    def execute(self, game_state):
        target_scene = game_state.get_scene(self.target_scene_id) or game_state.current_scene
        target_scene.set_flag(self.flag)


class UnsetSceneFlag(Action):

    def __init__(self, flag, target_scene_id):
        super().__init__()
        self.flag = flag
        self.target_scene_id = target_scene_id

    def execute(self, game_state):
         target_scene = game_state.get_scene(self.target_scene_id) or game_state.current_scene
         target_scene.unset_flag(self.flag)