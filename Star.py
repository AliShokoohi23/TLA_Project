import  json

input_file = "FA.json"
with open(input_file, 'r') as f:
    data = json.load(f)

data['states'] = eval(data['states'])
data['input_symbols'] = eval(data['input_symbols'])
data['final_states'] = eval(data['final_states'])

for key, value in data['transitions'].items():
    for k, v in value.items():
        data['transitions'][key][k] = eval(v)

states_set = data['states']
n = len(states_set)

a = "q"+str(n)
b = "q"+str(n+1)
data["states"].add(a)
data["states"].add(b)

new_final = {"" : a}
final = {b : new_final}
data['transitions'].update(final)

new_init = {"" : "{" + f"'{data['initial_state']}'" + "," + f"'{b}'" + "}"  }
init = {a : new_init}
data['transitions'].update(init)

for state in data["final_states"]:
    old_final_to_new_final = {"" : b}
    final_dict = {state : old_final_to_new_final}
    data['transitions'].update(final_dict)

data["initial_state"] = a
data["final_states"] = "{" + f"'{b}'" + "}"

print(data)