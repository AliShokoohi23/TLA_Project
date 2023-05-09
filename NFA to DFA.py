from collections import deque
import  json

def e_closure(nfa, states):
    result = set(states)
    stack = list(states)

    while stack:
        state = stack.pop()
        e_transitions = nfa["transitions"].get(state, {}).get("", [])

        for target in e_transitions:
            if target not in result:
                result.add(target)
                stack.append(target)

    return result


def nfa_to_dfa(nfa):
    dfa = {
        "states": set(),
        "input_symbols": nfa["input_symbols"],
        "transitions": {},
        "initial_state": "",
        "final_states": set()
    }

    initial_eclosure = frozenset(e_closure(nfa, [nfa["initial_state"]]))
    dfa["initial_state"] = "".join(sorted(initial_eclosure))

    if any(state in nfa["final_states"] for state in initial_eclosure):
        dfa["final_states"].add(dfa["initial_state"])

    worklist = deque([initial_eclosure])
    processed_states = set()

    while worklist:
        current_set = worklist.popleft()
        current_label = "".join(sorted(current_set))

        if current_label in processed_states:
            continue

        processed_states.add(current_label)
        dfa["states"].add(current_label)
        dfa["transitions"][current_label] = {}

        for symbol in nfa["input_symbols"]:
            next_set = set()

            for state in current_set:
                targets = nfa["transitions"].get(state, {}).get(symbol, [])
                next_set.update(e_closure(nfa, targets))

            next_label = "".join(sorted(next_set))

            if not next_label:
                next_label = "TRAP"

            dfa["transitions"][current_label][symbol] = next_label

            if next_label != "TRAP":
                if any(state in nfa["final_states"] for state in next_set):
                    dfa["final_states"].add(next_label)

                if next_label not in processed_states:
                    worklist.append(frozenset(next_set))

    dfa["states"].add("TRAP")
    dfa["transitions"]["TRAP"] = {symbol: "TRAP" for symbol in nfa["input_symbols"]}

    dfa["states"] = "{" + ",".join(sorted(f"'{state}'"for state in dfa["states"])) + "}"
    dfa["input_symbols"] = "{" + ",".join(sorted(f"'{state}'" for state in dfa["input_symbols"])) + "}"
    dfa["final_states"] = "{" + ",".join(sorted(f"'{state}'" for state in dfa["final_states"])) + "}"
    
    
    
    dfa_path = "DFA.json"
    with open(dfa_path, 'w') as output_file:
        json.dump(dfa, output_file, indent=2)
    return dfa

input_file = "NFA.json"
with open(input_file, 'r') as f:
    nfa = json.load(f)

nfa['states'] = eval(nfa['states'])
nfa['input_symbols'] = eval(nfa['input_symbols'])
nfa['final_states'] = eval(nfa['final_states'])

for key, value in nfa['transitions'].items():
    for k, v in value.items():
        nfa['transitions'][key][k] = eval(v)

dfa = nfa_to_dfa(nfa)