"""
MainFrame Code Generator - Core AI Agent

This module contains the main agent class that orchestrates
all mainframe code generation operations using AI.
"""

import os
import logging
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

from openai import OpenAI

from .config import Config
from .generators.cobol_generator import COBOLGenerator
from .generators.jcl_generator import JCLGenerator
from .generators.db2_generator import DB2Generator
from .generators.cics_generator import CICSGenerator
from .validators.code_validator import CodeValidator
from .templates.template_manager import TemplateManager


class MainFrameAgent:
    """AI Agent for generating MainFrame code (COBOL, JCL, DB2, CICS)."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the MainFrame Code Generator Agent.
        
        Args:
            config: Configuration object. If None, uses default config.
        """
        self.config = config or Config()
        self._setup_logging()
        self._initialize_components()
        
        self.logger.info("MainFrame Agent initialized successfully")

    def _setup_logging(self) -> None:
        """Set up logging for the agent."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(getattr(logging, self.config.log_level))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, self.config.log_level))
        console_formatter = logging.Formatter(self.config.log_format)
        console_handler.setFormatter(console_formatter)
        
        # File handler
        file_handler = logging.FileHandler(self.config.get("logging.file", "mainframe_generator.log"))
        file_handler.setLevel(getattr(logging, self.config.log_level))
        file_formatter = logging.Formatter(self.config.log_format)
        file_handler.setFormatter(file_formatter)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def _initialize_components(self) -> None:
        """Initialize all components."""
        # Initialize OpenAI client
        self.client = None
        if self.config.openai_api_key:
            self.client = OpenAI(api_key=self.config.openai_api_key)
            self.logger.info(f"OpenAI client initialized with model: {self.config.openai_model}")
        else:
            self.logger.warning("No OpenAI API key found. AI features will be limited.")

        # Initialize generators
        self.generators = {
            'cobol': COBOLGenerator(self.config),
            'jcl': JCLGenerator(self.config),
            'db2': DB2Generator(self.config),
            'cics': CICSGenerator(self.config)
        }
        
        # Initialize validator
        self.validator = CodeValidator(self.config)
        
        # Initialize template manager
        self.template_manager = TemplateManager(self.config)
        
        self.logger.info(f"Initialized {len(self.generators)} generators: {', '.join(self.generators.keys())}")

    def generate(
        self,
        code_type: str,
        description: str,
        params: Optional[Dict[str, Any]] = None,
        use_ai: bool = True
    ) -> str:
        """Generate mainframe code.
        
        Args:
            code_type: Type of code to generate (cobol, jcl, db2, cics)
            description: Description of the code to generate
            params: Additional parameters for code generation
            use_ai: Whether to use AI for generation (vs template-based)
            
        Returns:
            Generated mainframe code as string
            
        Raises:
            ValueError: If code_type is not supported
        """
        code_type = code_type.lower()
        
        if code_type not in self.generators:
            raise ValueError(f"Unsupported code type: {code_type}. Supported types: {', '.join(self.generators.keys())}")
        
        self.logger.info(f"Generating {code_type} code: {description[:50]}...")
        
        params = params or {}
        
        if use_ai and self.client:
            # Use AI-powered generation
            code = self._generate_with_ai(code_type, description, params)
        else:
            # Use template-based generation
            generator = self.generators[code_type]
            code = generator.generate(description, params)
        
        # Validate generated code
        if self.config.get("generation.validation_enabled", True):
            validation_result = self.validator.validate(code, code_type)
            if not validation_result.is_valid:
                self.logger.warning(f"Validation warnings: {validation_result.errors}")
        
        self.logger.info(f"Successfully generated {code_type} code")
        return code

    def _generate_with_ai(
        self,
        code_type: str,
        description: str,
        params: Dict[str, Any]
    ) -> str:
        """Generate code using OpenAI.
        
        Args:
            code_type: Type of code to generate
            description: Description of the code
            params: Additional parameters
            
        Returns:
            Generated code
        """
        system_prompt = self._get_system_prompt(code_type)
        user_prompt = self._build_user_prompt(code_type, description, params)
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            code = response.choices[0].message.content
            
            # Clean up the response (remove markdown code blocks if present)
            if code and code.startswith("```"):
                lines = code.split('\n')
                code = '\n'.join(lines[1:-1]) if lines[-1].startswith("```") else '\n'.join(lines[1:])
            
            return code.strip()
            
        except Exception as e:
            self.logger.error(f"AI generation failed: {str(e)}")
            # Fall back to template-based generation
            self.logger.info("Falling back to template-based generation")
            generator = self.generators[code_type]
            return generator.generate(description, params)

    def _get_system_prompt(self, code_type: str) -> str:
        """Get system prompt for specific code type."""
        prompts = {
            'cobol': """You are an expert COBOL programmer with 20+ years of experience.
