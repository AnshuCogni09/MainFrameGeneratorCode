"""
Template Manager for MainFrame Code Generator

Manages templates for different mainframe technologies.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from jinja2 import Environment, FileSystemLoader, Template


class TemplateManager:
    """Manages templates for mainframe code generation."""

    def __init__(self, config):
        """Initialize the template manager.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.templates_dir = self._get_templates_dir()
        self.jinja_env = None
        
        if self.templates_dir and Path(self.templates_dir).exists():
            self.jinja_env = Environment(
                loader=FileSystemLoader(self.templates_dir),
                trim_blocks=True,
                lstrip_blocks=True
            )
        
        # In-memory template storage
        self._templates: Dict[str, Dict[str, Any]] = {}
        self._load_default_templates()

    def _get_templates_dir(self) -> Optional[str]:
        """Get templates directory from config."""
        template_dir = self.config.get("templates.directory", "./templates")
        
        # Check if directory exists
        possible_paths = [
            template_dir,
            Path(__file__).parent.parent.parent / "templates",
            Path.cwd() / "templates"
        ]
        
        for path in possible_paths:
            if Path(path).exists():
                return str(path)
        
        return None

    def _load_default_templates(self) -> None:
        """Load default templates."""
        # COBOL templates
        self._templates['cobol'] = {
            'basic': self._get_basic_cobol_template(),
            'file_io': self._get_file_io_cobol_template(),
            'db2': self._get_db2_cobol_template(),
            'report': self._get_report_cobol_template()
        }
        
        # JCL templates
        self._templates['jcl'] = {
            'basic': self._get_basic_jcl_template(),
            'sort': self._get_sort_jcl_template(),
            'cobol_run': self._get_cobol_run_jcl_template()
        }
        
        # DB2 templates
        self._templates['db2'] = {
            'select': self._get_select_db2_template(),
            'insert': self._get_insert_db2_template(),
            'create_table': self._get_create_table_db2_template()
        }
        
        # CICS templates
        self._templates['cics'] = {
            'basic': self._get_basic_cics_template(),
            'screen': self._get_screen_cics_template(),
            'file': self._get_file_cics_template()
        }

    def get_template(
        self,
        code_type: str,
        template_name: str
    ) -> Optional[str]:
        """Get a specific template.
        
        Args:
            code_type: Type of code (cobol, jcl, db2, cics)
            template_name: Name of the template
            
        Returns:
            Template string or None
        """
        code_type = code_type.lower()
        
        if code_type in self._templates:
            return self._templates[code_type].get(template_name)
        
        return None

    def list_templates(self, code_type: str) -> List[str]:
        """List available templates for a code type.
        
        Args:
            code_type: Type of code
            
        Returns:
            List of template names
        """
        code_type = code_type.lower()
        
        if code_type in self._templates:
            return list(self._templates[code_type].keys())
        
        return []

    def add_template(
        self,
        code_type: str,
        template_name: str,
        template_content: str
    ) -> None:
        """Add a custom template.
        
        Args:
            code_type: Type of code
            template_name: Name of the template
            template_content: Template content
        """
        code_type = code_type.lower()
        
        if code_type not in self._templates:
            self._templates[code_type] = {}
        
        self._templates[code_type][template_name] = template_content

    def render_template(
        self,
        code_type: str,
        template_name: str,
        context: Dict[str, Any]
    ) -> Optional[str]:
        """Render a template with context.
        
        Args:
            code_type: Type of code
            template_name: Name of the template
            context: Variables to render
            
        Returns:
            Rendered template or None
        """
        template = self.get_template(code_type, template_name)
        
        if template:
            try:
                return template.format(**context)
            except KeyError as e:
                return None
        
        return None

    # Default template definitions
    def _get_basic_cobol_template(self) -> str:
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. {{program_name}}.
       AUTHOR. {{author}}.
       DATE-WRITTEN. {{date}}.
      *
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SOURCE-COMPUTER. IBM-MAINFRAME.
       OBJECT-COMPUTER. IBM-MAINFRAME.
      *
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-VARIABLES.
           05  WS-COUNTER         PIC 9(05) VALUE ZEROS.
           05  WS-STATUS          PIC X(01) VALUE SPACES.
      *
       PROCEDURE DIVISION.
       MAIN-PARA.
           DISPLAY 'Program started'
           PERFORM PROCESS-PARA
           STOP RUN.
      *
       PROCESS-PARA.
           DISPLAY 'Processing...'
           ADD 1 TO WS-COUNTER
           .
      *
       END PROGRAM {{program_name}}.
