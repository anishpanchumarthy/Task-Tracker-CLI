import sys
import json
from datetime import datetime
from pathlib import Path
# todo: make a description function
# todo: make a status changer
# todo: make a listing feature
# todo: make a deleting featyre


# initializes the id counter which will be return by the true id in create_file()
id_counter = 0
file = Path("/Users/anishpanchumarthy/Desktop/tasks/tasks.json")

def show_help():
    """Prints available commands to User """
    print('\n Available commands:')
    print('add             - adds whatever text that follows as a task that has status todo')
    print('help            - Show this guide')
    print('exit            - Close the application\n')

def get_time():
    """Returns the current time as a string"""
    return datetime.now().strftime('%Y-%m-%d %I:%M:%p')

def create_file():
    """Checks if a tasks.json file exists and creates it if it doesn't & adds the id counter to the beginning of the Json file"""
    global file
    if not file.is_file():
        #prog is a key for dictionary containing useful value for the application not the user
        json_dict = {'prog': {'id_counter': 0}}
        with open(file, 'w') as f:
            json.dump(json_dict, f)

def get_last_id():
    """Returns the last id of the last task added to the Json file"""
    global file
    with open(file, 'r') as f:
        json_dict = json.load(f)
        id_dict = json_dict.get('prog')
        id_counter = id_dict.get('id_counter')
        return id_counter


def add(task):
    """creates a task with the input as the string, gives it a id #, a createdat time, and the status to do
    the id # can be found as the key for the key:pair that has the dictionary with the rest of the elements"""
    global file
    id= get_last_id()
    id += 1
    print(id)
    #this block of code rewrites the id_counter in the file
    with open(file, 'r') as f:
        json_dict = json.load(f)
    #     id_dict = prog_dict.get('prog')
    #     id_dict.update({'id_counter', id})
    #this block of code creates the task and its info
    task_dict = {}
    task_dict.update({'task': task})
    task_dict.update({'createdat': get_time()})
    task_dict.update({'status': 'todo'})
    task_str = str(task_dict)
    json_dict.update({1: task_str})
    new_id = {"id_counter": id}
    json_dict.update({'prog': new_id})
    with open(file, 'w') as f:
        json.dump(json_dict, f)


def main():
    while True:
        create_file()
        try:
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
            elif command == 'add':
                add(arg)
            else:
                print(f'Unknown command: {command}')



        except (KeyboardInterrupt, EOFError):
            #handle Ctrl+C or Ctrl+D signals
            print("\nGoodbye!")
            sys.exit(0)

if __name__ == '__main__':
    main()
