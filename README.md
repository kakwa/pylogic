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

## Propositional Logic  ##

Propositional logic statements can be validated using logic.py, meaning their truth can be easily computed and returned as a Python bool. Depending on the situation, the user may wish to test that a logical statement is true for all valuations of all possible atoms (ie. that the statement is a tautology), that it is true for at least one valuation (ie. that the statement is satisfiable), or in cases where the statement is not a tautology, to print out a truth table showing the valuations that make the statement false.

## Grammar  ##

All public functions take a string as an argument that defines the statement to be validated. This logic string must conform to the syntax specified by logic.py. The grammar is designed in such a way to make logical statements simple to construct and easy to read. For this reason propositional atoms are allowed to be any string that begins with a [ and ends with a ].

The full grammar for propositional logic is specified by the following table: 

```
<atom>      ::= [any string in these brackets]   
   <formula>    ::= <formula> implies <formula>                 
            | <formula> therefore <formula>                 
            | <formula> or <formula>                 
            | <formula> and <formula>                 
            | not <formula>                 
            | {<formula>}                    
            | <atom> 
```
As with the usual precedence rules of propositional logic, the order of operations is not, and, or, implies, where therefore is synonymous with implies and is added as syntactic sugar to aid readability of logical sentences that would include the symbol `.

We can translate a traditional logical statement to our more human and machine-friendly syntax:




```
not [P] implies {[R] and [Q]} therefore [R] or [P]
```

## logic.validate() ##

The logic.validate() method is used to evaluate a string that represents a logical statement specifies in the above syntax. This function can be called directly from the logic module without instantiating any class objects. 

logic.validate() takes a string as an argument and returns a Python bool that is True if the logical statement is a tautology (meaning all possible valuations of propositional atoms lead to the statement being true), and False otherwise.

## logic.satisfiable() ##

Unlike logic.validate(), logic.satisfiable() returns True if there is at least one valuation of the propositional atoms in the logical statement that lead to the statement being true. This method returns a bool, so in order to determine details about the valuation for the atoms that led to this statement’s truth, you must call Context.printTruthTable().

## The Context Object ##

The Context object contains the state information that gets created in setting up or evaluating a logical statement. It also provides further control. With the Context object you can do perform two additional functions: printing a truth table, and specifing assumptions before calling validate().

The Context object is created with the one line call:

```python
c = logic.Context()
```

At this point you can print a truth table, which will simply produce a column for each propositional atom and one for the formula that the user passes in as an argument. It will not produce columns for any sub-formulas. As an optional second argument, the printTruthTable() function will take a string that will serve as the column separator in the printed output. By default this separator is a tab character.

```python
c = logic.Context()
c.printTruthTable("[P] and [Q] or [P] and [Q]", ",")


# This prints out the following:


# Q,P,{{{[P] and [Q]} or [P]} and [Q]}
# False,False,False
# True,False,False
# False,True,False
# True,True,True
```

The Context object will also accept a number of logical formulas as assumptions against which subsequent calls to validate() will be evaluated. For example, the statement:


```python
{{{[P] and [Q]} and [R]} and {[S] and [T]}} implies {[Q] and [S]}
```

can be simplified with the use of assumptions:


```
import logic
context = logic.Context()
context.assume("[P] and [Q] and [R]")
context.assume("[S] and [T]")
print str(context.validate("[Q] and [S]"))
# prints out "True"
```

With the last call to context.validate(), the Context object will reconstruct the longer sentence that includes the implication out of all of the assumptions that it knows about. In other words, all assumptions are composed in a conjunction. The formula in the validate() method will then be combined with an implication, and the resulting formula will be evaluated, with its truth being returned by validate().

Examples
--------
