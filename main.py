import subprocess

def run_script(script_name):
    subprocess.run(['python', script_name])

def main():
    run_script('make.py')
    run_script('ping.py')
    run_script('speed.py')
    run_script('xray.py')
if __name__ == "__main__":
    main()