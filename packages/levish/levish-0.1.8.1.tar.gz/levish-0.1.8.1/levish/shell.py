import os
from shlex import split as _split

from pyfiglet import figlet_format

from .utils import only_varargs as _only_varargs

#* ------------------------
#* --- Main Shell class ---
#* ------------------------

class Shell:
    """Creates a new Shell object
    
    Args:
        name (str): Name of the shell.
        show_cwd (bool, optional): Add current working directory to prefix, defaults to "False"
        prefix (str, optional): Shell prefix, defaults to "[>]"
        figlet (bool, optional): Enable figlet print on first start, defaults to "False"
        figlet_font (str, optional): Change figlet font, defaults to "standard"
    """
    def __init__(self, name, show_cwd=False, prefix="[>] ", figlet=False, figlet_font="standard"):
        self._name = name
        self._show_cwd = show_cwd
        self._prefix = prefix
        self._commands = {}
        self._help = ""
        self._figlet = figlet
        self._figlet_font = figlet_font
        self._looping = True

        self._add_internal_command(self._cmd_help, custom_cmd="help", description="Shows this help")
        self._add_internal_command(self._cmd_exit, custom_cmd="exit", description="Exit the shell")
        self._add_internal_command(self._cmd_about, custom_cmd="about", description="Show some info")


    #* ---------------------
    #* --- loop function ---
    #* ---------------------

    def _loop(self):
        """Main loop waiting for input and executing functions.

        Loop can be exited by calling "_break_loop()"
        """
        while self._looping:
            if self._show_cwd:
                inp = input(f"{self._name}@{os.getcwd()} {self._prefix}")
            else:
                inp = input(self._prefix)

            if (len(inp)) > 0:
                cmd, args = inp.split()[0], _split(inp)[1:]
                if cmd in self._commands:
                    self._exec_command(cmd, args)
                else:
                    print(f"Command '{cmd}' does not exist. Try 'help'")
                print("")
            else:
                continue

    def _exec_command(self, cmd, args):
        """Execute command with given args

        Args:
            cmd (str): key
            args (list): list of arguments
        """
        self._commands[cmd]["func"](*args)

    #* ----------------------------
    #* --- add command function ---
    #* ----------------------------
    def add_command(self, function, custom_cmd=None, description="No description"):
        """Add a new command to the Shell

        Args:
            function (function): Function that is called
            custom_cmd (str, optional): Overwrite command that has to be typed to call function. Default command name is function.__name__
            description (str, optional): Add a description. Defaults to "No description"

        Raises:
            CommandAlreadyExistError: Raised when added command already exists
            MissingVargsInFunctionError: Raised when passed in function has no *args as argument
            FunctionNotCallableError: Raised when passed in function is not a function
        """
        if callable(function):
            if _only_varargs(function, "args"):
                if custom_cmd != None and type(custom_cmd) == str:
                    cmd = custom_cmd
                else:
                    cmd = function.__name__
                if not cmd in self._commands:
                    self._commands[cmd] = {
                        "func": function,
                        "desc": description
                    }
                else:
                    raise CommandAlreadyExistError(cmd)
            else:
                raise MissingVargsInFunctionError(function.__name__) # (or wrong name)
        else:
            raise FunctionNotCallableError(function.__name__)


    def _add_internal_command(self, function, custom_cmd, description):
        if callable(function):
            cmd = custom_cmd
            if not cmd in self._commands:
                self._commands[cmd] = {
                    "func": function,
                    "desc": description
                }
            else:
                raise CommandAlreadyExistError(cmd)
        else:
            raise FunctionNotCallableError(function.__name__)

    

    #* --------------------------------------
    #* --- other internal functions start ---
    #* --------------------------------------

    def _break_loop(self):
        """Break out of _loop by setting self._looping to False."""
        self._looping = False

    def _build_help(self):
        """Builds the help string that is displayed when the 'help' command is executed."""
        self._help = "------------------------\nCOMMAND: DESCRIPTION"
        for cmd in self._commands:
            self._help += f"\n{cmd}: {self._commands[cmd]['desc']}"
        self._help += "\n------------------------"



    #* -------------------------
    #* --- internal commands ---
    #* -------------------------

    def _cmd_help(self, *args):
        if len(args) > 0:
            if args[0] in self._commands:
                print(self._commands[args[0]]["desc"])
            else:
                print(f"Command '{args[0]}' not found")
        else:
            print(self._help)

    def _cmd_exit(self, *args):
        self._break_loop()

    def _cmd_about(self, *args):
        print(
"""
Running levish v0.1.7.3\n
Made with love by aaronlyy
Github: github.com/aaronlyy/levish
"""
)

    #* --------------------
    #* --- run function ---
    #* --------------------

    def run(self):
        """Initialize the Shell and run self._loop"""
        # create help string
        self._build_help()
        # splash (figlet)
        if self._figlet:
            print(figlet_format(self._name, self._figlet_font))
        # start main loop
        self._loop()



    #* -------------------------
    #* --- custom exceptions ---
    #* -------------------------

class LevishError(Exception):
    pass

class CommandAlreadyExistError(LevishError):
    def __init__(self, cmd):
        self.message = f"'{cmd}': This command already exists."

    def __str__(self):
        return self.message

class FunctionNotCallableError(LevishError):
    def __init__(self, function_name):
        self.message = f"'{function_name}': The passed in function is not a callable object."

    def __str__(self):
        return self.message

class MissingVargsInFunctionError(LevishError):
    def __init__(self, function_name):
        self.message = f"'{function_name}': Missing '*args' in passed in function."

    def __str__(self):
        return self.message