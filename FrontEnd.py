# Import module
from tkinter import *
import os
from BackEnd import BackEnd


class FrontEnd(BackEnd):

    def __init__(self):
        super().__init__()
        self.root = Tk()
        self.root.geometry("1024x768")
        self.root.title("ShermanEngine V1")
        self.canvas = Canvas(self.root, width=1024, height=768)
        self.canvas.pack(fill="both", expand=True)

        self.images_dict = {}
        self.import_images_from_folder()
        self.engine_image = self.canvas.create_image(0, 0, image=self.images_dict["off"], anchor="nw")

        self.speed_text_id = self.canvas.create_text(510, 480, font=("Ariel", 40), fill="black")
        self.gear_text_id = self.canvas.create_text(510, 585, text="", font=("Ariel", 40), fill="black")
        self.speed_status_str_text_id = self.canvas.create_text(460, 365, text="", font=("Ariel", 15))
        self.speed_status_text_id = self.canvas.create_text(590, 365, text="", font=("Ariel", 15))

        self.copyrights = self.canvas.create_text(512, 750,
                                                  text="Powered By Yevgeni Smorgon & Shaked Kadosh & Ido Sherman",
                                                  font=("Ariel", 10))

        self.start_button = Button(self.root, image=self.images_dict["startengine_off"],
                                   borderwidth=0, command=self.sm.user.raise_start_engine_button)
        self.start_button.config(height=160, width=160)
        self.gas_button = Button(self.root, image=self.images_dict["gas"],
                                 borderwidth=0, command=self.sm.user.raise_gas_pressed_button)
        self.gas_button.config(height=150, width=180)
        self.brake_button = Button(self.root, image=self.images_dict["brake"],
                                   borderwidth=0, command=self.sm.user.raise_brake_pressed_button)
        self.brake_button.config(height=150, width=250)
        self.emergency_brake_button = Button(self.root, image=self.images_dict["emergencybrakebutton_off"],
                                             borderwidth=0, command=self.sm.user.raise_emergency_brake_button)
        self.emergency_brake_button.config(height=160, width=160)


        # Display Buttons
        self.canvas.create_window(50, 50, anchor="nw", window=self.start_button)
        self.canvas.create_window(800, 590, anchor="nw", window=self.gas_button)
        self.canvas.create_window(50, 590, anchor="nw", window=self.brake_button)
        self.canvas.create_window(800, 50, anchor="nw", window=self.emergency_brake_button)

    def update_gui(self):
        self.monitor_engine_started()
        self.monitor_buttons()
        self.monitor_gear_change()
        self.monitor_status_change()
        self.monitor_speed_status()
        self.root.after(1000, self.update_gui)

    def monitor_buttons(self):
        # disable start button when engine is working
        if self.gear and self.gear > 0:
            self.start_button["state"] = "disabled"
        else:
            self.start_button["state"] = "normal"


        # disable gas and brake buttons when system in overloaded start

        if self.status == "OverLoaded" or self.status == "EmergencyBrake":
            self.gas_button["state"] = "disabled"
            self.brake_button["state"] = "disabled"
            self.emergency_brake_button["state"] = "disabled"
            self.emergency_brake_button.configure(image=self.images_dict["emergencybrakebutton_on"])
        else:
            # allow press the emergency button only when speed change status is acc/slow
            if self.engineStarted and self.speed_change_status and self.speed_change_status != "Static":
                self.emergency_brake_button["state"] = "normal"
            else:
                self.emergency_brake_button["state"] = "disabled"
            self.emergency_brake_button.configure(image=self.images_dict["emergencybrakebutton_off"])
            # disable gas or brake when one of them pressed or engine is off
            if self.speed_change_status == "Accellerating" or not self.engineStarted:
                self.gas_button["state"] = "disabled"
            else:
                self.gas_button["state"] = "normal"

            if self.speed_change_status == "Slowing" or not self.engineStarted:
                self.brake_button["state"] = "disabled"
            else:
                self.brake_button["state"] = "normal"
            # self.gas_button["state"] = "normal"
            # self.brake_button["state"] = "normal"

    def monitor_gear_change(self):
        if self.gear is not None:  # not None -> engine started

            self.canvas.itemconfig(self.engine_image, image=self.images_dict[str(self.gear)])

    def monitor_status_change(self):
        if self.status == "OverLoaded":
            self.canvas.itemconfig(self.engine_image, image=self.images_dict[self.status])

        elif self.status == "InOverLoading" and self.sm.system.counter:  # display count until it gets overloded
            self.canvas.itemconfig(self.engine_image, image=self.images_dict["InOverLoading" + str(self.sm.system.counter)])
        elif self.status == "EmergencyBrake":
            self.canvas.itemconfig(self.engine_image, image=self.images_dict[self.status])

    def monitor_engine_started(self):
        if self.engineStarted:  # if engine started write the current speed
            self.canvas.itemconfig(self.speed_text_id, text=str(self.sm.system.speed), fill="grey")
            self.canvas.itemconfig(self.gear_text_id, text=str(self.gear), fill="grey")
            self.start_button.configure(image=self.images_dict["startengine_on"])
        else:  # if the engine is in stand by display off image
            self.start_button.configure(image=self.images_dict["startengine_off"])
            self.canvas.itemconfig(self.engine_image, image=self.images_dict["off"])
            self.canvas.itemconfig(self.gear_text_id, text="")
            self.canvas.itemconfig(self.speed_text_id, text="")

    def import_images_from_folder(self):
        # Add all relevant images file
        images_folder = os.path.join(os.path.dirname(__file__), 'images')
        images_list = os.listdir(images_folder)
        for file_ in images_list:
            file_name_without_extension = file_.split(".")[0]
            self.images_dict[file_name_without_extension] = PhotoImage(file=images_folder + "\\" +file_)

    def monitor_speed_status(self):
        if self.engineStarted and self.speed_change_status:
            self.canvas.itemconfig(self.speed_status_text_id, text=self.speed_change_status)
            self.canvas.itemconfig(self.speed_status_str_text_id, text="Speed Status:")
        else:
            self.canvas.itemconfig(self.speed_status_text_id, text="")
            self.canvas.itemconfig(self.speed_status_str_text_id, text="")

    def start_gui(self):
        while not self.sm.is_final():
            # Execute tkinter
            self.root.after(1000, self.update_gui)
            self.root.mainloop()
        self.shutdown()


if __name__ == '__main__':
    shermanEngine = FrontEnd()
    shermanEngine.setup()
    shermanEngine.start_gui()
