'''
Created on Mar 12, 2011

This rather lengthy Python program provides numerous examples of how to use the
logic.py module.

@author: rob
'''


### LOGICAL EXAMPLES ###

### YOU MUST IMPORT THE LOGIC MODULE FIRST ###
import logic

def computeAndPrintResult(sentence):
    print sentence + " is " + str(logic.validate(sentence)) + "\n"
    
def computeResultInContext(context,sentence, printTruthTable=False):
    print sentence + " is " + str(context.validate(sentence,printTruthTable)) + "\n"

### EVALUATE SIMPLE PROPOSITIONAL LOGIC FORMULAS ###

# Given a sentence that is obviously true, compute its truth:
print "Validate a rather simple sentence that is obviously true:"
computeAndPrintResult("[P] or not [P]")

# Given a sentence that is obviously false, compute its truth:
print "Validate a rather simple sentence that is obviously false:"
computeAndPrintResult("[P] and not [P]")

# In homework 1 we had to prove a number of logical validities
# Question 2:
# Assume (P and Q) and R, S and T, therefore Q and S
print "Homework 1, Question 2a: Assume (P and Q) and R, S and T, therefore Q and S"
computeAndPrintResult("{{{[P] and [Q]} and [R]} and {[S] and [T]}} implies {[Q] and [S]}")

print "Rewrite the previous problem as assumptions with run-time assertion checking."
c = logic.Context()
c.assume("{[P] and [Q]} and [R]")
c.assume("[S] and [T]")
print "Calling it this way allows you to specify whether you want to print out a truth table:"
print "Is it true? " + str(c.validate("[Q] and [S]",True)) + "\n"

print "Another example of run-time assertion checking, this time with readable logical atoms:"
c = logic.Context()
c.assume("[b is a baseball] implies {[b is a ball] and [b is white]}")
c.assume("[b is a baseball]")
print str(c.validate("[b is white]", True)) + "\n"

# another example from homework 1, this time question 3.b.
print "Question 3b from homework 1; this time using the therefore operator"
computeAndPrintResult("not [P] or not [Q] therefore not {[P] and [Q]}")

##### FIRST-ORDER LOGIC AND MODEL CHECKING #####
c = logic.Context()
c.setTermDomain(["apple", "banana", "carrot"])
# specify a situation that implicitly provides the terms which make the R predicate true
c.assume("[is a fruit(apple)] and [is a fruit(banana)]")
# check that our model definition, though implicitly defined through an assumption, is true
computeResultInContext(c,"[is a fruit(apple)] or [is a fruit(banana)] or [is a fruit(carrot)]")
print "Let's get the truth table for this to see what's going on:"
# print a truth table with a colon as a separator
c.printTruthTable("[is a fruit(apple)] or [is a fruit(banana)] or [is a fruit(carrot)]",";")
print "As can be seen, the first-order predicate function checking that is implemented uses a modified"
print "logical sentence that includes all of the terms that make the model true in an implication.\n"

### USE FIRST-ORDER QUANTIFIERS ###
print "Given this model of fruits and vegetables, can we verify that there exists a fruit?"
computeResultInContext(c,"exists food [is a fruit(food)]")
print "Let's verify also that there is one food item that is not a fruit"
computeResultInContext(c,"exists food [is a fruit(food)] and exists food {not [is a fruit(food)]}")

print "Let's see if every food item in the model is a fruit"
computeResultInContext(c,"all food [is a fruit(food)]")

print "Let's now define a new predicate function 'is crunchy'"
c.assume("[is crunchy(apple)]")
c.assume("[is crunchy(carrot)]")

print "Are all crunchy foods also fruits?"
computeResultInContext(c,"all food {[is crunchy(food)] implies [is a fruit(food)]}",True)

### THIS IS ALL GREAT, PREDICATES AND QUANTIFIERS... BUT WHY STILL COMPUTE EVERY TRUTH ROW ?? ###
# Well, as described above, each truth row is still computed because there's no requirement
# that the user enter just predicate instances in the c.assume() method. Technically these are
# treated like any other WFF, although they may represent a single predicate, a conjunction of predicates
# or even some other first-order logical statement that informs the model.
#
# But what if you'd like to get an answer more efficiently? You know you only care about cases
# where the predicates ARE true. For this reason, the logic module supports defining the model
# more explicitly. This can be done in two ways. 
#
# The first way is to tell the context exactly which terms make a predicate true: 
# c.assumePredicate("[is crunchy(carrot)]")
# c.assumePredicate("[is crunchy(apple)]")
# Defining the predicate-term combinations like this tell the context that when you validate, you
# only wish to consider cases where these predicate values are true. This leads to an optimization
# in execution time.
print "Notice in the last computation, only the last row of the truth table determined the "
print "truth of the statement. Using c.assumePredicate() will optimize the computation to " 
print "only consider rows where all the predicate-function assignments make the predicate true."

c = logic.Context()

c.setTermDomain(["apple", "banana", "carrot"])