"""

    def _get_file_io_cobol_template(self) -> str:
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. {{program_name}}.
       AUTHOR. {{author}}.
       DATE-WRITTEN. {{date}}.
      *
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT INPUT-FILE ASSIGN TO DDINPUT
                  ORGANIZATION IS SEQUENTIAL
                  FILE STATUS IS WS-INPUT-STATUS.
      *
       DATA DIVISION.
       FILE SECTION.
       FD  INPUT-FILE.
       01  INPUT-RECORD          PIC X(80).
      *
       WORKING-STORAGE SECTION.
       01  WS-INPUT-STATUS        PIC X(02).
       01  WS-EOF-SWITCH         PIC X(01) VALUE 'N'.
      *
       PROCEDURE DIVISION.
       MAIN-PARA.
           OPEN INPUT INPUT-FILE
           PERFORM READ-PARA UNTIL EOF-REACHED
           CLOSE INPUT-FILE
           STOP RUN.
      *
       READ-PARA.
           READ INPUT-FILE
               AT END SET EOF-REACHED TO TRUE
           END-READ
           .
      *
       END PROGRAM {{program_name}}.
"""

    def _get_db2_cobol_template(self) -> str:
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. {{program_name}}.
       AUTHOR. {{author}}.
       DATE-WRITTEN. {{date}}.
      *
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       EXEC SQL INCLUDE SQLCA END-EXEC.
       01  WS-HOST-VARS.
           05  WS-EMP-ID          PIC X(10).
           05  WS-EMP-NAME        PIC X(50).
      *
       PROCEDURE DIVISION.
       MAIN-PARA.
           EXEC SQL CONNECT TO {{database}} END-EXEC
           STOP RUN.
      *
       END PROGRAM {{program_name}}.
"""

    def _get_report_cobol_template(self) -> str:
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. {{program_name}}.
       AUTHOR. {{author}}.
       DATE-WRITTEN. {{date}}.
      *
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT INPUT-FILE ASSIGN TO DDINPUT.
           SELECT REPORT-FILE ASSIGN TO DDREPORT.
      *
       DATA DIVISION.
       FILE SECTION.
       FD  INPUT-FILE.
       01  INPUT-RECORD          PIC X(80).
      *
       FD  REPORT-FILE.
       01  REPORT-RECORD         PIC X(132).
      *
       WORKING-STORAGE SECTION.
       01  WS-COUNTERS.
           05  WS-LINE-COUNT     PIC 9(03) VALUE 60.
           05  WS-PAGE-COUNT     PIC 9(03) VALUE 1.
      *
       PROCEDURE DIVISION.
       MAIN-PARA.
           OPEN INPUT INPUT-FILE
           OPEN OUTPUT REPORT-FILE
           PERFORM PROCESS-RECORDS-PARA
           CLOSE INPUT-FILE OUTPUT-REPORT-FILE
           STOP RUN.
      *
       PROCESS-RECORDS-PARA.
           READ INPUT-FILE AT END CLOSE INPUT-FILE
           END-READ
           .
      *
       END PROGRAM {{program_name}}.
"""

    def _get_basic_jcl_template(self) -> str:
        return """//{{job_name}} JOB ({{account_info}}),'{{programmer_name}}',CLASS={{job_class}},
//             MSGCLASS={{msg_class}}
//*
//STEP1    EXEC PGM={{program_name}}
//DD1      DD DSN=INPUT.DATA,DISP=SHR
//DD2      DD SYSOUT=*
//
"""

    def _get_sort_jcl_template(self) -> str:
        return """//{{job_name}} JOB ({{account_info}}),'{{programmer_name}}',CLASS={{job_class}},
//             MSGCLASS={{msg_class}}
//*
//SORT     EXEC PGM=SORT
//SYSOUT   DD SYSOUT=*
//SORTIN   DD DSN={{input_dataset}},DISP=SHR
//SORTOUT  DD DSN={{output_dataset}},
//            DISP=(NEW,CATLG,DELETE),
//            SPACE=(TRK,(10,5),RLSE)
//SYSIN    DD *
  SORT FIELDS=({{sort_fields}})
/*
//
"""

    def _get_cobol_run_jcl_template(self) -> str:
        return """//{{job_name}} JOB ({{account_info}}),'{{programmer_name}}',CLASS={{job_class}},
//             MSGCLASS={{msg_class}}
//*
//COMPILE  EXEC PGM=IGYCRCTL,REGION=4M,
//             PARM='LIST,MAP'
//SYSPRINT DD SYSOUT=*
//SYSLIN   DD DSN=&&LOADSET,DISP=(NEW,PASS,DELETE)
//SYSUT1   DD UNIT=SYSDA,SPACE=(CYL,(1,1))
//SYSIN    DD DSN={{source_dataset}},DISP=SHR
//*
//LINK    EXEC PGM=IEWL,REGION=4M
//SYSLIN   DD DSN=&&LOADSET,DISP=SHR
//SYSLMOD  DD DSN={{load_library}}({{member}}),DISP=SHR
//*
//RUN     EXEC PGM={{member}},REGION=4M
//STEPLIB  DD DSN={{load_library}},DISP=SHR
//SYSOUT   DD SYSOUT=*
//
"""

    def _get_select_db2_template(self) -> str:
        return """-- Select from {{table_name}}
SELECT {{columns}}
FROM {{schema}}.{{table_name}}
WHERE {{where_clause}}
;
"""

    def _get_insert_db2_template(self) -> str:
        return """-- Insert into {{table_name}}
INSERT INTO {{schema}}.{{table_name}}
    ({{columns}})
VALUES
    ({{values}})
;
"""

    def _get_create_table_db2_template(self) -> str:
        return """-- Create table {{table_name}}
CREATE TABLE {{schema}}.{{table_name}}
    ({{columns}}
    )
    IN {{tablespace}}
    ;
"""

    def _get_basic_cics_template(self) -> str:
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. {{program_name}}.
       AUTHOR. {{author}}.
       DATE-WRITTEN. {{date}}.
      *
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  DFHCOMMAREA.
           05  CA-TRANSID         PIC X(04).
           05  CA-DATA            PIC X(50).
      *
       PROCEDURE DIVISION.
       MAIN-PARA.
           EXEC CICS RETURN
               TRANSID(EIBTRNID)
               COMMAREA(DFHCOMMAREA)
           END-EXEC
           .
      *
       END PROGRAM {{program_name}}.
