import sys 

class Logger(object):
    def __init__(self, file):
        self.file = file

    def printToLog(self, message=""):
        with open(self.file, 'a') as f:
            f.write(message + '\n')

    def printToTerminal(self, message=""):
        sys.stdout.write(message + '\n')

    def progressBar(self, iteration, total, idx, testcase, test, length=50):
        percent = 100 * (iteration / float(total))
        filled_length = int(length * iteration // total)
        bar = '█' * filled_length + '-' * (length - filled_length)
        sys.stdout.write(f'\r Dataset: {testcase.loc[idx, 'Dataset']}, Percobaan {test} |{bar}| ({idx+1}/{int((total-1)/3)} testcase) {percent:.2f}% Complete')

        sys.stdout.flush()
    