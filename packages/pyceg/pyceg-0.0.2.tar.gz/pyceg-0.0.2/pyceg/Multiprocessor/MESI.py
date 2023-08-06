# TODO Basic MESI Write-back Invalidation Protocol
from Protocol import Protocol
from States import MESIState as State
from Operations import MSIOps as Ops


###################
# MESI Protocol
###################


class MESI(Protocol):
    def __init__(self, n_processors=2, memory_content=None):
        super(MESI, self).__init__(n_processors, memory_content)

    def on_event(self, pid, event, function):
        state, transaction = self.get_processor_state(pid), None

        # Next State Logic
        if state == State.M:
            if event == Ops.BusRd:
                state = State.S
                transaction = Ops.Flush
            elif event == Ops.BusRdX:
                state = State.I
                transaction = Ops.Flush

        elif state == State.E:
            if event == Ops.PrWr:
                state = State.M
            elif event == Ops.BusRd:
                state = State.S
            elif event == Ops.BusRdX:
                state = State.I

        elif state == State.S:
            if event == Ops.PrWr:
                state = State.M
                transaction = Ops.BusUpgr
            elif event in (Ops.BusUpgr, Ops.BusRdX):
                state = State.I

        elif state == State.I:
            if event == Ops.PrWr:
                state = State.M
                transaction = Ops.BusRdX
            elif event == Ops.PrRd:
                state = State.S
                transaction = Ops.BusRd
        # Set State
        self.set_processor_state(pid, state)

        # Processor Write to Cache using an Operation
        if event == Ops.PrWr:
            self.perform_processor_operation(pid, function)

        # Invalidate copy
        if event in (Ops.BusUpgr, Ops.BusRdX):
            self.set_processor_cache_content(pid, None)

        # If the new state is modified, store the modified value
        if state == State.M:
            self.modified_value = self.get_processor_cache_content(pid)

        # Processor Read/Write from Memory
        if event in (Ops.PrRd, Ops.PrWr):
            cache_content = self.modified_value or self.memory_content
            self.set_processor_cache_content(pid, cache_content)

        return transaction


######################
# Example 1
######################
def example1():
    instructions = [
        (1, Ops.PrRd),
        (2, Ops.PrRd),
        (3, Ops.PrRd),
        (2, Ops.PrWr, lambda x: x + 2),
        (1, Ops.PrRd),
    ]
    mesi = MESI(n_processors=len(set(x[0] for x in instructions)), memory_content=10)
    mesi.perform_instructions(instructions)


###################
# Main
###################
example1()
