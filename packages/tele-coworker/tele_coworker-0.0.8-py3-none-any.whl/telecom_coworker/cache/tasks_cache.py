import logging

log = logging.getLogger("tasks_cache")


class TasksCache(object):

    def __init__(self, init_tasks: set):
        self.curr_tasks = set()
        self.next_tasks = init_tasks

    def update(self, next_tasks):
        self.next_tasks = set(next_tasks)

    def next_version(self, canceled_tasks_handle_func, added_tasks_handle_func):
        canceled_tasks = self.curr_tasks - self.next_tasks
        if canceled_tasks:
            canceled_tasks_handle_func(canceled_tasks)

        added_tasks = self.next_tasks - self.curr_tasks
        if added_tasks:
            added_tasks_handle_func(added_tasks)

        self.curr_tasks = self.next_tasks
        log.info("current tasks => {}".format(self.curr_tasks))

    @property
    def tasks(self):
        return self.curr_tasks

    def __len__(self):
        return len(self.curr_tasks)


if __name__ == '__main__':
    def foo(canceled_tasks):
        print("canceled tasks => {}".format(canceled_tasks))


    def added_foo(added_tasks):
        print("added tasks => {}".format(added_tasks))


    cache = TasksCache({"task1", "task2"})
    cache.next_version(foo, added_foo)
    print("---------------------")
    cache.update(["task3"])
    cache.next_version(foo, added_foo)

    print("current tasks => {}".format(cache.curr_tasks))
