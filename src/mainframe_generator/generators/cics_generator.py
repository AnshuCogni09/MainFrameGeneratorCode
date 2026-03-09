"""
CICS (Customer Information Control System) Generator

Generates CICS programs using templates and AI assistance.
"""

from typing import Dict, Any, Optional
from datetime import datetime


class CICSGenerator:
    """Generator for CICS programs."""

    def __init__(self, config):
        """Initialize CICS generator.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.template_library = self._load_templates()

    def _load_templates(self) -> Dict[str, str]:
        """Load CICS program templates."""
        return {
            'basic': self._basic_cics_template(),
            'screen': self._screen_program_template(),
            'file': self._file_program_template(),
            'db2': self._db2_cics_template(),
            'command': self._command_level_template(),
            'webservice': self._webservice_template(),
            'batch': self._batch_online_template()
        }

    def _basic_cics_template(self) -> str:
        """Basic CICS program template."""
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. {program_name}.
       AUTHOR. {author}.
       DATE-WRITTEN. {date}.
      *
       ENVIRONMENT DIVISION.
      *
       DATA DIVISION.
       WORKING-STORAGE SECTION.
      *------------------------
      * CICS Common Areas
      *------------------------
       01  DFHCOMMAREA.
           05  CA-TRANSID         PIC X(04).
           05  CA-RESPONSE        PIC S9(08) COMP.
           05  CA-LENGTH          PIC S9(04) COMP.
           05  CA-DATA            PIC X(100).
      *
       01  WS-RESPONSE            PIC S9(08) COMP.
       01  WS-RESPONSE2           PIC S9(08) COMP.
      *
      *------------------------
      * Mapset Definition
      *------------------------
       01  {mapset_name}-MAP.
           COPY {mapset_name}.
      *
       LINKAGE SECTION.
       01  DFHCOMMAREA-LNK        PIC X({commarea_length}).
      *
       PROCEDURE DIVISION.
      *
       MAIN-PARA.
           MOVE LOW-VALUES TO {mapset_name}-MAP
           
           IF EIBCALEN > 0
              MOVE DFHCOMMAREA TO DFHCOMMAREA-LNK
           END-IF
           
           EVALUATE EIBAID
               WHEN DFHENTER
                   PERFORM PROCESS-DATA-PARA
               WHEN DFHPF3
                   PERFORM EXIT-PARA
               WHEN DFHPF12
                   PERFORM EXIT-PARA
               WHEN OTHER
                   PERFORM INVALID-KEY-PARA
           END-EVALUATE
           
           EXEC CICS RETURN
               TRANSID(EIBTRNID)
               COMMAREA(DFHCOMMAREA)
               LENGTH({commarea_length})
           END-EXEC
           .
      *
       PROCESS-DATA-PARA.
           DISPLAY 'Processing data...'
           MOVE 'DATA PROCESSED' TO CA-DATA
           MOVE '00' TO CA-RESPONSE
           .
      *
       EXIT-PARA.
           EXEC CICS SEND CONTROL
               CLEAR(EIBTRMID)
               ERASE
           END-EXEC
           EXEC CICS RETURN
           END-EXEC
           .
      *
       INVALID-KEY-PARA.
           MOVE 'INVALID KEY PRESSED' TO MESSAGEO
           PERFORM SEND-MAP-PARA
           .
      *
       SEND-MAP-PARA.
           EXEC CICS SEND MAP('{mapset_name}')
               MAPSET('{mapset_name}')
               FROM({mapset_name}-MAP)
               ERASE
               RESP(WS-RESPONSE)
           END-EXEC
           .
      *
       END PROGRAM {program_name}.
"""

    def _screen_program_template(self) -> str:
        """CICS Screen/MAP program template."""
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. {program_name}.
       AUTHOR. {author}.
       DATE-WRITTEN. {date}.
      *
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
      *
       DATA DIVISION.
       WORKING-STORAGE SECTION.
      *------------------------
      * Screen Definition
      *------------------------
       01  {mapset_name}-MAP.
           COPY {mapset_name}.
      *
      *------------------------
      * Working Storage Variables
      *------------------------
       01  WS-VARIABLES.
           05  WS-ACTION          PIC X(01).
           05  WS-ERROR-MSG       PIC X(50).
           05  WS PIC S9(-RESP           08) COMP.
           05  WS-RESP2           PIC S9(08) COMP.
           05  WS-FOUND           PIC X(01) VALUE 'N'.
      *
      *------------------------
      * Communication Area
      *------------------------
       01  DFHCOMMAREA.
           05  CA-ACTION          PIC X(01).
           05  CA-KEY-DATA        PIC X(20).
           05  CA-RESPONSE        PIC X(02).
           05  CA-MESSAGE         PIC X(50).
      *
       LINKAGE SECTION.
       01  DFHCOMMAREA-LNK        PIC X(100).
      *
       PROCEDURE DIVISION.
      *
       MAIN-PARA.
           INITIALIZE WS-VARIABLES DFHCOMMAREA
           MOVE LOW-VALUES TO {mapset_name}-MAP
           
           IF EIBCALEN > ZERO
              MOVE DFHCOMMAREA TO DFHCOMMAREA-LNK
           END-IF
           
           PERFORM RECEIVE-MAP-PARA
           
           EVALUATE EIBAID
               WHEN DFHENTER
                   PERFORM PROCESS-ENTER-PARA
               WHEN DFHPA1
                   PERFORM REFRESH-PARA
               WHEN DFHPF3
                   PERFORM TERMINATE-PARA
               WHEN DFHPF12
                   PERFORM CANCEL-PARA
               WHEN OTHER
                   MOVE 'INVALID PF KEY' TO MSGTEXTO
                   PERFORM SEND-MAP-PARA
           END-EVALUATE
           
           EXEC CICS RETURN
               TRANSID(EIBTRNID)
               COMMAREA(DFHCOMMAREA)
           END-EXEC
           .
      *
       RECEIVE-MAP-PARA.
           EXEC CICS RECEIVE MAP('{mapset_name}')
               MAPSET('{mapset_name}')
               INTO({mapset_name}-MAP)
               RESP(WS-RESP)
           END-EXEC
           
           IF WS-RESP NOT = DFHRESP(NORMAL)
               MOVE 'RECEIVE MAP ERROR' TO MSGTEXTO
               PERFORM SEND-MAP-PARA
           END-IF
           .
      *
       PROCESS-ENTER-PARA.
           IF {key_field}L > ZERO
              PERFORM LOOKUP-DATA-PARA
              IF WS-FOUND = 'Y'
                 MOVE 'DATA FOUND' TO MSGTEXTO
              ELSE
                 MOVE 'NO DATA FOUND' TO MSGTEXTO
              END-IF
           ELSE
              MOVE 'KEY FIELD REQUIRED' TO MSGTEXTO
           END-IF
           
           PERFORM SEND-MAP-PARA
           .
      *
       LOOKUP-DATA-PARA.
           MOVE {key_field}I TO WS-KEY-DATA
           MOVE 'Y' TO WS-FOUND
           .
      *
       REFRESH-PARA.
           MOVE LOW-VALUES TO {mapset_name}-MAP
           MOVE 'SCREEN REFRESHED' TO MSGTEXTO
           PERFORM SEND-MAP-PARA
           .
      *
       TERMINATE-PARA.
           EXEC CICS SEND TEXT
               FROM('GOODBYE')
               ERASE
           END-EXEC
           EXEC CICS RETURN
           END-EXEC
           .
      *
       CANCEL-PARA.
           MOVE 'OPERATION CANCELLED' TO CA-MESSAGE
           EXEC CICS RETURN
               TRANSID(EIBTRNID)
               COMMAREA(DFHCOMMAREA)
           END-EXEC
           .
      *
       SEND-MAP-PARA.
           EXEC CICS SEND MAP('{mapset_name}')
               MAPSET('{mapset_name}')
               FROM({mapset_name}-MAP)
               ERASE
               CURSOR
               RESP(WS-RESP)
           END-EXEC
           .
      *
       END PROGRAM {program_name}.
