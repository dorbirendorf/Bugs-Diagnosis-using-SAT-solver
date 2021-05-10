

def parse_system(filename):  # name needs to contain the full path
    f = open(filename, "r")
    str = f.read()
    info = str.split('.')

    system_name = info[0]
    inputs = info[1][1:]
    outputs = info[2][1:]
    rows = info[3][2:-1].split(',\n')
    gates = []

    for row in rows:
        row = row[1:-1]
        gate_info = row.split(',')
        gate_type = gate_info[0]
        gate_name = gate_info[1]
        gate_output = gate_info[2]
        gate_inputs = gate_info[3:]
        gate = {
            "type": gate_type,
            "name": gate_name,
            "output": gate_output,
            "inputs": gate_inputs
        }
        gates.append(gate)

    return system_name, inputs, outputs, gates
