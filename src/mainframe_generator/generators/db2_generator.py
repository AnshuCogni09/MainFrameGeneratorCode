"""
DB2 SQL Generator

Generates DB2 SQL statements for IBM Mainframe databases.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime


class DB2Generator:
    """Generator for DB2 SQL statements."""

    def __init__(self, config):
        """Initialize DB2 generator.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.template_library = self._load_templates()

    def _load_templates(self) -> Dict[str, str]:
        """Load DB2 SQL templates."""
        return {
            'create_table': self._create_table_template(),
            'create_index': self._create_index_template(),
            'select': self._select_template(),
            'insert': self._insert_template(),
            'update': self._update_template(),
            'delete': self._delete_template(),
            'stored_procedure': self._stored_procedure_template(),
            'cursor': self._cursor_template(),
            'trigger': self._trigger_template(),
            'view': self._view_template()
        }

    def _create_table_template(self) -> str:
        """DB2 CREATE TABLE template."""
        return """-- Create Table: {table_name}
-- Generated: {date}
-- Author: {author}

CREATE TABLE {schema}.{table_name}
    ({columns}
    )
    IN {tablespace}
    INDEX IN {indexspace}
    COMPRESS YES
    APPEND NO
    BUFFERPOOL {bufferpool}
    ;
"""

    def _create_index_template(self) -> str:
        """DB2 CREATE INDEX template."""
        return """-- Create Index: {index_name}
-- Generated: {date}

CREATE UNIQUE INDEX {schema}.{index_name}
    ON {schema}.{table_name}
    ({index_columns})
    CLUSTER
    BUFFERPOOL {bufferpool}
    CLOSE NO
    COMPRESS NO
    PIECESIZE 4G
    ;
"""

    def _select_template(self) -> str:
        """DB2 SELECT statement template."""
        return """-- Select from {table_name}
-- Generated: {date}

SELECT {select_columns}
FROM {schema}.{table_name}
WHERE {where_condition}
ORDER BY {order_by}
FETCH FIRST {fetch_first} ROWS ONLY
;
"""

    def _insert_template(self) -> str:
        """DB2 INSERT statement template."""
        return """-- Insert into {table_name}
-- Generated: {date}

INSERT INTO {schema}.{table_name}
    ({columns})
VALUES
    ({values})
;
"""

    def _update_template(self) -> str:
        """DB2 UPDATE statement template."""
        return """-- Update {table_name}
-- Generated: {date}

UPDATE {schema}.{table_name}
SET {set_clause}
WHERE {where_condition}
;
"""

    def _delete_template(self) -> str:
        """DB2 DELETE statement template."""
        return """-- Delete from {table_name}
-- Generated: {date}

DELETE FROM {schema}.{table_name}
WHERE {where_condition}
;
"""

    def _stored_procedure_template(self) -> str:
        """DB2 Stored Procedure template."""
        return """-- Stored Procedure: {procedure_name}
-- Generated: {date}
-- Author: {author}

CREATE PROCEDURE {schema}.{procedure_name}
    ( {parameters}
    )
    LANGUAGE SQL
    SPECIFIC {procedure_name}
    DYNAMIC RESULT SETS 1
    CONCURRENT ACCESS RESOLUTION
    DETERMINISTIC
    READS SQL DATA
    CALLED ON NULL INPUT
    EXTERNAL NAME ' '
    LANGUAGE SQL
    P1: BEGIN
        -- Declare variables
        DECLARE v_sqlcode INTEGER DEFAULT 0;
        DECLARE v_sqlstate CHAR(5) DEFAULT '00000';
        DECLARE v_error_message VARCHAR(1000);
        
        -- Declare cursor
        DECLARE cursor_{table_name} CURSOR FOR
            SELECT {select_columns}
            FROM {schema}.{table_name}
            WHERE {where_condition};
        
        -- Handler for SQL errors
        DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
            SET v_sqlcode = SQLCODE, v_sqlstate = SQLSTATE;
        
        -- Procedure logic
        OPEN cursor_{table_name};
        
        -- Return result set
        SET result_set_1 = cursor_{table_name};
        
    END P1
;
"""

    def _cursor_template(self) -> str:
        """DB2 Cursor template."""
        return """-- Cursor for {table_name}
-- Generated: {date}

-- Declare cursor
DECLARE cursor_{table_name} CURSOR FOR
    SELECT {select_columns}
    FROM {schema}.{table_name}
    WHERE {where_condition}
    ORDER BY {order_by}
    FOR READ ONLY;

-- Open cursor
OPEN cursor_{table_name};

-- Fetch loop
FETCH cursor_{table_name}
INTO {into_variables};

WHILE v_sqlcode = 0 DO
    -- Process each row
    {process_logic}
    
    FETCH cursor_{table_name}
    INTO {into_variables};
END WHILE;

-- Close cursor
CLOSE cursor_{table_name};
"""

    def _trigger_template(self) -> str:
        """DB2 Trigger template."""
        return """-- Trigger: {trigger_name}
-- Generated: {date}
-- Author: {author}

CREATE TRIGGER {schema}.{trigger_name}
    {trigger_timing} {trigger_event}
    ON {schema}.{table_name}
    REFERENCING {old_new}
    FOR EACH ROW
    MODE DB2SQL
    BEGIN ATOMIC
        -- Trigger logic
        {trigger_logic}
    END
;
"""

    def _view_template(self) -> str:
        """DB2 View template."""
        return """-- View: {view_name}
-- Generated: {date}
-- Author: {author}

CREATE VIEW {schema}.{view_name}
    ({view_columns})
AS
    SELECT {select_columns}
    FROM {schema}.{table_name}
    WHERE {where_condition}
    WITH {check_option}
;
"""

    def generate(
        self,
        description: str,
        params: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate DB2 SQL code based on description.
        
        Args:
            description: Description of the DB2 SQL to generate
            params: Additional parameters
            
        Returns:
            Generated DB2 SQL code
        """
        params = params or {}
        
        # Determine template type from description
        template_type = self._determine_template_type(description)
        
        # Get template
        template = self.template_library.get(template_type, self.template_library['select'])
        
        # Fill in template parameters with defaults
        schema = params.get('schema', 'PRODUCTION')
        table_name = params.get('table_name', 'EMPLOYEE')
        author = params.get('author', 'Generated')
        date = datetime.now().strftime('%Y-%m-%d')
        
        code = template.format(
            schema=schema,
            table_name=table_name,
            author=author,
            date=date,
            columns=params.get('columns', self._default_columns(table_name)),
            tablespace=params.get('tablespace', 'TS' + table_name[:8].upper()),
            indexspace=params.get('indexspace', 'IX' + table_name[:8].upper()),
            bufferpool=params.get('bufferpool', 'BP0'),
            index_name=params.get('index_name', 'IX' + table_name[:8].upper()),
            index_columns=params.get('index_columns', 'COL1 ASC'),
            select_columns=params.get('select_columns', '*'),
            where_condition=params.get('where_condition', '1=1'),
            order_by=params.get('order_by', '1'),
            fetch_first=params.get('fetch_first', '100'),
            values=params.get('values', "'value1', 'value2'"),
            set_clause=params.get('set_clause', 'COL1 = new_value'),
            procedure_name=params.get('procedure_name', 'SP_' + table_name[:8].upper()),
            parameters=params.get('parameters', 'IN p_emp_id CHAR(10), OUT p_status INTEGER'),
            into_variables=params.get('into_variables', 'v_col1, v_col2'),
            process_logic=params.get('process_logic', 'DISPLAY v_col1'),
            trigger_name=params.get('trigger_name', 'TR_' + table_name[:8].upper()),
            trigger_timing=params.get('trigger_timing', 'AFTER'),
            trigger_event=params.get('trigger_event', 'INSERT'),
            old_new=params.get('old_new', 'NEW AS N'),
            trigger_logic=params.get('trigger_logic', 'INSERT INTO LOG_TABLE VALUES (N.emp_id, CURRENT TIMESTAMP)'),
            view_name=params.get('view_name', 'V_' + table_name[:8].upper()),
            view_columns=params.get('view_columns', 'col1, col2'),
            check_option=params.get('check_option', 'CASCADED CHECK OPTION')
        )
        
        return code

    def _default_columns(self, table_name: str) -> str:
        """Generate default column definitions."""
        return """    {table_name}_ID CHAR(10) NOT NULL,
    {table_name}_NAME VARCHAR(50) NOT NULL,
    {table_name}_DATE DATE,
    {table_name}_AMOUNT DECIMAL(10,2),
    {table_name}_STATUS CHAR(1) DEFAULT 'A',
    PRIMARY KEY ({table_name}_ID)
""".format(table_name=table_name[:20])

    def generate_create_table(
        self,
        table_name: str,
        columns: List[Dict[str, str]],
        schema: str = "PRODUCTION"
    ) -> str:
        """Generate CREATE TABLE statement.
        
        Args:
            table_name: Name of the table
            columns: List of column definitions (dict with name, type, null, etc.)
            schema: Database schema
            
        Returns:
            CREATE TABLE SQL statement
        """
        columns_str = ",\n    ".join([
            f"{col['name']} {col['type']}" + 
            (" NOT NULL" if not col.get('nullable', True) else "")
            for col in columns
        ])
        
        params = {
            'schema': schema,
            'table_name': table_name,
            'columns': columns_str
        }
        
        return self.generate('create table', f'Create table {table_name}', params)

    def generate_select(
        self,
        table_name: str,
        columns: List[str] = None,
        where: str = None,
        schema: str = "PRODUCTION"
    ) -> str:
        """Generate SELECT statement.
        
        Args:
            table_name: Name of the table
            columns: List of columns to select
            where: WHERE clause
            schema: Database schema
            
        Returns:
            SELECT SQL statement
        """
        select_columns = ", ".join(columns) if columns else "*"
        
        params = {
            'schema': schema,
            'table_name': table_name,
            'select_columns': select_columns,
            'where_condition': where or '1=1',
            'order_by': '1',
            'fetch_first': '100'
        }
        
        return self.generate('select', f'Select from {table_name}', params)

    def generate_insert(
        self,
        table_name: str,
        columns: List[str],
        values: List[str],
        schema: str = "PRODUCTION"
    ) -> str:
        """Generate INSERT statement.
        
        Args:
            table_name: Name of the table
            columns: List of column names
            values: List of values
            schema: Database schema
            
        Returns:
            INSERT SQL statement
        """
        params = {
            'schema': schema,
            'table_name': table_name,
            'columns': ", ".join(columns),
            'values': ", ".join(values)
        }
        
        return self.generate('insert', f'Insert into {table_name}', params)

    def generate_update(
        self,
        table_name: str,
        set_clause: str,
        where: str,
        schema: str = "PRODUCTION"
    ) -> str:
        """Generate UPDATE statement.
        
        Args:
            table_name: Name of the table
            set_clause: SET clause
            where: WHERE clause
            schema: Database schema
            
        Returns:
            UPDATE SQL statement
        """
        params = {
            'schema': schema,
            'table_name': table_name,
            'set_clause': set_clause,
            'where_condition': where
        }
        
        return self.generate('update', f'Update {table_name}', params)

    def _determine_template_type(self, description: str) -> str:
        """Determine which template to use based on description."""
        desc_lower = description.lower()
        
        if 'create table' in desc_lower:
            return 'create_table'
        elif 'create index' in desc_lower or 'index' in desc_lower:
            return 'create_index'
        elif 'insert' in desc_lower:
            return 'insert'
        elif 'update' in desc_lower:
            return 'update'
        elif 'delete' in desc_lower:
            return 'delete'
        elif 'procedure' in desc_lower or 'stored proc' in desc_lower:
            return 'stored_procedure'
        elif 'cursor' in desc_lower:
            return 'cursor'
        elif 'trigger' in desc_lower:
            return 'trigger'
        elif 'view' in desc_lower:
            return 'view'
        else:
            return 'select'

    def get_available_templates(self) -> list:
        """Get list of available templates."""
        return list(self.template_library.keys())

