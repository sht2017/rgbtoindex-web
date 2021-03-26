import os

class magick:
    def __init__(self, input_file, output_file):
        self.input_file=input_file
        self.output_file=output_file

    def process(self):
        os.popen("magick "+self.input_file+" -type Palette -strip "+self.output_file).readlines()