"""

    def _file_program_template(self) -> str:
        """CICS File Control program template."""
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. {program_name}.
       AUTHOR. {author}.
       DATE-WRITTEN. {date}.
      *
       DATA DIVISION.
       WORKING-STORAGE SECTION.
      *------------------------
      * File Definition
      *------------------------
       01  {file_name}-REC.
           COPY {copybook_name}.
      *
      *------------------------
      * File Control Variables
      *------------------------
       01  WS-FILE-STATUS.
           05  WS-EOF              PIC X(01) VALUE 'N'.
           05  WS-ERROR            PIC X(01) VALUE 'N'.
           05  WS-RESP             PIC S9(08) COMP.
           05  WS-RESP2            PIC S9(08) COMP.
      *
       01  WS-KEY-LENGTH           PIC S9(04) COMP VALUE {key_length}.
       01  WS-READ-OPTIONS.
           05  WS-EQUAL            PIC X(01) VALUE 'E'.
           05  WS-GTEQ             PIC X(01) VALUE 'G'.
      *
       LINKAGE SECTION.
       01  DFHCOMMAREA.
           05  CA-ACTION           PIC X(01).
           05  CA-KEY              PIC X({key_length}).
           05  CA-STATUS           PIC X(02).
      *
       PROCEDURE DIVISION.
      *
       MAIN-PARA.
           MOVE LOW-VALUES TO WS-FILE-STATUS
           MOVE 'N' TO WS-ERROR
           
           IF EIBCALEN > ZERO
              MOVE DFHCOMMAREA TO WS-COMMAREA-AREA
           END-IF
           
           EVALUATE CA-ACTION
               WHEN 'R'
                   PERFORM READ-RECORD-PARA
               WHEN 'W'
                   PERFORM WRITE-RECORD-PARA
               WHEN 'U'
                   PERFORM UPDATE-RECORD-PARA
               WHEN 'D'
                   PERFORM DELETE-RECORD-PARA
               WHEN OTHER
                   MOVE 'INVALID ACTION' TO CA-STATUS
           END-EVALUATE
           
           EXEC CICS RETURN
               TRANSID(EIBTRNID)
               COMMAREA(DFHCOMMAREA)
           END-EXEC
           .
      *
       READ-RECORD-PARA.
           EXEC CICS READ
               FILE('{file_name}')
               INTO({file_name}-REC)
               RIDFLD(CA-KEY)
               KEYLENGTH(WS-KEY-LENGTH)
               RESP(WS-RESP)
               RBA
           END-EXEC
           
           IF WS-RESP = DFHRESP(NORMAL)
              MOVE '00' TO CA-STATUS
              MOVE {file_name}-REC TO CA-RECORD-DATA
           ELSE
              IF WS-RESP = DFHRESP(NOTFND)
                 MOVE '12' TO CA-STATUS
              ELSE
                 MOVE '99' TO CA-STATUS
              END-IF
           END-IF
           .
      *
       WRITE-RECORD-PARA.
           MOVE CA-INPUT-DATA TO {file_name}-REC
           
           EXEC CICS WRITE
               FILE('{file_name}')
               FROM({file_name}-REC)
               RIDFLD(CA-KEY)
               KEYLENGTH(WS-KEY-LENGTH)
               RESP(WS-RESP)
           END-EXEC
           
           IF WS-RESP = DFHRESP(NORMAL)
              MOVE '00' TO CA-STATUS
           ELSE
              MOVE '99' TO CA-STATUS
           END-IF
           .
      *
       UPDATE-RECORD-PARA.
           EXEC CICS READ
               FILE('{file_name}')
               UPDATE
               RIDFLD(CA-KEY)
               KEYLENGTH(WS-KEY-LENGTH)
               RESP(WS-RESP)
           END-EXEC
           
           IF WS-RESP = DFHRESP(NORMAL)
              MOVE CA-INPUT-DATA TO {file_name}-REC
              EXEC CICS REWRITE
                  FILE('{file_name}')
                  FROM({file_name}-REC})
                  RESP(WS-RESP2)
              END-EXEC
              MOVE '00' TO CA-STATUS
           ELSE
              MOVE '99' TO CA-STATUS
           END-IF
           .
      *
       DELETE-RECORD-PARA.
           EXEC CICS DELETE
               FILE('{file_name}')
               RIDFLD(CA-KEY)
               KEYLENGTH(WS-KEY-LENGTH)
               RESP(WS-RESP)
           END-EXEC
           
           IF WS-RESP = DFHRESP(NORMAL)
              MOVE '00' TO CA-STATUS
           ELSE
              MOVE '99' TO CA-STATUS
           END-IF
           .
      *
       END PROGRAM {program_name}.
"""

    def _db2_cics_template(self) -> str:
        """CICS-DB2 program template."""
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. {program_name}.
       AUTHOR. {author}.
       DATE-WRITTEN. {date}.
      *
       DATA DIVISION.
       WORKING-STORAGE SECTION.
      *------------------------
      * DB2 SQLCA
      *------------------------
       EXEC SQL 
           INCLUDE SQLCA 
       END-EXEC.
      *
      *------------------------
      * Table Definition
      *------------------------
       EXEC SQL DECLARE {table_name} TABLE (
           {columns}
       ) END-EXEC.
      *
      *------------------------
      * Host Variables
      *------------------------
       01  WS-HOST-VARIABLES.
{host_variables}
      *
      *------------------------
      * Communication Area
      *------------------------
       01  DFHCOMMAREA.
           05  CA-ACTION          PIC X(01).
           05  CA-STATUS          PIC X(02).
           05  CA-MESSAGE         PIC X(50).
      *
       LINKAGE SECTION.
      *
       PROCEDURE DIVISION.
      *
       MAIN-PARA.
           INITIALIZE WS-HOST-VARIABLES
           
           IF EIBCALEN > ZERO
              MOVE DFHCOMMAREA TO WS-COMMAREA-AREA
           END-IF
           
           EVALUATE CA-ACTION
               WHEN 'S'
                   PERFORM SELECT-DATA-PARA
               WHEN 'I'
                   PERFORM INSERT-DATA-PARA
               WHEN 'U'
                   PERFORM UPDATE-DATA-PARA
               WHEN 'D'
                   PERFORM DELETE-DATA-PARA
               WHEN OTHER
                   MOVE 'INVALID ACTION' TO CA-STATUS
           END-EVALUATE
           
           EXEC CICS RETURN
               TRANSID(EIBTRNID)
               COMMAREA(DFHCOMMAREA)
           END-EXEC
           .
      *
       SELECT-DATA-PARA.
           EXEC SQL
               SELECT {select_columns}
               INTO {into_variables}
               FROM {schema}.{table_name}
               WHERE {where_condition}
           END-EXEC
           
           IF SQLCODE = 0
              MOVE '00' TO CA-STATUS
              MOVE 'SELECT SUCCESSFUL' TO CA-MESSAGE
           ELSE
              IF SQLCODE = 100
                 MOVE '12' TO CA-STATUS
                 MOVE 'NO DATA FOUND' TO CA-MESSAGE
              ELSE
                 MOVE '99' TO CA-STATUS
                 MOVE 'SQL ERROR' TO CA-MESSAGE
              END-IF
           END-IF
           .
      *
       INSERT-DATA-PARA.
           EXEC SQL
               INSERT INTO {schema}.{table_name}
                   ({columns})
               VALUES
                   ({values})
           END-EXEC
           
           IF SQLCODE = 0
              MOVE '00' TO CA-STATUS
              EXEC SQL COMMIT END-EXEC
           ELSE
              MOVE '99' TO CA-STATUS
              EXEC SQL ROLLBACK END-EXEC
           END-IF
           .
      *
       UPDATE-DATA-PARA.
           EXEC SQL
               UPDATE {schema}.{table_name}
               SET {set_clause}
               WHERE {where_condition}
           END-EXEC
           
           IF SQLCODE = 0
              MOVE '00' TO CA-STATUS
              EXEC SQL COMMIT END-EXEC
           ELSE
              MOVE '99' TO CA-STATUS
              EXEC SQL ROLLBACK END-EXEC
           END-IF
           .
      *
       DELETE-DATA-PARA.
           EXEC SQL
               DELETE FROM {schema}.{table_name}
               WHERE {where_condition}
           END-EXEC
           
           IF SQLCODE = 0
              MOVE '00' TO CA-STATUS
              EXEC SQL COMMIT END-EXEC
           ELSE
              MOVE '99' TO CA-STATUS
              EXEC SQL ROLLBACK END-EXEC
           END-IF
           .
      *
       END PROGRAM {program_name}.
