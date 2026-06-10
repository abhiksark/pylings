# Decorators

Source: https://docs.python.org/3/reference/compound_stmts.html#function-definitions

This local reference is generated from the official Python documentation and trimmed for pythonlings.

Decorators wrap or transform functions and classes with `@decorator` syntax.

## Extracted reference

8.7. Function definitions

A function definition defines a user-defined function object (see section
The standard type hierarchy):

```python

funcdef: [decorators] "def" funcname [type_params] "(" [parameter_list] ")"
["->" expression] ":" suite
decorators: decorator+
decorator: "@" assignment_expression NEWLINE
parameter_list: defparameter ("," defparameter)* "," "/" ["," [parameter_list_no_posonly]]
| parameter_list_no_posonly
parameter_list_no_posonly: defparameter ("," defparameter)* ["," [parameter_list_starargs]]
| parameter_list_starargs
parameter_list_starargs: "*" [star_parameter] ("," defparameter)* ["," [parameter_star_kwargs]]
| "*" ("," defparameter)+ ["," [parameter_star_kwargs]]
| parameter_star_kwargs
parameter_star_kwargs: "**" parameter [","]
parameter: identifier [":" expression]
star_parameter: identifier [":" ["*"] expression]
defparameter: parameter ["=" expression]
funcname: identifier

```
