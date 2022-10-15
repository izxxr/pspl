# PSPL
**P**seudocode **S**tyled **P**rogramming **L**anguage is a simple and experimental programming language heavily inspired from [CIE styled pseudocode](https://pdfcoffee.com/9618-pseudocode-guide-for-teachers-for-examination-from-2021-pdf-free.html).

## Background Information
This language is just an experimental and fun side project that can be used to evaluate
simple pseudocode. While it currently does not support all the features of pseudocode from
CIE specification and misses many basic features, it currently supports the following set
of features:

- Variables
- Some primitive data types
    - STRING
    - INTEGER
    - BOOLEAN
- Arithmetic Expressions
- Boolean Expressions
- Basic I/O operations
- Simple conditional statements
- Basic for loop

Following features are planned for the near future:

- More data types (e.g FLOAT)
- Further support for selection statements
- Further support for loops
- Procedures and Functions
- Record Type
- File I/O
- Basic data structures (1D/2D Arrays)

**Important Note!** This is purely an experimental language that follows the vague rules
of pseudocode. Many patterns in this language might not seem conventional (such as type
validation in `INPUT` statement) so bear with it.

## Installing and Usage
PSPL can be installed by simply cloning this repository. It is recommended to use Python 3.8
or a higher version.

Once cloned, simply use `python -m pspl <filename>` command in the cloned directory to
execute the file.
```
$ git clone https://github.com/nerdguyahmad/pspl.git
$ cd pspl
$ python -m pspl test.pspl
```

## Overview
Following is the basic overview of this language:

- PSPL is a dynamic language. There is no type validation at runtime. PSPL provides a `DECLARE` statement for declaring types of variables but that merely exists for compatiblity
with pseudocode.
- `OUTPUT` and `INPUT` statements are used for writing to console and taking input respectively. For more information on their syntax, see the relevant section in documentation below.
- Variables are assigned with `<-` operator rather than conventional `=` operator. This design choice is also directly derived from pseudocode syntax. `=` operator is used for equality expressions.
- The rules for identifier name are traditional. No starting with numbers, only alphanumeric characters are allowed.

A basic program with simple I/O operations is below, note that `DECLARE` statements
are not required for variables that are not used in an `INPUT` statement (`INPUT` converts
the input data to declared data type) so the third line here is not required:
```
DECLARE n1 : INTEGER
DECLARE n2 : INTEGER
DECLARE result : INTEGER

INPUT "Number 1: ", n1
INPUT "Number 2: ", n2
result <- n1 + n2

OUTPUT "Sum: " + result
```

## Documentation
The following is the basic documentation of PSPL.

### Identifier names
- Identifier names can contain alphanumeric characters and underscores only.
- The name cannot start with a number.

### Variables
Variables are assigned with `<-` operator rather than conventional `=` operator. This design 
choice is also directly derived from pseudocode syntax.

Example:
```
a <- 1
b <- 1
c <- a + b
```

### Data Types and Declaration
There are currently three primitive data types:

- String
- Integer
- Boolean

PSPL being a dynamic language does not provide type validation at runtime so there is no
real use of declaring types except type conversion in `INPUT` statement (see it's documentation) for more information.

The `DECLARE` statement is used for declaring types.

Example:
```
DECLARE a : INTEGER
```
Note that attempting to use `a` will still result in an `IdentifierNotDefined`.

### Strings
Strings are well... just, strings. In order to represent a string literal, the data
must be wrapped in double or single quotes.

Two strings can be concatenated to form a single string with data of both strings.

### Integers
Integers are simple numbers that support arithmetic operations. Nothing special.

#### Booleans
There are two boolean literals, `TRUE` and `FALSE` of course. Boolean expressions
also return a boolean.

### Arithmetic Expressions
Arithmetic expressions contain mathematical operations between integers.

Following are available arithmetic operators:
- `+`
- `-`
- `*`
- `/`

Example:
```
a <- 1 + 1
b <- (4+2) / 3 * 2
```

### Boolean Expressions
Boolean expressions return a boolean (TRUE or FALSE) as result.

Following are available boolean operators:
- `=` (Equal)
- `<>` (Not Equal)
- `>` & `>`
- `<` & `<=`


Example:
```
a <- 5
OUTPUT a > 1
```
Outputs `TRUE`.

### Basic I/O operations
`OUTPUT` statement is used for printing an expression to the console. e.g `OUTPUT "Hello World"`. It takes

`INPUT` statement can be used to take user input. This statement either takes a single 
operand, the identifier to store the input in or two operands with first one being the
prompt to show for input and second one as identifier.

It is worth noting that if the type of identifier provided has been declared before, that
type is used for implicit conversion of input. For example:
```
DECLARE a : INTEGER
INPUT a
```
Upon running above program, input will be prompted until user gives a valid integer and
`a` will be implicity converted to integer. For booleans, case insensitive `true` or `1`
input accounts for `TRUE` and vice versa.

## Conditionals
`IF` is the only type of conditional statements currently supported. The clause must be
terminated with an `ENDIF`.

Note that `ELSE IF` is not supported yet. Instead, consider using `IF` inside an `ELSE`
block.

Example:
```
DECLARE age : INTEGER
INPUT "Age: ", age

IF age >= 18 THEN
    OUTPUT "You can drive."
ELSE
    OUTPUT "You cannot drive."
ENDIF
```

## Loops
Currently, only a `FOR` loop is supported.

### FOR loop
A for loop is used to iterate through a specific range. The basic syntax is
shown in example below:
```
FOR a <- 1 TO 5
    OUTPUT a
ENDFOR
```
Additionally, a `STEP` can be added to increment or decrement numbers. For example,
to print the above set of numbers in reverse order:
```
FOR a <- 5 TO 1 STEP -1
    OUTPUT a
ENDFOR
```
`STEP` defaults to `1`.

## Contributing to PSPL
PSPL is an experimental and fun side project so I doubt if I will ever be seriously 
maintaining this so the chances of accepting major changes are really thin. Nonetheless,
I will rarely be accepting pull requests that implements a new feature however bug reports
and fixes are welcome.
