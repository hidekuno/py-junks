#!/usr/bin/env python
#
# This is a personal tool what I need for my working.
#
# hidekuno@gmail.com
#
import sys
import argparse
DELIMITER_CHAR = '.'

class Tree(object):
    def __init__(self, cname, delimiter, parent = None):
        self.cname = cname
        self.sep = delimiter
        self.parent = parent
        self.children = []

    def add(self, child):
        self.children.append(child)

    def accept(self, visitor):
        visitor.visit(self)

    def short_name(self):
        return self.cname[self.cname.rfind(self.sep) + 1:]

class Visitor(object) :
    def __init__(self):
        pass

    def visit(self, tree, indent = 0):
        print((indent * "  ") + tree.short_name())

        for c in tree.children:
            self.visit(c, indent + 1)

class RuledLine(object):
    def __init__(self,p1,p2,m1,m2):
        self.p1 = p1
        self.p2 = p2
        self.m1 = m1
        self.m2 = m2

    def visit(self, tree):

        if (tree.parent):
            p = tree.parent
            horizon = []
            while p.parent:
                horizon.append(self.p1 if p.parent.children[-1] == p else self.p2)
                p = p.parent

            horizon.reverse()
            horizon.append(self.m1 if tree.parent.children[-1] == tree else self.m2)
            sys.stdout.write("".join(horizon))

        print(tree.short_name())
        for c in tree.children:
            self.visit(c)

def create_tree_ordered(istream, delimiter):
    cache = {}
    top = None

    for line in istream:
        rec = line.rstrip()
        parent_name = rec[:rec.rfind(delimiter)]
        if parent_name in cache:
            cache[rec] = Tree(rec, delimiter,cache[parent_name])
            cache[parent_name].add(cache[rec] )
        else:
            cache[rec] = Tree(rec, delimiter)
            top = cache[rec]

    return top

def create_tree(istream, delimiter):
    cache = {}
    top = None

    for line in istream:
        rec = line.rstrip()

        items = ""
        for c in rec.split(delimiter):
            if items:
                items  = items + delimiter + c
            else:
                items  = c

            if items in cache:
                continue

            parent_name = items[:items.rfind(delimiter)]

            if parent_name in cache:
                cache[items] = Tree(items, delimiter, cache[parent_name])
                cache[parent_name].add(cache[items])
            else:
                cache[items] = Tree(items, delimiter)
                top = cache[items]
    return top

if __name__ == "__main__":
    delimiter = DELIMITER_CHAR

    parser = argparse.ArgumentParser()
    parser.add_argument('-l','--line',  action='store_true')
    parser.add_argument('-b','--bline', action='store_true')
    parser.add_argument('-m','--mline', action='store_true')
    parser.add_argument('-o','--order', action='store_true')
    parser.add_argument('-d','--delimiter', type=str, dest='delimiter')
    parser.add_argument('-f', '--filename', type=str, dest='filename')
    args = parser.parse_args(sys.argv[1:])

    create_tree_impl = create_tree
    visitor = Visitor()
    istream = sys.stdin

    if args.line:
        visitor = RuledLine("    ","|   ", "`-- " ,"|-- " )
    if args.bline:
        visitor = RuledLine("　　 " ,"┃　 ", "┗━━ "  ,"┣━━ " )
    if args.mline:
        visitor = RuledLine("　　 " ,"│　 ", "└── " , "├── " )
    if args.order:
        create_tree_impl = create_tree_ordered
    if args.filename:
        try:
            istream = open(args.filename, "r")
        except FileNotFoundError as e:
            print("No such file or directory: " +  args.filename)
            sys.exit(1)
    if args.delimiter:
        delimiter = args.delimiter

    top = create_tree_impl(istream, delimiter)
    top.accept(visitor)
