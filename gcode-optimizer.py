class GCodeParser:
    def __init__(self, gcode_filename):
        self.gcode_filename = gcode_filename
        self.z_commands = set()

    def extract_unique_z_commands(self):
        with open(self.gcode_filename, 'r') as file:
            for line in file:
                line = line.strip()  # Remove any leading/trailing whitespace
                if line.startswith('Z') or ' Z' in line:
                    self._process_line(line)
        
        return sorted(self.z_commands)

    def _process_line(self, line):
        words = line.split()
        for word in words:
            if word.startswith('Z'):
                try:
                    z_value = float(word[1:])
                    self.z_commands.add(z_value)
                except ValueError:
                    pass  # Ignore if there's an issue with the value

# Example usage
gcode_filename = 'test-gcode.ngc'  # Change this to your G-code file path
gcode_parser = GCodeParser(gcode_filename)
unique_z_commands = gcode_parser.extract_unique_z_commands()
print(unique_z_commands)
