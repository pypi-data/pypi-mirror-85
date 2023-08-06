# Basic MSI Write-back Invalidation Protocol
from Protocol import Protocol
from States import MSIState as State
from Operations import MSIOps as Ops


###################
# MSI Protocol
###################


class MSI(Protocol):
    def __init__(self, n_processors=2, memory_content=None):
        super(MSI, self).__init__(n_processors, memory_content)

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
# Nov 6th 2020 Lecture
######################
def example1():
    instructions = [
        (1, Ops.PrRd),
        (2, Ops.PrRd),
        (2, Ops.PrWr, lambda _: 10),
        (2, Ops.PrRd),
        (2, Ops.PrWr, lambda _: 15),
        (1, Ops.PrWr, lambda _: 20),
        (2, Ops.PrRd),
    ]
    msi = MSI(n_processors=len(set(x[0] for x in instructions)), memory_content=5)
    msi.perform_instructions(instructions)


###################
# Example 2
# Quiz 2 2019
# Question 3
###################
def example2():
    instructions = [
        (1, Ops.PrRd),
        (2, Ops.PrRd),
        (2, Ops.PrWr, lambda x: x + 2),
        (1, Ops.PrWr, lambda x: x * 2),
        (2, Ops.PrRd),
    ]
    msi = MSI(n_processors=len(set(x[0] for x in instructions)), memory_content=3)
    msi.perform_instructions(instructions)


###################
# Example 2a
# DGD 5 Fall 2020
###################
def example2a():
    instructions = [
        (1, Ops.PrRd),
        (2, Ops.PrRd),
        (2, Ops.PrWr, lambda x: x + 2),
        (1, Ops.PrWr, lambda x: x * 2),
        (2, Ops.PrRd),
    ]
    msi = MSI(n_processors=len(set(x[0] for x in instructions)), memory_content=10)
    msi.perform_instructions(instructions)


###################
# Example 3
# Bank Question / Final Exam 2005
###################
def example3():
    instructions = [
        (1, Ops.PrRd),
        (2, Ops.PrWr, lambda _: 8),
        (3, Ops.PrRd),
        (1, Ops.PrRd),
        (2, Ops.PrWr, lambda x: 9),
    ]
    msi = MSI(n_processors=len(set(x[0] for x in instructions)), memory_content=3)
    msi.perform_instructions(instructions)


###################
# Main
###################
# example1()
# example2a()
# example2()
# example3()
