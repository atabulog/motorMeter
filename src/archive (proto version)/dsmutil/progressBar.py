"""
Author: Austin Tabulog
Date: 11/30/19
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: Module to print recursive progress bar.
"""
def progressBar(iteration, total, prefix = 'Progress', suffix='Complete',
                      decimals = 1, length = 50, fill = '█'):
    """Call in a loop to create terminal progress bar.
    Args:
        iteration (int): current iteration.
        total (int) : total iterations.
        prefix [OPT] (str): prefix string.
        suffix [OPT] (str): suffix string.
        decimals [OPT] (int): positive number of decimals in percent complete.
        length [OPT] (int): character length of bar.
        fill [OPT] (str): bar fill character.
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()
