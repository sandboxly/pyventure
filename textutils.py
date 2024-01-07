from jinja2 import Template

def preprocess_text(text, game_state):
    template = Template(text)
    return template.render(flags=game_state.flags, scene_flags=game_state.current_scene.flags)
