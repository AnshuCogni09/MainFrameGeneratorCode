"""
MainFrame Code Generator - Setup Configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README if available
readme_file = Path(__file__).parent / "README.md"
long_description = "MainFrame Code Generator - AI Agent for generating MainFrame code"
if readme_file.exists():
    long_description = readme_file.read_text(encoding='utf-8')

setup(
    name="mainframe-generator",
    version="1.0.0",
    author="MainFrame Developer",
    author_email="developer@example.com",
    description="AI Agent for generating MainFrame Code (COBOL, JCL, DB2, CICS)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/mainframe-generator",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.12.0",
        "python-dotenv>=1.0.0",
        "rich>=13.7.0",
        "pyyaml>=6.0.1",
        "click>=8.1.7",
        "jinja2>=3.1.3",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "mypy>=1.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mainframe=mainframe_generator.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "mainframe_generator": ["*.yaml", "*.yml"],
    },
)

