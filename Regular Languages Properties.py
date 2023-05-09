import json

def concatenation():
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
    
    new_final_state = "q" + str(n)
    
    fa1["states"].append(new_final_state)
    
    old_final_to_new_final = {"" : new_final_state}
    
    fa1_final_to_fa2_init = {"" : fa2["initial_state"]}
    
    for state in fa1["final_states"]:
        final_dict = {state : fa1_final_to_fa2_init}
        fa1['transitions'].update(final_dict)
    
    for state in fa2["final_states"]:
        final_dict = {state : old_final_to_new_final}
        fa1['transitions'].update(final_dict)
    
    
    
    fa1["transitions"].update({new_final_state:{}})
    
    fa1["states"] = "{" + ",".join(f"'{state}'" for state in fa1["states"] ) + "}"
    
        
    fa1["input_symbols"] = "{" + ",".join(f"'{symbol}'" for symbol in fa1["input_symbols"]) + "}"
    
    fa1["final_states"] = "{" + ",".join(f"'{state}'" for state in fa1["final_states"] ) + "}"
    
    fa1["final_states"] = "{" f"'{new_final_state}'" "}"
    
    save_json_file(fa1,"concatenation.json")
    
    return fa1



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
    
    save_json_file(fa1, "union.json")
    
    return fa1

def star():
  input_file = "FA.json"
  with open(input_file, 'r') as f:
      fa = json.load(f)

  fa['states'] = eval(fa['states'])
  fa['input_symbols'] = eval(fa['input_symbols'])
  fa['final_states'] = eval(fa['final_states'])

  for key, value in fa['transitions'].items():
      for k, v in value.items():
          fa['transitions'][key][k] = eval(v)


  states_set = fa['states']
  n = len(states_set)

  a = "q"+str(n)
  b = "q"+str(n+1)
  fa["states"].add(a)
  fa["states"].add(b)


  new_final = {"" : a}
  final = {b : new_final}
  fa['transitions'].update(final)

  new_init = {"" : "{" + f"'{fa['initial_state']}'" + "," + f"'{b}'" + "}"  }
  init = {a : new_init}
  fa['transitions'].update(init)

  for state in fa["final_states"]:
      old_final_to_new_final = {"" : b}
      final_dict = {state : old_final_to_new_final}
      fa['transitions'].update(final_dict)


  fa["initial_state"] = a
  fa["final_states"] = "{" + f"'{b}'" + "}"
  fa["states"] = "{" + ",".join(f"'{state}'" for state in fa["states"] ) + "}"
    
        
  fa["input_symbols"] = "{" + ",".join(f"'{symbol}'" for symbol in fa["input_symbols"]) + "}"

  save_json_file(fa, "star.json")

def save_json_file(fa,name):
    with open(name, "w") as f:
        json.dump(fa, f, cls=SetEncoder, indent=2)


star_automata = star()
union_automata = union()
concat_automata = concatenation()


