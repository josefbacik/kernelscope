class StackGraph:
    def __init__(self):
        self.nodes = { "name": "root", "value": 0, "children":[] }

    def add_stack(self, stack, value):
        cur_node = self.nodes
        self.nodes['value'] += value;
        for sym in stack:
            node = {}
            if 'children' not in cur_node:
                cur_node['children'] = []
            cur_children = cur_node['children']
            for n in cur_children:
                if sym == n['name']:
                    node = n
                    break
            if node == {}:
                node['name'] = sym
                node['value'] = value
                cur_children.append(node)
            else:
                node['value'] += value
            cur_node = node

def build_flamegraph(values):
    stack_graph = StackGraph()
    if len(values) == 0:
        return stack_graph.nodes

    # Need to figure out which key has the stack in it, and if we selected an
    # elapsed value
    stack_key = ""
    value_key = ""
    for k,v in values[0].items():
        if type(v) == str and stack_key == "" and ";" in v:
            stack_key = k
            continue
        if value_key != "":
            continue
        try:
            numval = int(v)
            value_key = k
        except:
            continue
    if stack_key == "":
        return stack_graph.nodes

    for v in values:
        print v
        value = 1
        if value_key != "" and value_key in v:
            value = int(v[value_key])
        stack = v[stack_key].split(';')
        stack.reverse()
        stack_graph.add_stack(stack, value)
    return stack_graph.nodes
