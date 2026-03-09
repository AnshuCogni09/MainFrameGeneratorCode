"""
COBOL Code Generator

Generates COBOL programs using templates and AI assistance.
"""

from typing import Dict, Any, Optional
from datetime import datetime


class COBOLGenerator:
    """Generator for COBOL programs."""

    def __init__(self, config):
        """Initialize COBOL generator.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.template_library = self._load_templates()

    def _load_templates(self) -> Dict[str, str]:
        """Load COBOL program templates."""
        return {
            'basic': self._basic_program_template(),
            'file_io': self._file_io_template(),
            'db2': self._db2_template(),
            'report': self._report_template(),
            'subprogram': self._subprogram_template()
        }

    def _basic_program_template(self) -> str:
        """Basic COBOL program template."""
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. {program_name}.
       AUTHOR. {author}.
       DATE-WRITTEN. {date}.
      *
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SOURCE-COMPUTER. IBM-MAINFRAME.
       OBJECT-COMPUTER. IBM-MAINFRAME.
      *
       DATA DIVISION.
       WORKING-STORAGE SECTION.
      * 01 variables here
       01  WS-VARIABLES.
           05  WS-COUNTER         PIC 9(05) VALUE ZEROS.
           05  WS-STATUS          PIC X(01) VALUE SPACES.
           05  WS-DATE            PIC 9(08) VALUE ZEROS.
      *
       PROCEDURE DIVISION.
       MAIN-PARA.
           DISPLAY 'Program started at: ' WS-DATE
           PERFORM INITIALIZATION-PARA
           PERFORM PROCESS-PARA
           PERFORM TERMINATION-PARA
           STOP RUN.
      *
       INITIALIZATION-PARA.
           MOVE FUNCTION CURRENT-DATE TO WS-DATE
           DISPLAY 'Initialization complete'
           .
      *
       PROCESS-PARA.
           DISPLAY 'Processing...'
           ADD 1 TO WS-COUNTER
           DISPLAY 'Counter: ' WS-COUNTER
           .
      *
       TERMINATION-PARA.
           DISPLAY 'Program terminated normally'
           .
      *
       END PROGRAM {program_name}.
"""

    def _file_io_template(self) -> str:
        """COBOL program with file I/O template."""
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. {program_name}.
       AUTHOR. {author}.
       DATE-WRITTEN. {date}.
      *
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT INPUT-FILE ASSIGN TO DDINPUT
                  ORGANIZATION IS SEQUENTIAL
                  ACCESS MODE IS SEQUENTIAL
                  FILE STATUS IS WS-INPUT-STATUS.
           SELECT OUTPUT-FILE ASSIGN TO DDOUTPUT
                  ORGANIZATION IS SEQUENTIAL
                  ACCESS MODE IS SEQUENTIAL
                  FILE STATUS IS WS-OUTPUT-STATUS.
      *
       DATA DIVISION.
       FILE SECTION.
       FD  INPUT-FILE
           RECORD CONTAINS 80 CHARACTERS
           DATA RECORD IS INPUT-RECORD.
       01  INPUT-RECORD          PIC X(80).
      *
       FD  OUTPUT-FILE
           RECORD CONTAINS 80 CHARACTERS
           DATA RECORD IS OUTPUT-RECORD.
       01  OUTPUT-RECORD         PIC X(80).
      *
       WORKING-STORAGE SECTION.
       01  WS-FILE-STATUS.
           05  WS-INPUT-STATUS   PIC X(02).
           05  WS-OUTPUT-STATUS  PIC X(02).
       01  WS-EOF-SWITCH        PIC X(01) VALUE 'N'.
           88  EOF-REACHED       VALUE 'Y'.
       01  WS-RECORD-COUNTER     PIC 9(05) VALUE ZEROS.
      *
       PROCEDURE DIVISION.
       MAIN-PARA.
           PERFORM OPEN-FILES-PARA
           PERFORM READ-PROCESS-PARA UNTIL EOF-REACHED
           PERFORM CLOSE-FILES-PARA
           DISPLAY 'Records processed: ' WS-RECORD-COUNTER
           STOP RUN.
      *
       OPEN-FILES-PARA.
           OPEN INPUT INPUT-FILE
           IF WS-INPUT-STATUS NOT = '00'
              DISPLAY 'Error opening input file: ' WS-INPUT-STATUS
           ELSE
              DISPLAY 'Input file opened successfully'
           END-IF
           
           OPEN OUTPUT OUTPUT-FILE
           IF WS-OUTPUT-STATUS NOT = '00'
              DISPLAY 'Error opening output file: ' WS-OUTPUT-STATUS
           ELSE
              DISPLAY 'Output file opened successfully'
           END-IF
           .
      *
       READ-PROCESS-PARA.
           READ INPUT-FILE
               AT END
                   SET EOF-REACHED TO TRUE
               NOT AT END
                   MOVE INPUT-RECORD TO OUTPUT-RECORD
                   WRITE OUTPUT-RECORD
                   ADD 1 TO WS-RECORD-COUNTER
           END-READ
           .
      *
       CLOSE-FILES-PARA.
           CLOSE INPUT-FILE
           CLOSE OUTPUT-FILE
           DISPLAY 'Files closed successfully'
           .
      *
       END PROGRAM {program_name}.
