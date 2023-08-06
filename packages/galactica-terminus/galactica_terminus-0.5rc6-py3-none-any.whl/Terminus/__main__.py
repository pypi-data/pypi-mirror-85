# -*- coding: utf-8 -*-
# This software is part of the 'gal-terminus' software project.
#
# Copyright © Commissariat a l'Energie Atomique et aux Energies Alternatives (CEA)
#
#  FREE SOFTWARE LICENCING
#  -----------------------
# This software is governed by the CeCILL license under French law and abiding by the rules of distribution of free
# software. You can use, modify and/or redistribute the software under the terms of the CeCILL license as circulated by
# CEA, CNRS and INRIA at the following URL: "http://www.cecill.info". As a counterpart to the access to the source code
# and rights to copy, modify and redistribute granted by the license, users are provided only with a limited warranty
# and the software's author, the holder of the economic rights, and the successive licensors have only limited
# liability. In this respect, the user's attention is drawn to the risks associated with loading, using, modifying
# and/or developing or reproducing the software by the user in light of its specific status of free software, that may
# mean that it is complicated to manipulate, and that also therefore means that it is reserved for developers and
# experienced professionals having in-depth computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling the security of their systems and/or data
# to be ensured and, more generally, to use and operate it in the same conditions as regards security. The fact that
# you are presently reading this means that you have had knowledge of the CeCILL license and that you accept its terms.
#
#
# COMMERCIAL SOFTWARE LICENCING
# -----------------------------
# You can obtain this software from CEA under other licencing terms for commercial purposes. For this you will need to
# negotiate a specific contract with a legal representative of CEA.
#
"""
@author: Damien CHAPON (damien.chapon@cea.fr)
@author: Loic STRAFELLA (loic.strafella@cea.fr)
"""
import sys
import stat
import os
import shutil
import socket
import getpass
import argparse
from datetime import datetime
import readline
import glob
import re


def _fpath_auto_complete(text, state):
    if text.startswith("~"):
        search_path = os.path.expanduser(text)
    elif text.startswith("$"):
        search_path = os.path.expandvars(text)
    else:
        search_path = text
    return (glob.glob(search_path+'*')+[None])[state]


# Set filepath auto completion for input() calls
readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(_fpath_auto_complete)


