import sys
import json
from datetime import datetime
from pathlib import Path


# initializes the id counter which will be return by the true id in create_file()
id_counter = 0
file = Path("/Users/anishpanchumarthy/Projects/Github/Task-Tracker-CLI/tasks/tasks.json")

def show_help():
    """Prints available commands to User """
    print("\nAvailable commands:")
    print("add [task text]                       - Add whatever text that follows 'add' as a task that has status todo")
    print('\n')
    print("describe [task id] [description]      - Add a description to a task with id #")
    print('\n')
    print("mark [task id] [status]               - Add new status to a task with id #")
    print('\n')
    print("update [task id] [task text]          - Update a task with id #")
    print('\n')
    print("list [status(optional)]               - Lists all tasks or lists task in status category if specified")
    print('\n')
    print("delete [task id]                      - Delete a task or tasks with id #'s and moves up the rest of the tasks")
    print('\n')
    print('reset                                 - resets the entire task tracker')
    print('\n')
    print("help                                  - Show this guide")
    print('\n')
    print("exit                                  - Close the application\n")


def get_time():
    """Returns the current time as a string"""
    return datetime.now().strftime("%Y-%m-%d %I:%M:%p")

def create_file():
    """Checks if a tasks.json file exists and creates it if it doesn"t & adds the id counter to the beginning of the Json file"""
    global file
    if not file.is_file():
        #prog is a key for dictionary containing useful value for the application not the user
        json_dict = {"prog": {"id_counter": 0}}
        with open(file, "w") as f:
            json.dump(json_dict, f)

def get_last_id():
    """Returns the last id of the last task added to the Json file"""
    global file
    with open(file, "r") as f:
        json_dict = json.load(f)
        id_dict = json_dict.get("prog")
        id_counter = id_dict.get("id_counter")
        return id_counter

def add(task):
    """creates a task with the input as the string, gives it a id #, a createdat time, and the status to do
    the id # can be found as the key for the key:pair that has the dictionary with the rest of the elements"""
    global file
    id= get_last_id()
    id += 1
    #this block of code rewrites the id_counter in the file
    with open(file, "r") as f:
        json_dict = json.load(f)
    #     id_dict = prog_dict.get("prog")
    #     id_dict.update({"id_counter", id})
    #this block of code creates the task and its info
    task_dict = {}
    task_dict.update({"id": id})
    task_dict.update({"task": task})
    task_dict.update({"createdat": get_time()})
    task_dict.update({"status": "todo"})
    json_dict.update({id: task_dict})
    new_id = {"id_counter": id}
    json_dict.update({"prog": new_id})
    with open(file, "w") as f:
        json.dump(json_dict, f)

def describe(task_id,description):
    """Takes in two inputs: task_id and description string that adds a description to a task, it will replace a description if one already exists"""
    global file
    #this block of code adds a description key:pair
    descrip_dict = {"descrip": description}
    #opens file and takes out the tasks dictionary
    with open(file, "r") as f:
        json_dict = json.load(f)
    #checks to see if task id is valid
    if task_id not in json_dict.keys():
        print(f"There is not task with id # {task_id}")
    else:
        task_dict = json_dict.get(task_id)
        #updates the task dict with the new description
        task_dict.update(descrip_dict)
        json_dict.update({task_id: task_dict})
        with open(file, "w") as f:
            json.dump(json_dict, f)

def status(task_id,status):
    """Takes in two inputs: task_id and status that will change the status of the task to the new status"""
    global file
    #opens file and takes out the tasks dictionary
    with open(file, "r") as f:
        json_dict = json.load(f)
    #checks to see if task id is valid
    if task_id not in json_dict.keys():
        print(f"There is not task with id # {task_id}")
    else:
        status = status.lower()
        #checks to see if new status is valid
        if status not in ["todo","done","in progress"]:
            print(f"{status} is not a valid status")
        else:
            task_dict = json_dict.get(task_id)
            #updates the task dict with the new status
            task_dict["status"] = status
            task_dict["updatedat"] = get_time()
            json_dict.update({task_id: task_dict})
            with open(file, "w") as f:
                json.dump(json_dict, f)

def update(task_id,task):
    """Takes in two inputs: task_id and new task text that will change the name of the task"""
    global file
    #opens file and takes out the tasks dictionary
    with open(file, "r") as f:
        json_dict = json.load(f)
    #checks to see if task id is valid
    if task_id not in json_dict.keys():
        print(f"There is not task with id # {task_id}")
    else:
        task_dict = json_dict.get((task_id))
        #updates the task dict with the new status
        task_dict["task"] = task
        task_dict["updatedat"] = get_time()
        json_dict.update({task_id: task_dict})
        with open(file, "w") as f:
            json.dump(json_dict, f)

