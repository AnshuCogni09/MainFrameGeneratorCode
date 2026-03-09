"""
Tests for MainFrame Code Generator

This file tests the code generation functionality.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mainframe_generator import MainFrameAgent, Config
from mainframe_generator.generators import COBOLGenerator, JCLGenerator, DB2Generator, CICSGenerator
from mainframe_generator.validators import CodeValidator


def test_config():
    """Test configuration loading."""
    config = Config()
    assert config is not None
    assert config.default_language == "COBOL"
    print("✓ Config test passed")


def test_cobol_generator():
    """Test COBOL code generation."""
    config = Config()
    generator = COBOLGenerator(config)
    
    # Test basic program generation
    code = generator.generate("basic program", {'program_name': 'TEST001'})
    assert 'IDENTIFICATION DIVISION' in code
    assert 'PROGRAM-ID' in code
    assert 'TEST001' in code
    
    # Test templates
    templates = generator.get_available_templates()
    assert 'basic' in templates
    assert 'file_io' in templates
    
    print("✓ COBOL generator test passed")


def test_jcl_generator():
    """Test JCL code generation."""
    config = Config()
    generator = JCLGenerator(config)
    
    # Test basic JCL
    code = generator.generate("basic job", {'job_name': 'JOB001'})
    assert 'JOB' in code
    assert 'JOB001' in code
    
    # Test templates
    templates = generator.get_available_templates()
    assert 'basic' in templates
    
    print("✓ JCL generator test passed")


def test_db2_generator():
    """Test DB2 SQL code generation."""
    config = Config()
    generator = DB2Generator(config)
    
    # Test SELECT
    code = generator.generate("select employee", {'table_name': 'EMPLOYEE'})
    assert 'SELECT' in code.upper()
    assert 'EMPLOYEE' in code
    
    # Test CREATE TABLE
    code = generator.generate("create table employee", {'table_name': 'EMPLOYEE'})
    assert 'CREATE TABLE' in code.upper()
    
    print("✓ DB2 generator test passed")


def test_cics_generator():
    """Test CICS code generation."""
    config = Config()
    generator = CICSGenerator(config)
    
    # Test basic CICS
    code = generator.generate("basic cics program", {'program_name': 'PGM001'})
    assert 'IDENTIFICATION DIVISION' in code
    assert 'EXEC CICS RETURN' in code.upper()
    
    # Test templates
    templates = generator.get_available_templates()
    assert 'basic' in templates
    
    print("✓ CICS generator test passed")


def test_code_validator():
    """Test code validation."""
    config = Config()
    validator = CodeValidator(config)
    
    # Test COBOL validation
    cobol_code = """       IDENTIFICATION DIVISION.
       PROGRAM-ID. TEST001.
       PROCEDURE DIVISION.
       MAIN-PARA.
           STOP RUN.
       END PROGRAM TEST001.
"""
    result = validator.validate(cobol_code, 'cobol')
    assert result.is_valid == True
    
    # Test JCL validation
    jcl_code = """//JOB001 JOB (ACCT),'TEST',CLASS=A
//STEP1 EXEC PGM=IEFBR14
"""
    result = validator.validate(jcl_code, 'jcl')
    assert result.is_valid == True
    
    print("✓ Code validator test passed")


def test_agent():
    """Test main agent."""
    config = Config()
    agent = MainFrameAgent(config)
    
    # Test list generators
    generators = agent.list_generators()
    assert 'cobol' in generators
    assert 'jcl' in generators
    assert 'db2' in generators
    assert 'cics' in generators
    
    # Test supported languages
    languages = agent.get_supported_languages()
    assert 'COBOL' in languages
    assert 'JCL' in languages
    
    print("✓ Agent test passed")


def test_generate_methods():
    """Test convenience generate methods."""
    config = Config()
    agent = MainFrameAgent(config)
    
    # Test COBOL generation
    code = agent.generate_cobol("basic program")
    assert code is not None
    assert len(code) > 0
    
    # Test JCL generation
    code = agent.generate_jcl("basic job")
    assert code is not None
    
    # Test DB2 generation
    code = agent.generate_db2("select statement")
    assert code is not None
    
    # Test CICS generation
    code = agent.generate_cics("basic program")
    assert code is not None
    
    print("✓ Generate methods test passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*50)
    print("Running MainFrame Code Generator Tests")
    print("="*50 + "\n")
    
    try:
        test_config()
        test_cobol_generator()
        test_jcl_generator()
        test_db2_generator()
        test_cics_generator()
        test_code_validator()
        test_agent()
        test_generate_methods()
        
        print("\n" + "="*50)
        print("All tests passed! ✓")
        print("="*50 + "\n")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