class TerminusConfigManager(object):
    IP_ADDR_REGEXP = re.compile("^((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]\\d|\\d)\\.){3}"
                                "(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]\\d|\\d)$")
    _RABBITMQ_SECRET_FILE = "rabbitmq_server_pwd"
    _RABBITMQ_SECRET_DIR = "_secret"

    TERMINUS_ENV_FILE = "terminus.env"
    TERMINUS_SERVICE_FILE = "terminus.service"

    # _terminus_env_pythonpath = ""
    _job_scheduler_slurm = 0
    
    # config parameters
    terminus_parameters = {"TERMINUS_HOSTNAME": "", "TERMINUS_DOT_DIR": "", "TERMINUS_DATA_DIR": "",
                           "TERMINUS_JOB_DIR": "", "TERMINUS_ROOT": "", "TERMINUS_SERVICE_DIR": "", "User": "''",
                           "Group": "''", "TERMINUS_USE_SLURM": "", "RABBITMQ_USERNAME": "", "RABBITMQ_HOST": "",
                           "RABBITMQ_PORT": "", "RABBITMQ_VIRTUAL_HOST": ""}

    terminus_parameters_works = {"TERMINUS_DATA_DIR": False, "TERMINUS_JOB_DIR": False, "TERMINUS_SERVICE_DIR": False}

    # list of warning for path
    path_warning = []

    _terminus_celery_nodes = 2
    _terminus_celery_concurrency = 2

    def __init__(self):
        
        self._home_dir = os.path.expanduser("~")
        self._dot_terminus_dir = ".terminus"
        self._dot_terminus_path = os.path.join(self._home_dir, self._dot_terminus_dir)

        self._terminus_root_dir = os.path.dirname(os.path.abspath(__file__))

        # Terminus template directory that contains terminus.env and terminus.service template files
        self._terminus_template_dir = os.path.join(self._terminus_root_dir, "etc")

        self.terminus_parameters["TERMINUS_ROOT"] = self._terminus_root_dir

        # This makes great bug in case of Python 2 job script 
        #
        # get PYTHONPATH from user env
        # 
        # try:
        #     self._terminus_env_pythonpath = os.environ['PYTHONPATH']
        # except KeyError:
        #     self._terminus_env_pythonpath = ""
        
        # self._terminus_env_pythonpath += ":" + self._terminus_root_dir

        # get celery bin directory
        celery_name = {'linux': 'celery', 'win32': 'celery.exe'}[sys.platform]
        self._terminus_celery_path = os.path.join(os.path.dirname(sys.executable), celery_name)

        # this suppose that terminus.env and terminus.service are in .terminus directory which is supposed
        # to be at ~/.terminus
        self._terminus_env_file_path = os.path.join(self._dot_terminus_path, self.TERMINUS_ENV_FILE)
        self._terminus_serv_file_path = os.path.join(self._dot_terminus_path, self.TERMINUS_SERVICE_FILE)
        self._rabbitmq_secret_path = os.path.join(self._dot_terminus_path, self._RABBITMQ_SECRET_DIR)
        
        # check terminus directory
        if not os.path.isdir(self._dot_terminus_path):
            print("\n\t> Creating '%s' directory into the '%s' directory." % (self._dot_terminus_path, self._home_dir))
            os.makedirs(self._dot_terminus_path)  # Create `~/.terminus` directory

            # self._rabbitmq_secret_path = os.path.join(self._dot_terminus_path, self._RABBITMQ_SECRET_DIR)
            print("\t> Creating '%s' directory into the '%s' directory." % (self._RABBITMQ_SECRET_DIR,
                                                                            self._dot_terminus_path))
            os.makedirs(self._rabbitmq_secret_path)  # Create `~/.terminus/_secret` directory

            # copy terminus.env template to .terminus directory
            from_file = os.path.join(self._terminus_template_dir, self.TERMINUS_ENV_FILE)
            to_file = os.path.join(self._home_dir, self._dot_terminus_path)
            shutil.copy2(from_file, to_file)

            # copy terminus.service template to .terminus directory
            from_file = os.path.join(self._terminus_template_dir, self.TERMINUS_SERVICE_FILE)
            shutil.copy2(from_file, to_file)

            self.set_default_parameters()
        else:
            print("\nFound a '.terminus' directory into the home directory\n")
            self.load_terminus_config()

            # this is require because the load_terminus_config overide TERMINUS_ROOT key
            self.terminus_parameters["TERMINUS_ROOT"] = self._terminus_root_dir

    @property
    def template_dir(self):
        return self._terminus_template_dir

    def set_default_parameters(self):
        """
        Set default parameters for terminus_parameters
        """
        
        self.terminus_parameters["TERMINUS_HOSTNAME"] = (socket.gethostname()).lower()
        self.terminus_parameters["TERMINUS_DOT_DIR"] = self._dot_terminus_path

        # self.terminus_parameters["TERMINUS_WORKDIR"] = self._home_dir

        self.terminus_parameters["TERMINUS_DATA_DIR"] = self._home_dir
        self.terminus_parameters["TERMINUS_JOB_DIR"] = self._home_dir
        self.terminus_parameters["TERMINUS_SERVICE_DIR"] = self._home_dir

        self.terminus_parameters["TERMINUS_USE_SLURM"] = 0  # False by default

        self.terminus_parameters["User"] = getpass.getuser()
        self.terminus_parameters["Group"] = self.terminus_parameters["User"]

        # Default values
        self._terminus_celery_nodes = 2
        self._terminus_celery_concurrency = 2

    def load_terminus_config(self):
        """ 
        Load a terminus configuration file from home directory
        """
        # check if there is a terminus.env file in .terminus directory
        if not os.path.isfile(self._terminus_env_file_path):
            print("> No '%s' file found, create a new one from terminus template.\n" % self._terminus_env_file_path)

            # copy terminus.env template to .terminus directory
            from_file = os.path.join(self._terminus_template_dir, self.TERMINUS_ENV_FILE)
            to_file = os.path.join(self._home_dir, self._dot_terminus_path)
            shutil.copy2(from_file, to_file)

            self.set_default_parameters()

        else:

            # datetime object containing current date and time
            now = datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")

            # save current terminus.env by copying it to terminus.env.dat and
            # we'll override the terminus.env file
            from_file = self._terminus_env_file_path
            to_file = from_file + "." + dt_string

            shutil.copy2(from_file, to_file)
            print("> terminus.env configuration file found !")
            print("\t> backup to : '%s' \n" % to_file)
        
        # check if there is a terminus.service file in .terminus directory
        if not os.path.isfile(self._terminus_serv_file_path):
            print("> No '{tsfp:s}' file found, create a new one from terminus "
                  "template.\n".format(tsfp=self._terminus_serv_file_path))

            # copy terminus.service template to .terminus directory
            from_file = os.path.join(self._terminus_template_dir, self.TERMINUS_SERVICE_FILE)
            to_file = os.path.join(self._home_dir, self._dot_terminus_path)
            shutil.copy2(from_file, to_file)

            return
        else:

            # datetime object containing current date and time
            now = datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")

            # save current terminus.env by copying it to terminus.env.dat and
            # we'll override the terminus.env file
            from_file = self._terminus_serv_file_path
            to_file = from_file + "." + dt_string

            shutil.copy2(from_file, to_file)
            print("> terminus.service configuration file found !")
            print("\t> backup to : '%s' \n" % to_file)
        
        # open terminus.env file if it exists
        try:
            lines = []
            with open(self._terminus_env_file_path, "r") as f:
                lines = f.readlines()
        except IOError:
            print("Error trying to open terminus.env file")

        for tmp in lines:
            # let suppose the user use CELERY_NODES=n and not CELERY_NODES="w1@machine w2@machine w3@machine"
            if "CELERYD_NODES" in lines and "#" not in lines:
                self._terminus_celery_nodes = tmp.replace("\n", "").split("=")[1]
            
            elif "CELERYD_OPTS" in lines:
                self._terminus_celery_concurrency = tmp.replace("\n", "").split("=")[2].split(" ")[0]

            else:
                for k in self.terminus_parameters.keys():
                    if k in tmp:
                        self.terminus_parameters[k] = tmp.replace("\n", "").split("=")[1].replace("\"", "")
        
        self.terminus_parameters["TERMINUS_USE_SLURM"] = int(self.terminus_parameters["TERMINUS_USE_SLURM"])

        # should do better than that
        if self.terminus_parameters["TERMINUS_DOT_DIR"] == "__empty__":
            self.terminus_parameters["TERMINUS_DOT_DIR"] = self._dot_terminus_path

        # open terminus.service file
        try:
            lines = []
            with open(self._terminus_serv_file_path, "r") as f:
                lines = f.readlines()
        except IOError:
            print("Error trying to open terminus.service file")

        for tmp in lines:
            for k in self.terminus_parameters.keys():
                if k in tmp:
                    self.terminus_parameters[k] = tmp.replace("\n", "").split("=")[1]
        
        if self.check_terminus_config():
            print("Problem in terminus environment variables")

        # But we'll lost previous configuration if user cancel unless we read a
        # temrinus.env.date file
        #
        # this fix the ugly bug of having old var defined in existed terminus.env file
        # and allow to use always the last version of terminus.env template.
        #
        # copy terminus.env template to .terminus directory
        from_file = os.path.join(self._terminus_template_dir, self.TERMINUS_ENV_FILE)
        to_file = os.path.join(self._home_dir, self._dot_terminus_path)
        shutil.copy2(from_file, to_file)

        # this fix the ugly bug of having old var defined in existed terminus.service file
        # and allow to use always the last version of terminus.service template.
        #
        # copy terminus.service template to .terminus directory
        from_file = os.path.join(self._terminus_template_dir, self.TERMINUS_SERVICE_FILE)
        to_file = os.path.join(self._home_dir, self._dot_terminus_path)
        shutil.copy2(from_file, to_file)

        print("\nTerminus configuration loaded, ready to update.\n")

    def configure_terminus(self):
        """
        Configure terminus environment variables. In case of "enter hit" a defaut value
        """
        # self.terminus_parameters["TERMINUS_HOSTNAME"] = input("Enter a terminus host name (current %s): " %
        # self.terminus_parameters["TERMINUS_HOSTNAME"])
        tmp = input("Enter a terminus host name (current '%s'): " % self.terminus_parameters["TERMINUS_HOSTNAME"])
        if not tmp.replace(" ", ""):
            # small trick to be sure the HOSTNAME is not in MAJ
            self.terminus_parameters["TERMINUS_HOSTNAME"] = self.terminus_parameters["TERMINUS_HOSTNAME"].lower()
            print("\t> Default value used\n")
        else:
            self.terminus_parameters["TERMINUS_HOSTNAME"] = tmp.lower()

        # tmp = input("Enter a terminus work directory (current %s): " % self.terminus_parameters["TERMINUS_WORKDIR"])
        # if ( not tmp.replace(" ", "") ):
        #     print("\t> Default value used")
        # else:
        #     self.terminus_parameters["TERMINUS_WORKDIR"] = tmp
        
        # tmp = input("Enter a terminus data directory (current '%s'): " % self.terminus_parameters["TERMINUS_DATA_DIR"])
        # if not tmp.replace(" ", ""):
        #     print("\t> Default value used\n")
        # else:
        #     self.terminus_parameters["TERMINUS_DATA_DIR"] = tmp
        self.ask_path("TERMINUS_DATA_DIR", "terminus data directory")

        # tmp = input("Enter a terminus job directory (current '%s'): " % self.terminus_parameters["TERMINUS_JOB_DIR"])
        # if not tmp.replace(" ", ""):
        #     print("\t> Default value used\n")
        # else:
        #     self.terminus_parameters["TERMINUS_JOB_DIR"] = tmp
        self.ask_path("TERMINUS_JOB_DIR", "terminus job directory")
        
        # tmp = input("Enter a terminus service directory (current "
        #             "'{curr_serv_dir:s}'): ".format(curr_serv_dir=self.terminus_parameters["TERMINUS_SERVICE_DIR"]))
        # if not tmp.replace(" ", ""):
        #     print("\t> Default value used\n")
        # else:
        #     self.terminus_parameters["TERMINUS_SERVICE_DIR"] = tmp
        self.ask_path("TERMINUS_SERVICE_DIR", "terminus service directory")

        # Do not let the user the possibility to choose the User and Group for systemd
        # because the .terminus/ is created @ ${HOME}

        # tmp = input("Enter a terminus systemd user (current %s): " % self.terminus_parameters["User"])
        # if ( not tmp.replace(" ","") ):
        #     print("\t> Default value used")
        # else:
        #     self.terminus_parameters["User"] = tmp
        
        # tmp = input("Enter a terminus systemd group (current %s): " % self.terminus_parameters["Group"])
        # if ( not tmp.replace(" ","") ):
        #     print("\t> Default value used")
        # else:
        #     self.terminus_parameters["Group"] = tmp

        tmp = input("Enter a terminus number of nodes (current %s): " % self._terminus_celery_nodes)
        if not tmp.replace(" ", ""):
            print("\t> Default value used\n")
        else:
            self._terminus_celery_nodes = tmp

        tmp = input("Enter a terminus number of concurrency/node (current %s): " % self._terminus_celery_concurrency)
        if not tmp.replace(" ", ""):
            print("\t> Default value used\n")
        else:
            self._terminus_celery_concurrency = tmp

        val = 'N'
        val_int = 0
        if self.terminus_parameters["TERMINUS_USE_SLURM"] > 0:
            val = 'Y'
            val_int = 1
        
        tmp = input("Use SLURM for job submission ? (Y/n) (current %s): " % val)
        tmp = tmp.replace(" ", "")

        if not tmp:
            print("\t> Default value used\n")
            self.terminus_parameters["TERMINUS_USE_SLURM"] = val_int
        else:
            if tmp == 'Y' or tmp == 'y':
                self.terminus_parameters["TERMINUS_USE_SLURM"] = 1
            else:
                self.terminus_parameters["TERMINUS_USE_SLURM"] = 0

        print("\n------------------ RabbitMQ configuration ---------------\n")
        
        tmp = input("Enter a rabbitmq username (current '%s'): " % self.terminus_parameters["RABBITMQ_USERNAME"])
        if not tmp.replace(" ", ""):
            print("\t> Current value used\n")
        else:
            self.terminus_parameters["RABBITMQ_USERNAME"] = tmp

        while True:
            tmp = input("Enter a rabbitmq host IP (current '%s'): " % self.terminus_parameters["RABBITMQ_HOST"])
            if not tmp.replace(" ", ""):
                print("\t> Current value used\n")
                break
            else:
                if self.IP_ADDR_REGEXP.match(tmp) is not None:
                    self.terminus_parameters["RABBITMQ_HOST"] = tmp
                    break
                else:
                    print("\tInvalid IP address (format required: 'xxx.xxx.xxx.xxx').\n")
        
        tmp = input("Enter a rabbitmq port (current '%s'): " % self.terminus_parameters["RABBITMQ_PORT"])
        if not tmp.replace(" ", ""):
            print("\t> Current value used\n")
        else:
            self.terminus_parameters["RABBITMQ_PORT"] = tmp
        
        tmp = input("Enter a rabbitmq virtual host (current "
                    "'{rmq_vhost:s}'): ".format(rmq_vhost=self.terminus_parameters["RABBITMQ_VIRTUAL_HOST"]))
        if not tmp.replace(" ", ""):
            print("\t> Current value used\n")
        else:
            self.terminus_parameters["RABBITMQ_VIRTUAL_HOST"] = tmp
        
        rabbitmq_pwd_file_path = os.path.join(self._rabbitmq_secret_path, self._RABBITMQ_SECRET_FILE)
        
        # Attempt to create file for rabbitmq password
        if not os.path.isfile(rabbitmq_pwd_file_path):
            with open(rabbitmq_pwd_file_path, "w") as tempo:
                tempo.write("__DUMMY_PASSWD__")
            print("\n> Now add the given RabbitMQ server password in this file: %s" % rabbitmq_pwd_file_path)

        # Set sensitive information file permission to read|write for the user only.
        os.chmod(rabbitmq_pwd_file_path, stat.S_IREAD | stat.S_IWRITE)  # chmod 600 _secret/rabbitmq_server_pwd

        print("\n----------- RabbitMQ configuration completed -------------")
        
        print("\n> Configured User: %s" % self.terminus_parameters["User"])
        print("> Configured Group: %s\n" % self.terminus_parameters["Group"])

        # check for warning
        if len(self.path_warning) != 0:
            for k in self.path_warning:
                print("\t> Directory '%s' does not exist. This directory must be created before launching Terminus !\n"\
                        % (self.terminus_parameters[k]) )


        # if self.check_terminus_config():
        #     print("Problem in terminus environment variables, check your path !")
        #     return False
        # else:
        #     print("Path checked successfuly !")
        
        tmp = input("Save configuration ? [Y/n]: ")
        tmp = tmp.replace(" ", "")
        if tmp == 'Y' or tmp == 'y':
            if not self.write_terminus_config():
                print("Error while writting terminus_config file !")
                return False
            else:
                print("Terminus configuration file written successfuly.")
        else:
            print("Aborting.")

            # not really awesome but works
            self.load_terminus_config()

            # same as previously said. load_terminus_config override TERMINUS_ROOT key
            self.terminus_parameters["TERMINUS_ROOT"] = self._terminus_root_dir

            return False
        
        return True
    
    def ask_path(self, terminus_var, user_text):
        """
        Ask for a 'terminus_var' which must be a path. Display 'user_text' in prompt.
        Test if directory provided by user exist and if not propose to create it.
        """
        while True:
            tmp = input("Enter a %s (current '%s'): " % (user_text, self.terminus_parameters[terminus_var]))

            if not tmp.replace(" ", "") and self.terminus_parameters[terminus_var] != "__empty__":
                print("\t> Default value used\n")
                break
            else:
                self.terminus_parameters[terminus_var] = tmp

            if not os.path.isdir(tmp):
                rst = input("\t> Directory '%s' does not exist. Create directory ? (Y/n) : " % tmp)
                if rst.replace("\n", "").replace(" ", "").lower() == "y":
                    try:
                        os.makedirs(tmp)
                    except OSError:
                        print ("Creation of the directory %s failed" % tmp)
                    else:
                        print ("\t> Successfully created the directory '%s'. \n" % tmp)
                        break
                else:
                    # user says thanks, but no thanks for directory creation
                    self.path_warning.append(terminus_var)
                    break
            else:
                break

    def check_terminus_config(self):
        """
        Check terminus environment variables that are path to directory
        """
        problem = False

        for k in self.terminus_parameters.keys():
            if os.path.isdir(self.terminus_parameters[k]):
                self.terminus_parameters_works[k] = True

        for k in self.terminus_parameters_works.keys():
            if not self.terminus_parameters_works[k]:
                print("Error with '%s' for key '%s', directory does not exist !"%(self.terminus_parameters[k], k))
                problem = True
        
        # check that user and group match, if not fix them
        tmp = getpass.getuser()
        if getpass.getuser() != self.terminus_parameters["User"]:
            print("\t> Warning configured 'User' and 'Group' from terminus.service does not match current user !")
            self.terminus_parameters["User"] = tmp
            self.terminus_parameters["Group"] = tmp

        return problem

    def write_terminus_config(self):
        """
        Write terminus.env and terminus.service file in home directory with modified parameters
        """
        # For the terminus.env file
        if self._terminus_env_file_path is None:
            print("Error something went wrong, there is no _terminus_env_file_path set ! ")
            return False

        with open(self._terminus_env_file_path, "r") as f:
            lines = f.readlines()

        # print("TERMINUS_ROOT = " , self.terminus_parameters["TERMINUS_ROOT"])

        for i in range(0,len(lines)):
            if "CELERYD_PID_FILE" in lines[i]:
                lines[i] = "CELERYD_PID_FILE=" + os.path.join(self._dot_terminus_path, "pids", "%n.pid") + "\n"
            elif "CELERYD_LOG_FILE" in lines[i]:
                lines[i] = "CELERYD_LOG_FILE=" + os.path.join(self._dot_terminus_path, "logs", "%n.log") + "\n"
            elif "CELERY_BIN" in lines[i]:
                lines[i] = "CELERY_BIN=\"" + self._terminus_celery_path + "\"\n"
            elif "CELERYD_NODES" in lines[i] and "#" not in lines[i]:
                lines[i] = "CELERYD_NODES=" + str(self._terminus_celery_nodes) + "\n"
            elif "CELERYD_OPTS" in lines[i]:
                lines[i] = "CELERYD_OPTS=\"--concurrency=" + str(self._terminus_celery_concurrency) + " -Q " + \
                           self.terminus_parameters["TERMINUS_HOSTNAME"] + ".terminus_jobs\"\n"
            else:
                for k in self.terminus_parameters.keys():
                    if k in lines[i]:
                        lines[i] = k + "=\"" + str(self.terminus_parameters[k]) + "\"\n"
        
        with open(self._terminus_env_file_path, "w") as f:
            for tmp in lines:
                f.write(tmp)
        
        # For the terminus.service file
        if self._terminus_serv_file_path is None:
            print("Error something went wrong, there is no _terminus_serv_file_path set ! ")
            return False

        lines = []
        with open(self._terminus_serv_file_path, "r") as f:
            lines = f.readlines()

        for i in range(0, len(lines)):
            if "EnvironmentFile" in lines[i]:
                lines[i] = "EnvironmentFile=" + self._terminus_env_file_path + "\n"
            elif "WorkingDirectory" in lines[i]:
                lines[i] = "WorkingDirectory=" + self.terminus_parameters["TERMINUS_JOB_DIR"] + "\n"
            else:
                for k in self.terminus_parameters.keys():
                    if k in lines[i]:
                        lines[i] = k + "=" + self.terminus_parameters[k] + "\n"
        
        with open(self._terminus_serv_file_path, "w") as f:
            for tmp in lines:
                f.write(tmp)

        return True


