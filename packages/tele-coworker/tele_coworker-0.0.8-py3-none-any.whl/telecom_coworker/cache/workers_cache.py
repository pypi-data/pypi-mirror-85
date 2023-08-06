import logging

log = logging.getLogger("workers_cache")


class WorkersCache(object):

    def __init__(self, init_workers: set):
        self.curr_workers = set()
        self.next_workers = init_workers

    def update(self, next_workers):
        self.next_workers = set(next_workers)

    def next_version(self, lost_workers_handle_func, added_workers_handle_func):
        lost_workers = self.curr_workers - self.next_workers
        if lost_workers:
            lost_workers_handle_func(lost_workers)

        added_workers = self.next_workers - self.curr_workers
        if added_workers:
            added_workers_handle_func(added_workers)

        self.curr_workers = self.next_workers
        log.info("current workers {}".format(self.curr_workers))

    @property
    def workers(self):
        return self.curr_workers

    def __len__(self):
        return len(self.curr_workers)


if __name__ == '__main__':
    def foo(lost_workers):
        print("lost workers => {}".format(lost_workers))


    def added_foo(added_workers):
        print("added workers => {}".format(added_workers))


    cache = WorkersCache({"worker1", "worker2"})
    cache.next_version(foo, added_foo)
    print("-----------------------")
    cache.update(["worker2", "worker3"])
    cache.next_version(foo, added_foo)
    print("-----------------------")

    print("current workers => {}".format(cache.curr_workers))
