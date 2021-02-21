def check_mandatory(args,mandatory):
    '''
    The function checks if the parameters passed to the function "quotes_new" are correct
    Takes: the arguments to insert and a list with the correct arguments required
    Returns: True if everything is correct, otherwise returns a False
    '''
    for k in mandatory:
        if k not in args.keys():
            return False
    return True


def check_groups(args,field,mandatory): 
    '''
    The function checks if the queries for a selected field are included into the Database or not
    Takes: the querie(args), selected field and the list of possible queries
    Returns: True if everything is correct, otherwise returns a False
    '''
    if args[field] not in mandatory:
        return False
    return True