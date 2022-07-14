from cicd.core.utils.timeout import timeout


class Runner:
    def run(self, **kwargs):
        if not self.action:
            return

        timeout_in_sec = kwargs.get('timeout')
        if not timeout_in_sec:
            return self.action.run(**kwargs)

        @timeout(timeout_in_sec)
        def run_with_timeout():
            return self.action.run(**kwargs)

        return run_with_timeout()

    @property
    def action(self):
        pass