"""

    def _command_level_template(self) -> str:
        """General CICS Command Level program."""
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. {program_name}.
       AUTHOR. {author}.
       DATE-WRITTEN. {date}.
      *
       DATA DIVISION.
       WORKING-STORAGE SECTION.
      *
       01  WS-RESP                 PIC S9(08) COMP.
       01  WS-RESP2                PIC S9(08) COMP.
       01  WS-TSQ-AREA.
           05  WS-TSQ-QUEUE        PIC X(08).
           05  WS-TSQ-DATA         PIC X(1000).
       01  WS-TSQ-LENGTH           PIC S9(04) COMP VALUE 1008.
      *
       01  DFHCOMMAREA.
           05  CA-COMMAND          PIC X(10).
           05  CA-RESPONSE         PIC X(02).
      *
       LINKAGE SECTION.
      *
       PROCEDURE DIVISION.
      *
      *------------------------
      * Common CICS Commands
      *------------------------
      *
      * GET MAIN STORAGE
           EXEC CICS GETMAIN
               SET(ADDRESS OF WS-TSQ-AREA)
               LENGTH(WS-TSQ-LENGTH)
               INITIMG(LOW-VALUES)
               RESP(WS-RESP)
           END-EXEC
      *
      * WRITE TO TEMPORARY STORAGE QUEUE
           EXEC CICS WRITEQ TS
               QUEUE('MYQUEUE')
               FROM(WS-TSQ-AREA)
               LENGTH(WS-TSQ-LENGTH)
               RESP(WS-RESP)
           END-EXEC
      *
      * READ FROM TEMPORARY STORAGE QUEUE
           EXEC CICS READQ TS
               QUEUE('MYQUEUE')
               INTO(WS-TSQ-AREA)
               LENGTH(WS-TSQ-LENGTH)
               RESP(WS-RESP)
           END-EXEC
      *
      * DELETE TEMPORARY STORAGE QUEUE
           EXEC CICS DELETEQ TS
               QUEUE('MYQUEUE')
               RESP(WS-RESP)
           END-EXEC
      *
      * START ANOTHER TRANSACTION
           EXEC CICS START
               TRANSID('TRAN2')
               FROM(WS-TSQ-DATA)
               LENGTH(100)
               RESP(WS-RESP)
           END-EXEC
      *
      * WAIT FOR TRANSACTION
           EXEC CICS WAIT TRANSACTION
               TRANSID('TRAN1')
           END-EXEC
      *
      * FORMAT DATE
           EXEC CICS FORMATTIME
               ABSTIME(WS-ABSTIME)
               DATESEP('/')
               YEAR(WS-YEAR)
               MONTH(WS-MONTH)
               DAY(WS-DAY)
               RESP(WS-RESP)
           END-EXEC
      *
      * CURRENT DATE
           MOVE FUNCTION CURRENT-DATE TO WS-DATE-AREA
      *
       END PROGRAM {program_name}.
"""

    def _webservice_template(self) -> str:
        """CICS Web Service program template."""
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. {program_name}.
       AUTHOR. {author}.
       DATE-WRITTEN. {date}.
      *
       DATA DIVISION.
       WORKING-STORAGE SECTION.
      *------------------------
      * Web Service Variables
      *------------------------
       01  WS-HTTP-STATUS          PIC 9(03).
       01  WS-RESP                 PIC S9(08) COMP.
       01  WS-URI                  PIC X(255).
       01  WS-METHOD               PIC X(10).
       01  WS-BODY-LENGTH          PIC S9(04) COMP.
      *
       01  WS-RESPONSE-BODY.
           05  FILLER             PIC X(1000).
      *
       01  DFHHTTPBODY.
           05  FILLER             PIC X(32000).
      *
       LINKAGE SECTION.
      *
       PROCEDURE DIVISION.
      *
       MAIN-PARA.
           MOVE SPACES TO DFHHTTPBODY
           
           EXEC CICS WEB READ
               HTTPMETHOD(WS-METHOD)
               URIMAP('MYMAP')
               RESP(WS-RESP)
           END-EXEC
           
           EVALUATE WS-METHOD
               WHEN 'GET'
                   PERFORM HANDLE-GET-PARA
               WHEN 'POST'
                   PERFORM HANDLE-POST-PARA
               WHEN 'PUT'
                   PERFORM HANDLE-PUT-PARA
               WHEN 'DELETE'
                   PERFORM HANDLE-DELETE-PARA
               WHEN OTHER
                   PERFORM HANDLE-ERROR-PARA
           END-EVALUATE
           .
      *
       HANDLE-GET-PARA.
           MOVE '{"status":"success"}' TO DFHHTTPBODY
           MOVE 200 TO WS-HTTP-STATUS
           PERFORM SEND-RESPONSE-PARA
           .
      *
       HANDLE-POST-PARA.
           MOVE 'POST received' TO DFHHTTPBODY
           MOVE 201 TO WS-HTTP-STATUS
           PERFORM SEND-RESPONSE-PARA
           .
      *
       HANDLE-PUT-PARA.
           MOVE 'PUT received' TO DFHHTTPBODY
           MOVE 200 TO WS-HTTP-STATUS
           PERFORM SEND-RESPONSE-PARA
           .
      *
       HANDLE-DELETE-PARA.
           MOVE '{"status":"deleted"}' TO DFHHTTPBODY
           MOVE 204 TO WS-HTTP-STATUS
           PERFORM SEND-RESPONSE-PARA
           .
      *
       HANDLE-ERROR-PARA.
           MOVE '{"error":"Method not allowed"}' TO DFHHTTPBODY
           MOVE 405 TO WS-HTTP-STATUS
           PERFORM SEND-RESPONSE-PARA
           .
      *
       SEND-RESPONSE-PARA.
           EXEC CICS WEB SEND
               STATUSCODE(WS-HTTP-STATUS)
               STATUSTEXT('OK')
               BODY(DFHHTTPBODY)
               BODYLENGTH(LENGTH OF DFHHTTPBODY)
               CONTENTTYPE('application/json')
               RESP(WS-RESP)
           END-EXEC
           .
      *
       END PROGRAM {program_name}.