"""

    def _db2_template(self) -> str:
        """COBOL-DB2 program template."""
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. {program_name}.
       AUTHOR. {author}.
       DATE-WRITTEN. {date}.
      *
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
      *
       EXEC SQL 
           INCLUDE SQLCA 
       END-EXEC.
      *
      * Table: {table_name}
       EXEC SQL DECLARE {table_name}_TABLE TABLE (
           {db2_columns}
       ) END-EXEC.
      *
       01  WS-SQL-STATUS.
           05  SQL-CODE          PIC S9(09) COMP-5.
           05  SQL-STATE          PIC X(05).
           05  SQL-MESSAGE        PIC X(100).
      *
       01  WS-DB2-VARIABLES.
           05  WS-{table_name}-REC.
{db2_variables}
      *
       PROCEDURE DIVISION.
       MAIN-PARA.
           PERFORM CONNECT-DATABASE-PARA
           PERFORM FETCH-DATA-PARA
           PERFORM DISCONNECT-DATABASE-PARA
           STOP RUN.
      *
       CONNECT-DATABASE-PARA.
           EXEC SQL
               CONNECT TO {database_name}
           END-EXEC
           IF SQLCODE = 0
              DISPLAY 'Connected to database successfully'
           ELSE
              DISPLAY 'Database connection failed: ' SQLCODE
           END-IF
           .
      *
       FETCH-DATA-PARA.
           EXEC SQL
               SELECT {select_columns}
               INTO {into_variables}
               FROM {table_name}
               WHERE {where_condition}
           END-EXEC
           
           IF SQLCODE = 0
              DISPLAY 'Data fetched successfully'
              DISPLAY 'Data: ' WS-{table_name}-REC
           ELSE
              IF SQLCODE = 100
                 DISPLAY 'No data found'
              ELSE
                 DISPLAY 'SQL Error: ' SQLCODE
              END-IF
           END-IF
           .
      *
       DISCONNECT-DATABASE-PARA.
           EXEC SQL
               CONNECT RESET
           END-EXEC
           DISPLAY 'Disconnected from database'
           .
      *
       END PROGRAM {program_name}.
"""

    def _report_template(self) -> str:
        """COBOL report generation template."""
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. {program_name}.
       AUTHOR. {author}.
       DATE-WRITTEN. {date}.
      *
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT INPUT-FILE ASSIGN TO DDINPUT
                  ORGANIZATION IS SEQUENTIAL.
           SELECT REPORT-FILE ASSIGN TO DDREPORT
                  ORGANIZATION IS LINE SEQUENTIAL.
      *
       DATA DIVISION.
       FILE SECTION.
       FD  INPUT-FILE
           RECORD CONTAINS 80 CHARACTERS.
       01  INPUT-RECORD          PIC X(80).
      *
       FD  REPORT-FILE
           RECORD CONTAINS 132 CHARACTERS.
       01  REPORT-RECORD         PIC X(132).
      *
       WORKING-STORAGE SECTION.
       01  WS-REPORT-VARIABLES.
           05  WS-PAGE-NUMBER     PIC 9(03) VALUE 1.
           05  WS-LINE-COUNTER    PIC 9(02) VALUE 60.
           05  WS-LINES-PER-PAGE  PIC 9(02) VALUE 55.
           05  WS-RECORD-COUNTER  PIC 9(05) VALUE ZEROS.
           05  WS-TOTAL-AMOUNT    PIC 9(10)V99 VALUE ZEROS.
      *
       01  WS-DETAIL-LINE.
           05  FILLER             PIC X(10) VALUE SPACES.
           05  DL-ACCOUNT         PIC X(10).
           05  FILLER             PIC X(10) VALUE SPACES.
           05  DL-NAME            PIC X(30).
           05  FILLER             PIC X(10) VALUE SPACES.
           05  DL-AMOUNT          PIC Z,ZZZ,ZZ9.99.
      *
       01  WS-HEADING-LINE.
           05  FILLER             PIC X(50) VALUE 
               'PAGE NUMBER: '.
           05  HL-PAGE-NUMBER     PIC 9(03).
           05  FILLER             PIC X(60) VALUE SPACES.
      *
       01  WS-HEADER-1.
           05  FILLER             PIC X(50) VALUE ALL '-'.
           05  FILLER             PIC X(82) VALUE ALL '-'.
      *
       01  WS-HEADER-2.
           05  FILLER             PIC X(10) VALUE 'ACCOUNT'.
           05  FILLER             PIC X(10) VALUE SPACES.
           05  FILLER             PIC X(10) VALUE 'NAME'.
           05  FILLER             PIC X(30) VALUE SPACES.
           05  FILLER             PIC X(10) VALUE 'AMOUNT'.
      *
       01  WS-TOTAL-LINE.
           05  FILLER             PIC X(50) VALUE 
               'TOTAL RECORDS: '.
           05  TL-RECORD-COUNT    PIC 9(05).
           05  FILLER             PIC X(30) VALUE SPACES.
           05  TL-TOTAL-AMOUNT    PIC Z,ZZZ,ZZZ,ZZ9.99.
      *
       PROCEDURE DIVISION.
       MAIN-PARA.
           PERFORM OPEN-FILES-PARA
           PERFORM WRITE-HEADINGS-PARA
           PERFORM PROCESS-RECORDS-PARA
           PERFORM WRITE-TOTALS-PARA
           PERFORM CLOSE-FILES-PARA
           STOP RUN.
      *
       OPEN-FILES-PARA.
           OPEN INPUT INPUT-FILE
           OPEN OUTPUT REPORT-FILE
           .
      *
       WRITE-HEADINGS-PARA.
           WRITE REPORT-RECORD FROM WS-HEADING-LINE
           WRITE REPORT-RECORD FROM WS-HEADER-1
           WRITE REPORT-RECORD FROM WS-HEADER-2
           WRITE REPORT-RECORD FROM WS-HEADER-1
           MOVE 4 TO WS-LINE-COUNTER
           .
      *
       PROCESS-RECORDS-PARA.
           READ INPUT-FILE
               AT END DISPLAY 'Processing complete'
               NOT AT END
                   MOVE SPACES TO WS-DETAIL-LINE
                   MOVE INPUT-RECORD TO WS-DETAIL-LINE
                   WRITE REPORT-RECORD FROM WS-DETAIL-LINE
                   ADD 1 TO WS-RECORD-COUNTER
                   ADD 1 TO WS-LINE-COUNTER
                   IF WS-LINE-COUNTER > WS-LINES-PER-PAGE
                       ADD 1 TO WS-PAGE-NUMBER
                       PERFORM WRITE-HEADINGS-PARA
                   END-IF
           END-READ
           .
      *
       WRITE-TOTALS-PARA.
           WRITE REPORT-RECORD FROM WS-HEADER-1
           MOVE WS-RECORD-COUNTER TO TL-RECORD-COUNT
           MOVE WS-TOTAL-AMOUNT TO TL-TOTAL-AMOUNT
           WRITE REPORT-RECORD FROM WS-TOTAL-LINE
           .
      *
       CLOSE-FILES-PARA.
           CLOSE INPUT-FILE
           CLOSE REPORT-FILE
           .
      *
       END PROGRAM {program_name}.
