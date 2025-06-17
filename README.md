# OBDA Empirical Analysis: University Database Ontology Reasoning Demonstration

## Experimental Objectives

Through a simple university database case, demonstrate:
1. How OBDA maps relational databases to the semantic layer
2. How ontology reasoning enriches query results
3. The advantages of SPARQL queries compared to SQL

## Case Background: University Personnel Management System

Suppose we have a traditional university database that stores information about faculty, staff, and students. The database was designed without considering conceptual hierarchies; tables were simply created according to departmental needs. Now, we aim to use OBDA technology to add a semantic layer to this database, enabling it to answer more intelligent queries.

## Quick Start

1. Start the SPARQL endpoint:
   ```bash
   ./start_endpoint.sh
   ```

2. Run example queries:
   ```bash
   ./run_all_queries.sh
   ```

3. Compare with SQL queries:
   ```bash
   ./verify_sql.sh
   ```

## Key Concept Demonstration

### 1. Subclass Reasoning
- Querying `Person` automatically includes all `Employee` and `Student`
- Querying `AcademicStaff` automatically includes `Professor`, `AssociateProfessor`, and `Lecturer`

### 2. Equivalent Class Reasoning
- `Teacher` is defined as "an employee with teaching duties"
- The system automatically infers who is a Teacher

### 3. Multi-level Reasoning
- `Professor` is a subclass of `AcademicStaff`
- `AcademicStaff` is a subclass of `Employee`
- `Employee` is a subclass of `Person`
- When querying `Person`, `Professor` will be included

## Query Description

1. **01_all_persons.sparql**: Demonstrates reasoning for the Person class
2. **02_academic_staff.sparql**: Demonstrates multi-level subclass reasoning
3. **03_teachers.sparql**: Demonstrates equivalent class reasoning
4. **04_supervisors.sparql**: Demonstrates inverse property reasoning
5. **05_graduate_info.sparql**: Demonstrates a complex query
6. **06_dept_teaching_load.sparql**: Demonstrates an aggregate query

## Reasoning Effect Comparison

| Query Target | SQL Result | SPARQL + Reasoning Result | Reason for Difference |
|--------------|------------|---------------------------|-----------------------|
| All Persons  | Cannot query | 9 records                 | SQL has no Person concept, SPARQL reasoning includes all subclasses |
| All Teachers | Requires complex JOIN | 3 records                 | SPARQL automatically infers equivalent class definition |
| All AcademicStaff | Requires OR conditions | 4 records                 | SPARQL automatically includes all subclasses |

## Technical Architecture

```
User <--SPARQL--> Ontop <--SQL--> MySQL
                   |
              Ontology + Mappings
                   |
             Reasoning Engine
```

## Further Learning

1. Modify the ontology file, add new classes or properties
2. Modify the mapping file, try different mapping strategies
3. Write new SPARQL queries, explore reasoning capabilities
4. Use debug mode to view the query rewriting process:
   ```bash
   ./run_query.sh queries/01_all_persons.sparql --log-level=DEBUG
   ```