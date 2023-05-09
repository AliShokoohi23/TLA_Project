import json

def is_accepted(automata, input_str):
    current_states = {automata["initial_state"]}
    
    for symbol in input_str:
        next_states = set()
        for state in current_states:
            if state in automata["transitions"] and symbol in automata["transitions"][state]:
                next_states |= set(automata["transitions"][state][symbol])
        
        current_states = next_states
    

    return any(state in automata["final_states"] for state in current_states)


FA_input = "FA.json"
with open(FA_input, 'r') as f:
    FA = json.load(f)
    
string_input = input()
print("Accepted" if is_accepted(FA, string_input) else "Rejected")