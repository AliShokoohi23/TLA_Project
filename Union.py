import json

def union():
    file1 = "FA1.json"
    file2 = "FA2.json"
    
    with open(file1, "r") as f1, open(file2, "r") as f2:
        fa1 = json.load(f1)
        fa2 = json.load(f2)

    fa1["states"] = list(eval(fa1["states"]))
    fa1["input_symbols"] = list(eval(fa1["input_symbols"]))
    fa2["states"] = eval(fa2["states"])
    fa2["input_symbols"] = eval(fa2["input_symbols"])
    fa1['final_states'] = eval(fa1['final_states'])
    fa2['final_states'] = eval(fa2['final_states'])
    
    for key, value in fa1['transitions'].items():
        for k, v in value.items():
            fa1['transitions'][key][k] = eval(v)
            
    for key, value in fa2['transitions'].items():
        for k, v in value.items():
            fa2['transitions'][key][k] = eval(v)
    
    n = len(fa1["states"])
    fa1["states"].extend(["q" + str(i + n) for i in range(len(fa2["states"]))])

    fa1["input_symbols"].extend(fa2["input_symbols"])


    for state, transitions in fa2["transitions"].items():
        new_state = "q" + str(int(state[1:]) + n)
        new_transitions = {}
        for symbol, target_states in transitions.items():
            new_target_states = {"q" + str(int(target[1:]) + n) for target in target_states}
            new_target_states ="{" + ",".join(new_target_states) + "}"
            new_transitions[symbol] = new_target_states
        fa1["transitions"][new_state] = new_transitions

    
    fa2["initial_state"] = "q" + str(int(fa2["initial_state"][1:]) + n)

    for state in fa2["final_states"]:
        fa2["final_states"].add("q" +  str(int(state[1:]) + n))
        fa2["final_states"].remove(state)
        
    n = len(fa1["states"])
    
    new_init_state =  "q"+ str(n)
    new_final_state = "q" + str(n + 1)
    
    fa1["states"].extend([new_init_state, new_final_state])
    old_init_to_new_init = {new_init_state :{"" : {fa1["initial_state"] , fa2["initial_state"]}}}
    fa1["transitions"].update(old_init_to_new_init)
    old_final_to_new_final = {"" : new_final_state}
    
    
    
    for state in fa1["final_states"]:
        final_dict = {state : old_final_to_new_final}
        fa1['transitions'].update(final_dict)
    
    for state in fa2["final_states"]:
        final_dict = {state : old_final_to_new_final}
        fa1['transitions'].update(final_dict)
    
    fa1["initial_state"] = new_init_state
    
    fa1["transitions"].update({new_final_state:{}})
    
    fa1["states"] = "{" + ",".join(f"'{state}'" for state in fa1["states"] ) + "}"
    
        
    fa1["input_symbols"] = "{" + ",".join(f"'{symbol}'" for symbol in fa1["input_symbols"]) + "}"
    
    fa1["final_states"] = "{" f"'{new_final_state}'" "}"
    
    return fa1



union_automata = union()