#!/usr/bin/env python3

import os, subprocess

class Process:

    @staticmethod
    def execute(command, workdir = None):

        current = os.getcwd()
        if workdir:
            os.chdir(workdir)

        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
            output, error = process.communicate()

        os.chdir(current)

        return output.decode('ascii')