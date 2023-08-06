'''
DESCRIPTION:
    This module is always available.
	It provides access to input validation functions.

'''
def input_check_float(a: str = 'Enter value: ') -> float:
    '''Returns the converted input string to float.
		Otherwise, it returns a warning and repeats input.'''

    string = input(f'{a}')
    try:
        return float(string)
    except:
        print('You entered invalid type. (must be int)')
        return input_check_float(a)

def input_check_int(a: str = 'Enter value: ') -> int:
    '''Returns the converted input string to int.
		Otherwise, it returns a warning and repeats input.'''

    string = input(f'{a}')
    try:
        if int(string) == float(string):
            return int(string)
    except:
        print('You entered invalid type. (must be int)')
        return input_check_int(a)
