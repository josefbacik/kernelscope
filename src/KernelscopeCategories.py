import MySQLdb
import Constraints
import FlameGraph
import Database

# This is where you add tablename and columns
_categories = {}
_categories['offcputime'] = ["hostname", "time", "process", "pid", "stack", "elapsed"]

def _insert_entry(db, category, entry):
    columns = []
    for k,v in entry.items():
        if k in _categories[category]:
            columns.append(k)
    cmd = "INSERT INTO " + category + " (" + ",".join(columns) + ") VALUES ("
    cmd += (db.arg_str() + ",") * len(columns)
    cmd = cmd[:-1]
    cmd += ")"
    values = []
    for c in columns:
        values.append(entry[c])
    print cmd
    print values
    cur = db.cursor()
    cur.execute(cmd, tuple(values))

def _load(db, category, query):
    # Queries can't be escaped, so we have to sanity check the elements we are
    # wanting to select to avoid bobby droptables
    columns = []
    for e in query['elements']:
        if e not in _categories[category]:
            continue
        columns.append(e)
    if len(columns) == 0:
        return {}

    cmd = "SELECT " + ",".join(columns)
    cmd += " FROM " + category
    (constraintstr, constraintargs) = Constraints.build_constraints(db, query, _categories[category])
    if len(constraintstr) > 0:
        cmd += " WHERE " + constraintstr
    if 'limit' in query:
        cmd += " LIMIT " + db.arg_str()
        constraintargs += (query['limit'],)
    print cmd
    print constraintargs
    cur = db.cursor()
    cur.execute(cmd, constraintargs)
    return cur.fetchall()

def dump(db, obj):
    if 'hostname' not in obj or 'time' not in obj:
        return
    for k,v in obj.items():
        if k in _categories:
            for e in obj[k]:
                e['hostname'] = obj['hostname']
                e['time'] = obj['time']
                _insert_entry(db, k, e)
    db.commit()

def load(db, constraints):
    retval = {}
    for k,v in constraints.items():
        if k in _categories:
            vals = _load(db, k, constraints[k])
            if 'format' in constraints[k] and 'flamegraph' == constraints[k]['format']:
                return FlameGraph.build_flamegraph(vals)
            else:
                retval[k] = vals
    return retval

def get_categories():
    return _categories
