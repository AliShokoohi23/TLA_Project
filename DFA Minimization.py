import json

def partition_states(states, is_final, transitions, input_symbols):
    partitions = [set(), set()]
    for state in states:
        if is_final(state):
            partitions[1].add(state)
        else:
            partitions[0].add(state)

    updated = True
    while updated:
        updated = False
        for partition in partitions[:]:
            for symbol in input_symbols:
                blocks = {}
                for state in partition:
                    next_state = transitions[state][symbol]
                    for idx, block in enumerate(partitions):
                        if next_state in block:
                            if idx not in blocks:
                                blocks[idx] = set()
                            blocks[idx].add(state)
                            break

                if len(blocks) > 1:
                    partitions.remove(partition)
                    partitions.extend(blocks.values())
                    updated = True
                    break

            if updated:
                break

    return partitions


def minimize_dfa(dfa):
    states = set(dfa["states"])
    input_symbols = set(dfa["input_symbols"])
    transitions = dfa["transitions"]
    initial_state = dfa["initial_state"]
    final_states = set(dfa["final_states"])

    is_final = lambda state: state in final_states
    partitions = partition_states(states, is_final, transitions, input_symbols)

    min_states = ["".join(sorted(partition)) for partition in partitions]
    min_transitions = {}
    for min_state in min_states:
        if min_state == initial_state:
            min_initial_state = min_state
        if min_state in final_states:
            min_final_states = min_state
            

        for symbol in input_symbols:
                try:next_state = transitions[min_state][symbol]
                except: next_state = transitions[min_state[:2]][symbol]
                for partition in partitions:
                    if next_state in partition:
                        min_next_state = "".join(sorted(partition))
                        break
                if min_state not in min_transitions:
                    min_transitions[min_state] = {}
                min_transitions[min_state][symbol] = min_next_state

    return {
        "states": min_states,
        "input_symbols": list(input_symbols),
        "transitions": min_transitions,
        "initial_state": min_initial_state,
        "final_states": {min_final_states},
    }

input = "DFA.json"
with open(input, "r") as f:
    dfa = json.load(f)
    

dfa["states"] = eval(dfa["states"])
dfa["input_symbols"] = eval(dfa["input_symbols"])
dfa["final_states"] = eval(dfa["final_states"])

minimized_dfa = minimize_dfa(dfa)
print(minimized_dfa)