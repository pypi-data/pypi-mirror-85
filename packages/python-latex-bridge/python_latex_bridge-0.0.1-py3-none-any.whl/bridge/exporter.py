import os
    
def typeset_latex_math(variable) -> str:
    """
    Returns `variable` as a string with LaTeX math typesetting.

    Args:
        variable: The python variable to be saved.

    Returns:
        str: String accoring to LaTeX typesetting.

    """
    has_unit = hasattr(variable, 'u')
    if has_unit:
        if str(variable.u) == 'dimensionless':
            suffix = None
        else:
            suffix = r'\,' + '{:Lx}'.format(variable.u)
        value = variable.magnitude
    else:
        suffix = None
        value = variable
    has_error = hasattr(value, 'std_dev')
    if has_error:
        payload = '{:L}'.format(value)
    else:
        payload = str(value)
    if suffix is not None:
        if has_error:
            payload = '({}){}'.format(payload, suffix)
        else:
            payload += suffix
    return payload

def save_formatted_variable(value: str, name: str, path: str) -> None:
    """
    Creates `name.dat` at the directoriy specified by `path` containing `value`.

    Args:
       value: Vale to be saved.
       name: Filename of output.
       path: Directory to create file at.
    """
    file_path = '{}/{}.dat'.format(path, name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w+') as file:
        data = file.read()
        file.seek(0)
        file.write(value)
        file.truncate()

def save(variable, name: str='variable', path: str=None) -> None:
    """"
    Saves `variable` as a string in `path/name.dat` according to LaTeX math typesetting.

    If path is missing, a `variables` folder is created in the project root directory.
    In case `name` is not specified, the file is named 'variable'.

    Args:
        variable: A python variable to be saved.
        name (optional): Filename to be used. When not specified, name `variable` is used.
        path (optional): Path to save `name.dat`, defaults to `.variables/`.
    """        
    if path is None:
        path = 'variables/'
    formatted_variable = typeset_latex_math(variable)
    save_formatted_variable(formatted_variable, name, path)