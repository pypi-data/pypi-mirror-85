#!/usr/bin/env python
# -*-coding:utf-8-*-

from ..exceptions import OutOfChoiceError

def radix_conversion(number, output_radix, input_radix=None):
    """
    number radix conversion.
    number+input_radix: if given number is a string, then you must give the input_radix parameter.
    the radix support input: ['bin', 'oct', 'dec', 'hex', 2, 8, 10, 16]

>>> radix_conversion(10, 'bin')
'1010'
>>> radix_conversion('0xff', 2, 16)
'11111111'
>>> radix_conversion(0o77, 'hex')
'3f'
>>> radix_conversion(100, 10)
'100'
>>> radix_conversion(100,1)
Traceback (most recent call last):
......
my_python_module.exceptions.OutOfChoiceError: radix is out of choice.

    """
    name_map = {'bin': 2, 'oct': 8, 'dec': 10, 'hex': 16}

    for index, radix in enumerate([input_radix, output_radix]):
        if radix is None:
            continue

        if radix not in ['bin', 'oct', 'dec', 'hex', 2, 8, 10, 16]:
            raise OutOfChoiceError("radix is out of choice.")

        if radix in name_map.keys():
            if index == 0:
                input_radix = name_map[radix]
            elif index == 1:
                output_radix = name_map[radix]

    if isinstance(number, str) and input_radix:
        number = int(number, input_radix)

    if output_radix == 2:
        return f'{number:b}'
    elif output_radix == 8:
        return f'{number:o}'
    elif output_radix == 10:
        return f'{number:d}'
    elif output_radix == 16:
        return f'{number:x}'


