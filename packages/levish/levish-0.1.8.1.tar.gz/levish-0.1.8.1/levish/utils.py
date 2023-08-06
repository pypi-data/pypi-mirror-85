from inspect import getfullargspec

def only_varargs(function, name):
    '''
    Tests if a function has only varargs with given name
    '''
    args = getfullargspec(function).args
    varargs = getfullargspec(function).varargs
    varkw= getfullargspec(function).varkw
    if args == [] and varkw == None and varargs == name:
        return True
    else:
        return False