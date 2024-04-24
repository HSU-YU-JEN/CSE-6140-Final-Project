import multiprocessing
import subprocess

def run_script(script_name):
    print(f"Running {script_name}...")
    subprocess.run(["python3", script_name])

def main():
    scripts = [
        "code/main_1(1-3).py",
        "code/main_1(3-5).py",
        "code/main_1(5-8).py",
        "code/main_1(8-12).py",
        "code/main_1(12-15).py",
        "code/main_1(15-18).py",
        "code/main_1(18-20).py",
        "code/main_1(20-22).py"
    ]
    
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    
    pool.map(run_script, scripts)
    
    pool.close()

    pool.join()
    
    print("All scripts completed.")

if __name__ == "__main__":
    main()
