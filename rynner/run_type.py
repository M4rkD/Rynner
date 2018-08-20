class RunAction:
    def __init__(self, label, function):
        self.label = label
        self.function = function


class RunType:
    def __init__(self, runner, interface):
        self.runner = runner
        self.interface = interface
        self.__actions = []

    def create(self):
        # display configuration window
        accepted = self.interface.show()

        if accepted and len(self.interface.invalid()) == 0:
            data = self.interface.data()

            # TODO : what about host? This should be part of the dict as well?
            self.runner(data)

    def add_action(self, label, function):
        action = RunAction(label, function)
        self.__actions.append(action)
        return action

    def actions(self):
        return self.__actions
