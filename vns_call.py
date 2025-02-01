import subprocess
commands =[
    ["python3", "vns_call_n.py", "graphs/ vns2/ 10 0.01"],
    ["python3", "vns_call_n.py", "graphs/ vns2/ 10 0.05"],
    ["python3", "vns_call_n.py", "graphs/ vns2/ 10 0.1"],
    ["python3", "vns_call_n.py", "graphs/ vns2/ 10 0.2"],
    ["python3", "vns_call_n.py", "graphs/ vns2/ 10 0.5"],
    ["python3", "vns_call_n.py", "graphs/ vns2/ 10 0.9"],
]

processes = [subprocess.Popen(cmd) for cmd in commands]
for p in processes:
    p.wait()