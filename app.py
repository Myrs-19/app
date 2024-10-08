import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

class NetworkTopologyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Topology")

        # Создаем Notebook для вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Вкладка для работы с топологией
        self.topology_frame = tk.Frame(self.notebook)
        self.notebook.add(self.topology_frame, text="Network Topology")

        self.canvas = tk.Canvas(self.topology_frame, width=600, height=400, bg="white")
        self.canvas.pack()

        self.nodes = {}  # Словарь для хранения узлов
        self.node_positions = {}  # Хранение координат узлов на холсте
        self.channels = []  # Список для хранения каналов
        self.node_failure_data = {}  # Данные об отказах узлов
        self.channel_characteristics = {}  # Характеристики каналов
        self.node_count = 0  # Счетчик узлов
        self.global_topology_data = {
            "average_message_length": 0.0,
            "message_intensity": 0.0,
            "minimum_delivery_time": 0.0,
            "message_source": "",
            "message_destination": ""
        }  # Глобальные данные для всей сети

        # Кнопки для добавления узлов, каналов и очистки холста
        self.add_node_button = tk.Button(self.topology_frame, text="Add Node", command=self.add_node)
        self.add_node_button.pack(side=tk.LEFT)

        self.add_channel_button = tk.Button(self.topology_frame, text="Add Channel", command=self.add_channel)
        self.add_channel_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.topology_frame, text="Clear Canvas", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)

        self.send_topology_button = tk.Button(self.topology_frame, text="Send Topology", command=self.send_topology)
        self.send_topology_button.pack(side=tk.LEFT)

        # Привязываем событие клика мыши к холсту
        self.canvas.bind("<Button-1>", self.add_node_by_click)

        # Вкладка для формы данных о вероятности отказов и времени восстановления узлов
        self.failure_data_frame = tk.Frame(self.notebook)
        self.notebook.add(self.failure_data_frame, text="Node Failure Data")

        # Фрейм для формы
        self.node_form_frame = tk.Frame(self.failure_data_frame)
        self.node_form_frame.pack(pady=10)

        self.form_entries = {}

        # Добавляем заголовки для столбцов формы
        self.add_form_headers()

        # Кнопка для обновления данных
        self.update_button = tk.Button(self.failure_data_frame, text="Update Data", command=self.update_failure_data)
        self.update_button.pack(pady=10)

        # Вкладка для глобальных данных топологии сети
        self.global_data_frame = tk.Frame(self.notebook)
        self.notebook.add(self.global_data_frame, text="Global Topology Data")

        # Поля для глобальных данных
        self.add_global_data_form()

        # Вкладка для характеристик каналов
        self.channel_data_frame = tk.Frame(self.notebook)
        self.notebook.add(self.channel_data_frame, text="Channel Characteristics")

        # Поля для данных характеристик каналов
        self.add_channel_data_form()

    def add_form_headers(self):
        """Добавление заголовков для столбцов формы сверху"""
        node_label = tk.Label(self.node_form_frame, text="Node", font=('Arial', 10, 'bold'))
        node_label.grid(row=0, column=0, padx=10)

        failure_prob_label = tk.Label(self.node_form_frame, text="Failure Probability", font=('Arial', 10, 'bold'))
        failure_prob_label.grid(row=0, column=1, padx=10)

        recovery_time_label = tk.Label(self.node_form_frame, text="Recovery Time", font=('Arial', 10, 'bold'))
        recovery_time_label.grid(row=0, column=2, padx=10)

    def add_node(self):
        """Добавление узла через кнопку с вводом имени"""
        node_name = simpledialog.askstring("Input", "Enter node name:")
        if node_name:
            x, y = 100 + self.node_count * 50, 100  # Простая логика для расположения узлов
            self.create_node(node_name, x, y)

    def add_node_by_click(self, event):
        """Добавление узла по клику мыши"""
        node_name = simpledialog.askstring("Input", "Enter node name:")
        if node_name:
            x, y = event.x, event.y  # Используем координаты клика мыши
            self.create_node(node_name, x, y)

    def create_node(self, node_name, x, y):
        """Создание узла на холсте"""
        self.node_positions[node_name] = (x, y)
        self.nodes[node_name] = self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="lightblue")
        self.canvas.create_text(x, y, text=node_name)
        self.node_failure_data[node_name] = {"failure_prob": 0.0, "recovery_time": 0.0}  # Добавляем начальные данные
        self.node_count += 1

        # Обновляем форму после добавления узла
        self.update_failure_form()
        self.update_channel_form()  # Обновляем форму каналов после добавления узла

    def add_channel(self):
        """Добавление канала между узлами"""
        node1 = simpledialog.askstring("Input", "Enter first node:")
        node2 = simpledialog.askstring("Input", "Enter second node:")

        if node1 in self.node_positions and node2 in self.node_positions:
            x1, y1 = self.node_positions[node1]
            x2, y2 = self.node_positions[node2]
            self.canvas.create_line(x1, y1, x2, y2, fill="black")
            self.channels.append((node1, node2))  # Сохраняем канал как пару узлов

            # Добавляем данные канала
            self.channel_characteristics[(node1, node2)] = {
                "modulation_speed": 0.0,
                "channel_bundle_count": 0,
                "recovery_time": 0.0,
                "failure_probability": 0.0,
                "avg_packet_length": 0.0
            }

            # Обновляем форму для характеристик каналов
            self.update_channel_form()

    def clear_canvas(self):
        """Очистка холста"""
        self.canvas.delete("all")  # Удаление всех элементов с холста
        self.nodes.clear()  # Очистка данных узлов
        self.node_positions.clear()  # Очистка позиций узлов
        self.channels.clear()  # Очистка списка каналов
        self.node_failure_data.clear()  # Очистка данных об отказах узлов
        self.channel_characteristics.clear()  # Очистка характеристик каналов
        self.node_count = 0  # Сброс счетчика узлов

        # Очищаем формы
        self.update_failure_form()
        self.update_channel_form()

    def send_topology(self):
        """Отправка топологии на обработку"""
        if not self.nodes:
            messagebox.showwarning("Warning", "No nodes in topology!")
            return

        if not self.channels:
            messagebox.showwarning("Warning", "No channels in topology!")
            return

        # Собираем информацию о топологии
        topology_data = {
            "nodes": list(self.node_positions.keys()),  # Имена узлов
            "channels": self.channels,  # Каналы в виде пар (узел1, узел2)
            "failure_data": self.node_failure_data,  # Данные об отказах узлов
            "channel_data": self.channel_characteristics,  # Данные о каналах
            "global_data": self.global_topology_data  # Глобальные данные о топологии
        }

        # В дальнейшем можно добавить функции для обработки топологии
        messagebox.showinfo("Topology Data", f"Nodes: {len(topology_data['nodes'])}, Channels: {len(topology_data['channels'])}")

    def update_failure_form(self):
        """Обновление формы для ввода данных по вероятности отказов и времени восстановления узлов"""
        # Удаляем старые элементы формы
        for widget in self.node_form_frame.winfo_children():
            if isinstance(widget, tk.Entry) or isinstance(widget, tk.Label):
                widget.destroy()

        self.form_entries = {}

        # Перерисовываем заголовки столбцов
        self.add_form_headers()

        # Создаем новые поля для каждого узла
        for i, node in enumerate(self.node_positions, start=1):
            label = tk.Label(self.node_form_frame, text=node)
            label.grid(row=i, column=0, padx=10, pady=5)

            failure_entry = tk.Entry(self.node_form_frame)
            failure_entry.grid(row=i, column=1, padx=5, pady=5)
            failure_entry.insert(0, str(self.node_failure_data[node]["failure_prob"]))

            recovery_entry = tk.Entry(self.node_form_frame)
            recovery_entry.grid(row=i, column=2, padx=5, pady=5)
            recovery_entry.insert(0, str(self.node_failure_data[node]["recovery_time"]))

            self.form_entries[node] = (failure_entry, recovery_entry)

    def update_channel_form(self):
        """Обновление формы характеристик каналов"""
        # Удаляем старые элементы формы
        for widget in self.channel_data_frame.winfo_children():
            if isinstance(widget, tk.Entry) or isinstance(widget, tk.Label):
                widget.destroy()

        channel_data_label = tk.Label(self.channel_data_frame, text="Channel Characteristics", font=('Arial', 12, 'bold'))
        channel_data_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Добавляем заголовки
        headers = ["Channel", "Modulation Speed", "Channel Bundle Count", "Recovery Time", "Failure Probability", "Avg Packet Length"]
        for col, header in enumerate(headers):
            header_label = tk.Label(self.channel_data_frame, text=header, font=('Arial', 10, 'bold'))
            header_label.grid(row=1, column=col, padx=10, pady=5)

        # Создаем новые поля для каждого канала
        for i, (node1, node2) in enumerate(self.channels):
            channel_label = tk.Label(self.channel_data_frame, text=f"{node1} <-> {node2}")
            channel_label.grid(row=i+2, column=0, padx=10, pady=5)

            modulation_speed_entry = tk.Entry(self.channel_data_frame)
            modulation_speed_entry.grid(row=i+2, column=1, padx=5, pady=5)
            modulation_speed_entry.insert(0, str(self.channel_characteristics[(node1, node2)]["modulation_speed"]))

            bundle_count_entry = tk.Entry(self.channel_data_frame)
            bundle_count_entry.grid(row=i+2, column=2, padx=5, pady=5)
            bundle_count_entry.insert(0, str(self.channel_characteristics[(node1, node2)]["channel_bundle_count"]))

            recovery_time_entry = tk.Entry(self.channel_data_frame)
            recovery_time_entry.grid(row=i+2, column=3, padx=5, pady=5)
            recovery_time_entry.insert(0, str(self.channel_characteristics[(node1, node2)]["recovery_time"]))

            failure_prob_entry = tk.Entry(self.channel_data_frame)
            failure_prob_entry.grid(row=i+2, column=4, padx=5, pady=5)
            failure_prob_entry.insert(0, str(self.channel_characteristics[(node1, node2)]["failure_probability"]))

            avg_packet_length_entry = tk.Entry(self.channel_data_frame)
            avg_packet_length_entry.grid(row=i+2, column=5, padx=5, pady=5)
            avg_packet_length_entry.insert(0, str(self.channel_characteristics[(node1, node2)]["avg_packet_length"]))

            self.channel_characteristics[(node1, node2)] = {
                "modulation_speed": modulation_speed_entry,
                "channel_bundle_count": bundle_count_entry,
                "recovery_time": recovery_time_entry,
                "failure_probability": failure_prob_entry,
                "avg_packet_length": avg_packet_length_entry
            }

    def update_failure_data(self):
        """Сохранение данных об отказах и времени восстановления узлов"""
        for node, (failure_entry, recovery_entry) in self.form_entries.items():
            self.node_failure_data[node]["failure_prob"] = float(failure_entry.get())
            self.node_failure_data[node]["recovery_time"] = float(recovery_entry.get())

        messagebox.showinfo("Data Updated", "Node failure data updated successfully!")

    def add_global_data_form(self):
        """Форма для ввода глобальных данных топологии"""
        global_data_label = tk.Label(self.global_data_frame, text="Global Topology Data", font=('Arial', 12, 'bold'))
        global_data_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Средняя длина сообщения
        avg_msg_len_label = tk.Label(self.global_data_frame, text="Average Message Length")
        avg_msg_len_label.grid(row=1, column=0, padx=10, pady=5)
        self.avg_msg_len_entry = tk.Entry(self.global_data_frame)
        self.avg_msg_len_entry.grid(row=1, column=1, padx=10, pady=5)

        # Интенсивность сообщения
        msg_intensity_label = tk.Label(self.global_data_frame, text="Message Intensity")
        msg_intensity_label.grid(row=2, column=0, padx=10, pady=5)
        self.msg_intensity_entry = tk.Entry(self.global_data_frame)
        self.msg_intensity_entry.grid(row=2, column=1, padx=10, pady=5)

        # Минимальное время доставки
        min_delivery_time_label = tk.Label(self.global_data_frame, text="Minimum Delivery Time")
        min_delivery_time_label.grid(row=3, column=0, padx=10, pady=5)
        self.min_delivery_time_entry = tk.Entry(self.global_data_frame)
        self.min_delivery_time_entry.grid(row=3, column=1, padx=10, pady=5)

        # Адресация сообщения: начальный узел
        msg_source_label = tk.Label(self.global_data_frame, text="Message Source Node")
        msg_source_label.grid(row=4, column=0, padx=10, pady=5)
        self.msg_source_entry = tk.Entry(self.global_data_frame)
        self.msg_source_entry.grid(row=4, column=1, padx=10, pady=5)

        # Адресация сообщения: конечный узел
        msg_destination_label = tk.Label(self.global_data_frame, text="Message Destination Node")
        msg_destination_label.grid(row=5, column=0, padx=10, pady=5)
        self.msg_destination_entry = tk.Entry(self.global_data_frame)
        self.msg_destination_entry.grid(row=5, column=1, padx=10, pady=5)

        # Кнопка для сохранения глобальных данных
        self.update_global_data_button = tk.Button(self.global_data_frame, text="Update Global Data", command=self.update_global_data)
        self.update_global_data_button.grid(row=6, column=0, columnspan=2, pady=10)

    def update_global_data(self):
        """Обновление глобальных данных топологии"""
        self.global_topology_data["average_message_length"] = float(self.avg_msg_len_entry.get())
        self.global_topology_data["message_intensity"] = float(self.msg_intensity_entry.get())
        self.global_topology_data["minimum_delivery_time"] = float(self.min_delivery_time_entry.get())
        self.global_topology_data["message_source"] = self.msg_source_entry.get()
        self.global_topology_data["message_destination"] = self.msg_destination_entry.get()

        messagebox.showinfo("Global Data Updated", "Global topology data updated successfully!")

    def add_channel_data_form(self):
        """Форма для ввода характеристик каналов"""
        channel_data_label = tk.Label(self.channel_data_frame, text="Channel Characteristics", font=('Arial', 12, 'bold'))
        channel_data_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Скорость модуляции
        modulation_speed_label = tk.Label(self.channel_data_frame, text="Modulation Speed")
        modulation_speed_label.grid(row=1, column=0, padx=10, pady=5)
        self.modulation_speed_entry = tk.Entry(self.channel_data_frame)
        self.modulation_speed_entry.grid(row=1, column=1, padx=10, pady=5)

        # Число каналов в пучке
        bundle_count_label = tk.Label(self.channel_data_frame, text="Channel Bundle Count")
        bundle_count_label.grid(row=2, column=0, padx=10, pady=5)
        self.bundle_count_entry = tk.Entry(self.channel_data_frame)
        self.bundle_count_entry.grid(row=2, column=1, padx=10, pady=5)

        # Время ожидания восстановления канала
        recovery_time_label = tk.Label(self.channel_data_frame, text="Channel Recovery Time")
        recovery_time_label.grid(row=3, column=0, padx=10, pady=5)
        self.recovery_time_entry = tk.Entry(self.channel_data_frame)
        self.recovery_time_entry.grid(row=3, column=1, padx=10, pady=5)

        # Вероятность отказа канала
        failure_prob_label = tk.Label(self.channel_data_frame, text="Channel Failure Probability")
        failure_prob_label.grid(row=4, column=0, padx=10, pady=5)
        self.failure_prob_entry = tk.Entry(self.channel_data_frame)
        self.failure_prob_entry.grid(row=4, column=1, padx=10, pady=5)

        # Средняя длина пакета
        avg_packet_len_label = tk.Label(self.channel_data_frame, text="Average Packet Length")
        avg_packet_len_label.grid(row=5, column=0, padx=10, pady=5)
        self.avg_packet_len_entry = tk.Entry(self.channel_data_frame)
        self.avg_packet_len_entry.grid(row=5, column=1, padx=10, pady=5)

        # Кнопка для сохранения характеристик каналов
        self.update_channel_data_button = tk.Button(self.channel_data_frame, text="Update Channel Data", command=self.update_channel_data)
        self.update_channel_data_button.grid(row=6, column=0, columnspan=2, pady=10)

    def update_channel_data(self):
        """Сохранение данных о характеристиках каналов"""
        # Обновляем данные о каждом канале
        for (node1, node2), entries in self.channel_characteristics.items():
            modulation_speed = float(entries["modulation_speed"].get())
            channel_bundle_count = int(entries["channel_bundle_count"].get())
            recovery_time = float(entries["recovery_time"].get())
            failure_probability = float(entries["failure_probability"].get())
            avg_packet_length = float(entries["avg_packet_length"].get())

            self.channel_characteristics[(node1, node2)] = {
                "modulation_speed": modulation_speed,
                "channel_bundle_count": channel_bundle_count,
                "recovery_time": recovery_time,
                "failure_probability": failure_probability,
                "avg_packet_length": avg_packet_length
            }

        messagebox.showinfo("Channel Data Updated", "Channel characteristics updated successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkTopologyApp(root)
    root.mainloop()
