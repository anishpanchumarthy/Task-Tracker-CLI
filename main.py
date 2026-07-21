import sys

from pathlib import Path

def show_help():
    """Prints available commands to User """
    print('\n Available commands:')
    print('help            - Show this guide')
    print('exit            - Close the application\n')

def create_file():
    """Checks if a tasks.json file exists and creates it if it doesn't"""
    path = Path('/Users/anishpanchumarthy/Desktop/tasks/')
    file = Path("/Users/anishpanchumarthy/Desktop/tasks/tasks.json")
    if not file.is_file():
        with open(path/'tasks.json', 'w') as f:
            f.write('This is your task tracker file. Your tasks are ')
def main():
    while True:
        try:
            create_file()
            user_input = input("Task_Tracker_CLI: ").strip()

            if not user_input:
                continue
            parts = user_input.split()
            command = parts[0].lower()
            arg = parts[1:]

            if command == 'exit':
                print('Goodbye')
                sys.exit(0)
            elif command == 'help':
                show_help()

            else:
                print(f'Unknown command: {command}')



        except (KeyboardInterrupt, EOFError):
            #handle Ctrl+C or Ctrl+D signals
            print("\nGoodbye!")
            sys.exit(0)

if __name__ == '__main__':
    main()