def list(status = "all"):
    """lists out tasks, by default all but if a status is put in it will list the ones with the status"""
    global file
    # opens file and takes out the tasks dictionary
    with open(file, "r") as f:
        json_dict = json.load(f)
    del json_dict["prog"]
    tasks_dict = json_dict
    if status == "all":
        print('All tasks:')
        for d in tasks_dict.values():
            if "updatedat" in d and "descrip" in d:
                print(f"Task {d.get('id')}: {d.get("task")} | Status: {d.get("status")}\nDescription: {d.get("descrip")}\nCreated at: {d.get("createdat")} | Updated at: {d.get("updatedat")}")
                print('---------------------')
            elif "descrip" in d:
                print(f"Task {d.get('id')}: {d.get("task")} | Status: {d.get("status")}\nDescription: {d.get("descrip")}\nCreated at: {d.get("createdat")}")
                print('---------------------')
            elif "updatedat" in d:
                print( f"Task {d.get('id')}: {d.get("task")} | Status: {d.get("status")}\nCreated at: {d.get("createdat")} | Updated at: {d.get("updatedat")}")
                print('---------------------')
            else:
                print(f"Task {d.get('id')}: {d.get("task")} | Status: {d.get("status")}\nCreated at: {d.get("createdat")}")
                print('---------------------')
    elif status == "todo":
        print('To-do tasks:')
        for d in tasks_dict.values():
            if d["status"] == "todo":
                if "updatedat" in d and "descrip" in d:
                    print(
                        f"Task {d.get('id')}: {d.get("task")} | Status: {d.get("status")}\nDescription: {d.get("descrip")}\nCreated at: {d.get("createdat")} | Updated at: {d.get("updatedat")}")
                    print('---------------------')
                elif "descrip" in d:
                    print(
                        f"Task {d.get('id')}: {d.get("task")} | Status: {d.get("status")}\nDescription: {d.get("descrip")}\nCreated at: {d.get("createdat")}")
                    print('---------------------')
                elif "updatedat" in d:
                    print(
                        f"Task {d.get('id')}: {d.get("task")} | Status: {d.get("status")}\nCreated at: {d.get("createdat")} | Updated at: {d.get("updatedat")}")
                    print('---------------------')
                else:
                    print(f"Task {d.get('id')}: {d.get("task")} | Status: {d.get("status")}\nCreated at: {d.get("createdat")}")
                    print('---------------------')
    elif status == "done":
        print('Done tasks:')
        for d in tasks_dict.values():
            if d["status"] == "done":
                if "updatedat" in d and "descrip" in d:
                    print(
                        f"Task {d.get('id')}: {d.get("task")} | Status: {d.get("status")}\nDescription: {d.get("descrip")}\nCreated at: {d.get("createdat")} | Updated at: {d.get("updatedat")}")
                    print('---------------------')
                elif "descrip" in d:
                    print(
                        f"Task {d.get('id')}: {d.get("task")} | Status: {d.get("status")}\nDescription: {d.get("descrip")}\nCreated at: {d.get("createdat")}")
                    print('---------------------')
                elif "updatedat" in d:
                    print(
                        f"Task {d.get('id')}: {d.get("task")} | Status: {d.get("status")}\nCreated at: {d.get("createdat")} | Updated at: {d.get("updatedat")}")
                    print('---------------------')
    elif status == "in progress":
        print('In Progress tasks:')
        for d in tasks_dict.values():
            if d["status"] == "in progress":
                if "updatedat" in d and "descrip" in d:
                    print(
                        f"Task {d.get('id')}: {d.get("task")} | Status: {d.get("status")}\nDescription: {d.get("descrip")}\nCreated at: {d.get("createdat")} | Updated at: {d.get("updatedat")}")
                    print('---------------------')
                elif "descrip" in d:
                    print(
                        f"Task {d.get('id')}: {d.get("task")} | Status: {d.get("status")}\nDescription: {d.get("descrip")}\nCreated at: {d.get("createdat")}")
                    print('---------------------')
                elif "updatedat" in d:
                    print(
                        f"Task {d.get('id')}: {d.get("task")} | Status: {d.get("status")}\nCreated at: {d.get("createdat")} | Updated at: {d.get("updatedat")}")
                    print('---------------------')

def delete(task_id):
    """takes in a task_id and deletes a task"""
    global file
    # opens file and takes out the tasks dictionary
    with open(file, "r") as f:
        json_dict = json.load(f)
    # checks to see if task id is valid
    if task_id not in json_dict.keys():
        print(f"There is not task with id # {task_id}")
    else:
        num_changes = len(json_dict) - int(task_id)
        del json_dict[task_id]
        for x in (range(num_changes-1)):
            num = x + int(task_id)
            newspot = json_dict.pop(str(num + 1))
            newspot['id'] = num
            json_dict[num] = newspot
        new_id_count = json_dict.get('prog').get('id_counter') - 1
        json_dict['prog'] = {'id_counter': new_id_count}
        with open(file, "w") as f:
            json.dump(json_dict, f)

def reset():
    global file
    json_dict = {"prog": {"id_counter": 0}}
    with open(file, "w") as f:
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

            if command == "exit":
                print("Goodbye")
                sys.exit(0)
            elif command == "help":
                show_help()
            elif command == "add":
                combined_arg = " ".join(arg)
                add(combined_arg)
            elif command == "describe":
                combined_arg = " ".join(arg[1:])
                describe(arg[0], combined_arg)
            elif command == "mark":
                combined_arg = " ".join(arg[1:])
                status(arg[0], combined_arg)
            elif command == "update":
                combined_arg = " ".join(arg[1:])
                update(arg[0], combined_arg)
            elif command == "list":
                combined_arg = " ".join(arg)
                if combined_arg in ['done','todo','in progress']:
                    list(combined_arg)
                else:
                    print(combined_arg)
                    list()
            elif command == "delete":
                if len(arg) != 1:
                    arg = sorted(arg, key=int, reverse=True)
                    for x in arg:
                        delete(x)
                else:
                    delete(arg[0])
            elif command == "reset":
                reset()
            else:
                print(f"Unknown command: {command}")


        except (KeyboardInterrupt, EOFError):
            #handle Ctrl+C or Ctrl+D signals
            print("\nGoodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()
