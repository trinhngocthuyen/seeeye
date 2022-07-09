class Runner:
    def run(self, **kwargs):
        if self.action:
            return self.action.run(**kwargs)

    @property
    def action(self):
        pass
