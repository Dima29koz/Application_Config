import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
import math
from functools import partial
from datetime import datetime, timedelta

from firmware import Firmware
from GUI.tooltip import create_tool_tip


class App:
    def __init__(self, firmware: Firmware):
        matplotlib.use('TkAgg')
        self.firmware = firmware
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title('Состояние контроллеров')
        self.show_interface()
        self.root.mainloop()

    def show_interface(self):
        status_frame = tk.Frame(self.root)
        self.show_status_page(status_frame)
        status_frame.pack(expand=1)

    @staticmethod
    def hide_page(page):
        page.pack_forget()

    def show_status_page(self, canvas):
        font = "Arial 12"
        for i, cont in enumerate(self.firmware.controllers[:20]):
            name_lab = tk.Label(canvas, text=f'{cont.name}:', font=font, padx=5)
            btn = tk.Button(canvas, text='Перейти к контроллеру', padx=5,
                            command=partial(self.go_to_cont, cont.name, canvas))
            if cont.is_active:
                status_lab = tk.Label(canvas, text='Активен', fg='green', font=font, padx=5)
                # status_lab.bind("<Enter>", partial(self.show_status, cont.name))
                time_from_error = datetime.now() - cont.last_error_time
                time_overall = datetime.now() - cont.start_time
                errors_amount = len(self.firmware.get_controller_errors(cont.name))
                create_tool_tip(status_lab, text=f'Время работы после последнего сбоя: {str(time_from_error)}\n'
                                                 f'Время работы: {str(time_overall)}\n'
                                                 f'Число сбоев за время работы: {str(errors_amount)}')
            else:
                status_lab = tk.Label(canvas, text='Отключен', fg='red', font=font, padx=5)
                btn.configure(state=tk.DISABLED)

            name_lab.grid(row=i, column=0)
            status_lab.grid(row=i, column=1)
            btn.grid(row=i, column=2)

    def go_to_cont(self, cont_name: str, canvas):
        self.hide_page(canvas)
        self.show_controller_page(cont_name)

    def show_controller_page(self, cont_name):
        cont_frame = tk.Frame(self.root)
        self.draw_graph(cont_frame)
        cont_frame.pack(expand=1)

    def draw_graph(self, cont_frame):
        fig, ax = plt.subplots()
        canvas = FigureCanvasTkAgg(fig, master=cont_frame)
        plot_widget = canvas.get_tk_widget()

        date = []
        activ = []

        cont = self.firmware.get_controllers_names()[0]
        log = self.firmware.get_controller_log(cont)

        for elem in log['data']:
            if isinstance(elem, dict):
                date.append(elem['timestamp'])
                activ.append(0)
            else:
                date.append(elem)
                activ.append(1)
        ax.set_title('Статус работы')
        ax.step(date, activ, linewidth=1)
        ax.set_xticklabels([])
        ax.set_yticklabels([])

        data = self.firmware.get_controller_data(cont)
        btn_frame = tk.Frame(cont_frame)
        btn = tk.Button(btn_frame, text='<-', padx=10,
                        command=partial(self.back_page, cont_frame))
        btn.pack(side=tk.LEFT)
        sensors = list(data[0].keys())[:-1]
        for i, sensor in enumerate(sensors, 1):
            btn = tk.Button(btn_frame, text=sensor, padx=5,
                            command=partial(self.update_graph, sensor, cont, fig, ax))
            btn.pack(side=tk.LEFT)

        btn_frame.grid(row=0, column=0)
        plot_widget.grid(row=1, column=0)

    def update_graph(self, sensor, cont, fig, ax):
        plt.cla()
        data = self.firmware.get_controller_data(cont)

        date = []
        value = []

        for elem in data:
            date.append(elem['timestamp'])
            value.append(elem[sensor])
        ax.set_title(sensor)
        ax.plot(date, value, linewidth=1)
        ax.set_xticklabels([])
        fig.canvas.draw()

    def back_page(self, cur_page):
        self.hide_page(cur_page)
        self.show_interface()
