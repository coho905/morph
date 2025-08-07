import sys

class Morph:
    def __init__(self):
        self.tokens = []
        self.hadError = False
    
    def main(self):
        if(len(sys.argv) > 2):
            print("Usage: morph [script]")
            sys.exit(100)
        elif len(sys.argv) == 2:
            self._run_file(sys.argv[1])
        else:
            self._run_prompt()

    def _run_file(self, filename):
        all_text = open(filename, "r").read()
        self.run(all_text)
        if self.hadError:
            sys.exit(65)

    def _run_prompt(self):
        while True:
            line = input("morph> ")
            if line == "exit" or line == None:
                break
            self.run(line)
            self.hadError = False
        print("Complete")

    def _run(self, source):
        self.run(source)
    
    def run(self, source):
        tokens = source.split()
        for token in tokens:
            print(token)
    
    @staticmethod
    def error(line, message):
        print(f"[line {line}] Error: {message}")
        sys.exit(1)

if __name__ == "__main__":
    morph = Morph()
    morph.main()