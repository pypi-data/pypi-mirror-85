# -*- coding: utf-8 -*-
# This software is part of the Galactica software project.
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
"""

# No longer needed in Python 3
# import exceptions
import os


class PostProcessingServiceNotFoundError(BaseException):
    def __init__(self, service_name):
        super(PostProcessingServiceNotFoundError, self).__init__()
        self.not_found_service = service_name


class JobSubmissionError(BaseException):
    def __init__(self, err_msg):
        super(JobSubmissionError, self).__init__()
        self.error_message = err_msg


class DataDirectoryNotFoundError(BaseException):
    def __init__(self, path):
        super(DataDirectoryNotFoundError, self).__init__()
        self.not_found_path = path


class TerminusCommons(object):
    ENVVAR_TERMINUS_HOSTNAME = "TERMINUS_HOSTNAME"
    ENVVAR_ROOT_DIR = "TERMINUS_ROOT"
    ENVVAR_DOT_DIR = "TERMINUS_DOT_DIR"
    ENVVAR_SERVICE_DIR = "TERMINUS_SERVICE_DIR"
    ENVVAR_DATA_DIR = "TERMINUS_DATA_DIR"
    ENVVAR_JOBRUNS_DIR = "TERMINUS_JOB_DIR"
    ENVVAR_TERMINUS_USE_SLURM = "TERMINUS_USE_SLURM"

    ENVVAR_UPLOAD_HOST = "GALACSTORAGE_SSH_ALIAS"

    ENVVAR_RABBITMQ_USER = "RABBITMQ_USERNAME"
    ENVVAR_RABBITMQ_HOST = "RABBITMQ_HOST"
    ENVVAR_RABBITMQ_PORT = "RABBITMQ_PORT"
    ENVVAR_RABBITMQ_VIRTUAL_HOST = "RABBITMQ_VIRTUAL_HOST"

    PENDING_STATUS = 'pending'
    RUNNING_STATUS = 'running'
    FAILURE_STATUS = 'failed'
    TIMED_OUT_STATUS = 'timed_out'
    SUCCESS_STATUS = 'success'
    PUBLISHED_STATUS = 'uploaded'

    __instance = None

    def __new__(cls, debug=False):
        if TerminusCommons.__instance is None:
            TerminusCommons.__instance = super(TerminusCommons, cls).__new__(cls)
            TerminusCommons.__instance._init = False
        return TerminusCommons.__instance

    def __init__(self, debug=False):
        if self._init:
            return

        self._debug_mode = debug

        # Service + data + job run directory checks, set in environment variables
        try:
            self._terminus_hostname = os.environ[TerminusCommons.ENVVAR_TERMINUS_HOSTNAME]
            self._root_path = os.environ[TerminusCommons.ENVVAR_ROOT_DIR]
            
            # ref to ${HOME}/.terminus directory
            self._dot_dir = os.environ[TerminusCommons.ENVVAR_DOT_DIR]

            self._service_path = os.environ[TerminusCommons.ENVVAR_SERVICE_DIR]
            self._datadir_path = os.environ[TerminusCommons.ENVVAR_DATA_DIR]
            self._jobdir_path = os.environ[TerminusCommons.ENVVAR_JOBRUNS_DIR]

            self._use_slurm = False
            if int(os.environ[TerminusCommons.ENVVAR_TERMINUS_USE_SLURM]) > 0:
                self._use_slurm = os.environ[TerminusCommons.ENVVAR_TERMINUS_USE_SLURM]

            self._terminus_root_dir = os.path.dirname(os.path.abspath(__file__))
            self._upload_hostname = os.environ.get(TerminusCommons.ENVVAR_UPLOAD_HOST, 'Galactica')
            if not self._debug_mode:
                self._rabbitmq_user = os.environ[TerminusCommons.ENVVAR_RABBITMQ_USER]
                self._rabbitmq_host = os.environ[TerminusCommons.ENVVAR_RABBITMQ_HOST]
                self._rabbitmq_port = int(os.environ[TerminusCommons.ENVVAR_RABBITMQ_PORT])
                self._rabbitmq_vhost = os.environ[TerminusCommons.ENVVAR_RABBITMQ_VIRTUAL_HOST]
        except KeyError as ke:

            print("Environment variable '%s' is not set." % ke.args[0])
            self.get_env_var()
            # raise EnvironmentError("Environment variable '%s' is not set." % ke.args[0])

        # Get upload hostname (optional) set in alias & override if possible
        # try:
        #     self._upload_hostname = os.environ.get(TerminusCommons.ENVVAR_UPLOAD_HOST, 'Galactica')
        # except KeyError as ke:
        #     pass

        if not os.path.isdir(self._service_path):
            raise EnvironmentError("The path provided in the '%s' environment variable is not a valid directory." %
                                   TerminusCommons.ENVVAR_SERVICE_DIR)

        if not os.path.isdir(self._datadir_path):
            raise EnvironmentError("The path provided in the '%s' environment variable is not a valid directory." %
                                   TerminusCommons.ENVVAR_DATA_DIR)

        if not os.path.isdir(self._jobdir_path):
            raise EnvironmentError("The path provided in the '%s' environment variable is not a valid directory." %
                                   TerminusCommons.ENVVAR_JOBRUNS_DIR)

        if self._debug_mode:
            self._rabbitmq_user = "guest"
            self._rabbitmq_userpwd = "guest"
            self._rabbitmq_host = "localhost"
            self._rabbitmq_port = 8672
        else:
            # SECURITY WARNING: keep the rabbbitmq server password used in production secret!
            TERMINUS_SECRET_DIR = os.path.join(self._dot_dir, '_secret')
            with open(os.path.join(TERMINUS_SECRET_DIR, 'rabbitmq_server_pwd'), 'r') as f:
                self._rabbitmq_userpwd = f.read().strip()

        self._init = True

    # Test 
    def get_env_var(self):

        # we assume there is a .terminus directory @ ${HOME}
        _dot_dir = os.path.join(os.path.expanduser("~"), ".terminus")
        _dot_terminus_env_path = os.path.join(_dot_dir, "terminus.env")
        
        lines = []
        with open(_dot_terminus_env_path, "r") as f:
            lines = f.readlines()
        
        for tmp in lines:
            if "TERMINUS_HOSTNAME" in tmp:
                TerminusCommons.ENVVAR_TERMINUS_HOSTNAME = tmp.replace("\n", "").split("=")[1].replace("\"", "")
            elif "TERMINUS_DOT_DIR" in tmp:
                TerminusCommons.ENVVAR_DOT_DIR = tmp.replace("\n", "").split("=")[1].replace("\"", "")
            elif "TERMINUS_DATA_DIR" in tmp:
                TerminusCommons.ENVVAR_DATA_DIR = tmp.replace("\n", "").split("=")[1].replace("\"", "")
            elif "TERMINUS_JOB_DIR" in tmp:
                TerminusCommons.ENVVAR_JOBRUNS_DIR = tmp.replace("\n", "").split("=")[1].replace("\"", "")
            elif "TERMINUS_USE_SLURM" in tmp:
                self._use_slurm = False
                if int(tmp.replace("\n", "").split("=")[1].replace("\"", "")) > 0:
                    self._use_slurm = True
            elif "TERMINUS_SERVICE_DIR" in tmp:
                TerminusCommons.ENVVAR_SERVICE_DIR = tmp.replace("\n", "").split("=")[1].replace("\"", "")
            elif "TERMINUS_ROOT" in tmp:
                TerminusCommons.ENVVAR_ROOT_DIR = tmp.replace("\n", "").split("=")[1].replace("\"", "")
            elif "RABBITMQ_USERNAME" in tmp:
                TerminusCommons.ENVVAR_RABBITMQ_USER = tmp.replace("\n", "").split("=")[1].replace("\"", "")
            elif "RABBITMQ_HOST" in tmp:
                TerminusCommons.ENVVAR_RABBITMQ_HOST = tmp.replace("\n", "").split("=")[1].replace("\"", "")
            elif "RABBITMQ_PORT" in tmp:
                TerminusCommons.ENVVAR_RABBITMQ_PORT = tmp.replace("\n", "").split("=")[1].replace("\"", "")
            elif "RABBITMQ_VIRTUAL_HOST" in tmp:
                TerminusCommons.ENVVAR_RABBITMQ_VIRTUAL_HOST = tmp.replace("\n", "").split("=")[1].replace("\"", "")
            elif "GALACSTORAGE_SSH_ALIAS" in tmp:
                self._upload_hostname = tmp.replace("\n", "").split("=")[1].replace("\"", "")
            else:
                pass
        
        print("> Get env var initiated ! \n") 
        print("\t> TERMINUS_HOSTNAME: ", TerminusCommons.ENVVAR_TERMINUS_HOSTNAME)
        print("\t> TERMINUS_DOT_DIR: ", TerminusCommons.ENVVAR_DOT_DIR)
        print("\t> TERMINUS_DATA_DIR: ", TerminusCommons.ENVVAR_DATA_DIR)
        print("\t> TERMINUS_JOB_DIR: ", TerminusCommons.ENVVAR_JOBRUNS_DIR)
        print("\t> TERMINUS_SERVICE_DIR: ", TerminusCommons.ENVVAR_SERVICE_DIR)
        print("\t> TERMINUS_ROOT: ", TerminusCommons.ENVVAR_ROOT_DIR)
        print("\t> Upload hostname : ", self._upload_hostname)

        self._terminus_hostname = TerminusCommons.ENVVAR_TERMINUS_HOSTNAME
        self._root_path = TerminusCommons.ENVVAR_ROOT_DIR
        
        # ref to ${HOME}/.terminus directory
        self._dot_dir = TerminusCommons.ENVVAR_DOT_DIR

        self._service_path = TerminusCommons.ENVVAR_SERVICE_DIR
        self._datadir_path = TerminusCommons.ENVVAR_DATA_DIR
        self._jobdir_path = TerminusCommons.ENVVAR_JOBRUNS_DIR
        self._terminus_root_dir = TerminusCommons.ENVVAR_ROOT_DIR

        self._rabbitmq_user = TerminusCommons.ENVVAR_RABBITMQ_USER
        self._rabbitmq_host = TerminusCommons.ENVVAR_RABBITMQ_HOST
        self._rabbitmq_port = int(TerminusCommons.ENVVAR_RABBITMQ_PORT)
        self._rabbitmq_vhost = TerminusCommons.ENVVAR_RABBITMQ_VIRTUAL_HOST

    @property
    def debug(self):
        return self._debug_mode

    @property
    def use_slurm(self):
        return self._use_slurm

    @property
    def rabbitmq_url(self):
        return "amqp://{rabmq_user!s}:{rabmq_pwd!s}@{rabmq_host!s}:{rabmq_port:d}/{rabmq_vhost!s}"\
            .format(rabmq_user=self._rabbitmq_user, rabmq_pwd=self._rabbitmq_userpwd,
                    rabmq_host=self._rabbitmq_host, rabmq_port=self._rabbitmq_port, rabmq_vhost=self._rabbitmq_vhost)

    def __getitem__(self, item):
        if item == "hostname":
            return self._terminus_hostname
        elif item == "service_path":
            return self._service_path
        elif item == "datadir_path":
            return self._datadir_path
        elif item == "jobdir_path":
            return self._jobdir_path
        elif item == 'failed_jobs_dir':
            return os.path.join(self._jobdir_path, "__failed")
        elif item == "upload_hostname":
            return self._upload_hostname
        elif item == "terminus_root":
            return self._terminus_root_dir
        else:
            raise KeyError("'%s' key was not found in commons." % item)


__all__ = ['TerminusCommons', "DataDirectoryNotFoundError", "PostProcessingServiceNotFoundError", "JobSubmissionError"]
