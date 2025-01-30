import asyncio
import sys, os
from multiprocessing import Process

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)
import subprocess
import signal
import click
import uvicorn

PID_FILE = os.path.join(ROOT_DIR, "paig_server.pid")

@click.command()
@click.option(
    "--host",
    type=click.STRING,
    default="127.0.0.1",
    help="Host to run the server on",
)
@click.option(
    "--port",
    type=click.INT,
    default=4545,
    help="Port to run the server on",
)
@click.option(
    "--config_path",
    type=click.Path(),
    default=None,
    help="Absolute Path to the configuration folder",
)
@click.option(
    "--custom_config_path",
    type=click.Path(),
    default=None,
    help="Absolute Path to the custom configuration folder",
)
@click.option(
    "--paig_deployment",
    type=click.STRING,
    default="dev",
    help="Paig deployment environment",
)
@click.option(
    "--workers",
    type=click.INT,
    default=1,
    help="Configure number of workers for the server",
)
@click.option(
    "--background",
    type=click.STRING,
    default="false",
    help="Run server in background",
)
@click.argument('action', type=click.STRING, required=False)
def main(
        host: str,
        port: int,
        config_path: str,
        custom_config_path: str,
        paig_deployment: str,
        workers: int,
        background,
        action: str,
    ) -> None:

    if action.lower() == "stop":
        stop_server()
        return
    elif action.lower() == "status":
        pid = is_server_running()
        if pid:
            print("PAIG Server is running")
        else:
            print("PAIG Server is not running")
        return
    set_up_standalone_mode(
        host,
        port,
        config_path,
        custom_config_path,
        paig_deployment,
        ROOT_DIR
    )
    cleanup()
    from alembic_db import create_or_update_tables, create_default_user_and_ai_application
    from api.encryption.events.startup import create_default_encryption_keys
    if action == 'create_tables':
        create_or_update_tables(ROOT_DIR)
    if action == 'run' or action == 'start':
        if is_server_running():
            return print("PAIG Server is already running.")
        create_or_update_tables(ROOT_DIR)
        create_default_user_and_ai_application()
        asyncio.run(create_default_encryption_keys())
        start_server(host, port, background, workers)
    else:
        return print("Please provide an action. Options: create_tables|run|start|status|stop")


def _is_colab():
    try:
        import google.colab
    except ImportError:
        return False
    try:
        from IPython.core.getipython import get_ipython
    except ImportError:
        return False
    return True



def set_up_standalone_mode(
        host,
        port,
        config_path,
        custom_config_path,
        paig_deployment,
        ROOT_DIR
):
    from core import constants
    constants.SINGLE_USER_MODE = _is_colab()
    constants.HOST = host
    constants.PORT = port
    constants.MODE = "standalone"
    if config_path is None:
        config_path = os.path.join(ROOT_DIR, "conf")
    if custom_config_path is None:
        custom_config_path = 'custom-conf'
    os.environ["CONFIG_PATH"] = str(config_path)
    os.environ["EXT_CONFIG_PATH"] = str(custom_config_path)
    os.environ["PAIG_ROOT_DIR"] = str(ROOT_DIR)
    if paig_deployment:
        os.environ["PAIG_DEPLOYMENT"] = str(paig_deployment)


def cleanup():
    import shutil
    import os
    from core import constants
    _temp_dir = os.path.join(ROOT_DIR, constants.TEMP_DIR)
    if os.path.exists(_temp_dir):
        shutil.rmtree(_temp_dir, ignore_errors=True)


