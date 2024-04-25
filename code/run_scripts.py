import multiprocessing
import subprocess

def run_script(script_name):
    print(f"Running {script_name}...")
    subprocess.run(["python3", script_name])

def main():
    scripts = [
        # "code/main_6.py",
        # "code/main_19.py",
        # "code/main_20.py",
        # "code/main_21.py"
    ]
    
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    
    pool.map(run_script, scripts)
    
    pool.close()

    pool.join()
    
    print("All scripts completed.")

if __name__ == "__main__":
    main()
