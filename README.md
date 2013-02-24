pylogic
=======

Python Module for Logical Validation (forked from Rob Truxler library)

Original Author
===============

Rob Truxler (http://rob.truxler.com)

License
=======

* Source code: LGPL
* Documentation: Commons Attribution 3.0 Unported License.

Description
===========

A python module for validation of propositional and first-order logic
statements.

Simple software verification can be achieved through use of this module. A basic
scenario is when you wish to confirm that some state is achieved after running a
block of code.  Typically this is done through unit tests. The trouble with unit
tests is that they require much effort to set up and typically only test as many
cases as the programmer's time can afford. Unit tests can be augmented with a
simple model that enumerates a representative set of inputs so that a logical
statement can be validated with a single call to logic.validate() or
Context.validate().

The simplest use of the logic module is to check the validity of propositional
logic statements. To evaluate propositional logic statements, see
logic.validate() or Context.validate(). Truth tables can also be printed with
Context.printTruthTable().

Unless you're testing very simple conditions and testing your logic, you
probably want to use first-order logic so that you can specify sets, define
relationships (between objects in a domain), and test using quantifiers (that a
statement is true for at least one object in the domain, or all objects).
Statements are verified by use of the Context.validate() function. A domain of
objects can be set on the context with Context.setTermDomain(), which takes a
list.

Predicate functions can be defined either implicitly or explicitly. Implicit
predicate functions are defined through a call to Context.assume(sentence) or
Context.assumePredicate(predicate). Context.assume(sentence) will infer which
predicate invocations must be true in order to make sentence true.
Context.assumePredicate(predicate) will tell the logic engine that predicate is
necessarily true without requiring inferencing. Using this method leads to more
optimal performance in the validate() function. Finally Python functions can be
used to define predicate functions. You can tell a Context to use a Python
function by passing the function in as an argument to
Context.setPredicateFunction(function, arity).

For further documentation see individual function documentation or
logic_examples.py

Note: logic_examples.py is simply a self-documenting Python module full of example usage. It is not
a necessary file for use of logic.py, but it should provide ample examples that can be copied
and modified.

Install
=======

To install pylogic:


```shell
#exec as root
./setup.py install
```

It will install logic.py, yacc.py and lex.py in pylogic module.

Usage
=====

Api Documentation
-----------------

Examples
--------
