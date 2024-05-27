from collections import defaultdict
import json
import re

def parse_text_to_nodes(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    nodos = text.strip().split('================')
    dict_nodes = {}

    for nodo in nodos:
        nodo = nodo.strip()
        if not nodo:
            continue

        # Encontrar el identificador del nodo (valor después de 'start address:')
        match = re.search(r'start address:\s*([\w_]+)', nodo)
        if match:
            start_address = match.group(1)
            dict_nodes[start_address] = nodo

    return dict_nodes

def node_cost_calculation(nodes, opcode_counter, opcode_cost):
    total_cost = 0
    total_opcode_appearances = defaultdict(int)

    for node in nodes:
        if node not in opcode_counter:
            print(f"Warning: Node '{node}' not found in base opcodes.")
            continue

        if DEBUG:
            print(f"Node {node} opcode appearances:")
            print(opcode_counter[node])

        for opcode, count in opcode_counter[node].items():
            total_opcode_appearances[opcode] += count
            if opcode in opcode_cost:
                total_cost += count * opcode_cost[opcode]
            else:
                print(f"Warning: opcode '{opcode}' has no associated cost")

    return total_cost, total_opcode_appearances

def wrap_opcodes(nodes):
    opcodes = {}

    for identifier, node in nodes.items():
        opcode_appearances = defaultdict(int)
        words = re.findall(r'\b[A-Z]+\d*\b', node)
        for opcode in words:
            opcode_appearances[opcode] += 1
        opcodes[identifier] = opcode_appearances

    return opcodes


# Function's nodes list
POWER_OF_TWO = [
    '0','15','25','78','369','390','349','327','318','336','346','363',
    '403','99','212','220','261','104','427','412','318_0','421','446',
    '117'
]
POWER_OF_TWO_LOOP = [
    '220','229','904','318_1','914','318_2','925','949','240',
    '955','318_3','965','1015','253'
]
PARAM_LENGTH = [
    '0','15','25','41','52','63','164','788','809','838','743','763','639','592',
    '618','652','566','301','575','517','456','526','557','587','657','692','694',
    '733','779','850','185','291','190','427_0','412_0','318_5','421_0','446_0','203'
]
PARAM_LENGTH_LOOP = [
    '694','703','349_1','327_1','318_6','336_1','346_1','363_1','713'
]
SSTORE = [
    '0','15','25','41','52','136','369_0','390_0','349_0','327_0','318_4','336_0','346_0',
    '363_0','403_0','157','282','162'
]
NOTHING = [
    '0','15','25','41','126','271','134'
]

DEBUG = False

def main():
    with open('opcode_gas_costs.json', 'r') as json_file:
        opcode_gas_costs = json.load(json_file)

    # Fichero cfg y lista de identificadores de nodos para calcular el coste
    path_file = 'costabs/cfg_GasUsageTest.cfg'
    list_nodes = PARAM_LENGTH  

    nodes = parse_text_to_nodes(path_file)
    nodes_opcodes = wrap_opcodes(nodes)
    total_cost, total_opcodes_appaerances = node_cost_calculation(list_nodes, nodes_opcodes, opcode_gas_costs)

    print("TOTAL COST:", total_cost)

    opcodes_info = []
    for opcode, count in total_opcodes_appaerances.items():
        cost = opcode_gas_costs.get(opcode, 0)
        total_cost = count * cost
        opcodes_info.append((opcode, cost, count, total_cost))

    opcodes_info.sort(key=lambda x: x[3], reverse=True)

    for opcode, cost, count, total_cost in opcodes_info:
        print(f"Opcode: {opcode}, Coste: {cost}, Ap: {count}, Total gas: {total_cost}")


if __name__=='__main__':
    main()