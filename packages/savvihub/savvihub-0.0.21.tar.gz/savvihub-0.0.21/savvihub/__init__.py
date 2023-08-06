from savvihub.common.context import Context


def log(step, row=None):
    """
    step: a step for each iteration (required)
    row: a dictionary to log
    """
    context = Context()
    context.experiment.log(step, row)
