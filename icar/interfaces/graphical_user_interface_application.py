import tkinter as tk

import icar.interfaces.graphical_user_interface.views.main_view as main_view


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=tk.BOTH)

        self._current_frame = None
        self.current_open_database = None
        self.current_open_table = None
        self.operation_result_message = None

        self.replace_frame(main_view.MainPage(self))

    def replace_frame(self, frame):
        if self._current_frame:
            self._current_frame.destroy()
        self._current_frame = frame
        self._current_frame.configure()
        self._current_frame.pack(fill=tk.BOTH, expand=1)
        self.operation_result_message = None


def retrieve_centered_root():
    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    application_width = 600
    application_heigth = 400

    x_position = int(screen_width / 2 - application_width / 2)
    y_position = int(screen_height / 3 - application_heigth / 2)

    root.geometry('{}x{}+{}+{}'.format(application_width, application_heigth, x_position, y_position))

    return root


if __name__ == '__main__':
    root = retrieve_centered_root()

    app = Application(master=root)
    app.mainloop()
