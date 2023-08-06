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
import os
import stat
import re
import shutil
import subprocess
from Terminus.commons import TerminusCommons, PostProcessingServiceNotFoundError, DataDirectoryNotFoundError,\
    JobSubmissionError

from celery.utils.log import get_task_logger

log = get_task_logger(__name__)

class JobSubmitter(object):
    """
    Job submission class
    """
    JOB_PYTHON_FILENAME = "job.py"
    DIGIT_STARTING_SERVICE_MODULE = re.compile("^[0-9].*$")

    def __init__(self):
        self._commons = TerminusCommons()

    @property
    def service_list(self):
        """
        Get the list of installed services
        """
        services = {}
        for d in os.listdir(self._commons["service_path"]):
            p = os.path.join(self._commons["service_path"], d)
            if os.path.isdir(p):
                services[d] = p
        return services

    def submit(self, job):
        """
        Job submission method

        Parameters
        ----------
        job: ``TerminusJob``
            post-processing job instance
        """
        template_dir = os.path.join(self._commons["terminus_root"], "etc")

        # Check job service exists on the server
        sdict = self.service_list
        if job.service not in sdict:
            raise PostProcessingServiceNotFoundError(job.service)
        # job_script_base = os.path.join(self._commons["service_path"], JobSubmitter.JOB_PYTHON_FILENAME)
        job_script_base = os.path.join(template_dir, JobSubmitter.JOB_PYTHON_FILENAME)

        module_file = os.path.join(sdict[job.service], "{service_name!s}.py".format(service_name=job.service))
        if not os.path.isfile(job_script_base) or not os.path.isfile(module_file):
            raise PostProcessingServiceNotFoundError(job.service)

        # Check data directory exists on the server
        abs_data_path = job.absolute_data_path
        if not os.path.isdir(abs_data_path):
            raise DataDirectoryNotFoundError(job.data_path)

        # Clear/create job run directory
        job_dir = job.find_job_directory(check=False)
        if os.path.isdir(job_dir):
            shutil.rmtree(job_dir, ignore_errors=True)
        os.makedirs(os.path.join(job_dir, "out"))

        # read python.info from service directory. This file has to be created 
        # by the user that create the service
        python_info_path = os.path.join(sdict[job.service], "python.info")
        job_custom_python_interp_path = ""
        try:
            with open(python_info_path, 'r') as python_infofile:
                for line in python_infofile:
                    if "PYTHON=" in line or "python=" in line:
                        job_custom_python_interp_path = line.replace("\n", "").split("=")[1]
        except IOError as e:
            raise JobSubmissionError(str(e))

        # Copy main service module file + job_status module + job submission script in job run directory
        if JobSubmitter.DIGIT_STARTING_SERVICE_MODULE.match(job.service) is None:
            job_module_file = job.service
        else:
            job_module_file = "script_{job_service!s}".format(job_service=job.service)
        shutil.copy(module_file, os.path.join(job_dir, "{job_modfile!s}.py".format(job_modfile=job_module_file)))
        job_status_module_file = os.path.join(self._commons["terminus_root"], "job_status.py")
        shutil.copy(job_status_module_file, os.path.join(job_dir, "job_status.py"))
        job_script = os.path.join(job_dir, JobSubmitter.JOB_PYTHON_FILENAME)
        try:
            lines = []
            with open(job_script_base, 'r') as base_jobfile:
                for line in base_jobfile:
                    line = line.replace("__TERMINUS_python_interpreter__", job_custom_python_interp_path)
                    line = line.replace("__TERMINUS_job_name__", job.job_name)
                    line = line.replace("__TERMINUS_data_path__", abs_data_path)
                    line = line.replace("__TERMINUS_data_ref__", job.data_reference)
                    line = line.replace("__TERMINUS_host_name__", self._commons["hostname"])
                    line = line.replace("__TERMINUS_service_name__", job_module_file)
                    line = line.replace("__TERMINUS_func_kwargs__", job.param_values_string)
                    lines.append(line)

            with open(job_script, 'w') as jobfile:
                for line in lines:
                    jobfile.write(line)
        except IOError as e:
            raise JobSubmissionError(str(e))

        # set chmod on job_script - BUG in daemonization if not
        os.chmod(job_script, stat.S_IXUSR | stat.S_IXGRP | stat.S_IRUSR | stat.S_IRGRP)

        if not self._commons.use_slurm:
            log.warning("Submission info python interp   : %s !" % job_custom_python_interp_path)
            log.warning("Submission info python file job :  %s !" % job_script)
            log.warning("Submission info python job dir  :  %s !" % job_dir)
            p = subprocess.Popen([job_custom_python_interp_path, job_script], cwd=job_dir, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

        else:  # submit SLURM job in batch mode using 'sbatch'
            p = subprocess.Popen(['sbatch', job_script], cwd=job_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # if p.wait() != 0:
        #     # TODO Handle job submission errors
        #     log.warning("A job submission error occured with file %s !" % job_script)
            
        #     pass


__all__ = ["JobSubmitter"]