"""

    def _subprogram_template(self) -> str:
        """COBOL subprogram (called program) template."""
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. {program_name}.
       AUTHOR. {author}.
       DATE-WRITTEN. {date}.
      *
       DATA DIVISION.
       LINKAGE SECTION.
      * Parameters passed from calling program
       01  LK-PARAMETERS.
           05  LK-ACTION         PIC X(01).
           05  LK-INPUT-DATA     PIC X(50).
           05  LK-OUTPUT-DATA    PIC X(50).
           05  LK-RETURN-CODE    PIC 9(02).
           05  LK-STATUS-MESSAGE PIC X(100).
      *
       WORKING-STORAGE SECTION.
       01  WS-WORK-VARIABLES.
           05  WS-ERROR-FOUND    PIC X(01) VALUE 'N'.
           88  ERROR-OCCURRED    VALUE 'Y'.
      *
       PROCEDURE DIVISION USING LK-PARAMETERS.
       MAIN-PARA.
           MOVE SPACES TO LK-STATUS-MESSAGE
           MOVE ZEROS TO LK-RETURN-CODE
           
           EVALUATE LK-ACTION
               WHEN 'R'
                   PERFORM READ-PARA
               WHEN 'W'
                   PERFORM WRITE-PARA
               WHEN 'U'
                   PERFORM UPDATE-PARA
               WHEN 'D'
                   PERFORM DELETE-PARA
               WHEN OTHER
                   MOVE 'Invalid action code' TO LK-STATUS-MESSAGE
                   MOVE 99 TO LK-RETURN-CODE
           END-EVALUATE
           
           GOBACK
           .
      *
       READ-PARA.
           DISPLAY 'Read operation: ' LK-INPUT-DATA
           MOVE 'Data read successfully' TO LK-STATUS-MESSAGE
           MOVE 0 TO LK-RETURN-CODE
           .
      *
       WRITE-PARA.
           DISPLAY 'Write operation: ' LK-INPUT-DATA
           MOVE 'Data written successfully' TO LK-STATUS-MESSAGE
           MOVE 0 TO LK-RETURN-CODE
           .
      *
       UPDATE-PARA.
           DISPLAY 'Update operation: ' LK-INPUT-DATA
           MOVE 'Data updated successfully' TO LK-STATUS-MESSAGE
           MOVE 0 TO LK-RETURN-CODE
           .
      *
       DELETE-PARA.
           DISPLAY 'Delete operation: ' LK-INPUT-DATA
           MOVE 'Data deleted successfully' TO LK-STATUS-MESSAGE
           MOVE 0 TO LK-RETURN-CODE
           .
      *
       END PROGRAM {program_name}.
"""

    def generate(
        self,
        description: str,
        params: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate COBOL code based on description.
        
        Args:
            description: Description of the COBOL program to generate
            params: Additional parameters
            
        Returns:
            Generated COBOL code
        """
        params = params or {}
        
        # Determine template type from description
        template_type = self._determine_template_type(description)
        
        # Get template
        template = self.template_library.get(template_type, self.template_library['basic'])
        
        # Fill in template parameters
        program_name = params.get('program_name', 'PROG001')
        author = params.get('author', 'Generated')
        date = params.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        code = template.format(
            program_name=program_name.upper(),
            author=author,
            date=date,
            table_name=params.get('table_name', 'EMPLOYEE'),
            database_name=params.get('database_name', 'DB2PROD'),
            db2_columns=params.get('db2_columns', 'EMP_ID CHAR(10), EMP_NAME VARCHAR(50)'),
            db2_variables=params.get('db2_variables', '           05  WS-EMP-ID           PIC X(10).\n           05  WS-EMP-NAME         PIC X(50).'),
            select_columns=params.get('select_columns', '*'),
            into_variables=params.get('into_variables', ':WS-EMP-ID, :WS-EMP-NAME'),
            where_condition=params.get('where_condition', 'EMP_ID = :WS-EMP-ID')
        )
        
        return code

    def _determine_template_type(self, description: str) -> str:
        """Determine which template to use based on description."""
        desc_lower = description.lower()
        
        if 'file' in desc_lower or 'read' in desc_lower or 'write' in desc_lower:
            return 'file_io'
        elif 'db2' in desc_lower or 'sql' in desc_lower or 'database' in desc_lower:
            return 'db2'
        elif 'report' in desc_lower or 'print' in desc_lower:
            return 'report'
        elif 'subprogram' in desc_lower or 'called' in desc_lower or 'module' in desc_lower:
            return 'subprogram'
        else:
            return 'basic'

    def get_available_templates(self) -> list:
        """Get list of available templates."""
        return list(self.template_library.keys())

