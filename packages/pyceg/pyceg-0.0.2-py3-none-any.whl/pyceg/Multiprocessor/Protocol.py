from tabulate import tabulate
from Processor import Processor
from Operations import MSIOps as Ops


class Protocol:
    def __init__(self, n_processors=2, memory_content=None):
        self.n_processors = n_processors
        self.processors = [Processor(pid=i + 1) for i in range(n_processors)]
        self.memory_content = memory_content
        self.modified_value = None
        self.history = []

    def __repr__(self):
        return tabulate(self.history, headers=self.get_headers(), stralign="center", numalign="center")

    def on_event(self, pid, event, function):
        pass

    def get_headers(self):
        headers = ["Step"]
        [headers.extend(["P{} State".format(i + 1), "P{} Cache".format(i + 1)]) for i, p in enumerate(self.processors)]
        headers.extend(["Content of Memory Location X", "Bus Transaction", "Modified"])
        return headers

    def step_count(self):
        return len(self.history)

    def save_history(self, step_name, transaction):
        fields = [step_name]
        [fields.extend([p.state, p.cache_content or '-']) for p in self.processors]
        fields.extend([self.memory_content or '-', transaction or '-', self.modified_value or '-'])
        self.history.append(fields)

    def get_processor_state(self, pid):
        return self.processors[pid - 1].state

    def set_processor_state(self, pid, state):
        self.processors[pid - 1].state = state

    def get_processor_cache_content(self, pid):
        return self.processors[pid - 1].cache_content

    def set_processor_cache_content(self, pid, cache_content):
        self.processors[pid - 1].cache_content = cache_content

    def perform_processor_operation(self, pid, function):
        if function and callable(function):
            cache_content = function(self.modified_value or self.get_processor_cache_content(pid))
            self.set_processor_cache_content(pid, cache_content)

    def format_instruction_name(self, processor_id, event):
        return "{}. P{} {}".format(len(self.history) + 1, processor_id, event)

    def flush(self, value):
        """"
        Request that indicates that a whole cache block is being written back to the memory
        Places the value of value of the cache line on the bus and updates the memory
        """
        self.memory_content = value

    def _perform_instruction(self, pid, event, function):
        # Perform the current Processor Event
        main_transaction = self.on_event(pid, event, function)
        # Update the other processors
        for processor in self.processors:
            if processor.pid != pid:
                cache_content = self.get_processor_cache_content(processor.pid)
                transaction = self.on_event(processor.pid, main_transaction, function)
                if transaction == Ops.Flush:
                    self.flush(cache_content)
                    main_transaction += "/" + Ops.Flush

        # Save the current state into history for printing
        step_name = self.format_instruction_name(pid, event)
        self.save_history(step_name, main_transaction)

    def perform_instructions(self, instructions):
        for i in instructions:
            pid, operation, function = i[0], i[1], i[2] if len(i) == 3 else None
            self._perform_instruction(pid, operation, function)
        print(self, '\n')