def start_server(host, port, background, workers):
    background = background.lower() == "true"

    if not background:
        print('Starting PAIG Server in foreground mode')
        # Start Celery worker in a separate process
        celery_process = Process(target=start_celery_worker)
        celery_process.start()

        try:
            # Start the FastAPI app
            uvicorn.run(
                app="server:app",
                host=host,
                port=port,
                workers=workers,
            )
        finally:
            # Ensure the Celery worker process is terminated when FastAPI stops
            celery_process.terminate()
            celery_process.join()
    else:
        print('Starting PAIG Server in background mode')
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "server:app", "--host", str(host), "--port", str(port),
             "--workers", str(workers),
             "--app-dir", ROOT_DIR],
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        # Start the Celery worker as a background process
        celery_process = subprocess.Popen(
            [
                sys.executable, "-m", "celery", "-A", "celery_app_pk.celery_app_st.celery_app", "worker",
                "--loglevel=info",
                "--concurrency=4",
            ],
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Save PIDs for both processes
        with open(PID_FILE, "w") as f:
            f.write(f"{process.pid}\n{celery_process.pid}\n")

        print(f"Server started in background with PID {process.pid}")
        print(f"Celery worker started in background with PID {celery_process.pid}")
        print(f"PAIG Server is running on http://{host}:{port}")


def is_server_running():
    """Check if the server or Celery worker is already running based on the PID file."""
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                pids = [int(pid.strip()) for pid in f.readlines()]  # Read multiple PIDs
            valid_pids = []
            import psutil
            for pid in pids:
                if psutil.pid_exists(pid):
                    process = psutil.Process(pid)
                    cmdline = " ".join(process.cmdline())
                    # Check if the PID belongs to a process with the expected command line
                    if ("uvicorn" in cmdline and "server:app" in cmdline) or "celery" in cmdline:
                        valid_pids.append(pid)
            if valid_pids:
                return valid_pids  # Return list of valid PIDs
            os.remove(PID_FILE)  # Remove stale PID file if no valid processes
        except (ValueError, ProcessLookupError, PermissionError, psutil.Error):
            print("PID file is invalid or inaccessible")
            os.remove(PID_FILE)
    return []


def stop_server():
    pids = is_server_running()  # Get list of running PIDs
    if pids:
        for pid in pids:
            try:
                os.kill(pid, signal.SIGTERM)  # Send termination signal
                print(f"Process with PID {pid} stopped.")
            except Exception as err:
                print(f"Error occurred while stopping process with PID {pid}: {err}")
        os.remove(PID_FILE)  # Clean up the PID file
        print("All processes stopped, and PID file removed.")
    else:
        print("No server or worker processes are currently running.")


def start_celery_worker():
    """
    Start the Celery worker programmatically.
    """
    # Command to start the Celery worker in a subprocess
    command = [
        sys.executable,  # Use the current Python interpreter
        "-m", "celery",  # Run Celery as a module
        "-A", "celery_app_pk.celery_app_st.celery_app",  # Specify the Celery app
        "worker",  # Start the worker
        "--loglevel=info",  # Set log level
        "--queues=celery,queue1,queue2", # Specify queues (adjust as needed)
        "--concurrency=4",  # Set concurrency (adjust as needed)
        "--logfile=logs/celery_worker.log",
    ]

    # Start the worker in a subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Start the worker in a subprocess
    # process = subprocess.Popen(
    #     command,
    #     stdout=subprocess.PIPE,  # Capture standard output
    #     stderr=subprocess.PIPE,  # Capture error output
    #     universal_newlines=True,  # Decode output to strings
    # )

    # Optionally, capture and log output if necessary
    stdout, stderr = process.communicate()
    if stdout:
        print(stdout.decode())
    if stderr:
        print(stderr.decode())

    # Display logs in real time
    # print("Starting Celery worker...")
    # try:
    #     while True:
    #         output = process.stdout.readline()
    #         if output == "" and process.poll() is not None:
    #             break
    #         if output:
    #             print(output.strip())  # Print each line of the log
    # except KeyboardInterrupt:
    #     print("Stopping Celery worker...")
    #     process.terminate()
    #     process.wait()

    return process


# def start_celery_worker():
#     celery_process = subprocess.Popen(
#         [
#             sys.executable, "-m", "celery", "-A", "celery_app_pk.celery_app_st.celery_app", "worker",
#             "--loglevel=info",
#             "--concurrency=4",
#         ],
#         start_new_session=True,
#         stdout=subprocess.DEVNULL,
#         stderr=subprocess.DEVNULL,
#     )
#
#     return celery_process


if __name__ == "__main__":
    main()
