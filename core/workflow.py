from typing import List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from .task import BaseTask

console = Console()

class Workflow:
    """Manages sequential execution of tasks across agents."""

    def __init__(self, name: str, description: str, tasks: List[BaseTask]):
        self.name = name
        self.description = description
        self.tasks = tasks

    def run(self) -> Dict[str, str]:
        console.print(Panel(f"[bold cyan]{self.name}[/bold cyan]\n[dim]{self.description}[/dim]", title="🚀 Scenario Execution"))
        
        context_accumulator = ""
        results = {}

        for idx, task in enumerate(self.tasks, start=1):
            console.print(f"\n[bold yellow]Step {idx}/{len(self.tasks)}: Executing Task '{task.name}' with Agent '{task.agent.name}' ({task.agent.role})...[/bold yellow]")
            
            output = task.run(context=context_accumulator if context_accumulator else None)
            results[task.name] = output

            # Display result panel
            console.print(Panel(Markdown(output), title=f"✓ Task Output: {task.name}", border_style="green"))

            # Accumulate output for context passing
            context_accumulator += f"\n\n--- [Output from Task: {task.name} ({task.agent.name})] ---\n{output}"

        console.print(f"\n[bold green]✨ Scenario '{self.name}' completed successfully![/bold green]")
        return results