c.assumePredicate("is a fruit(apple)")
c.assumePredicate("is a fruit(banana)")
c.assumePredicate("is crunchy(apple)")
c.assumePredicate("is crunchy(carrot)")

computeResultInContext(c,"all food {[is crunchy(food)] implies [is a fruit(food)]}",True)

# This can get quite tedious if you're trying to define a pretty complex model, or even
# a simple one that just has many more values in the domain. It may be easier to just
# define a function that represents your predicate function.

print "Consider if I now have an integer domain including all integers from 0 to 20 inclusive."

c = logic.Context()

# define the domain using a Python convenience, the range function
c.setTermDomain(range(21))

# define the equal predicate function
# notice here that you have to cast every argument as an int
# this is because the logic module may cast all terms to strings
def equal(x,y):
    return (int(x) == int(y))

# define a second predicate function that determines if the sum of two
# numbers is greater than 39
def sum_greater_than_39(x,y):
    return (int(x)+int(y)) > 39

# register both predicate functions with the context. For each, give
# the arity (the number of arguments). Optionally, provide as a third argument
# the predicate name that this function should define. If not provided, the
# function's name will be taken.
c.setPredicateFunction(equal, 2)
c.setPredicateFunction(sum_greater_than_39,2)

print "Let's check something simple"
computeResultInContext(c, "exists x [sum_greater_than_39(x,20)]")
print "To show that it respects domain boundaries..."
computeResultInContext(c, "exists x [sum_greater_than_39(19,x)]")

print "And to show that we can do something a little more complicated"
print "without the use of a literal..."
#s = "exists x [sum_greater_than_39(x,3)]"
#print s + "? " + str(c.validate(s))
## now check if there is an x and y where x is not y, but x + y is greater than 39
computeResultInContext(c, "exists x {exists y {not [equal(x,y)] and [sum_greater_than_39(x,y)]}}")
computeResultInContext(c, "all x {all y{[sum_greater_than_39(x,y)] implies [equal(x,y)]}}")
#print s + "? " + str(c.validate(s,False))

#### LET'S GAIN SOME CONFIDENCE IN A QUICKSORT IMPLEMENTATION ####
# quick sort implementation taken from hetland.org, May 4, 2011
# http://hetland.org/coding/python/quicksort.html

def partition(list, start, end):
    pivot = list[end]                          # Partition around the last value
    bottom = start-1                           # Start outside the area to be partitioned
    top = end                                  # Ditto

    done = 0
    while not done:                            # Until all elements are partitioned...

        while not done:                        # Until we find an out of place element...
            bottom = bottom+1                  # ... move the bottom up.

            if bottom == top:                  # If we hit the top...
                done = 1                       # ... we are done.
                break

            if list[bottom] > pivot:           # Is the bottom out of place?
                list[top] = list[bottom]       # Then put it at the top...
                break                          # ... and start searching from the top.

        while not done:                        # Until we find an out of place element...
            top = top-1                        # ... move the top down.
            
            if top == bottom:                  # If we hit the bottom...
                done = 1                       # ... we are done.
                break

            if list[top] < pivot:              # Is the top out of place?
                list[bottom] = list[top]       # Then put it at the bottom...
                break                          # ...and start searching from the bottom.

    list[top] = pivot                          # Put the pivot in its place.
    return top                                 # Return the split point


def quicksort(list, start, end):
    if start < end:                            # If there are two or more elements...
        split = partition(list, start, end)    # ... partition the sublist...
        quicksort(list, start, split-1)        # ... and sort both halves.
        quicksort(list, split+1, end)
    else:
        return

def shuffle(list):
    import random
    numSwaps = len(list)
    for i in range(numSwaps):
        # perform a swap
        idx1 = random.randrange(0,len(list))
        idx2 = random.randrange(0,len(list))
        temp = list[idx1]
        list[idx1] = list[idx2]
        list[idx2] = temp

print "Define some predicates to aid in evaluation of quicksort's effectiveness:"
print "define greater than:"

list = range(21)
c = logic.Context()
c.setTermDomain(list)

def greaterThan(x, y):
    return int(x) > int(y)

print "define adjacency predicate"
def follows(x,y):
    return list.index(int(x)) == list.index(int(y))+1

c.setPredicateFunction(greaterThan, 2)
c.setPredicateFunction(follows,2)

print "Our list is a the ordered list from 0 to 20. Let's test that our shuffle worked"
shuffle(list)
print "Verify that at least one element is out of order after shuffling"
computeResultInContext(c, "exists x {exists y{not [greaterThan(x,y)] and [follows(x,y)]}}")
quicksort(list,0,len(list)-1)
print "We've sorted .. let's verify that every element is in order"
## THE CONTEXT HAS CHANGED A BIT ... SINCE THE LIST HAS CHANGED WE NEED TO RESET THE DOMAIN
# the context will remember which predicates returned with what values
# since our predicates will behave differently now that the domain has
# been sorted, let's forget the cached values
c.forgetPredicateInvocations()
computeResultInContext(c, "all x all y [follows(x,y)] implies [greaterThan(x,y)]")
