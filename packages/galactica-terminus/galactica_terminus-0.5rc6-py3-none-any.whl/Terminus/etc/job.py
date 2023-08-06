#!__TERMINUS_python_interpreter__
# -*- coding: utf-8 -*-
#SBATCH --job-name=__TERMINUS_job_name__   # job name
#SBATCH -N 1                               # number of nodes
#SBATCH -n 8                               # number of cores
#SBATCH --mem 2048                         # memory pool for per node (MB)
#SBATCH --time=00:30:00                    # time (DD-HH:MM)
#SBATCH --output=log_%j.out                # STDOUT
#SBATCH --error=log_%j.err                 # STDERR

from __future__ import unicode_literals, absolute_import

import signal
import sys
import os
import time
from datetime import datetime
import json
from job_status import JobStatus

# debug
import logging
from logging import handlers

log = logging.getLogger("job") # nom Terminus.job
log.addHandler(logging.handlers.RotatingFileHandler("out/job.log"))

log.warn("Import done")

import_retries = 0
while True:
    
    log.warn("Try to import run from __TERMINUS_service_name__ ( test #%d)"%import_retries)

    try:
        from __TERMINUS_service_name__ import run
        break

    except ImportError as exc:
        log.warn("Import run from __TERMINUS_service_name__ FAILURE ( test #%d)"%import_retries)

        if import_retries >= 12:
            JobStatus.update('failed', str(exc))
            raise IOError("Service module could not be imported after 1 minute filesystem cache sync. timeout")

    except Exception as exc:
        JobStatus.update('failed', str(exc))
        sys.exit(1)
    
    log.warn("Service module cannot be imported... Wait 5 seconds")
    import_retries += 1
    time.sleep(5)  # Wait 5 seconds to sync filesystem cache


log.warn("Import run from __TERMINUS_service_name__")

job_name = "__TERMINUS_job_name__"
datapath = "__TERMINUS_data_path__"
data_ref = "__TERMINUS_data_ref__"
func_kwargs = __TERMINUS_func_kwargs__


# ---------- Define SIGTERM signal handler (sent shortly before job timeout, SIGKILL is sent upon timeout) ----------- #
def signal_term_handler(sig, frame):
    JobStatus.update('timed out', "job timed out.")
    sys.exit(1)
signal.signal(signal.SIGTERM, signal_term_handler)
# -------------------------------------------------------------------------------------------------------------------- #

log.warn("signal_term_handler defined")

# Publish message to set job status as RUNNING before running the job
JobStatus.update('running', "job is running")

log.warn("Job is running ... ")

# Start time
str_beg = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

try:
    run(datapath, data_ref, **func_kwargs)
    log.warn("Job launched from run function ... ")

except Exception as exc:
    # Publish message to set job status as ERROR if job failed
    JobStatus.update('failed', str(exc))

    log.warn("Job failed ... ")

    sys.exit(1)


# Stop time
str_end = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

log.warn("Job finished successfuly ... ")

# --------------------------- Save run info in JSON config file (documentation) ---------------------------------- #
# Get simulation data path relative to base data directory (in 'TERMINUS_DATA_DIR' env. variable)
d = {   'service_name': '__TERMINUS_service_name__',
        'host': "__TERMINUS_host_name__",
        'data': {'data_path': '__TERMINUS_data_path__', 'data_reference': data_ref},

        'run_parameters': func_kwargs,

        'time_info': {'job_start': str_beg, 'job_finished': str_end},
    }

with open(os.path.join("out", "processing_config.json"), 'w') as f:
    json.dump(d, f, indent=4)
# ---------------------------------------------------------------------------------------------------------------- #

log.warn("Json file created ! ")

# Publish message to set job status as COMPLETED if job succeeded
JobStatus.update('completed', "job executed successfully")

log.warn("Job completed ! ")

sys.exit(0)