Help on built-in module CheckInputs:

NAME
    CheckInputs
	
DESCRIPTION
	This module is always available.
	It provides access to input validation functions.

FUNCTIONS
    input_check_float(...)
        type of arg:
		
		Example:
		input_check_float('Enter number: ')
        
		Returns the converted input('Enter number: ') string to float.
		Otherwise, it returns a warning and repeats input('Enter number: ').
		
	input_check_int(...)
        type of arg: str
		
		Example:
		input_check_float('Enter number: ')
        
		Returns the converted input('Enter number: ') string to int.
		Otherwise, it returns a warning and repeats input('Enter number: ').