"""

    def _batch_online_template(self) -> str:
        """CICS Batch-like Online program."""
        return """       IDENTIFICATION DIVISION.
       PROGRAM-ID. {program_name}.
       AUTHOR. {author}.
       DATE-WRITTEN. {date}.
      *
       DATA DIVISION.
       WORKING-STORAGE SECTION.
      *------------------------
      * Batch Control Variables
      *------------------------
       01  WS-BATCH-CONTROL.
           05  WS-RECORD-COUNT     PIC 9(07) VALUE ZEROS.
           05  WS-SUCCESS-COUNT    PIC 9(07) VALUE ZEROS.
           05  WS-ERROR-COUNT      PIC 9(07) VALUE ZEROS.
           05  WS-EOF-SWITCH       PIC X(01) VALUE 'N'.
           88  EOF-REACHED         VALUE 'Y'.
      *
       01  WS-BATCH-STATUS.
           05  BS-RETURN-CODE     PIC 9(02) VALUE 0.
           05  BS-ABEND-CODE       PIC X(04) VALUE SPACES.
      *
       LINKAGE SECTION.
      *
       PROCEDURE DIVISION.
      *
       MAIN-PARA.
           DISPLAY 'BATCH ONLINE PROGRAM STARTED'
           PERFORM INITIALIZE-PARA
           PERFORM OPEN-FILES-PARA
           PERFORM PROCESS-RECORDS-PARA
           PERFORM CLOSE-FILES-PARA
           PERFORM WRITE-REPORT-PARA
           PERFORM RETURN-TO-CICS-PARA
           .
      *
       INITIALIZE-PARA.
           INITIALIZE WS-BATCH-CONTROL WS-BATCH-STATUS
           .
      *
       OPEN-FILES-PARA.
           DISPLAY 'Opening files...'
           .
      *
       PROCESS-RECORDS-PARA.
           PERFORM READ-RECORD-PARA
           
           PERFORM UNTIL EOF-REACHED
               PERFORM PROCESS-RECORD-PARA
               PERFORM READ-RECORD-PARA
           END-PERFORM
           .
      *
       READ-RECORD-PARA.
           ADD 1 TO WS-RECORD-COUNT
           .
      *
       PROCESS-RECORD-PARA.
           DISPLAY 'Processing record: ' WS-RECORD-COUNT
           ADD 1 TO WS-SUCCESS-COUNT
           .
      *
       CLOSE-FILES-PARA.
           DISPLAY 'Closing files...'
           .
      *
       WRITE-REPORT-PARA.
           DISPLAY 'RECORDS READ    : ' WS-RECORD-COUNT
           DISPLAY 'SUCCESS COUNT  : ' WS-SUCCESS-COUNT
           DISPLAY 'ERROR COUNT    : ' WS-ERROR-COUNT
           DISPLAY 'RETURN CODE    : ' BS-RETURN-CODE
           .
      *
       RETURN-TO-CICS-PARA.
           EXEC CICS RETURN
               COMMAREA(WS-BATCH-STATUS)
               LENGTH(6)
           END-EXEC
           .
      *
       END PROGRAM {program_name}.
