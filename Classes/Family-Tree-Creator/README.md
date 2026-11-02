# Family Tree Creator

**Category:** Classes

## Problem

Create a class called Person which will have a name, when they were born and when (and if) they died. Allow the user to create these Person classes and put them into a family tree structure. Print out the tree to the screen.

## Solution

`Person` stores name, birth/death years and bidirectional parent/child links; `FamilyTree` renders the descendants recursively with box-drawing prefixes, computes ancestors iteratively, and classifies relationships by identity (parent, child, sibling, ancestor, descendant, unrelated).

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --demo
```

## Example

```text
Ada Sr. 1930-2005
  └─ Grace b. 1955
    └─ Katherine b. 1980
      └─ Ada Jr. b. 2010
    └─ Tim b. 1983
  └─ Alan b. 1957
Katherine -> Ada Sr.: descendant
Grace and Alan: sibling
ancestors of Ada Jr.: Katherine, Grace, Ada Sr.
```