"""

    def _get_screen_cics_template(self) -> str:
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. {{program_name}}.
       AUTHOR. {{author}}.
       DATE-WRITTEN. {{date}}.
      *
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  {{mapset_name}}-MAP.
           COPY {{mapset_name}}.
       01  WS-RESP                PIC S9(08) COMP.
      *
       PROCEDURE DIVISION.
       MAIN-PARA.
           PERFORM RECEIVE-MAP-PARA
           EVALUATE EIBAID
               WHEN DFHENTER PERFORM PROCESS-PARA
               WHEN DFHPF3  PERFORM EXIT-PARA
           END-EVALUATE
           EXEC CICS RETURN TRANSID(EIBTRNID) END-EXEC
           .
      *
       RECEIVE-MAP-PARA.
           EXEC CICS RECEIVE MAP('{{mapset_name}}') END-EXEC
           .
      *
       PROCESS-PARA.
           DISPLAY 'Processing...'
           .
      *
       EXIT-PARA.
           EXEC CICS RETURN END-EXEC
           .
      *
       END PROGRAM {{program_name}}.
"""

    def _get_file_cics_template(self) -> str:
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. {{program_name}}.
       AUTHOR. {{author}}.
       DATE-WRITTEN. {{date}}.
      *
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  {{file_name}}-REC.
           COPY {{copybook_name}}.
       01  WS-RESP                PIC S9(08) COMP.
      *
       LINKAGE SECTION.
       01  DFHCOMMAREA.
           05  CA-KEY             PIC X({{key_length}}).
           05  CA-ACTION          PIC X(01).
      *
       PROCEDURE DIVISION.
       MAIN-PARA.
           EVALUATE CA-ACTION
               WHEN 'R' PERFORM READ-RECORD-PARA
               WHEN 'W' PERFORM WRITE-RECORD-PARA
           END-EVALUATE
           EXEC CICS RETURN TRANSID(EIBTRNID) END-EXEC
           .
      *
       READ-RECORD-PARA.
           EXEC CICS READ FILE('{{file_name}}') INTO({{file_name}}-REC)
               RIDFLD(CA-KEY) RESP(WS-RESP) END-EXEC
           .
      *
       WRITE-RECORD-PARA.
           EXEC CICS WRITE FILE('{{file_name}}') FROM({{file_name}}-REC)
               RIDFLD(CA-KEY) RESP(WS-RESP) END-EXEC
           .
      *
       END PROGRAM {{program_name}}.
"""

