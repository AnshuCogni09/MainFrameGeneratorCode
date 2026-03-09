"""
MainFrame Code Generator - CLI Interface

Command-line interface for the MainFrame Code Generator agent.
"""

import os
import sys
import click
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

from . import MainFrameAgent, Config
from .generators import COBOLGenerator, JCLGenerator, DB2Generator, CICSGenerator


console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """MainFrame Code Generator - AI Agent for generating MainFrame code.
    
    Generate COBOL, JCL, DB2 SQL, and CICS programs using AI.
    """
    pass


@cli.command()
@click.option('--config', '-c', type=click.Path(exists=True), help='Path to config file')
@click.option('--model', '-m', default='gpt-4o', help='OpenAI model to use')
@click.option('--temperature', '-t', default=0.2, type=float, help='Generation temperature')
def init(config: Optional[str], model: str, temperature: float):
    """Initialize the MainFrame Code Generator."""
    # Load config
    cfg = Config(config) if config else Config()
    
    # Override with CLI options
    if model:
        cfg._config.setdefault('openai', {})['model'] = model
    if temperature:
        cfg._config.setdefault('openai', {})['temperature'] = temperature
    
    # Display welcome
    console.print(Panel.fit(
        "[bold cyan]MainFrame Code Generator v1.0.0[/bold cyan]\n\n"
        "AI Agent for generating MainFrame code\n"
        "Supports: COBOL, JCL, DB2 SQL, CICS",
        border_style="cyan"
    ))
    
    # Check API key
    if cfg.openai_api_key:
        console.print("[green]✓[/green] OpenAI API key configured")
        console.print(f"  Model: {cfg.openai_model}")
        console.print(f"  Temperature: {cfg.temperature}")
    else:
        console.print("[yellow]⚠[/yellow] No OpenAI API key found")
        console.print("  Set OPENAI_API_KEY environment variable")
    
    console.print("\n[bold]Ready to generate MainFrame code![/bold]")


@cli.command()
@click.argument('code_type')
@click.argument('description')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--params', '-p', multiple=True, help='Additional parameters (key=value)')
@click.option('--no-ai', is_flag=True, help='Use template-based generation only')
@click.option('--config', '-c', type=click.Path(exists=True), help='Config file path')
def generate(code_type: str, description: str, output: Optional[str], 
             params: tuple, no_ai: bool, config: Optional[str]):
    """Generate MainFrame code.
    
    CODE_TYPE: Type of code (cobol, jcl, db2, cics)
    DESCRIPTION: Description of what the code should do
    
    Examples:
        mainframe generate cobol "basic program to read a file"
        mainframe generate jcl "sort job to sort input file"
        mainframe generate db2 "select employee where id = :ws-id"
        mainframe generate cics "screen program for employee inquiry"
    """
    # Parse parameters
    param_dict = {}
    for param in params:
        if '=' in param:
            key, value = param.split('=', 1)
            param_dict[key.strip()] = value.strip()
    
    # Initialize agent
    cfg = Config(config) if config else Config()
    agent = MainFrameAgent(cfg)
    
    # Generate code
    try:
        use_ai = not no_ai and bool(cfg.openai_api_key)
        
        with console.status(f"[bold green]Generating {code_type.upper()} code..."):
            code = agent.generate(code_type, description, param_dict, use_ai=use_ai)
        
        # Display code
        console.print(Panel(
            code,
            title=f"[bold]{code_type.upper()} Code[/bold]",
            border_style="green"
        ))
        
        # Save to file if specified
        if output:
            filepath = agent.save_to_file(code, output)
            console.print(f"\n[green]✓[/green] Saved to: {filepath}")
        
        # Validate
        if cfg.get("generation.validation_enabled", True):
            result = agent.validator.validate(code, code_type)
            if result.warnings:
                console.print("\n[yellow]Warnings:[/yellow]")
                for warning in result.warnings:
                    console.print(f"  • {warning.message}")
    
    except ValueError as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {str(e)}")
        sys.exit(1)


