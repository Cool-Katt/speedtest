import subprocess 

def runFetcher():
    s = subprocess.check_call("speedtest.exe")
    print(s)

if __name__ == "__main__":
    runFetcher()
