"""
MainFrame Code Generator - AI Agent for Generating MainFrame Code

This package provides an AI agent that can generate MainFrame code including:
- COBOL programs
- JCL (Job Control Language)
- DB2 SQL
- CICS programs
"""

__version__ = "1.0.0"
__author__ = "MainFrame Developer"

from .agent import MainFrameAgent
from .config import Config

__all__ = ["MainFrameAgent", "Config"]

