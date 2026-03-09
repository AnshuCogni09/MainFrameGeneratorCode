"""
JCL (Job Control Language) Generator

Generates JCL for IBM Mainframe jobs using templates and AI assistance.
"""

from typing import Dict, Any, Optional
from datetime import datetime


class JCLGenerator:
    """Generator for JCL (Job Control Language)."""

    def __init__(self, config):
        """Initialize JCL generator.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.template_library = self._load_templates()

    def _load_templates(self) -> Dict[str, str]:
        """Load JCL templates."""
        return {
            'basic': self._basic_job_template(),
            'sort': self._sort_job_template(),
            'cobol_run': self._cobol_run_template(),
            'db2_utilities': self._db2_utilities_template(),
            'iefbr14': self._iefbr14_copy_template(),
            ' repro': self._repro_template(),
            'ftp': self._ftp_job_template(),
            'conditional': self._conditional_job_template()
        }

    def _basic_job_template(self) -> str:
        """Basic JCL job template."""
        return """//{job_name} JOB ({account_info}),'{programmer_name}',CLASS={job_class},
//             MSGCLASS={msg_class},REGION={region}
//*
//* {description}
//*
//JOBLIB   DD DSN=YOUR.COBOL.LIBRARY,DISP=SHR
//         DD DSN=YOUR.LOAD.LIBRARY,DISP=SHR
//*
//STEP1    EXEC PGM={program_name},REGION={region}
{dd_statements}
//
"""

    def _sort_job_template(self) -> str:
        """JCL for DFSORT job."""
        return """//{job_name} JOB ({account_info}),'{programmer_name}',CLASS={job_class},
//             MSGCLASS={msg_class},REGION={region}
//*
//* SORT Job - {description}
//*
//SORT     EXEC PGM=SORT,REGION={region}
//SYSOUT   DD SYSOUT=*
//SORTIN   DD DSN={input_dataset},DISP=SHR
//SORTOUT  DD DSN={output_dataset},
//            DISP=(NEW,CATLG,DELETE),
//            SPACE=(TRK,({primary},{secondary}),RLSE),
//            UNIT={unit}
//SYSIN    DD *
  SORT FIELDS=({sort_fields})
  OUTREC FIELDS=({outrec_fields})
