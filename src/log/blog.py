HEADER = '\033[95m'
NORMAL = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def warn(log):
    print(WARNING + "==> [WARN] " + ENDC + log)

def error(log):
    print(FAIL + "==> [ERROR] " + ENDC + log)

def info(log):
    print(OKGREEN + "==> " + ENDC + log)

def web_log(log):
    print(OKCYAN + " -> " + ENDC + log)
