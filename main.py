

#!/usr/bin/env python3
"""
Zoheb LLM Agent Toolkit - Main CLI Entry Point.
"""

import sys
import os
import io
import subprocess
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Ensure UTF-8 stdout on Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from scenarios import registry
from config import Config

console = Console()

BANNER = """[bold cyan]
==================================================
  ZOHEB LLM AGENT TOOLKIT - CYBERSECURITY LAB
==================================================[/bold cyan]
[bold yellow]Multi-Agent Security Operations & Adversary Emulation Framework[/bold yellow]
"""

@click.group()
def cli():
    """Zoheb LLM Agent Toolkit CLI - Run agent workflows and servers in lab environments."""
    pass

@cli.command(name="list")
def list_scenarios():
    """List all registered security scenarios."""
    console.print(BANNER)
    scenarios = registry.get_all()

    table = Table(title="Registered Lab Scenarios", show_header=True, header_style="bold magenta")
    table.add_column("Scenario Name", style="cyan", width=20)
    table.add_column("Description", style="white")

    for name, data in scenarios.items():
        table.add_row(name, data["description"])

    console.print(table)
    console.print("\n[dim]Run a scenario using: python main.py run <scenario_name>[/dim]")

@cli.command(name="run")
@click.argument("scenario_name")
def run_scenario(scenario_name: str):
    """Run a specific scenario by name."""
    console.print(BANNER)
    success = registry.run_scenario(scenario_name)
    if not success:
        console.print(f"[bold red]Error:[/bold red] Scenario '{scenario_name}' not found.")
        console.print("Run [bold cyan]python main.py list[/bold cyan] to see available scenarios.")

@cli.command(name="serve-http")
@click.option("--host", default=Config.LAB_HTTP_HOST, help="Host address to bind HTTP server.")
@click.option("--port", default=Config.LAB_HTTP_PORT, type=int, help="Port to run HTTP server.")
def serve_http(host, port):
    """Start local HTTP server for lab testing & exfiltration/download demos."""
    from servers.http_server import run_http_server
    run_http_server(host=host, port=port)

@cli.command(name="serve-ftp")
@click.option("--host", default=Config.LAB_FTP_HOST, help="Host address to bind FTP server.")
@click.option("--port", default=Config.LAB_FTP_PORT, type=int, help="Port to run FTP server.")
def serve_ftp(host, port):
    """Start mock FTP server for lab file transfer testing."""
    from servers.ftp_server import run_ftp_server
    run_ftp_server(host=host, port=port)

@cli.command(name="notebook")
@click.option("--ip", default="0.0.0.0", help="Network interface IP to expose notebook server on.")
@click.option("--port", default=8888, type=int, help="Port for Jupyter notebook server.")
def start_notebook(ip, port):
    """Launch Jupyter Notebook server exposed on specified IP (for VM access)."""
    console.print(f"[bold green]Starting Jupyter Notebook server on {ip}:{port}...[/bold green]")
    cmd = [sys.executable, "-m", "jupyter", "notebook", f"--ip={ip}", f"--port={port}", "--no-browser"]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        console.print("\nJupyter server stopped.")

@cli.command(name="serve-web")
@click.option("--host", default="127.0.0.1", help="Host address for Web GUI Dashboard.")
@click.option("--port", default=5000, type=int, help="Port to run Web GUI Dashboard.")
def serve_web(host, port):
    """Launch interactive Web Application Dashboard at http://localhost:5000."""
    from web_gui import run_web_gui
    run_web_gui(host=host, port=port)

if __name__ == "__main__":
    cli()
