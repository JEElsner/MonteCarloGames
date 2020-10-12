'''
Provides the vectorize() function to make objects work with NumPy universal
functions.
'''

import numpy as np


def vectorize(t):
    '''
    Copies object methods in class t and adds NumPy universal functions to the
    class.

    Creates static v_funcs with the name v_[method name] for each object method
    in class t.

    Arguments:

        t       the type to create v_funcs off of

    Returns:
        True if the object was vectorized
        False otherwise, even if the object was previously vectorized
    '''

    # Check a flag to see if the methods have already been vectorized
    if getattr(t, 'vectorized', False) == False:

        # Vectorize each method
        for name in dir(t):
            if not name.startswith('_'):  # Ignore built-in/private methods
                attr = getattr(t, name)
                setattr(t, 'v_' + name, np.vectorize(attr))

        # Set the flag to indicate the type has been vectorized
        setattr(t, 'vectorized', True)
        return True
    else:
        return False
