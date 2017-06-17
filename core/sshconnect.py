from json import load
from .objdict import Objdict
from subprocess import call


def connect_to(connection):
    """Connect to selected host

    Parameters:
    -----------
    connection: Objdict
        The connection object

    Returns:
    --------
    None
    """

    conn_cmd = 'ssh {username}@{host}'.format(username=connection.user, host=connection.host)
    if connection.X11:
        conn_cmd = '{} -X'.format(conn_cmd)
    try:
        conn_cmd = '{} -p{}'.format(conn_cmd, connection.port)
    except AttributeError:
        pass
    call(conn_cmd, shell=True)


def get_connections(filename):
    """Parse a JSON file to dict

    Parameters:
    -----------
    filename: str
        /path/to/jsonfile.json

    Returns:
    --------
    list
        The connections
    """

    with open(file=filename) as jsonfile:
        connections = load(jsonfile)
    return connections


def select_connection(connections):
    """Show connections list to user select

    Parameters:
    -----------
    connections: list
        A list of connections

    Returns:
    --------
    Objdict
        The selected connection
    """

    while True:
        for index, connection in enumerate(connections):
            print('  \033[1m{}\033[0m\t{} server'.format(index, connection['name']))
        try:
            conn = int(input('Choose connection: '))
            s_conn = connections[conn]
            connection = Objdict({'X11': s_conn['X11'],
                                  'user': s_conn['user']})
            access_type = input('(I)nternal or (E)xternal Access: ')
            if access_type is 'E' or access_type is 'e':
                connection.update(s_conn['external'])
            elif access_type is 'I' or access_type is 'i':
                connection.update(s_conn['internal'])
            else:
                print('\033[1mInvalid connection type. Please try again!\033[0m')
            return connection
        except IndexError:
            print('\033[1mInvalid connection number. Please try again!\033[0m')
        except ValueError:
            print('\033[1mOnly digits are allowed! Please try again!\033[0m')