/*
//
"""

    def _cobol_run_template(self) -> str:
        """JCL to compile and run a COBOL program."""
        return """//{job_name} JOB ({account_info}),'{programmer_name}',CLASS={job_class},
//             MSGCLASS={msg_class},REGION={region}
//*
//* Compile and Run COBOL Program: {program_name}
//*
//* Compile Step
//COMPILE  EXEC PGM=IGYCRCTL,REGION={region},
//             PARM='LIST,MAP,NUMBER,RENT'
//SYSPRINT DD SYSOUT=*
//SYSLIB   DD DSN=YOUR.COBOL.LIBRARY,DISP=SHR
//         DD DSN=SYS1.COBLIB,DISP=SHR
//SYSUT1   DD UNIT=SYSDA,SPACE=(CYL,(1,1))
//SYSUT2   DD UNIT=SYSDA,SPACE=(CYL,(1,1))
//SYSUT3   DD UNIT=SYSDA,SPACE=(CYL,(1,1))
//SYSUT4   DD UNIT=SYSDA,SPACE=(CYL,(1,1))
//SYSUT5   DD UNIT=SYSDA,SPACE=(CYL,(1,1))
//SYSUT6   DD UNIT=SYSDA,SPACE=(CYL,(1,1))
//SYSUT7   DD UNIT=SYSDA,SPACE=(CYL,(1,1))
//SYSLIN   DD DSN=&&LOADSET,DISP=(NEW,PASS,DELETE),
//            UNIT=SYSDA,SPACE=(TRK,(1,1)),
//            DCB=(RECFM=FB,LRECL=80,BLKSIZE=3120)
//SYSIN    DD DSN=YOUR.COBOL.SOURCE({member_name}),DISP=SHR
//*
//* Link Step
//LINK    EXEC PGM=IEWL,REGION={region},
//             PARM='LIST,XREF,RENT,REFR'
//SYSLIN   DD DSN=&&LOADSET,DISP=SHR
//         DD DSN=SYS1.COBLIB,DISP=SHR
//SYSLMOD  DD DSN=YOUR.LOAD.LIBRARY({member_name}),DISP=SHR
//SYSUT1   DD UNIT=SYSDA,SPACE=(TRK,(1,1))
//SYSOUT   DD SYSOUT=*
//*
//* Run Step
//RUN     EXEC PGM={member_name},REGION={region}
//STEPLIB  DD DSN=YOUR.LOAD.LIBRARY,DISP=SHR
//SYSPRINT DD SYSOUT=*
//SYSOUT   DD SYSOUT=*
{dd_statements}
//
"""

    def _db2_utilities_template(self) -> str:
        """JCL for DB2 utilities (RUNSTATS, REORG, CHECK)."""
        return """//{job_name} JOB ({account_info}),'{programmer_name}',CLASS={job_class},
//             MSGCLASS={msg_class},REGION={region}
//*
//* DB2 Utility: {utility_name}
//*
//DB2ENV   EXEC PGM=IKJEFT01,DYNAMNBR=30,REGION={region}
//SYSTSPRT DD SYSOUT=*
//SYSTSIN  DD *
  DSN SYSTEM({db2_subsystem})
  RUNSTATS TABLESPACE {database_name}.{tablespace_name}
    TABLE({table_name})
    INDEX({index_name})
/*
//*
//
"""

    def _iefbr14_copy_template(self) -> str:
        """JCL using IEFBR14 for dataset operations."""
        return """//{job_name} JOB ({account_info}),'{programmer_name}',CLASS={job_class},
//             MSGCLASS={msg_class}
//*
//* Dataset Operations using IEFBR14
//*
//* Step 1: Delete existing dataset
//DELETE   EXEC PGM=IEFBR14
//DD1      DD DSN={dataset_name},
//            DISP=(MOD,DELETE,DELETE),
//            UNIT={unit}
//*
//* Step 2: Allocate new dataset
//ALLOC    EXEC PGM=IEFBR14
//DD1      DD DSN={dataset_name},
//            DISP=(NEW,CATLG,DELETE),
//            SPACE=({space_units},({primary},{secondary}),RLSE),
//            UNIT={unit},
//            DCB=(RECFM={recfm},LRECL={lrecl},BLKSIZE={blksize})
//*
//* Step 3: Copy data
//COPY     EXEC PGM=IEBGENER
//SYSIN    DD DUMMY
//SYSPRINT DD SYSOUT=*
//SYSUT1   DD DSN={source_dataset},DISP=SHR
//SYSUT2   DD DSN={dataset_name},DISP=SHR
//*
//
"""

    def _repro_template(self) -> str:
        """JCL for IDCAMS REPRO operation."""
        return """//{job_name} JOB ({account_info}),'{programmer_name}',CLASS={job_class},
//             MSGCLASS={msg_class}
//*
//* IDCAMS REPRO - Copy dataset
//*
//REPRO    EXEC PGM=IDCAMS,REGION={region}
//SYSPRINT DD SYSOUT=*
//IN       DD DSN={input_dataset},DISP=SHR
//OUT      DD DSN={output_dataset},
//            DISP=(NEW,CATLG,DELETE),
//            SPACE=(TRK,({primary},{secondary}),RLSE),
//            UNIT={unit}
//SYSIN    DD *
  REPRO -
    INDATASET(IN) -
    OUTDATASET(OUT) -
    REPLACE
/*
//
"""

    def _ftp_job_template(self) -> str:
        """JCL for FTP operations."""
        return """//{job_name} JOB ({account_info}),'{programmer_name}',CLASS={job_class},
//             MSGCLASS={msg_class}
//*
//* FTP Job - Transfer {direction}
//*
//FTP      EXEC PGM=FTP,REGION={region}
//SYSPRINT DD SYSOUT=*
//SYSIN    DD *
{ftp_host}
{ftp_user}
{ftp_password}
{binary_mode}
{ftp_commands}
//*
//
"""

    def _conditional_job_template(self) -> str:
        """JCL with conditional execution."""
        return """//{job_name} JOB ({account_info}),'{programmer_name}',CLASS={job_class},
//             MSGCLASS={msg_class},REGION={region}
//*
//* Conditional Job Execution
//*
//* Step 1: Check condition
//CHECK    EXEC PGM=IKJEFT01
//SYSTSPRT DD SYSOUT=*
//SYSTSIN  DD *
  LISTCAT ENTRIES({dataset_name}) ALL
/*
//*
//* Step 2: Execute only if previous step succeeds (COND=EVEN allows first run)
//PROCESS  EXEC PGM={program_name},COND=(0,NE,CHECK)
//SYSPRINT DD SYSOUT=*
{dd_statements}
//*
//* Step 3: Alternative processing if step 2 doesn't run
//ALTPRoc  EXEC PGM=ALTPGM,COND=(0,LE,PROCESS)
//SYSPRINT DD SYSOUT=*
//*
//
"""

    def generate(
        self,
        description: str,
        params: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate JCL code based on description.
        
        Args:
            description: Description of the JCL job to generate
            params: Additional parameters
            
        Returns:
            Generated JCL code
        """
        params = params or {}
        
        # Determine template type from description
        template_type = self._determine_template_type(description)
        
        # Get template
        template = self.template_library.get(template_type, self.template_library['basic'])
        
        # Fill in template parameters with defaults
        job_name = params.get('job_name', 'JOB001').upper()[:8]
        account_info = params.get('account_info', 'ACCT123')
        programmer_name = params.get('programmer_name', 'PROGRAMMER')
        job_class = params.get('job_class', 'A')
        msg_class = params.get('msg_class', 'H')
        region = params.get('region', '4M')
        program_name = params.get('program_name', 'PROGRAM1')
        description = params.get('description', 'Generated JCL')
        
        # Generate DD statements if provided
        dd_statements = params.get('dd_statements', self._default_dd_statements())
        
        code = template.format(
            job_name=job_name,
            account_info=account_info,
            programmer_name=programmer_name,
            job_class=job_class,
            msg_class=msg_class,
            region=region,
            program_name=program_name,
            description=description,
            dd_statements=dd_statements,
            input_dataset=params.get('input_dataset', 'YOUR.INPUT.DATA'),
            output_dataset=params.get('output_dataset', 'YOUR.OUTPUT.DATA'),
            sort_fields=params.get('sort_fields', '1,5,A'),
            outrec_fields=params.get('outrec_fields', '1,80'),
            member_name=params.get('member_name', 'PROG001'),
            db2_subsystem=params.get('db2_subsystem', 'DB2P'),
            database_name=params.get('database_name', 'DBNAME'),
            tablespace_name=params.get('tablespace_name', 'TSNAME'),
            table_name=params.get('table_name', 'TABNAME'),
            index_name=params.get('index_name', 'INDNAME'),
            utility_name=params.get('utility_name', 'RUNSTATS'),
            dataset_name=params.get('dataset_name', 'YOUR.DATASET.NAME'),
            unit=params.get('unit', 'SYSDA'),
            primary=params.get('primary', '10'),
            secondary=params.get('secondary', '5'),
            space_units=params.get('space_units', 'TRK'),
            recfm=params.get('recfm', 'FB'),
            lrecl=params.get('lrecl', '80'),
            blksize=params.get('blksize', '27920'),
            source_dataset=params.get('source_dataset', 'YOUR.SOURCE.DATA'),
            direction=params.get('direction', 'files'),
            ftp_host=params.get('ftp_host', 'ftp.example.com'),
            ftp_user=params.get('ftp_user', 'userid'),
            ftp_password=params.get('ftp_password', 'password'),
            binary_mode=params.get('binary_mode', 'binary'),
            ftp_commands=params.get('ftp_commands', 'get file.txt')
        )
        
        return code

    def _default_dd_statements(self) -> str:
        """Generate default DD statements."""
        return """//SYSIN    DD DUMMY
//SYSPRINT DD SYSOUT=*
//SYSOUT   DD SYSOUT=*"""

    def _determine_template_type(self, description: str) -> str:
        """Determine which template to use based on description."""
        desc_lower = description.lower()
        
        if 'sort' in desc_lower:
            return 'sort'
        elif 'cobol' in desc_lower or 'compile' in desc_lower:
            return 'cobol_run'
        elif 'db2' in desc_lower or 'runstats' in desc_lower or 'reorg' in desc_lower:
            return 'db2_utilities'
        elif 'copy' in desc_lower or 'iefbr14' in desc_lower:
            return 'iefbr14'
        elif 'repro' in desc_lower or 'idcams' in desc_lower:
            return ' repro'
        elif 'ftp' in desc_lower:
            return 'ftp'
        elif 'conditional' in desc_lower or 'if' in desc_lower:
            return 'conditional'
        else:
            return 'basic'

    def get_available_templates(self) -> list:
        """Get list of available templates."""
        return list(self.template_library.keys())

