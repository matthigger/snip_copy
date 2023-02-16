# complete the function below

def add_all_even_idx(x):
    """ adds all even indexed items in x

    Args:
        x (list): a list of values which can be summed

    Returns:
        x_even_sum: sum
    """

    # ! snip: student
    x_even = x[::2]
    return sum(x_even)
    # ! snip-end

# ! snip: student, solution
# rubric notes
# 100 pts for documentation
# 1 pts for function which works
# (note: no snip-end command given, adds one @ file end if needed)
