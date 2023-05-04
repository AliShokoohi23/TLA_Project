import json
input_file = "NFA.json"
with open(input_file, 'r') as f:
    nfa = json.load(f)

nfa['states'] = eval(nfa['states'])
nfa['input_symbols'] = eval(nfa['input_symbols'])
nfa['final_states'] = eval(nfa['final_states'])

for key, value in nfa['transitions'].items():
    for k, v in value.items():
        nfa['transitions'][key][k] = eval(v)
