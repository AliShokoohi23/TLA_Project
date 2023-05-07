import json

input = "DFA.json"
with open(input, "r") as f:
    dfa = json.load(f)
    

dfa["states"] = eval(dfa["states"])
dfa["input_symbols"] = eval(dfa["input_symbols"])
dfa["final_states"] = eval(dfa["final_states"])
