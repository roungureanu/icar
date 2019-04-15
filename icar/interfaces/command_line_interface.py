class Application(object):
    def __init__(self):
        self.stop_required = False

    def run(self):
        while not self.should_stop():
            command = input('> ')

            if command.lower() in {'exit', 'stop', 'quit', 'bye', 'q'}:
                print('bye :(')
                self.stop_required = True
                break

            result = self.process_command(command)
            print(result)

    def process_command(self, command):
        if command:
            return 'ayy lmao'

    def should_stop(self):
        return self.stop_required


if __name__ == '__main__':
    app = Application()
    app.run()
