import re

from .base import Base
from util import defn


class Slurm(Base):
    def set_config_defaults(self):
        c = self.config.cast

        if c.command is None:
            c.command = ["sbatch", "{{script_path}}"]

        if c.command_script_stdin is None:
            c.command_script_stdin = False

        if c.script is None:
            c.script = SCRIPT_TEMPLATE

        if c.script_executable is None:
            c.script_executable = True

    def determine_resources_by_job_name(self, job_name):
        # Define job-specific resource allocations here
        if "small_job" in job_name.lower():
            return "2G", "1"
        elif "medium_job" in job_name.lower():
            return "8G", "2"
        elif "large_job" in job_name.lower():
            return "16G", "4"
        else:
            return "4G", "1"  # Default values

    def determine_job_settings(self, job):
        s_debug, s_write = self.determine_singularity_settings(job)

        # Use job name to determine RAM and CPU
        ram, cpu = self.determine_resources_by_job_name(job.name)

        # This setting can be modified to account for multiple GPUs per node
        # For now, we will assume that a job will only request one GPU
        if "gpu" in job.tags:
            gpu = "1"
        else:
            gpu = None

        return defn.JobSettings(
            fw_id=str(job.id),
            singularity_debug=s_debug,
            singularity_writable=s_write,
            ram=ram,
            cpu=cpu,
            gpu=gpu,
        )

    def format_scheduler_ram_and_cpu_settings(
        self, scheduler_ram: str, scheduler_cpu: str
    ) -> (str, str):
        # Use the values determined by job name, ignore scheduler_ram and scheduler_cpu
        return self.ram, self.cpu

SCRIPT_TEMPLATE = """#!/bin/bash
#SBATCH --job-name=fw-{{job.fw_id}}
#SBATCH --ntasks=1
#SBATCH --cpus-per-task={{job.cpu}}
#SBATCH --mem={{job.ram}}
#SBATCH --output {{script_log_path}}

set -euo pipefail

source "{{cast_path}}/settings/credentials.sh"
cd "{{engine_run_path}}"

set -x
srun ./engine run --single-job {{job.fw_id}}

"""
