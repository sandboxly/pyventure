import argparse

from fileio import load_game_state_from_file
from textutils import preprocess_text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str, help='Game data file path', default='examples/lost-love.pyventure')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')

    args = parser.parse_args()
    filename = args.filename
    game_state = load_game_state_from_file(filename)
    game_state.debug = args.debug
    
    description = preprocess_text(game_state.current_scene.description, game_state)
    print(description)

    while True:
        game_state.build_command_context()
        utterance = input("What do you want to do? ").strip().lower()
        command = game_state.command_context.get(utterance)
        
        if command is None:
            print('I don\'t understand that command.')
        else:
            command.execute()

main()