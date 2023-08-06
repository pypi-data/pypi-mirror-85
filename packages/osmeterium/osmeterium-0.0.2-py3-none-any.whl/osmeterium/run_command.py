import subprocess
from threading import Thread
from typing import Callable, Union


def get_command_std_iter(process_std):
    for line in iter(process_std.readline, ''):
        yield line


def read_from_pipe(process_std, on_output):
    for stdout_line in get_command_std_iter(process_std):
        stripped_line = stdout_line.strip()
        if len(stripped_line) > 0:
            on_output(stripped_line)
    process_std.close()


def create_read_stream_thread(process_std, on_output):
    thread = Thread(target=read_from_pipe, args=(process_std, on_output))
    thread.daemon = True
    return thread


def do_nothing(useless: str) -> None:
    pass


def run_command(command: str,
                on_stdout_output: Callable[[str], None] = do_nothing,
                on_stderr_output: Callable[[str], None] = do_nothing,
                on_process_fail: Callable[[str], None] = do_nothing,
                on_process_success: Callable[[str], None] = do_nothing) -> None:
    process = subprocess.Popen(command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                        shell=True)
    thread_stdout = create_read_stream_thread(process.stdout, on_stdout_output)
    thread_stderr = create_read_stream_thread(process.stderr, on_stderr_output)

    threads = (thread_stdout, thread_stderr)
    for t in threads:
        t.start()
    return_code = process.wait()
    for t in threads:
        t.join()
    if (return_code != 0):
        return on_process_fail(return_code)
    return on_process_success()


def run_command_async(command: str,
                            on_stdout_output: Callable[[str], None],
                            on_stderr_output: Callable[[str], None],
                            on_process_fail: Callable[[int], None],
                            on_process_success: Callable[[], None]) -> Thread:
    command_thread = Thread(target=run_command, args=(command, on_stdout_output, on_stderr_output, on_process_fail, on_process_success))
    command_thread.daemon = True
    command_thread.start()
    return command_thread
