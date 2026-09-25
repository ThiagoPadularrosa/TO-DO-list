tasks = []

while True:
    print("1. View Tasks:")
    print("2. Add Task:")
    print("3. Delete a Task:")
    print("4. Exit")

    user_choice = input("Enter your choice (1-4): ")

    if user_choice == "1":
      for index, task in enumerate(tasks, start=1):
        print(f"{index}. {task}")
    elif user_choice == "2":
        task = input("Add task: ")
        tasks.append(task)
    elif user_choice == "3":
        user_delete_task = input("Select the task (1 to ..): ")
        try:
           index = int(user_delete_task) - 1
           selected_task = tasks[index] 
           tasks.remove(selected_task)
        except ValueError:
           print("Please enter a valid whole number")
        except IndexError:
           print("That index is out of range for this list.")
    elif user_choice == "4":
        break