def check_current_config(tcm):
    """
    Check the current config file

    Parameters
    ----------
    tcm: TerminusConfigManager object
    """
    env_fpath = os.path.join(tcm.template_dir, "terminus.env")
    try:
        lines = []
        with open(env_fpath, "r") as f:
            lines = f.readlines()
    except IOError:
        print("Error with file {evfp:s} ".format(evfp=env_fpath))

    for tmp in lines:
        for k in tcm.config_parameters.keys():
            if k in tmp:
                tcm.config_parameters[k] = tmp.replace("\n", "").split("=")[1]


def server_config(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    print("\n# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #")
    print("# ~~~~~~~~~~~~~~~~~~~~~~ Terminus server configuration helper ~~~~~~~~~~~~~~~~~~~~~~~ #")
    print("# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #\n")
    config_manager = TerminusConfigManager()
    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do. Return values are exit codes.

    # parser = argparse.ArgumentParser(description="Run on-demand data post-processing server for the Galactica "
    #                                              "astrophysical simulation database")
    # parser.add_argument('--debug', dest='debug', action='store_true', help='Run in debug mode')
    # pargs = parser.parse_args()
    # is_debug = pargs.debug

    while True:
        try:
            res = handle_action(config_manager)
            if not res:
                break
        except KeyboardInterrupt:

            # save current state of configuration
            config_manager.write_terminus_config()

            print("\nCanceled...\n"
                  "# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #")
            break
    return 0


def handle_action(cfg_manager: TerminusConfigManager):
    """
    Handle user command-line interaction

    Parameters
    ----------
    cfg_manager: :class:`Terminus.TerminusConfigManager`
    """
    print("Select an option :\n"
          " - [1] Configure Terminus \n"
          " - [2] Quit ")
    
    try:
        option = int(input("\nYour choice ? : "))
        if option not in [1, 2]:
            print("Error: Valid choices are [1, 2]")
            return True
    except SyntaxError:
        option = 1

    if option == 2:
        print("\nDone...\n"
              "# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #")
        return False

    else:  # if option == 1:
        print("Configuration of Terminus")
        is_ok = cfg_manager.configure_terminus()

        if not is_ok:
            return True


if __name__ == "__main__":
    sys.exit(server_config())
