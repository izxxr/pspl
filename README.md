# PSPL
**P**seudocode **S**tyled **P**rogramming **L**anguage (PSPL) is an experimental programming language written in Python.

## Overview
The syntax of this language is heavily inspired from (or should I say, exactly identical to) the
[CAIE A Level Computer Science (9618) Pseudocode](https://pdfcoffee.com/9618-pseudocode-guide-for-teachers-for-examination-from-2021-pdf-free.html).
This makes this project a use case for students who are studying Computer Science in A Level and educators who are teaching the syllabus.

The features that have been implemented are:

- [x] Variables and Constants
- [x] Basic Data Types (STRING, INTEGER, FLOAT, BOOLEAN)
- [x] Type Checking (at runtime)
- [x] I/O Operations (OUTPUT, INPUT)
- [x] Arithmetic Operations
- [x] Conditional Statements (IF, ELSE)
- [x] Loops (FOR, WHILE, REPEAT-UNTIL)
- [x] Modules (Functions and Procedures)

The features that are either in development or are yet to be implemented are:

- [ ] Formatting support for `OUTPUT`
- [ ] Record Data Type
- [ ] File I/O
- [ ] 1D and 2D Arrays

## Installation and Usage
Python 3.8 or a higher version is required for using this language.

**1. Clone the repository**

If you have Git installed, simply use the following command:

```
$ git clone https://github.com/izxxr/pspl.git
```

If Git is not installed, use the `Code` button on GitHub to download the source code. Extract the downloaded ZIP file.

**2. Open terminal in the downloaded directory.**

Open Command Prompt or any preferred terminal in the downloaded folder. If you
cloned using `git` in step 1, use the following command to enter downloaded directory:

```
$ cd pspl
```

**3. Write PSPL code.**

Create a `main.pspl` file and write the PSPL code in this file.

- main.pspl:

```
DECLARE Name : STRING

INPUT "Enter your name: ", Name
OUTPUT "Hello, " + Name
```

**4. Run the code.**

Use the following command to run the code.

```
$ python -m pspl main.pspl
```

In some cases, you might need to use `python3` instead of `python`.

## Documentation
A basic program with simple I/O operations is shown below:

```
DECLARE A : INTEGER
DECLARE B : INTEGER
DECLARE C : INTEGER

INPUT "Number 1: ", A
INPUT "Number 2: ", B
C <- A + B

OUTPUT "Sum: " + C
```

Some basics of the languages that can be illustrated from above code are:

- `DECLARE` is used to define the type of a variable. PSPL provides type checking at runtime.
- `INPUT` is used for reading user input.
- `OUTPUT` is used to print a message.
- `<-` is used for assignment (instead of conventional `=`)

### Identifier names
Variable and function names follow the conventional identifier name rules:

1. Can contain alphanumeric characters and underscores only.
2. Cannot start with a number.

### Variables
Variables are assigned with `<-` operator rather than conventional `=` operator. This design
choice is due to use of arrow symbol in pseudocode for assignment.

Example:
```
Age <- 20
```

### Constants
Constants are identifiers that cannot be modified after initial definition. In order to define
a constant, the `CONSTANT` keyword statement.

Note that instead of `<-`, `=` is used for assigning constant values.
```
CONSTANT Pi = 3.14
CONSTANT g = 9.81
```

If we try to modify a constant, an error is raised:
```
g <- 0

At line 3, column 1, index 25:
IdentifierAlreadyDefined: Identifier 'g' has already been defined as constant
```

### Data Types
There are currently four primitive data types:

- STRING - for textual data, wrapped in quotes
- INTEGER - for whole numbers
- FLOAT - for floating point numbers
- BOOLEAN - for `TRUE`/`FALSE` values

The `DECLARE` statement is used for declaring types of variables.

Example:
```
DECLARE A : INTEGER
```

PSPL provides type checking at runtime. This means `A` can only be assigned an integer
otherwise an error is raised.

When variables are created without any explicit declaration, the type of variable is inferred
from the type of value assigned initially.

### Arithmetic Expressions
Arithmetic expressions contain mathematical operations between integers or floating point numbers.

Available arithmetic operators are `+` (addition), `-` (subtract), `*` (multiply) and `/` (divide).

Example:
```
A <- 20 + 1
B <- (4 + 2) / (3 * 2)
```

### Logical Expressions
Logical expressions return `TRUE` or `FALSE` as result.

Following are available boolean operators:'

- `=` (Equal To)
- `<>` (Not Equal To)
- `>` & `>=`
- `<` & `<=`

Example:
```
A <- 5
OUTPUT A > 1
```

Outputs `TRUE`

### I/O operations
`OUTPUT` statement is used for printing an expression to the console. e.g `OUTPUT "Hello World"`

`INPUT` statement can be used to take user input. This statement either takes a single 
operand, the identifier to store the input in or two operands with first one being the
prompt to show for input and second one as identifier.

If the type of identifier provided has been declared before, it is used for implicit conversion of
input to that type. For example:

```
DECLARE A : INTEGER
INPUT A
```

Upon running above program, input will be prompted until user gives a valid integer and
`A` will be implicity converted to integer. For booleans, case insensitive `true` or `1`
input accounts for `TRUE` and vice versa.

## Conditional Statements
Following conditional clauses are supported:

- `IF`-`ENDIF`
- `IF`-`ELSE`-`ENDIF`

Example:
```
DECLARE Age : INTEGER
INPUT "Age: ", Age

IF Age >= 18 THEN
    OUTPUT "You can drive."
ELSE
    OUTPUT "You cannot drive."
ENDIF
```

## Loops
There are three different types of loops:

- `FOR` (count-controlled) loop
- `WHILE` (pre-condition) loop
- `REPEAT`-`UNTIL` (post-condition) loop

### FOR loop
A for loop is used to iterate through a specific range. The basic syntax is
shown in example below:

```
FOR A <- 1 TO 5
    OUTPUT A
ENDFOR
```

Above code will print numbers from 1 to 5 inclusive.

Additionally, a `STEP` can be added to increment or decrement numbers. For example,
to print the above set of numbers in reverse order:

```
FOR A <- 5 TO 1 STEP -1
    OUTPUT A
ENDFOR
```

`STEP` defaults to `1`.

### WHILE loop
`WHILE` loop is used to run a block of code until a condition is `TRUE`.

Example of taking inputs until user does not enter the number `123`:

```
DECLARE Num : INTEGER
Num <- 0

WHILE Num <> 123 DO
    INPUT Num
ENDWHILE
```

### REPEAT-UNTIL loop
A repeat until loop is similar to while loop except that the condition is written
after the loop body and loop body is executed at least once even if the condition
is not true.

Example:
```
DECLARE Num : INTEGER
Num <- 123

REPEAT
    INPUT Num
UNTIL Num <> 123
```
In above example, despite `Num` already being `123`, the loop body still executes once.

### Procedures
Procedures are modules that are similar to functions but do not `RETURN` anything.

`CALL` is used for calling procedures.

```
PROCEDURE SayHello
    OUTPUT "Hello World"
ENDPROCEDURE

CALL SayHello
```

Procedures also take parameters:

```
PROCEDURE SayHello (N : INTEGER, Cool : BOOLEAN)
    IF Cool THEN
        Message <- "Howdy World"
    ELSE
        Message <- "Hello World"

    FOR Index <- 1 TO N
        OUTPUT Message
    ENDFOR
ENDPROCEDURE

CALL SayHello (5, TRUE)
```

Output:

```
Howdy World
Howdy World
Howdy World
Howdy World
Howdy World
```

## Contributing to PSPL
Pull requests and issues are welcome. Please ensure that you follow the general guidelines:

- Provide description that includes every information related to the issue. Include:
    - Minimal reproduction code for a bug.
    - System information if applicable.
    - Explanation of the issue.

- When opening pull requests:
    - Follow PEP-8 standard guidelines for code style.
    - Test the changes or if not, mention that the changes could not be tested.
    - Use descriptive commit messages.
    - Type check the code.
