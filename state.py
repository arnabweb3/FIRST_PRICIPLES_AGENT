def initialize_state(goal):
    return {
        "goal": goal,
        "status" : "running",
        "actions" : [],
        "observations" : [],
        "current_step" : 0,
        "final_answer" : None
    }

def record_action(state, tool_name, arguments):
    action = {
        "step" : state['current_step'] + 1,
        "tools" : tool_name,
        "arguments" : arguments
    }

    state['actions'].append(action)
    state['current_step'] += 1


    return state


def record_observation(state, tool_name, result, success=True):
    observation = {
        "tool" : tool_name,
        "result" : result,
        "success" : success
    }

    state['observations'].append(observation)

    return state


def update_status(state, status, final_answer=None):
    state['status'] = status
    state['final_answer'] = final_answer

    return state


def build_context(state):

    return {
        "goal": state['goal'],
        "status" : state['status'],
        "actions" : state['actions'],
        "observations" : state['observations'],
        "current_step" : state['current_step'],
        "final_answer" : state['final_answer']
    }
