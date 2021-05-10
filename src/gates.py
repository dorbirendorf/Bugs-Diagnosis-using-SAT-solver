from sympy.logic.boolalg import *
class LogicGate:

    def __init__(self, label, n, type):
        self.label = label
        self.num_of_inputs = n
        self.output = None  # 0 or 1
        self.pins = [None] * n  # connectors
        self.isDiagnosis = 0
        self.type=type



    def __eq__(self, other):
        return self.label == other.label

    def __repr__(self):
        return self.label

    def __hash__(self):
        return hash(self.label)

    def getLabel(self):
        return self.label

    def getType(self):
        return self.type

    def getOutput(self):
        self.output = self.performGateLogic()
        return self.output

    def get_Nth_pin_value(self, n):
        if not isinstance(self.pins[n], int):
            return self.pins[n].getFrom().getOutput()  # case is a connector
        else:
            return self.pins[n]  # case is an input (0 or 1)

    def setIsDiagnosis(self):
        self.isDiagnosis = 1

    def ResetIsDiagnosis(self):
        self.isDiagnosis = 0

    def setNextPin(self, source):
        for i in range(len(self.pins)):
            if self.pins[i] is None:
                self.pins[i] = source
                break

    def getLogicClause(self):
        to_cnf()




class AndGate(LogicGate):

    def __init__(self, label, n):
        LogicGate.__init__(self, label, n,"AND")

    def performGateLogic(self):
        inputs = [None] * self.num_of_inputs
        for i in range(self.num_of_inputs):
            inputs[i] = self.get_Nth_pin_value(i)

        if all(input == 1 for input in inputs):
            if self.isDiagnosis == 0:
                return 1
            else:
                return 0
        else:
            if self.isDiagnosis == 0:
                return 0
            else:
                return 1

            return res

    def get_logic_clause(self):
        gateName=self.label

        gate_output=self.output


class NandGate(LogicGate):

    def __init__(self, label, n):
        LogicGate.__init__(self, label, n,"NAND")

    def performGateLogic(self):
        inputs = [None] * self.num_of_inputs
        for i in range(self.num_of_inputs):
            inputs[i] = self.get_Nth_pin_value(i)

        if all(input == 1 for input in inputs):
            if self.isDiagnosis == 0:
                return 0
            else:
                return 1
        else:
            if self.isDiagnosis == 0:
                return 1
            else:
                return 0


class OrGate(LogicGate):

    def __init__(self, label, n):
        LogicGate.__init__(self, label, n,"OR")

    def performGateLogic(self):
        inputs = [None] * self.num_of_inputs
        for i in range(self.num_of_inputs):
            inputs[i] = self.get_Nth_pin_value(i)

        if any(input == 1 for input in inputs):
            if self.isDiagnosis == 0:
                return 1
            else:
                return 0
        else:
            if self.isDiagnosis == 0:
                return 0
            else:
                return 1


class XorGate(LogicGate):

    def __init__(self, label, n):
        LogicGate.__init__(self, label, n,"XOR")

    def performGateLogic(self):
        ones = 0
        inputs = [None] * self.num_of_inputs
        for i in range(self.num_of_inputs):
            inputs[i] = self.get_Nth_pin_value(i)
            if inputs[i] == 1:
                ones += 1

        if ones % 2 == 0:
            if self.isDiagnosis == 0:
                return 0
            else:
                return 1
        else:
            if self.isDiagnosis == 0:
                return 1
            else:
                return 0


class NorGate(LogicGate):

    def __init__(self, label, n):
        LogicGate.__init__(self, label, n,"NOR")

    def performGateLogic(self):
        inputs = [None] * self.num_of_inputs
        for i in range(self.num_of_inputs):
            inputs[i] = self.get_Nth_pin_value(i)

        if any(input == 1 for input in inputs):
            if self.isDiagnosis == 0:
                return 0
            else:
                return 1
        else:
            if self.isDiagnosis == 0:
                return 1
            else:
                return 0


class InverterGate(LogicGate):

    def __init__(self, label):
        LogicGate.__init__(self, label, 1,"NOT")

    def performGateLogic(self):
        input = self.get_Nth_pin_value(0)
        if input == 1:
            if self.isDiagnosis == 0:
                return 0
            else:
                return 1
        else:
            if self.isDiagnosis == 0:
                return 1
            else:
                return 0


class BufferGate(LogicGate):

    def __init__(self, label):
        LogicGate.__init__(self, label, 1,'BUFFER')

    def performGateLogic(self):
        input = self.get_Nth_pin_value(0)

        if input == 1:
            if self.isDiagnosis == 0:
                return input
            else:
                return 0
        else:
            if self.isDiagnosis == 0:
                return 0
            else:
                return 1


class Connector:

    def __init__(self, fgate, tgate,label):
        self.fromgate = fgate
        self.togate = tgate
        self.label=label

        tgate.setNextPin(self)

    def __eq__(self, other):
        return self.fromgate == other.fromgate and self.togate == other.togate

    def __repr__(self):
        return self.label

    def getFrom(self):
        return self.fromgate

    def getTo(self):
        return self.togate

    def getLabel(self):
        return self.label





