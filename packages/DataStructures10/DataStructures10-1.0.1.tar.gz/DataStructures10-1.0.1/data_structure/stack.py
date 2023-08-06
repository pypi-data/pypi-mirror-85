class Stack:

    def __init__(self):
        self.stack = []

    def push(self, dataval):

        if dataval not in self.stack:
            self.stack.append(dataval)
            return f"{dataval} pushed"
        else:
            return False

    def remove(self):
        if len(self.stack) <= 0:
            return ("No element in the Stack")
        else:
            return self.stack.pop()

    def peek(self):
        return self.stack[-1]


