import tkinter as tk

import icar.interfaces.graphical_user_interface.views.main_view as main_view


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self._current_frame = None
        self.current_open_database = None
        self.current_open_table = None
        self.operation_result_message = None

        self.replace_frame(main_view.MainPage(self))

    def replace_frame(self, frame):
        if self._current_frame:
            self._current_frame.destroy()
        self._current_frame = frame
        self._current_frame.pack()
        self.operation_result_message = None


def retrieve_centered_root():
    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    application_width = 800
    application_heigth = 200

    x_position = int(screen_width / 2 - application_width / 2)
    y_position = int(screen_height / 3 - application_heigth / 2)

    root.geometry('{}x{}+{}+{}'.format(application_width, application_heigth, x_position, y_position))

    return root


root = retrieve_centered_root()
app = Application(master=root)
app.mainloop()
