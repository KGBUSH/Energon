try:
    from IPython.display import display, Markdown
except:
    pass

# Helper functions
def is_notebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter

def print_graph(g):
    g_str = g.serialize(format='turtle').decode('utf-8')
    new_g_str = ''
    for line in g_str.split('\n'):
        if 'prefix' not in line:
            new_g_str += line + '\n'
    if is_notebook():
        display(Markdown('```turtle\n' + new_g_str + '\n```'))
    else:
        print(g_str)