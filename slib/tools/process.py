# -*- coding: utf-8 -*-


import subprocess

from slib import logger


##### Exceptions #####
class SubprocessFailure(Exception) :
	pass


##### Public methods #####
def execProcess(proc_args_list, proc_input = None, env_dict = None, fatal_flag = True, shell_flag=False, confidential_input_flag = False) :
	logger.log("Executing child process \"%s\"" % (str(proc_args_list)))

	if isinstance(env_dict, dict) :
		env_dict = dict(env_dict)
		env_dict.setdefault("LC_ALL", "C")

	proc = subprocess.Popen(proc_args_list, shell=shell_flag, bufsize=1024, close_fds=True,
		stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env_dict)
	(proc_stdout, proc_stderr) = proc.communicate(proc_input)

	if proc.returncode != 0 : # pylint: disable=E1101
		if proc_input == None :
			proc_input = ""
		elif confidential_input_flag :
			proc_input = "<CONFIDENTIAL>"
		proc_stdout_clean = proc_stdout.strip() #pylint: disable=E1103
		proc_stderr_clean = proc_stderr.strip() #pylint: disable=E1103
		error_text = "Error while execute \"%s\"\nStdout: %s\nStderr: %s\nStdin: %s\nReturn code: %d" % (
			str(proc_args_list), proc_stdout_clean, proc_stderr_clean, proc_input, proc.returncode ) # pylint: disable=E1101
		if fatal_flag :
			raise SubprocessFailure(error_text)
		logger.log(error_text)

	logger.log("Child process \"%s\" finished, return_code=%d" % (str(proc_args_list), proc.returncode)) # pylint: disable=E1101

	return (proc_stdout, proc_stderr, proc.returncode) # pylint: disable=E1101

