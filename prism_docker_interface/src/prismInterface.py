import os
import docker
import paramiko
import subprocess as sp


class PrismInterface():
    """
    Interface class to use PRISM either on local pc or on docker

    For installing prism locally, see https://www.prismmodelchecker.org/

    For Dockerfile, see https://github.com/aria-systems-group/prism-docker
    Build docker image with the command `docker build -t prism .`
    To run a docker container, first cd to the home directory of
    regret_synthesis_toolbox library and then run
    `run_docker.sh` located in the home directory.
    This will start a docker container and we can now send commands to this container
    using this PrismInterface class.

    If you change prism_binary to prismgames, you can also interact with prism-games
    """

    def __init__(self, prism_binary: str = 'prism',
                 use_docker: bool = False, image_name: str = 'prism', container_name: str = None,
                 hostname: str = None, port: int = 22, username: str = None, password: str = None,
                 local_dir: str=os.path.join(os.getcwd(), 'prism'), remote_dir='/prism/configs'):
        """
        Tell PrismInterface where the prism binary is.
        Either
        1. If prism_binary is not specified => We will use local binary prism OR prismgames
        2. You can specify the binary location e.g.) `/SOMEWHERE/prism`
        3. You can choose to use prism-docker and access prism in a docker container
        4. Similarly you can use ssh to access a docker container
        You will need hostname (required), address, username, and password if you have any
        """
        self._prism_binary = prism_binary

        # Initially, we assume that we are running locally
        self._interface_method = 'local'
        self._local_dir = local_dir
        self._remote_dir = local_dir

        if use_docker:
            self._interface_method = 'docker'
            self._image_name = image_name
            self._container_name = container_name
            self._remote_dir = remote_dir
        if hostname:
            self._interface_method = 'ssh'
            self._client = paramiko.SSHClient()
            self._client.connect(hostname, port, username, password)
            self._remote_dir = remote_dir

    def run_prism(self, model_filename: str, prop_filename: str = None,
                  get_help: bool = False, **kwargs) -> str:
        """
        Call prism command
        - Model file is required
        - Property is required
            - as a file
            - as a command
        """
        cmd = self._get_command(**kwargs)

        if get_help:
            prism_call = self._prism_binary + ' ' + '-help'
        else:
            if prop_filename:
                prism_call = self._prism_binary + ' ' + model_filename + ' ' + prop_filename + ' ' + cmd
            else:
                if 'pctl' not in kwargs:
                    raise ValueError('Please provide either a property file or pctl formula')
                prism_call = self._prism_binary + ' ' + model_filename + ' ' + cmd

        completed_process = self._run_command(prism_call)

        return completed_process

    def _get_command(self, **kwargs) -> str:
        """
        gets a list of popt commands to send the binary

        :param      kwargs:  The flexfringe tool keyword arguments

        :returns:   The list of commands.
        """

        # default argument is to print the program's man page
        if(len(kwargs) > 1):
            cmds = []
            for key, value in kwargs.items():
                if isinstance(value, bool) and value:
                    c = '-' + key
                else:
                    c = '-' + key + ' ' + str(value)
                cmds.append(c)
            cmd = ' '.join(cmds)
        else:
            cmd = '-help'
            print('no options specified, printing tool help:')

        return cmd

    def _run_command(self, command_string: str):
        """
        Run provided command on either local, docker or ssh
        """
        if self._interface_method == 'local':
            completed_process = sp.run(command_string)
            return completed_process.stdout.decode()

        elif self._interface_method == 'docker':
            if self._container_name:
                container_name = self._container_name
            else:
                client = docker.from_env()
                cl = client.containers.list(filters={'ancestor': self._image_name})
                if len(cl) <= 0:
                    msg = f'There is no running container whose image name is {self._image_name}'
                    raise NameError(msg)
                elif len(cl) >= 2:
                    print(f'There are multiple containers with same image name. Please choose from the following option. Either specify the index or the container name\n')
                    choice = input('\n'.join([f'[{i}] {c.name}' for i, c in enumerate(cl)]))
                    include_number = lambda s: bool(re.search(r'\d', choice))
                    if include_number(choice):
                        index = int(choice)
                    else:
                        for i, c in enumerate(cl):
                            if c.name == choice:
                                index = i
                else:
                    index = 0

                container_name = cl[index].name

            command_string = f'docker exec -it {container_name} {command_string}'
            completed_process = sp.run(command_string, shell=True,
                                       stdout=sp.PIPE, stderr=sp.PIPE)
            return completed_process.stdout.decode()

        elif self._interface_method == 'ssh':
            stdin, stdout, stderr = self._client.exec_command(command_string)
            return stdout

        else:
            raise NotImplementedError('Choose either local or docker')
