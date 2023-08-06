class ContextHandler(object):
    def __init__(self):
        self.contexts = []

    def enter_cm(self, context_manager):
        val = context_manager.__enter__()
        self.contexts.append(context_manager)
        return val

    def close_all_context_managers(self):
        while self.contexts:
            cm = self.contexts.pop()
            cm.__exit__(None, None, None)
