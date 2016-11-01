_valid_constraints = ('=', '<', '<=', '>', '>=', '!=', 'contains')

# TODO: should probably throw errors for the various incorrect statement
# building, but for now assume we are perfect and just silently ignore invalid
# queries
def build_constraints(query, valid_columns):
    if 'constraints' not in query:
        return ('', ())
    constraints = query['constraints']
    strs = []
    args = []
    for constraint in constraints:
        # Each constraint requires a conditions array
        if 'conditions' not in constraint:
            continue
        conditions = constraint['conditions']

        # If we have more than one condition we must have an operation to join
        # the two of them together
        if len(conditions) > 1 and 'oper' not in constraint:
            continue

        cur_strs = []
        for statement in conditions:
            # Each condition statement must have exactly 2 fields, one is the
            # column and value pair, the other is the constraint type.
            if len(statement) != 2:
                continue
            if 'expr' not in statement:
                continue
            column = ""
            expr = ""
            for k,v in statement.items():
                if k == 'expr':
                    if v not in _valid_constraints:
                        continue
                    expr = v
                else:
                    column = k
            if expr == "" or column == "":
                continue

            #Sql doesn't take escaped columns for it's query, so we have to add
            #it directly to the string, so we need to make sure its only one
            #of the defined values to avoid bobby droptables
            if column not in valid_columns:
                continue

            value = statement[column]

            # Gotta make this mysql-y.  If we do other databases eventually
            # we'll need to tell this thing about it so we can do the right
            # thing here
            if len(cur_strs) > 0:
                cur_strs.append(constraint['oper'])
            if expr == 'contains':
                expr = "LIKE"
                value = '%' + value + '%'

            cur_strs.append(column)
            cur_strs.append(expr)
            cur_strs.append("%s")
            args.append(value)

        # Right now just AND all groups together, not sure if this will ever
        # happen in practice and I lack the desire for foresight
        if len(strs) > 0:
            strs.append("AND")
        strs.extend(cur_strs)
    return (" ".join(strs), tuple(args))
