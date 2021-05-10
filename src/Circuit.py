from src.gates import *
import re
from src.parse import *


class Circuit:
    def __init__(self, filename, input_values):

        (connectors, gates, gates_info,component_to_num) = buildCircuit(filename)
        self.component_to_num=component_to_num
        self.connectors = connectors
        self.gates = gates
        self.gates_info = gates_info
        self.input_valuesDic = InputValuesToDic(input_values, gates_info)  # 1 or 0 for input empty list for connctors
        self.addConnctorsToLastGates()
        self.initInputs()  # add the inputs i1-in to the circuit



    def get_gates(self):
        return self.gates

    def get_gates_info(self):
        return self.gates_info

    def get_connectors(self):
        return self.connectors

    def get_input_valuesDic(self):
        return self.input_valuesDic

    def getOutputValues(self):
        outputs = {}
        for info in self.gates_info:

            letter, number = re.search(r"([a-z]+)(\d+)?", info["output"]).groups()
            if letter == 'o':
                outputs[number] = findGateByName(self.gates, info["name"]).getOutput()

        val_list = list(outputs.values())
        return val_list
    def getOutputConnectorByGate(self,gate):
        for c in self.get_connectors():
            if c.getFrom().getLabel()==gate.getLabel():
                return c
        return None


    def addConnctorsToLastGates(self):
        gates_info=self.get_gates_info()
        for gate_info in gates_info:
            if gate_info["output"][0]=='o':
                gate=findGateByName(self.get_gates(),gate_info['name'])
                c=Connector(gate,gate_info["output"],'C'+gate_info["output"])
                self.connectors.append(c)

        # add the inputs i1-in to the system
    def initInputs(self):
        i=0
        for gateName in self.input_valuesDic:
            inputVals = self.input_valuesDic[gateName]
            if inputVals:
                gate = findGateByName(self.gates, gateName)
                for i in range(len(gate.pins)):
                    if not gate.pins[i]:  # if None, insert input. otherwise, there is already a connector
                        c=Connector(inputVals.pop(),gate,"i"+str(i))
                        gate.pins[i] = c




def buildCircuit(fileName):
    (system_name, inputs, outputs, gates_info) = parse_system(fileName)

    component_to_num={}
    counter=0


    gates = list()
    for gate_info in gates_info:
        g = createGate(gate_info)
        component_to_num[gate_info["name"]]=counter
        counter+=1
        gates.append(g)

    (connectors, gates,component_to_num) = conncetCircuit(gates, gates_info,counter,component_to_num)
    return (connectors, gates, gates_info,component_to_num)


def split_vals(word):
    type, num_of_inputs = re.search(r"([a-z]+)(\d+)?", word).groups()
    return type, int(num_of_inputs or 0)


# create logic gate with n pins from gate info
def createGate(gate_info):
    (type, name, output, input) = (gate_info["type"], gate_info["name"], gate_info["output"], gate_info["inputs"])
    (gateType, numOfInputs) = split_vals(type)

    if gateType == 'and':
        g = AndGate(name, numOfInputs)
    elif gateType == 'or':
        g = OrGate(name, numOfInputs)
    elif gateType == 'inverter':
        g = InverterGate(name)
    elif gateType == 'nand':
        g = NandGate(name, numOfInputs)
    elif gateType == 'buffer':
        g = BufferGate(name)
    elif gateType == 'xor':
        g = XorGate(name, numOfInputs)
    elif gateType == 'nor':
        g = NorGate(name, numOfInputs)
    else:
        print('gate type erorr!!!')
    return g


# add conncetors and connect the gates
def conncetCircuit(gates, gates_info,counter,component_to_num):
    connectors = list()
    i=0
    for gate_info in gates_info:
        type, name, output, inputs = (gate_info[k] for k in ("type", "name", "output", "inputs"))
        fromGate = findGateByName(gates, name)
        tatgetGates = findGatesWithInput(gates, gates_info, output)

        for target in tatgetGates:
            c = Connector(fromGate, target,'C'+str(i))
            connectors.append(c)
            component_to_num[c.getLabel()]=counter
            counter+=1
            i+=1
    return (connectors, gates,component_to_num)


def findGateByName(gates, name):
    for gate in gates:
        if gate.label == name:
            return gate


# find the gate that recive input @input
def findGatesWithInput(gates, gatesinfo, input):
    gates_to_return = list()
    for info in gatesinfo:
        if input in info['inputs']:
            name = info['name']
            for gate in gates:
                if gate.label == name:
                    gates_to_return.append(gate)
    return gates_to_return


# create dictionary  gate Name --> input cords (i1-in)
def InputValuesToDic(input_values, gatesinfo):
    inputsDic = dict()
    for info in gatesinfo:
        inputs = info['inputs']
        inputsDic[info['name']] = list()
        for i in inputs:
            if i[0] == 'i':
                letter, number = re.search(r"([a-z]+)(\d+)?", i).groups()
                inputsDic[info['name']].append(input_values[int(number) - 1])

    return inputsDic



