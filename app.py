import tkinter
import tkinter.messagebox
import customtkinter
import tkinter as tk
import subprocess
from tkinter import filedialog
from tkinter.filedialog import askdirectory
from sys import platform
import queue
import threading
import re


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    def __init__(self):
        self.file_path = "sample/metadata.csv"
        super().__init__()

        # configure window
        self.title("Music Libray Query GUI")
        self.minsize(800, 580)
        self.geometry(f"{1100}x{580}")


        # create frame with title
        self.main_frame = customtkinter.CTkFrame(self, width=1100, corner_radius=10)
        self.main_frame.pack(fill="both", expand=True)  # Update this line
        self.main_label = customtkinter.CTkLabel(self.main_frame, text="Music Library Analyzer", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.main_label.pack(padx=20, pady=(20, 10))

        # create a scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.main_frame)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.csv_label = customtkinter.CTkLabel(self.scrollable_frame, text="Upload or Generate a CSV?", bg_color="transparent", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.csv_label.pack(padx=20, pady=(20, 5))
        self.csv_label = customtkinter.CTkLabel(self.scrollable_frame, text="A CSV file is needed for analysis, you can copy a generated one from sample/ for example.", bg_color="transparent", font=customtkinter.CTkFont(size=15))
        self.csv_label.pack(padx=20, pady=(5, 5))   

        # create csv buttons
        self.button_frame = customtkinter.CTkFrame(self.scrollable_frame)
        self.button_frame.pack(padx=20, pady=(5, 5))
        self.upload_csv_btn = customtkinter.CTkButton(self.button_frame, text="Upload", command=lambda:self.upload_csv())
        self.upload_csv_btn.pack(side="left", padx=5)
        self.generate_csv_btn = customtkinter.CTkButton(self.button_frame, text="Generate", command=lambda:self.generate_csv())
        self.generate_csv_btn.pack(side="right", padx=5)

        self.csv_textbox = customtkinter.CTkTextbox(self.scrollable_frame, width=250, state="disabled")
        self.csv_textbox.pack(fill="both", padx=(20, 0), pady=(10, 0))

        # artist search
        self.artist_query_label = customtkinter.CTkLabel(self.scrollable_frame, text="Query Data Set", bg_color="transparent", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.artist_query_label.pack(padx=20, pady=(20, 5))
        self.artist_query_label = customtkinter.CTkLabel(self.scrollable_frame, text="Query an artist to see their contributions to your music library or select any of the other options for more insite.", bg_color="transparent", font=customtkinter.CTkFont(size=15))
        self.artist_query_label.pack(padx=20, pady=(5, 5))

        self.artist_entry_box = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="Enter Artist Name")
        self.artist_entry_box.pack(side="left", padx=(2, 0), pady=(10, 0))

        self.q_button = customtkinter.CTkButton(self.scrollable_frame, text="Query Artist", command=lambda:self.query_artist())
        self.q_button.pack(side="left", padx=(5, 0), pady=(10, 0))

        self.artist_textbox = customtkinter.CTkTextbox(self.scrollable_frame, width=750, state="disabled")
        self.artist_textbox.pack(side="right", padx=(5, 0), pady=(10, 0))

    def upload_csv(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.csv_textbox.configure(state='normal')
            self.csv_textbox.insert('end', f"The following CSV {self.file_path} will be analyzed\n")
            self.csv_textbox.see('end')
            self.csv_textbox.configure(state='disabled')

    def generate_csv(self):
        self.file_path = "build/metadata.csv"
        folder = askdirectory(title='Select Folder')
        if not folder:
            return

        self.csv_textbox.configure(state='normal')

        # Create a queue to communicate with the worker thread
        self.queue = queue.Queue()

        # Create a worker thread that will run the process
        self.worker_thread = threading.Thread(target=self.run_process, args=(folder,))

        # Start the worker thread
        self.worker_thread.start()

        # Update the textbox with the output from the process
        self.after(100, self.update_textbox)

    def run_process(self, folder):
        if platform == "win32":
            process = subprocess.Popen(["python", "analyzer.py", folder], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            process = subprocess.Popen(["python3", "analyzer.py", folder], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        for line in process.stdout:
            # Put the output line in the queue
            self.queue.put(line)

    def update_textbox(self):
        try:
            # Get the next line of output
            line = self.queue.get_nowait()
        except queue.Empty:
            # If there are no more lines of output, check again after 100ms
            self.after(100, self.update_textbox)
        else:
            # If there is a line of output, add it to the textbox and check again immediately
            self.csv_textbox.insert('end', line.decode())
            self.csv_textbox.see('end')
            self.update_textbox()
    
    def query_artist(self):
        process = subprocess.Popen(["Rscript", "R/search_by_artist.r", f"{self.artist_entry_box.get()}", self.file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()


        quary_output = output.decode().splitlines()

        self.artist_textbox.configure(state='normal')
        self.artist_textbox.delete(1.0, "end")

        # print first 3 lines
        self.artist_textbox.insert("end", f"{quary_output[0]}\n")
        self.artist_textbox.insert("end", f"{quary_output[1]}\n")

        n_albums = re.findall(r'[0-9]+', quary_output[1])[0]
        
        line = 2

        for i in range(2, int(n_albums)):
            self.artist_textbox.insert("end", f"Album {i - 1} : {quary_output[i]}\n")
            line += 1

        #self.artist_textbox.insert("end", f"{output.decode()}")
        self.artist_textbox.configure(state='disable')

    # def __init__(self):
    #     super().__init__()

    #     # configure window
    #     self.title("CustomTkinter complex_example.py")
    #     self.geometry(f"{1100}x{580}")

    #     # configure grid layout (4x4)
    #     self.grid_columnconfigure(1, weight=1)
    #     self.grid_columnconfigure((2, 3), weight=0)
    #     self.grid_rowconfigure((0, 1, 2), weight=1)

    #     # create sidebar frame with widgets
    #     self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
    #     self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
    #     self.sidebar_frame.grid_rowconfigure(4, weight=1)
    #     self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CustomTkinter", font=customtkinter.CTkFont(size=20, weight="bold"))
    #     self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
    #     self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
    #     self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
    #     self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
    #     self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
    #     self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
    #     self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
    #     self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
    #     self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
    #     self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
    #                                                                    command=self.change_appearance_mode_event)
    #     self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
    #     self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
    #     self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
    #     self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
    #                                                            command=self.change_scaling_event)
    #     self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

    #     # create main entry and button
    #     self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
    #     self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

    #     self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
    #     self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    #     # create textbox
    #     self.textbox = customtkinter.CTkTextbox(self, width=250)
    #     self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

    #     # create tabview
    #     self.tabview = customtkinter.CTkTabview(self, width=250)
    #     self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
    #     self.tabview.add("CTkTabview")
    #     self.tabview.add("Tab 2")
    #     self.tabview.add("Tab 3")
    #     self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
    #     self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

    #     self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
    #                                                     values=["Value 1", "Value 2", "Value Long Long Long"])
    #     self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
    #     self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
    #                                                 values=["Value 1", "Value 2", "Value Long....."])
    #     self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
    #     self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
    #                                                        command=self.open_input_dialog_event)
    #     self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
    #     self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
    #     self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

    #     # create radiobutton frame
    #     self.radiobutton_frame = customtkinter.CTkFrame(self)
    #     self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
    #     self.radio_var = tkinter.IntVar(value=0)
    #     self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="CTkRadioButton Group:")
    #     self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
    #     self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0)
    #     self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
    #     self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1)
    #     self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
    #     self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2)
    #     self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

    #     # create slider and progressbar frame
    #     self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
    #     self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
    #     self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
    #     self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
    #     self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
    #     self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
    #     self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
    #     self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
    #     self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
    #     self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
    #     self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
    #     self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
    #     self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
    #     self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
    #     self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
    #     self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")

    #     # create scrollable frame
    #     self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="CTkScrollableFrame")
    #     self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
    #     self.scrollable_frame.grid_columnconfigure(0, weight=1)
    #     self.scrollable_frame_switches = []
    #     for i in range(100):
    #         switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
    #         switch.grid(row=i, column=0, padx=10, pady=(0, 20))
    #         self.scrollable_frame_switches.append(switch)

    #     # create checkbox and switch frame
    #     self.checkbox_slider_frame = customtkinter.CTkFrame(self)
    #     self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
    #     self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
    #     self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
    #     self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
    #     self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
    #     self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
    #     self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

    #     # set default values
    #     self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
    #     self.checkbox_3.configure(state="disabled")
    #     self.checkbox_1.select()
    #     self.scrollable_frame_switches[0].select()
    #     self.scrollable_frame_switches[4].select()
    #     self.radio_button_3.configure(state="disabled")
    #     self.appearance_mode_optionemenu.set("Dark")
    #     self.scaling_optionemenu.set("100%")
    #     self.optionmenu_1.set("CTkOptionmenu")
    #     self.combobox_1.set("CTkComboBox")
    #     self.slider_1.configure(command=self.progressbar_2.set)
    #     self.slider_2.configure(command=self.progressbar_3.set)
    #     self.progressbar_1.configure(mode="indeterminnate")
    #     self.progressbar_1.start()
    #     self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
    #     self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
    #     self.seg_button_1.set("Value 2")

    # def open_input_dialog_event(self):
    #     dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
    #     print("CTkInputDialog:", dialog.get_input())

    # def change_appearance_mode_event(self, new_appearance_mode: str):
    #     customtkinter.set_appearance_mode(new_appearance_mode)

    # def change_scaling_event(self, new_scaling: str):
    #     new_scaling_float = int(new_scaling.replace("%", "")) / 100
    #     customtkinter.set_widget_scaling(new_scaling_float)

    # def sidebar_button_event(self):
    #     print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()

