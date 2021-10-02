import requests

from pyinfra.operations import apt, python, server

# Assumes the repo is configured/apt is updated
apt.packages(
    name='Install ZeroTier',
    packages=['zerotier-one'],
)

def authorize_server(state, host):
    # Run a command on the server and collect status, stderr and stdout
    status, stdout, stderr = host.run_shell_command('cat /var/lib/zerotier-one/identity.public')
    assert status is True  # ensure the command executed OK

    # First line of output is the identity
    server_id = stdout[0]

    # Authorize via the ZeroTier API
    response = requests.post('https://my.zerotier.com/.../{0}'.format(server_id))
    response.raise_for_status()

python.call(
    name='Authorize the server on ZeroTier',
    function=authorize_server,
)

server.shell(
    name='Execute some shell',
    commands=['echo "back to other operations!"'],
)

