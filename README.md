# MainFrame Code Generator

An AI-powered agent for generating MainFrame code (COBOL, JCL, DB2 SQL, CICS programs).

## Features

- **AI-Powered Generation**: Uses OpenAI GPT-4o for intelligent code generation
- **Multiple Languages**: Supports COBOL, JCL, DB2 SQL, and CICS
- **Template-Based Generation**: Fallback to template-based code generation
- **Code Validation**: Validates generated code for syntax and best practices
- **CLI Interface**: Easy-to-use command-line interface
- **Interactive Mode**: Interactive mode for exploring the generator

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (for AI-powered generation)

### Install from Source

```bash
# Clone or download the repository
cd MainFrame

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Environment Setup

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Add your OpenAI API key to `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Command Line

```bash
# Initialize the generator
mainframe init

# Generate COBOL code
mainframe generate cobol "basic program to read a file"

# Generate JCL
mainframe generate jcl "sort job to sort input file"

# Generate DB2 SQL
mainframe generate db2 "select employee where id = :ws-id"

# Generate CICS code
mainframe generate cics "screen program for employee inquiry"

# List available templates
mainframe templates cobol

# List supported languages
mainframe languages

# Validate code
mainframe validate cobol "program.cbl"

# Interactive mode
mainframe interactive
```

### Python API

```python
from mainframe_generator import MainFrameAgent, Config

# Initialize agent
agent = MainFrameAgent()

# Generate COBOL code
code = agent.generate_cobol("basic program to process employee data")

# Generate JCL
jcl = agent.generate_jcl("sort job")

# Generate DB2 SQL
sql = agent.generate_db2("select from employee table")

# Generate CICS
cics = agent.generate_cics("screen program")

# Save to file
agent.save_to_file(code, "program.cbl")

# Validate code
result = agent.validator.validate(code, "cobol")
print(f"Valid: {result.is_valid}")
```

## Supported Code Types

### COBOL
- Basic programs
- File I/O programs
- DB2 programs
- Report programs
- Subprograms

### JCL (Job Control Language)
- Basic jobs
- Sort jobs
- COBOL compile and run
- DB2 utilities
- Dataset operations
- Conditional execution

### DB2 SQL
- SELECT statements
- INSERT/UPDATE/DELETE
- CREATE TABLE
- CREATE INDEX
- Stored procedures
- Cursors
- Triggers
- Views

### CICS
- Basic programs
- Screen/MAP programs
- File control programs
- DB2 programs
- Web services

## Configuration

Edit `config.yaml` to customize:

```yaml
openai:
  model: "gpt-4o"
  temperature: 0.2
  max_tokens: 4000

generation:
  default_language: "COBOL"
  validation_enabled: true

output:
  default_directory: "./output"
```

## Development

### Running Tests

```bash
# Run all tests
python tests/test_generators.py

# Or using pytest
pytest tests/
```

### Project Structure

```
MainFrame/
├── src/
│   └── mainframe_generator/
│       ├── __init__.py
│       ├── agent.py          # Main agent
│       ├── config.py         # Configuration
│       ├── cli.py            # CLI interface
│       ├── generators/       # Code generators
│       ├── validators/       # Code validators
│       └── templates/        # Templates
├── tests/
│   └── test_generators.py
├── config.yaml
├── requirements.txt
└── setup.py
```

## License

MIT License

## Author

MainFrame Developer

