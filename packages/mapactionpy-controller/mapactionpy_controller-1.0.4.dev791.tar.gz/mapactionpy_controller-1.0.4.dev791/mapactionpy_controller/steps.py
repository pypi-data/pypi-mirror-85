import logging
import traceback


class Step():
    """
    This represents the atomic "unit of work" within the map production automation.

    The contract for functions
        'state' - An object of any kind. Either generated by the previous Step or passed as the `initial_state`
                  parameter of `main_stack.process_stack` function.

    Return values:
        Any object. Does not need to be a dict. The return value will be wrapped in the dict prior to being
        passed to the next step.  kwargs = {'state' : return_value}

    Exceptions:

            pass_back['result'] = result
            pass_back['exp'] = exp
            pass_back['stack_trace'] = traceback.format_exc()


    :param func: A callable which will do the relevant "unit of work".
        * Must accept a **kwargs param. If there is a state object this is passed as `kwargs['state']`.
          The stack does not guarentee the type of object that will be passed as the state.
        * If the function completes successfully it should return the updated state object. This should be
          "bare" (ie not wrapped in a dict ala kwargs)
        * If the function does not complete successfully it should raise an exception.
    :param fail_threshold: Expresses the severity with which an exception from `func` should be treated. In
        any case the exception will be handled and a JIRA tasks logged as appropriate.
        * If = `logging.ERROR` - the exception will terminate the program.
        * If = `logging.WARNING` - the exception will not result in termination. A JRIA task will be logged
          the program will attempt to continue, though the results may not be want the user intended.
    :param running_msg: A descriptive string to display (ie on the terminal) whilst this step is running.
    :param complete_msg: A descriptive string to display (eg on the terminal or in the logs) when the step as
                         completed successfully.
    :param fail_msg: A descriptive string to display (eg on the terminal or in the logs) if the step fails to
                     complete successfully.
    :returns: Either:
        * An object which will be passed to the next Step. The returned value will be wrapped in the dict prior
          to being passed to the next step.  kwargs = {'state' : return_value}
        * Or one or more Step objects. If multiple Step objects then these should be contained within a list.
          Any Step objects will be added to the stack in reverse order. (eg the list object in the list will be
          the next to be executed).
    """

    def __init__(self, func, fail_threshold, running_msg, complete_msg, fail_msg):
        self.func = func
        self.fail_threshold = fail_threshold
        self.running_msg = running_msg
        self.complete_msg = complete_msg
        self.fail_msg = fail_msg

    def run(self, set_feedback, **kwargs):
        pass_back = kwargs.copy()

        try:
            result = self.func(**kwargs)
            # long_msg = '{}\n{}'.format(self.complete_msg, result)
            pass_back['result'] = result
            set_feedback(logging.INFO, self.complete_msg, self, **pass_back)
            return result
        # Because this is defacto part of the main stack we do want to catch
        # a top level Exception here:
        except Exception as exp:
            pass_back['exp'] = exp
            pass_back['stack_trace'] = traceback.format_exc()
            set_feedback(self.fail_threshold, self.fail_msg, self, **pass_back)
            # set_feedback(logging.ERROR, self.fail_msg, self, **pass_back)

            # Do we want to raise an ERROR or a WARNING?
            if self.fail_threshold >= logging.ERROR:
                raise exp

            # If this is just a warning then we return the unaltered state object
            # TODO Review is it is possible in the case of warnings, to pass back an updated
            # state as an args to the relevant Exception.
            return kwargs.get('state', None)
