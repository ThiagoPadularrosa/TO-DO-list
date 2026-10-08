import typer
import httpx
from rich.console import Console
from rich.table import Table
from typing import Optional

console = Console()

app = typer.Typer(help="CLI Client for my FastAPI backend.")
BASE_URL = "http://127.0.0.1:8000"

@app.command()
def list_tasks(
  skip: int = typer.Option(0, help="Number of tasks to skip"),
  limit: int = typer.Option(100, help="Max number of tasks to return")
):
  """
  Display all todo tasks in a styled table.
  """
  params = { "skip": skip, "limit": limit }

  try:
    with httpx.Client() as client:
      response = client.get(f"{BASE_URL}/user/task/", params=params)

    if response.status_code == 200: 
      tasks = response.json()
      if not tasks:
          console.print("[yellow] Your todo list is completely empty![/yellow]")
          return

      table = Table(title="My MySQL todo list")
      table.add_column("ID", justify="center", style="cyan", no_wrap=True)
      table.add_column("Status", justify="center")
      table.add_column("Title", style="magenta")
      table.add_column("Description", style="green")

      for task in tasks:
        status = "[green] Done[/green]" if task["is_completed"] else "[red]Pending[/red]"
        table.add_row(
          str(task["id"]),
          status,
          task["title"],
          task["description"] or ""
        )

      console.print(table)
    else:
      console.print(f"[red]Failed to fetch tasks. Server responded with: {response.status_code}[/red]")
  except httpx.RequestError as exc:
    console.print(f"[red]Could not connect to API server: {exc}[/red]")

@app.command()
def add_task(
  title: str = typer.Argument(..., help="The title of the task"),
  description: Optional[str] = typer.Option(None, "--desc", "-d", help="Optional description")
):
  """Add a new task making and persist it to the database (MySQL)."""
  payload = { "title": title, "description": description }

  with httpx.Client() as client:
    response = client.post(f"{BASE_URL}/user/task/add", json=payload)

  if response.status_code == 201:
    task_id = response.json()["id"]
    console.print(f"[green]Success![/green] Created task [bold cyan]#{task_id}[/bold cyan]: '{title}'")
  else:
    console.print(f"[red]Failed to create task: {response.status_code}[/red]")

@app.command()
def update_task( 
  task_id: int = typer.Argument(..., help="ID of the task to update"),
):
  """
  Update/Modify an existing task's payload or completion status (PUT).
  """
  with httpx.Client() as client:
    response = client.get(f"{BASE_URL}/user/task/{task_id}")
    if response.status_code == 200:
      existing_task = response.json()
      new_title = typer.prompt("Enter updated title", default=existing_task["title"])
      new_description = typer.prompt("Enter updated description", default=existing_task["description"])
      new_completed = typer.confirm("Is this task completed?", default=existing_task["is_completed"])

      # This has to map exactly the Pydantic model
      payload = {
        "title": new_title,
        "description": new_description,
        "is_completed": new_completed
      } 

      response2 = client.put(f"{BASE_URL}/user/task/{task_id}", json=payload)
      if response2.status_code == 200:
        console.print(f"[green]Task #{task_id} successfully synchronized and updated with MySQL![/green]")
        console.print(response2.json())
      else:
        console.print(f"[red]Failed to apply update. Server returned status: {response2.status_code}")
        console.print(response2.json())

    elif response.status_code == 404:
      console.print(f"[yellow] Task #{task_id} does not exist.[/yellow]")
      raise typer.Exit()
    elif response.status_code == 422:
      console.print(f"[red] Validation Error[/red]")
      console.print(response.json())
    else:
      console.print(f"[red]Error updating resource: {response.status_code}[/red]")

@app.command()
def remove(task_id: int = typer.Argument(..., help="ID of the task to vaporize")):
  """
    Permanently drop a task row by ID (DELETE)
  """
  with httpx.Client() as client:
    response = client.delete(f"{BASE_URL}/user/task/{task_id}")
    if response.status_code == 204:
      typer.confirm("Are you sure?")
      console.print(f"[green]Task #{task_id} dropped successfully from database.[/green]")
    elif response.status_code == 404:
      console.print(f"[yellow]Task #{task_id} not found.[/yellow]")
    else:
      console.print(f"[red]Server error: {response.status_code}[/red]")

if __name__ == "__main__":
  app()