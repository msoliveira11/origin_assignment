# origin_assignment
Repository meant to store the resolution of Original Backend Take Home Assignment.

(0.1) Language utilized and some decision-why's.

This solution was implemented using Python3 (more specifically Python 3.8.10).
Python was chosen due to specification "wish", by having built-in
support for dealing with JSON objects and also by being a programmer-friendly
language allowing the creation of projects in a short time.

The OS utilized was Ubuntu 20.04.

I have chosen the "class" approach to keep the methods binded togheter,
letting them reach common data easily. It also allows to someone extend
this class for a different purpose, if needed.

(0.2) File descriptions.

- "README.md" -> This file.
- "problem_specifications.txt" -> Contains the main guidelines and business
rules to develop the solution as requested.
- "risk_calc_engine.py" -> Contains the application's core code. It contains
the classe responsible for the risk insurance calculations according to the
rules described in the previous file.
- "run_tests.py" -> Test script containing the test cases. The procedure tests
the code and verifies if the answers are correct. It also generates a concise
report regarding if the tests were executed successfully.
- "calc_interface.py" -> Interface to expose the functionalities of "risk_calc_engine.py"
without instatiang any class.

(1) How to run:

If you are working in a Linux environment, you may run the test script "run_tests.py"
via terminal using the following command:
$ ./run_tests.py
If it fails to execute, please check if you have permission to execute. If not, please run:
$ chmod +x run_tests.py
Or run using this command:
python3 run_tests.py

You may also call this script through your Python3 interpreter:
$ python3
>>> import run_tests
>>> run_tests.main()

If you wish to import the code to your own application, you may:
- Import the calculation class. Please check "calc_interface.py" lines 12 and 15
to see an example.
- Import the interface file. Please check "run_tests.py" lines 11 and 110
to see an example.

