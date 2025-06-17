#!/usr/bin/env python3
"""
OBDA Reasoning Demo Executor
Interactive demonstration of query differences with and without reasoning
"""

import subprocess
import mysql.connector
import json
import time
from typing import List, Dict, Tuple
import requests
from tabulate import tabulate
import colorama
from colorama import Fore, Back, Style

# Initialize colors
colorama.init()

class OBDADemoRunner:
    """OBDA Demo Runner"""
    
    def __init__(self, config_file='config/demo_config.json'):
        # Default configuration
        self.config = {
            'ontop_path': './lib/ontop-cli-*/ontop',
            'ontology': 'ontology/university.ttl',
            'mappings': 'mappings/university.obda',
            'properties': 'config/university.properties',
            'sparql_endpoint': 'http://localhost:8080/sparql',
            'mysql': {
                'host': 'localhost',
                'user': 'root',
                'database': 'university_demo'
            }
        }
        
        # Try to load configuration file
        try:
            with open(config_file, 'r') as f:
                self.config.update(json.load(f))
        except:
            pass
    
    def print_header(self, text: str):
        """Print header"""
        print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{text.center(60)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")
    
    def print_section(self, text: str):
        """Print section title"""
        print(f"\n{Fore.GREEN}▶ {text}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'-' * 40}{Style.RESET_ALL}")
    
    def print_query(self, query: str, query_type: str = "SPARQL"):
        """Print query"""
        print(f"\n{Fore.YELLOW}{query_type} Query:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{query}{Style.RESET_ALL}")
    
    def print_result(self, result: List, label: str = "Results"):
        """Print results"""
        print(f"\n{Fore.MAGENTA}{label}: {len(result)} records{Style.RESET_ALL}")
        if result:
            if isinstance(result[0], tuple):
                # Multi-column results
                headers = [f"Column{i+1}" for i in range(len(result[0]))]
                print(tabulate(result, headers=headers, tablefmt="grid"))
            else:
                # Single column results
                for item in result[:10]:  # Show only first 10 records
                    print(f"  • {item}")
                if len(result) > 10:
                    print(f"  ... {len(result) - 10} more records")
    
    def execute_sql(self, query: str) -> List:
        """Execute SQL query"""
        if not hasattr(self, 'db_conn'):
            password = input("Please enter MySQL password: ")
            self.db_conn = mysql.connector.connect(
                host=self.config['mysql']['host'],
                user=self.config['mysql']['user'],
                password=password,
                database=self.config['mysql']['database']
            )
        
        cursor = self.db_conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
    
    def execute_sparql_cli(self, query: str, enable_reasoning: bool = True) -> List:
        with open('temp_query.sparql', 'w') as f:
            f.write(query)
        
        cmd = [
            'bash', '-c',
            f"{self.config['ontop_path']} query "
            f"--ontology={self.config['ontology']} "
            f"--mapping={self.config['mappings']} "
            f"--properties={self.config['properties']} "
            f"--query=temp_query.sparql "
            f"--disable-reasoning={'false' if enable_reasoning else 'true'}"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            lines = result.stdout.strip().split('\n')
            results = []
            for line in lines[1:]:  # Skip header line
                if line.strip() and not line.startswith('-'):
                    results.append(line.strip())
            
            return results
        except subprocess.TimeoutExpired:
            return ["overtime: query execution took too long"]
        except Exception as e:
            return [f"error: {str(e)}"]
        
    def demo_1_basic_hierarchy(self):
        """Demo 1: Basic class hierarchy reasoning"""
        self.print_header("Demo 1: Class Hierarchy Reasoning")
        
        # Scenario description
        print("Scenario: Query all persons (Person)")
        print("There are no records directly marked as Person in the database,")
        print("but Employee and Student are subclasses of Person.")
        
        # SQL query (simulating no reasoning)
        self.print_section("SQL Query (no reasoning concept)")
        sql_query = """
        -- SQL cannot understand Person concept, must query separately
        SELECT name, 'Employee' as type FROM employees
        UNION ALL
        SELECT name, 'Student' as type FROM students
        """
        self.print_query(sql_query, "SQL")
        sql_results = self.execute_sql(sql_query)
        self.print_result(sql_results, "SQL Results")
        
        # SPARQL query (with reasoning)
        self.print_section("SPARQL Query (with reasoning)")
        sparql_query = """
PREFIX : <http://example.org/university#>

SELECT ?person ?name
WHERE {
    ?person a :Person ;
            :hasName ?name .
}
ORDER BY ?name
"""
        self.print_query(sparql_query, "SPARQL")
        
        # Execute query
        print(f"\n{Fore.CYAN}Executing...{Style.RESET_ALL}")
        sparql_results = self.execute_sparql_cli(sparql_query, enable_reasoning=True)
        self.print_result(sparql_results, "SPARQL Results (reasoning enabled)")
        
        # Compare without reasoning
        print(f"\n{Fore.RED}With reasoning disabled:{Style.RESET_ALL}")
        no_reasoning_results = self.execute_sparql_cli(sparql_query, enable_reasoning=False)
        self.print_result(no_reasoning_results, "SPARQL Results (reasoning disabled)")
        
        # Summary
        print(f"\n{Fore.GREEN}【Key Findings】{Style.RESET_ALL}")
        print("• SQL requires manual UNION of all related tables")
        print("• SPARQL without reasoning returns 0 records (no direct Person instances)")
        print("• SPARQL with reasoning automatically includes all subclass instances")
    
    def demo_2_equivalent_class(self):
        """Demo 2: Equivalent class reasoning"""
        self.print_header("Demo 2: Equivalent Class Reasoning")
        
        print("Scenario: Query all teachers (Teacher)")
        print("Teacher is defined as: employees with teaching assignments")
        print("This is a dynamically computed concept, not a static label.")
        
        # SQL query
        self.print_section("SQL Query (manual JOIN)")
        sql_query = """
        SELECT DISTINCT e.name
        FROM employees e
        INNER JOIN teaching_records t ON e.emp_id = t.emp_id
        ORDER BY e.name
        """
        self.print_query(sql_query, "SQL")
        sql_results = self.execute_sql(sql_query)
        self.print_result([r[0] for r in sql_results], "SQL Results")
        
        # SPARQL query
        self.print_section("SPARQL Query (automatic reasoning)")
        sparql_query = """
PREFIX : <http://example.org/university#>

SELECT DISTINCT ?teacher ?name
WHERE {
    ?teacher a :Teacher ;
             :hasName ?name .
}
ORDER BY ?name
"""
        self.print_query(sparql_query, "SPARQL")
        
        print(f"\n{Fore.CYAN}Executing...{Style.RESET_ALL}")
        sparql_results = self.execute_sparql_cli(sparql_query, enable_reasoning=True)
        self.print_result(sparql_results, "SPARQL Results")
        
        # Show reasoning process
        print(f"\n{Fore.YELLOW}Reasoning Process:{Style.RESET_ALL}")
        print("1. Teacher ≡ Employee ⊓ ∃teaches.Course")
        print("2. System automatically finds all instances that satisfy this definition")
        print("3. No need to manually write JOIN logic")
    
    def demo_3_multi_level_hierarchy(self):
        """Demo 3: Multi-level hierarchy reasoning"""
        self.print_header("Demo 3: Multi-level Class Reasoning")
        
        print("Scenario: Query all academic staff (AcademicStaff)")
        print("Includes: Professor, AssociateProfessor, Lecturer")
        
        # SQL query
        self.print_section("SQL Query (manual enumeration)")
        sql_query = """
        SELECT name, position
        FROM employees
        WHERE position IN ('Professor', 'Associate Professor', 'Lecturer')
        ORDER BY name
        """
        self.print_query(sql_query, "SQL")
        sql_results = self.execute_sql(sql_query)
        self.print_result(sql_results, "SQL Results")
        
        # SPARQL query
        self.print_section("SPARQL Query (automatic subclass inclusion)")
        sparql_query = """
PREFIX : <http://example.org/university#>

SELECT ?staff ?name
WHERE {
    ?staff a :AcademicStaff ;
           :hasName ?name .
}
ORDER BY ?name
"""
        self.print_query(sparql_query, "SPARQL")
        
        sparql_results = self.execute_sparql_cli(sparql_query, enable_reasoning=True)
        self.print_result(sparql_results, "SPARQL Results")
        
        print(f"\n{Fore.GREEN}【Advantages】{Style.RESET_ALL}")
        print("• SQL requires hardcoding all position types")
        print("• Adding new positions (like Assistant Professor) requires SQL modification")
        print("• SPARQL automatically adapts to ontology changes")
    
    def demo_4_complex_reasoning(self):
        """Demo 4: Complex reasoning query"""
        self.print_header("Demo 4: Combined Reasoning Query")
        
        print("Scenario: Find advisor information for all graduate students")
        print("Demonstrates combination of multiple concept reasoning")
        
        # SPARQL query
        sparql_query = """
PREFIX : <http://example.org/university#>

SELECT ?student ?studentName ?advisor ?advisorName
WHERE {
    ?student a :GraduateStudent ;
             :hasName ?studentName ;
             :hasAdvisor ?advisor .
    
    ?advisor a :AcademicStaff ;
             :hasName ?advisorName .
}
ORDER BY ?studentName
"""
        self.print_query(sparql_query, "SPARQL")
        
        results = self.execute_sparql_cli(sparql_query, enable_reasoning=True)
        self.print_result(results, "Results")
        
        print(f"\n{Fore.YELLOW}Reasoning Key Points:{Style.RESET_ALL}")
        print("1. GraduateStudent inferred through JOIN")
        print("2. AcademicStaff includes all academic positions")
        print("3. Multiple reasoning concepts combined in one query")
    
    def show_reasoning_comparison(self):
        """Show reasoning effect summary comparison"""
        self.print_header("Reasoning Effect Summary")
        
        comparisons = [
            ["Query Target", "SQL Method", "SPARQL No Reasoning", "SPARQL With Reasoning"],
            ["All Person", "Manual UNION two tables", "0 records", "9 records (auto subclass inclusion)"],
            ["All Teacher", "Manual JOIN teaching records", "0 records", "4 records (equivalent class reasoning)"],
            ["All AcademicStaff", "WHERE IN enumeration", "0 records", "4 records (subclass reasoning)"],
            ["Complex combined query", "Multi-table JOIN+conditions", "Partial results", "Complete results"]
        ]
        
        print(tabulate(comparisons, headers="firstrow", tablefmt="grid"))
        
        print(f"\n{Fore.GREEN}Core Advantages:{Style.RESET_ALL}")
        print("1. Concept abstraction: Use business concepts instead of physical structure")
        print("2. Automatic reasoning: No need to manually handle class hierarchy relationships")
        print("3. Easy maintenance: Modify ontology only, no need to change queries")
        print("4. Semantic richness: Support complex concept definitions and reasoning")
    
    def interactive_mode(self):
        """Interactive demo mode"""
        self.print_header("OBDA Reasoning Interactive Demo")
        
        demos = {
            '1': ('Class hierarchy reasoning', self.demo_1_basic_hierarchy),
            '2': ('Equivalent class reasoning', self.demo_2_equivalent_class),
            '3': ('Multi-level reasoning', self.demo_3_multi_level_hierarchy),
            '4': ('Complex combined query', self.demo_4_complex_reasoning),
            '5': ('View reasoning effect summary', self.show_reasoning_comparison),
            'q': ('Exit', None)
        }
        
        while True:
            print(f"\n{Fore.CYAN}Please select demo:{Style.RESET_ALL}")
            for key, (desc, _) in demos.items():
                print(f"  {key}. {desc}")
            
            choice = input(f"\n{Fore.YELLOW}Enter choice: {Style.RESET_ALL}").strip()
            
            if choice == 'q':
                print(f"{Fore.GREEN}Thank you for using!{Style.RESET_ALL}")
                break
            
            if choice in demos and demos[choice][1]:
                try:
                    demos[choice][1]()
                    input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")

def main():
    """Main function"""
    import sys
    
    runner = OBDADemoRunner()
    
    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] == 'demo1':
            runner.demo_1_basic_hierarchy()
        elif sys.argv[1] == 'demo2':
            runner.demo_2_equivalent_class()
        elif sys.argv[1] == 'demo3':
            runner.demo_3_multi_level_hierarchy()
        elif sys.argv[1] == 'demo4':
            runner.demo_4_complex_reasoning()
        elif sys.argv[1] == 'summary':
            runner.show_reasoning_comparison()
        else:
            print("Usage: python obda_demo_runner.py [demo1|demo2|demo3|demo4|summary]")
    else:
        # Interactive mode
        runner.interactive_mode()

if __name__ == "__main__":
    main()