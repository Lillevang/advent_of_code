# Part 2 explained

The code reads descriptions of wires and gates from the input file, constructs a network of logic gates, then checks each gate against specific criteria to identify “suspicious” ones.
We doen’t simulate the logic flow in a typical sense. Instead, I “validate” or “flag” certain gates based on naming rules (like prefixes “x”, “y”, “z”, or the substring “00”) and the operators used (“AND”, “XOR”, “OR”).
Finally, it collects the outputs of any gates meeting those suspicious criteria, sorts them, and prints them in a comma-separated list.
