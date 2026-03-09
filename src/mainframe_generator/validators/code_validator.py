"""
Code Validator for MainFrame Code

Validates generated mainframe code for syntax and best practices.
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class ValidationLevel(Enum):
    """Validation severity levels."""
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class ValidationIssue:
    """Represents a validation issue found in the code."""
    level: ValidationLevel
    message: str
    line_number: Optional[int] = None
    code_snippet: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of code validation."""
    is_valid: bool = True
    errors: List[ValidationIssue] = field(default_factory=list)
    warnings: List[ValidationIssue] = field(default_factory=list)
    info: List[ValidationIssue] = field(default_factory=list)

    def add_issue(self, issue: ValidationIssue) -> None:
        """Add a validation issue."""
        if issue.level == ValidationLevel.ERROR:
            self.errors.append(issue)
            self.is_valid = False
        elif issue.level == ValidationLevel.WARNING:
            self.warnings.append(issue)
        else:
            self.info.append(issue)


class CodeValidator:
    """Validator for mainframe code."""

    def __init__(self, config):
        """Initialize the validator.
        
        Args:
            config: Configuration object
        """
        self.config = config

    def validate(self, code: str, code_type: str) -> ValidationResult:
        """Validate code based on type.
        
        Args:
            code: Code to validate
            code_type: Type of code (cobol, jcl, db2, cics)
            
        Returns:
            ValidationResult object
        """
        code_type = code_type.lower()
        
        if code_type == 'cobol':
            return self.validate_cobol(code)
        elif code_type == 'jcl':
            return self.validate_jcl(code)
        elif code_type == 'db2':
            return self.validate_db2(code)
        elif code_type == 'cics':
            return self.validate_cics(code)
        else:
            result = ValidationResult()
            result.add_issue(ValidationIssue(
                ValidationLevel.WARNING,
                f"Unknown code type: {code_type}"
            ))
            return result

    def validate_cobol(self, code: str) -> ValidationResult:
        """Validate COBOL code."""
        result = ValidationResult()
        lines = code.split('\n')
        
        # Check for required divisions
        has_identification = False
        has_data_division = False
        has_procedure_division = False
        
        for line in lines:
            line_upper = line.upper().strip()
            
            if 'IDENTIFICATION DIVISION' in line_upper or 'ID DIVISION' in line_upper:
                has_identification = True
            elif 'DATA DIVISION' in line_upper:
                has_data_division = True
            elif 'PROCEDURE DIVISION' in line_upper:
                has_procedure_division = True
        
        if not has_identification:
            result.add_issue(ValidationIssue(
                ValidationLevel.ERROR,
                "Missing IDENTIFICATION DIVISION"
            ))
        
        if not has_data_division:
            result.add_issue(ValidationIssue(
                ValidationLevel.WARNING,
                "Missing DATA DIVISION"
            ))
        
        if not has_procedure_division:
            result.add_issue(ValidationIssue(
                ValidationLevel.WARNING,
                "Missing PROCEDURE DIVISION"
            ))
        
        # Check for PROGRAM-ID
        if 'PROGRAM-ID' not in code.upper():
            result.add_issue(ValidationIssue(
                ValidationLevel.ERROR,
                "Missing PROGRAM-ID"
            ))
        
        # Check for proper column formatting (COBOL columns 1-72)
        for i, line in enumerate(lines, 1):
            if len(line) > 72:
                result.add_issue(ValidationIssue(
                    ValidationLevel.WARNING,
                    f"Line exceeds 72 columns (COBOL standard)",
                    line_number=i
                ))
        
        # Check for STOP RUN or GOBACK
        if 'STOP RUN' not in code.upper() and 'GOBACK' not in code.upper():
            result.add_issue(ValidationIssue(
                ValidationLevel.WARNING,
                "Missing STOP RUN or GOBACK statement"
            ))
        
        return result

    def validate_jcl(self, code: str) -> ValidationResult:
        """Validate JCL code."""
        result = ValidationResult()
        lines = code.split('\n')
        
        # Check for JOB statement
        has_job = False
        
        for line in lines:
            line_stripped = line.strip()
            
            if line_stripped.startswith('//') and 'JOB' in line_stripped:
                has_job = True
                break
        
        if not has_job:
            result.add_issue(ValidationIssue(
                ValidationLevel.ERROR,
                "Missing JOB statement"
            ))
        
        # Check for EXEC statements
        if 'EXEC' not in code.upper():
            result.add_issue(ValidationIssue(
                ValidationLevel.WARNING,
                "Missing EXEC statement"
            ))
        
        # Check for proper DD statements
        if 'DD ' not in code and 'DD\t' not in code:
            result.add_issue(ValidationIssue(
                ValidationLevel.INFO,
                "No DD statements found"
            ))
        
        # Check for dataset naming conventions
        for i, line in enumerate(lines, 1):
            if 'DSN=' in line.upper():
                # Check for invalid characters
                if any(c in line for c in [' ', '(', ')']):
                    # Check it's in proper format
                    if not re.search(r'DSN=[^(\s]+', line, re.IGNORECASE):
                        result.add_issue(ValidationIssue(
                            ValidationLevel.WARNING,
                            "Invalid dataset name format",
                            line_number=i
                        ))
        
        return result

    def validate_db2(self, code: str) -> ValidationResult:
        """Validate DB2 SQL code."""
        result = ValidationResult()
        
        # Check for semicolons
        if ';' not in code:
            result.add_issue(ValidationIssue(
                ValidationLevel.ERROR,
                "Missing statement terminator (;)"
            ))
        
        # Check for common SQL keywords
        keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP']
        has_keyword = any(k in code.upper() for k in keywords)
        
        if not has_keyword:
            result.add_issue(ValidationIssue(
                ValidationLevel.WARNING,
                "No recognized SQL keyword found"
            ))
        
        # Check for table references
        if 'FROM' in code.upper() and not re.search(r'FROM\s+\w+', code, re.IGNORECASE):
            result.add_issue(ValidationIssue(
                ValidationLevel.WARNING,
                "Invalid FROM clause"
            ))
        
        # Check for WHERE in modification statements
        if any(k in code.upper() for k in ['UPDATE', 'DELETE']):
            if 'WHERE' not in code.upper():
                result.add_issue(ValidationIssue(
                    ValidationLevel.WARNING,
                    "UPDATE/DELETE without WHERE clause - may affect multiple rows"
                ))
        
        return result

    def validate_cics(self, code: str) -> ValidationResult:
        """Validate CICS code."""
        result = ValidationResult()
        
        # Check for EXEC CICS statements
        if 'EXEC CICS' not in code.upper():
            result.add_issue(ValidationIssue(
                ValidationLevel.WARNING,
                "No EXEC CICS commands found"
            ))
        
        # Check for RETURN statement
        if 'EXEC CICS RETURN' not in code.upper():
            result.add_issue(ValidationIssue(
                ValidationLevel.ERROR,
                "Missing EXEC CICS RETURN - required for CICS programs"
            ))
        
        # Check for DFHCOMMAREA
        if 'DFHCOMMAREA' not in code.upper():
            result.add_issue(ValidationIssue(
                ValidationLevel.WARNING,
                "DFHCOMMAREA not defined - may be needed for communication"
            ))
        
        # Check for EIBAID (attention identifier handling)
        if 'EIBAID' not in code.upper():
            result.add_issue(ValidationIssue(
                ValidationLevel.INFO,
                "No EIBAID handling - consider handling different PF keys"
            ))
        
        # Check for RESP or HANDLE conditions
        if 'RESP(' not in code:
            result.add_issue(ValidationIssue(
                ValidationLevel.WARNING,
                "No RESP handling - recommend using RESP for error handling"
            ))
        
        return result

    def check_syntax(self, code: str, code_type: str) -> bool:
        """Quick syntax check.
        
        Args:
            code: Code to check
            code_type: Type of code
            
        Returns:
            True if basic syntax is valid
        """
        result = self.validate(code, code_type)
        return result.is_valid