"""

    def generate(
        self,
        description: str,
        params: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate CICS code based on description.
        
        Args:
            description: Description of the CICS program to generate
            params: Additional parameters
            
        Returns:
            Generated CICS code
        """
        params = params or {}
        
        # Determine template type from description
        template_type = self._determine_template_type(description)
        
        # Get template
        template = self.template_library.get(template_type, self.template_library['basic'])
        
        # Fill in template parameters
        program_name = params.get('program_name', 'PGM001').upper()
        author = params.get('author', 'Generated')
        date = params.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        code = template.format(
            program_name=program_name,
            author=author,
            date=date,
            mapset_name=params.get('mapset_name', 'MAP001').upper(),
            commarea_length=params.get('commarea_length', '100'),
            file_name=params.get('file_name', 'FILE001').upper(),
            copybook_name=params.get('copybook_name', 'REC001').upper(),
            key_length=params.get('key_length', '10'),
            table_name=params.get('table_name', 'EMPLOYEE').upper(),
            schema=params.get('schema', 'PRODUCTION'),
            columns=params.get('columns', 'EMP_ID CHAR(10), EMP_NAME VARCHAR(50)'),
            host_variables=params.get('host_variables', '           05  WS-EMP-ID     PIC X(10).\n           05  WS-EMP-NAME   PIC X(50).'),
            select_columns=params.get('select_columns', '*'),
            into_variables=params.get('into_variables', ':WS-EMP-ID, :WS-EMP-NAME'),
            where_condition=params.get('where_condition', 'EMP_ID = :WS-EMP-ID'),
            values=params.get('values', ':WS-EMP-ID, :WS-EMP-NAME'),
            set_clause=params.get('set_clause', 'EMP_NAME = :WS-EMP-NAME'),
            key_field=params.get('key_field', 'EMPID')
        )
        
        return code

    def _determine_template_type(self, description: str) -> str:
        """Determine which template to use based on description."""
        desc_lower = description.lower()
        
        if 'screen' in desc_lower or 'map' in desc_lower or 'display' in desc_lower:
            return 'screen'
        elif 'file' in desc_lower or 'vsam' in desc_lower:
            return 'file'
        elif 'db2' in desc_lower or 'sql' in desc_lower:
            return 'db2'
        elif 'command' in desc_lower or 'web' in desc_lower or 'ws' in desc_lower:
            return 'command'
        elif 'webservice' in desc_lower or 'http' in desc_lower or 'rest' in desc_lower:
            return 'webservice'
        elif 'batch' in desc_lower:
            return 'batch'
        else:
            return 'basic'

    def get_available_templates(self) -> list:
        """Get list of available templates."""
        return list(self.template_library.keys())