You generate production-ready COBOL programs following best practices:
- Use proper COBOL syntax (COBOL 85 or newer)
- Include appropriate DATA DIVISION, PROCEDURE DIVISION sections
- Follow naming conventions (01 level for records, 77 for independent items)
- Include proper error handling and file status checking
- Add meaningful comments
- Use structured programming techniques""",
            
            'jcl': """You are an expert in JCL (Job Control Language) for IBM Mainframes.
You generate production-ready JCL:
- Use proper JCL statements (JOB, EXEC, DD)
- Include proper dataset definitions
- Use appropriate DISP parameters
- Include COND statements for conditional execution
- Use PROC and symbolic parameters when appropriate
- Follow IBM standards""",
            
            'db2': """You are an expert in DB2 SQL for IBM Mainframes.
You generate production-ready DB2 SQL:
- Use proper SQL syntax for DB2
- Include appropriate table definitions with proper data types
- Use indexes for performance
- Follow naming conventions
- Include primary and foreign keys
- Use stored procedures when appropriate""",
            
            'cics': """You are an expert in CICS (Customer Information Control System) programming.
You generate production-ready CICS programs:
- Use proper CICS API calls (EXEC CICS ...)
- Include proper BMS map definitions
- Use appropriate transaction IDs
- Follow CICS programming best practices
- Include proper error handling"""
        }
        
        return prompts.get(code_type, "You are an expert mainframe programmer.")

    def _build_user_prompt(
        self,
        code_type: str,
        description: str,
        params: Dict[str, Any]
    ) -> str:
        """Build user prompt for code generation."""
        prompt = f"Generate {code_type.upper()} code for: {description}\n\n"
        
        if params:
            prompt += "Additional requirements:\n"
            for key, value in params.items():
                prompt += f"- {key}: {value}\n"
        
        prompt += "\nPlease provide only the code without explanations, unless the description explicitly asks for explanation."
        
        return prompt

    def generate_cobol(
        self,
        description: str,
        params: Optional[Dict[str, Any]] = None,
        use_ai: bool = True
    ) -> str:
        """Generate COBOL code."""
        return self.generate('cobol', description, params, use_ai)

    def generate_jcl(
        self,
        description: str,
        params: Optional[Dict[str, Any]] = None,
        use_ai: bool = True
    ) -> str:
        """Generate JCL code."""
        return self.generate('jcl', description, params, use_ai)

    def generate_db2(
        self,
        description: str,
        params: Optional[Dict[str, Any]] = None,
        use_ai: bool = True
    ) -> str:
        """Generate DB2 SQL code."""
        return self.generate('db2', description, params, use_ai)

    def generate_cics(
        self,
        description: str,
        params: Optional[Dict[str, Any]] = None,
        use_ai: bool = True
    ) -> str:
        """Generate CICS code."""
        return self.generate('cics', description, params, use_ai)

    def save_to_file(
        self,
        code: str,
        filename: str,
        output_dir: Optional[str] = None
    ) -> str:
        """Save generated code to file.
        
        Args:
            code: Generated code to save
            filename: Name of the file
            output_dir: Output directory. Uses config default if not specified
            
        Returns:
            Full path to saved file
        """
        output_dir = output_dir or self.config.output_directory
        
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        filepath = Path(output_dir) / filename
        filepath.write_text(code)
        
        self.logger.info(f"Code saved to: {filepath}")
        return str(filepath)

    def list_generators(self) -> List[str]:
        """List available code generators."""
        return list(self.generators.keys())

    def get_supported_languages(self) -> List[str]:
        """Get list of supported mainframe languages."""
        return ["COBOL", "JCL", "DB2", "CICS"]

