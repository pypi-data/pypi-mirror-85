from .hook import Hook, _hook_inner

__all__ = ["Hook", "_hook_inner", "get_output_size", "SavingFn", "Hooking"]


def get_output_size(module, input, output):
    return output.size()


class SavingFn:
    def __init__(self, fn):
        self.results = []
        self.fn = fn

    def __call__(self, *args, **kwargs):
        self.results.append(self.fn(*args, **kwargs))


class Hooking:
    def __init__(self,
                 modules_to_hook, hook_fn,
                 register_fn=lambda module, hook: module.register_forward_hook(hook)):
        self.saving = [SavingFn(hook_fn) for _ in modules_to_hook]
        self.handles = [register_fn(module=m, hook=h) for m, h in zip(modules_to_hook, self.saving)]
        self.removed = False

    def remove(self):
        if not self.removed:
            for handle in self.handles:
                handle.remove()
            self.removed = True

    def results(self):
        return [s.results for s in self.saving]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.remove()
