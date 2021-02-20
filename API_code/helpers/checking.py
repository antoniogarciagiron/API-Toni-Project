def check_mandatory(args,mandatory):
    """
    
    """
    for k in mandatory:
        if k not in args.keys():
            return False
    return True


def check_groups(args,field,mandatory): 
    if args[field] not in mandatory:
        return False
    return True