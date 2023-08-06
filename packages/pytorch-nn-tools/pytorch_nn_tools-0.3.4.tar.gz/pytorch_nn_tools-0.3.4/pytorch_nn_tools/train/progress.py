class ProgressTracker:
    def __init__(self):
        """
        Keeps track of global number of iterations.
        >>> tracker = ProgressTracker()
        >>> for i in tracker.track((1,2,3)): assert tracker.cnt_total_iter == i
        >>> assert tracker.cnt_total_iter == 3
        >>> for i in tracker.track((1,2,3,4)): assert tracker.cnt_total_iter == i + 3
        >>> assert tracker.cnt_total_iter == 7
        """
        self.cnt_total_iter = 0

    def track(self, dl):
        def tracked_iterator():
            for x in dl:
                self.cnt_total_iter += 1
                yield x

        return tracked_iterator()