@cli.command()
@click.argument('code_type')
@click.option('--config', '-c', type=click.Path(exists=True), help='Config file path')
def templates(code_type: str, config: Optional[str]):
    """List available templates for a code type."""
    cfg = Config(config) if config else Config()
    
    if code_type.lower() == 'cobol':
        gen = COBOLGenerator(cfg)
    elif code_type.lower() == 'jcl':
        gen = JCLGenerator(cfg)
    elif code_type.lower() == 'db2':
        gen = DB2Generator(cfg)
    elif code_type.lower() == 'cics':
        gen = CICSGenerator(cfg)
    else:
        console.print(f"[red]Unknown code type: {code_type}[/red]")
        sys.exit(1)
    
    template_list = gen.get_available_templates()
    
    table = Table(title=f"Available {code_type.upper()} Templates")
    table.add_column("Template Name", style="cyan")
    table.add_column("Description", style="white")
    
    descriptions = {
        'basic': 'Basic program structure',
        'file_io': 'File input/output operations',
        'db2': 'Database operations',
        'report': 'Report generation',
        'subprogram': 'Called program/subroutine',
        'sort': 'Sort utility job',
        'cobol_run': 'Compile and run COBOL',
        'db2_utilities': 'DB2 utility jobs',
        'iefbr14': 'Dataset operations',
        'repro': 'IDCAMS REPRO',
        'ftp': 'FTP transfer',
        'conditional': 'Conditional execution',
        'select': 'SELECT statement',
        'insert': 'INSERT statement',
        'update': 'UPDATE statement',
        'delete': 'DELETE statement',
        'stored_procedure': 'Stored procedure',
        'cursor': 'Cursor operations',
        'trigger': 'Trigger definition',
        'view': 'View definition',
        'screen': 'Screen/MAP program',
        'file': 'File control program',
        'command': 'Command level program',
        'webservice': 'Web service program',
        'batch': 'Batch online program'
    }
    
    for template in template_list:
        desc = descriptions.get(template, 'Custom template')
        table.add_row(template, desc)
    
    console.print(table)


@cli.command()
@click.option('--config', '-c', type=click.Path(exists=True), help='Config file path')
def list_languages(config: Optional[str]):
    """List supported mainframe languages."""
    cfg = Config(config) if config else Config()
    agent = MainFrameAgent(cfg)
    
    languages = agent.get_supported_languages()
    
    table = Table(title="Supported MainFrame Languages")
    table.add_column("Language", style="cyan")
    table.add_column("Description", style="white")
    
    descriptions = {
        'COBOL': 'Common Business-Oriented Language',
        'JCL': 'Job Control Language',
        'DB2': 'IBM Database 2 SQL',
        'CICS': 'Customer Information Control System'
    }
    
    for lang in languages:
        table.add_row(lang, descriptions.get(lang, ''))
    
    console.print(table)


@cli.command()
@click.argument('code_type')
@click.argument('code')
@click.option('--config', '-c', type=click.Path(exists=True), help='Config file path')
def validate(code_type: str, code: str, config: Optional[str]):
    """Validate MainFrame code syntax."""
    cfg = Config(config) if config else Config()
    agent = MainFrameAgent(cfg)
    
    # Read code from file if it exists
    if Path(code).exists():
        code = Path(code).read_text()
    
    result = agent.validator.validate(code, code_type)
    
    if result.is_valid:
        console.print("[green]✓[/green] Code is valid!")
    else:
        console.print("[red]✗[/red] Code has errors:")
        for error in result.errors:
            if error.line_number:
                console.print(f"  Line {error.line_number}: {error.message}")
            else:
                console.print(f"  {error.message}")
    
    if result.warnings:
        console.print("\n[yellow]Warnings:[/yellow]")
        for warning in result.warnings:
            if warning.line_number:
                console.print(f"  Line {warning.line_number}: {warning.message}")
            else:
                console.print(f"  {warning.message}")


@cli.command()
def interactive():
    """Start interactive mode."""
    cfg = Config()
    agent = MainFrameAgent(cfg)
    
    console.print(Panel.fit(
        "[bold cyan]Interactive Mode[/bold cyan]\n\n"
        "Type 'help' for available commands\n"
        "Type 'exit' to quit",
        border_style="cyan"
    ))
    
    while True:
        try:
            user_input = console.input("\n[bold cyan]>[/bold cyan] ")
            user_input = user_input.strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            if user_input.lower() == 'help':
                console.print("\n[bold]Available commands:[/bold]")
                console.print("  cobol <description>  - Generate COBOL code")
                console.print("  jcl <description>   - Generate JCL code")
                console.print("  db2 <description>   - Generate DB2 SQL")
                console.print("  cics <description> - Generate CICS code")
                console.print("  languages           - List supported languages")
                console.print("  templates <type>   - List templates")
                console.print("  exit                - Exit interactive mode")
                continue
            
            if user_input.lower() == 'languages':
                languages = agent.get_supported_languages()
                console.print(f"Supported: {', '.join(languages)}")
                continue
            
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            description = parts[1] if len(parts) > 1 else ''
            
            if command in ['cobol', 'jcl', 'db2', 'cics']:
                if not description:
                    console.print("[yellow]Please provide a description[/yellow]")
                    continue
                
                code = agent.generate(command, description)
                console.print(Panel(code, border_style="green"))
            else:
                console.print(f"[red]Unknown command: {command}[/red]")
                console.print("Type 'help' for available commands")
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit[/yellow]")
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")


def main():
    """Main entry point."""
    cli()


if __name__ == '__main__':
    main()

