import math
import tkinter as tk
from PIL import Image, ImageTk
import pywinauto as pwa
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import time


class MortarCalculator:
    pixel_scale = 6.08108108
    shell_gravity = 34.65 #34.75 original
    shell_muzzle_velocity = 415
    player_gravity = 36.36
    player_muzzle_velocity = 397.82
    gravity = 34.75
    muzzle_velocity = 415
    def __init__(self):
        self.azimuth = 0
        self.azimuth_1 = 0

        self.cal_x = 0
        self.cal_y = 0

        self.cal_x_1 = 0
        self.cal_y_1 = 0

        self.x = 0
        self.y = 0

        self.ship_x = 0
        self.ship_y = 0

        self.target_x = 0
        self.target_y = 0

        self.on_canvas = None

        self.map_opened = False
        self.root = tk.Tk()
        self.root.title("Mortar Calculator")
        self.root.geometry("350x400")

        self.root.attributes('-topmost', True)
        self.root.resizable(False, False)

        self.frame = tk.Frame(self.root)

        self.open_map_button = tk.Button(self.frame, text="Calibrate", command=self.calibration)
        self.open_map_button.pack(side="top", padx=5, pady=5)

        OPTIONS_CAL = ["One Point", "Two Point"]
        default_cal = tk.StringVar(self.frame)
        default_cal.set(OPTIONS_CAL[0])
        self.calibration_type = "One Point"
        self.select_calibration = tk.OptionMenu(self.frame, default_cal,*OPTIONS_CAL, command=self.__set_calibration_type)
        self.select_calibration.pack(side="top", padx=5, pady=5)
        OPTIONS_AMM = ["Player", "Shell"]
        default_amm = tk.StringVar(self.frame)
        default_amm.set(OPTIONS_AMM[1])
        self.select_ammunition = tk.OptionMenu(self.frame, default_amm,*OPTIONS_AMM, command=self.__set_ammunition_type)
        self.select_ammunition.pack(side="top", padx=5, pady=5)

        aim_button = tk.Button(self.root,text = "Open Roblox to Use.")
        self.app = None
        self.window = None
        try:
            self.app = Application(backend="uia").connect(title="Roblox")
            self.window = self.app.window(best_match="Roblox")
            self.window.set_focus()
            self.window.maximize()
            time.sleep(1)
            aim_button.configure(text="Azimuth Controls", command=self.__subdegree)
        except pwa.findwindows.ElementNotFoundError:
            print("No window found!")
            aim_button.configure(state=tk.DISABLED)


            
        target_button = tk.Button(self.frame, text = "Select Target", command=self.__set_target)
        aim_button.pack(side = "bottom",padx=5, pady=5)
        target_button.pack(side="bottom", padx=5, pady=5)
        self.frame.pack(side="top")

        self.root.mainloop()


    def __set_calibration_type(self, value):
        self.calibration_type = value
    def __set_ammunition_type(self,value):
        if value == "Shell":
            self.gravity = self.shell_gravity
            self.muzzle_velocity = self.shell_muzzle_velocity
        else:
            if value == "Player":
                self.gravity = self.player_gravity
                self.muzzle_velocity = self.player_muzzle_velocity

    def __subdegree(self):
        sleep_time = 0.3
        degree_window = tk.Toplevel(self.root)
        degree_window.attributes('-topmost', True)
        degree_window.resizable(False, False)
        degree_window.geometry("400x300")

        self.displ = 0
        label = tk.Label(degree_window, text="Displacement: " + str(self.displ))

        frame = tk.Frame(degree_window)
        def counterclockwise():
            self.displ-=0.1
            label.config(text="Displacement: " + str(self.displ) + "°")
            self.window.set_focus()
            self.window.maximize()
            time.sleep(0.1)
            send_keys("{a down}")
            time.sleep(sleep_time)
            send_keys("{a up}")
            time.sleep(0.1)
            send_keys("{d down}")
            time.sleep(sleep_time - 0.0166666667)
            send_keys("{d up}")
            time.sleep(1)
        counter_clockwise_button = tk.Button(frame, text="Counter Clockwise", command=counterclockwise)

        def clockwise():
            self.displ += 0.1
            label.config(text = "Displacement: " + str(self.displ) + "°")
            self.window.set_focus()
            self.window.maximize()
            time.sleep(0.1)
            send_keys("{d down}")
            time.sleep(sleep_time)
            send_keys("{d up}")
            time.sleep(0.1)
            send_keys("{a down}")
            time.sleep(sleep_time - 0.0166666667)
            send_keys("{a up}")
            time.sleep(1)
        clockwise_button = tk.Button(frame, text="Clockwise", command=clockwise)

        def reset():
            self.displ = 0
            label.config(text="Displacement: " + str(self.displ))
        reset_button = tk.Button(degree_window, text="Reset Displacement", command=reset)

        instruction_label = tk.Label(degree_window, text="Use reset to set accumulated\n displacement to 0")

        counter_clockwise_button.pack(side="left", padx=5, pady=5)
        clockwise_button.pack(side="right", padx=5, pady=5)
        reset_button.pack(side="top", padx=5, pady=5)
        frame.pack(side="top", padx=5, pady=5)
        label.pack(side="top", padx=5, pady=10)
        instruction_label.pack(side="top", padx=5, pady=5)

        degree_window.mainloop()



    def __set_target(self):
        if self.map_opened:
            return
        self.map_opened = True

        isle_map = tk.Toplevel(master=self.root)
        isle_map.title("Select Target")
        isle_map.geometry("600x650")
        isle_map.attributes('-topmost', True)
        isle_map.resizable(False, False)

        image_path = "Map.png"
        pil_image = Image.open(image_path).resize((520,390))
        img = ImageTk.PhotoImage(pil_image)

        canvas = tk.Canvas(isle_map, width=520, height=390)
        canvas.config(background="white")
        canvas.create_image(0,0,anchor=tk.NW, image=img)

        x_line = canvas.create_line(0,0,520,0,fill = 'red', width=1)
        y_line = canvas.create_line(0,0,0,390,fill = 'red', width=1)

        instructions = tk.Label(isle_map, text="Select target point.")

        x_pos_label = tk.Label(isle_map, text="X: 0")
        y_pos_label = tk.Label(isle_map, text="Y: 0")


        self.on_canvas = False
        def on_motion(event):
            self.x = event.x
            self.y = event.y

            x_pos_label.config(text = "X: " + str(int(event.x*self.pixel_scale)))
            y_pos_label.config(text = "Y: " + str(int(event.y*self.pixel_scale)))
            if self.on_canvas:
                canvas.coords(x_line, 0, self.y, 520, self.y)
                canvas.coords(y_line, self.x, 0, self.x, 390)
                canvas.update()

        isle_map.bind('<Motion>', on_motion)

        solution_label = tk.Label(isle_map, text="")
        def calculate():
            print("Ship Position: " , self.ship_x," ",self.ship_y)
            print("Target Position: ", self.target_x, " ", self.target_y)
            azimuth = -math.degrees(math.atan2(self.target_y - self.ship_y,self.target_x - self.ship_x))
            if azimuth < 0:
                azimuth += 360
            distance = math.sqrt((self.ship_x - self.target_x)**2+(self.ship_y - self.target_y)**2)
            try:
                angle_1 = math.atan((self.muzzle_velocity ** 2 + math.sqrt(
                    self.muzzle_velocity ** 4 - self.gravity ** 2 * distance ** 2)) / (self.gravity * distance))
                angle_2 = math.atan((self.muzzle_velocity ** 2 - math.sqrt(
                    self.muzzle_velocity ** 4 - self.gravity ** 2 * distance ** 2)) / (self.gravity * distance))
                angle_1 = math.degrees(angle_1)
                angle_2 = math.degrees(angle_2)
                angle = 0
                if not math.isnan(angle_1) and not math.isnan(angle_2):
                    if 87 > angle_1 > 44:
                        angle = str(round(angle_1,2))
                    if 87 > angle_2 > 44 and angle_2>angle_1:
                        angle = str(round(angle_2,2))
                    if (angle_1<44 or  angle_1>87) and (angle_2<44 or angle_2>87):
                        angle = "No solution possible"
                    print(angle_1 , " ", angle_2)
                elif not math.isnan(angle_2):
                    print(angle_2)
                    angle = str(round(angle_2,2))
                elif not math.isnan(angle_1):
                    print(angle_1)
                    angle = str(round(angle_1,2))
                else:
                    print("No solution possible")
                    angle = "No solution possible"

                solution = "Azimuth: " + str(round(azimuth, 1)) + "° Angle: " + str(angle) + "°"
                solution_label.configure(text=solution)
                solution_label.pack()
            except ValueError:
                solution = "No solution possible"
                solution_label.configure(text=solution)
                solution_label.pack()


        select = tk.Button(isle_map, text='Enter', command=calculate)

        canvas.pack()

        instructions.pack()
        x_pos_label.pack()
        y_pos_label.pack()



        select.pack(side="bottom", padx=5, pady=5)

        self.on_canvas = False
        def reset(event):
            if event.widget != isle_map:
                return
            self.map_opened = False
        isle_map.bind("<Destroy>", reset)
        target = canvas.create_oval(-10, -10, -6, -6, fill="red")
        def select_target(event):
            if not self.on_canvas:
                return
            canvas.coords(target, event.x - 2, event.y - 2, event.x + 2, event.y + 2)
            self.target_x = event.x * self.pixel_scale
            self.target_y = event.y * self.pixel_scale
            print("Target Position: ", self.target_x, " ", self.target_y)

            canvas.update()
        def hide_cursor(event):
            self.on_canvas = True
            event.widget.config(cursor="none")

        def show_cursor(event):
            canvas.coords(x_line, 0, -10, 520, -10)
            canvas.coords(y_line, -10, 0, -10, 390)
            canvas.update()
            self.on_canvas = False
            event.widget.config(cursor="arrow")


        canvas.bind("<Enter>", hide_cursor)
        canvas.bind("<Leave>", show_cursor)

        isle_map.bind("<Button-1>", select_target)
        isle_map.mainloop()

#TODO:HIGHLIGHTED
    def calibration(self):
        if self.map_opened:
            return
        self.map_opened = True
        isle_map = tk.Toplevel(master=self.root)
        isle_map.title("Calibration Point Setup")
        isle_map.geometry("600x650")
        isle_map.attributes('-topmost', True)
        isle_map.resizable(False, False)
        image_path = "Map.png"
        pil_image = Image.open(image_path).resize((520,390))
        img = ImageTk.PhotoImage(pil_image)

        x_pos_label = tk.Label(isle_map, text="X: 0")
        y_pos_label = tk.Label(isle_map, text="Y: 0")

        canvas = tk.Canvas(isle_map, width=520, height=390)

        canvas.config(background="white")
        canvas.create_image(0,0,anchor=tk.NW, image=img)

        self.on_canvas = False
        def hide_cursor(event):
            self.on_canvas = True
            event.widget.config(cursor="none")

        def show_cursor(event):
            canvas.coords(x_line, 0, -10, 520, -10)
            canvas.coords(y_line, -10, 0, -10, 390)
            canvas.update()
            self.on_canvas = False
            event.widget.config(cursor="arrow")


        canvas.bind("<Enter>", hide_cursor)
        canvas.bind("<Leave>", show_cursor)

        x_line = canvas.create_line(0,0,520,0,fill = 'red', width=1)
        y_line = canvas.create_line(0,0,0,390,fill = 'red', width=1)

        self.cal_x = 0
        self.cal_y = 0
        self.cal_x_1 = 0
        self.cal_y_1 = 0

        if self.calibration_type == "One Point":
            instruct_label = tk.Label(isle_map, text="Select calibration point.")
            instruct_label.pack(side = 'bottom', padx=5, pady=5)
            canvas.itemconfigure(x_line, fill = "green")
            canvas.itemconfigure(y_line, fill="green")
            cal_point = canvas.create_oval(-10,-10,-6,-6, fill="green")
            def set_calibration_point(event):
                canvas.coords(cal_point,event.x - 2, event.y - 2, event.x + 2, event.y + 2)
                self.cal_x = event.x*self.pixel_scale
                self.cal_y = event.y*self.pixel_scale
                canvas.update()


            canvas.bind("<Button-1>", set_calibration_point)

            def select_point():
                canvas.unbind("<Button-1>")
                instruct_label.config(text="Aim at calibration point and enter respective azimuth and elevation information.")
                azimuth_label = tk.Label(isle_map, text="Azimuth:")
                elevation_label = tk.Label(isle_map, text="Elevation:")
                azimuth_entry = tk.Entry(isle_map, width=4)
                elevation_entry = tk.Entry(isle_map, width=4)
                azimuth_entry.insert(0, "212")
                elevation_entry.insert(0, "44.0")
                azimuth_label.pack(side="left", padx=5, pady=5)
                azimuth_entry.pack(side="left", padx=5, pady=5)
                elevation_label.pack(side="left", padx=5, pady=5)
                elevation_entry.pack(side="left", padx=5, pady=5)

                def send_data():
                    select.config(state="disabled")
                    azimuth = float(azimuth_entry.get())
                    elevation = float(elevation_entry.get())

                    travel_time = 2*math.sin(math.radians(elevation))*self.muzzle_velocity/self.gravity
                    horizontal_distance = travel_time*math.cos(math.radians(elevation))*self.muzzle_velocity

                    y_direction = math.sin(math.radians(azimuth))*horizontal_distance
                    x_direction = -math.cos(math.radians(azimuth))*horizontal_distance

                    self.ship_x = self.cal_x+x_direction
                    self.ship_y = self.cal_y+y_direction

                    isle_map.destroy()



                select.config(command=send_data)


            select = tk.Button(isle_map, text='Enter', command=select_point)
            select.pack(side="bottom", padx=5, pady=5)
        else:
            instruct_label = tk.Label(isle_map, text="Select calibration point 1.")
            instruct_label.pack(side='bottom', padx=5, pady=5)
            canvas.itemconfigure(x_line, fill = "red")
            canvas.itemconfigure(y_line, fill="red")
            azimuth_label = tk.Label(isle_map, text="Azimuth:")
            azimuth_entry = tk.Entry(isle_map, width=4)
            cal_point = canvas.create_oval(-10,-10,-6,-6, fill="red")
            cal_point_2 = canvas.create_oval(-10, -10, -6, -6, fill="green")
            def set_calibration_point_1(event):
                canvas.coords(cal_point,event.x - 2, event.y - 2, event.x + 2, event.y + 2)
                self.cal_x = event.x*self.pixel_scale
                self.cal_y = event.y*self.pixel_scale
                canvas.update()
            def select_point_1():
                canvas.unbind("<Button-1>")
                instruct_label.config(text="Aim at calibration point and enter azimuth information.")
                azimuth_entry.insert(0, "212")
                azimuth_label.pack(side="left", padx=5, pady=5)
                azimuth_entry.pack(side="left", padx=5, pady=5)
                select.config(command=setup_point_2)
            def setup_point_2():
                canvas.itemconfigure(x_line,fill = "green")
                canvas.itemconfigure(y_line, fill="green")
                def set_calibration_point_2(event):
                    canvas.coords(cal_point_2, event.x - 2, event.y - 2, event.x + 2, event.y + 2)
                    self.cal_x_1 = event.x * self.pixel_scale
                    self.cal_y_1 = event.y * self.pixel_scale
                    canvas.update()
                canvas.bind("<Button-1>", set_calibration_point_2)
                instruct_label.config(text="Select calibration point 2.")
                select.config(command=select_point_2)

                azimuth_label.pack_forget()
                azimuth_entry.pack_forget()
                canvas.update()

            def select_point_2():
                canvas.unbind("<Button-1>")
                self.azimuth = float(azimuth_entry.get())
                azimuth_entry.delete(0, tk.END)
                azimuth_entry.insert(0, "212")
                instruct_label.config(text="Aim at calibration point and enter azimuth information.")
                azimuth_label.pack(side="left", padx=5, pady=5)
                azimuth_entry.pack(side="left", padx=5, pady=5)
                select.config(command=send_data)

            def send_data():
                select.config(state="disabled")

                self.azimuth_1 = float(azimuth_entry.get())
                m_1 = -math.tan(math.radians(self.azimuth))
                m_2 = -math.tan(math.radians(self.azimuth_1))


                b_2 = self.cal_y_1-self.cal_x_1*m_2
                b_1 = self.cal_y-self.cal_x*m_1

                x_intersect = (b_2-b_1)/(m_1-m_2)
                y_intersect = m_1*(x_intersect-self.cal_x)+self.cal_y

                self.ship_x = x_intersect
                self.ship_y = y_intersect

                isle_map.destroy()

            canvas.bind("<Button-1>", set_calibration_point_1)
            select = tk.Button(isle_map, text='Enter', command=select_point_1)
            select.pack(side="bottom", padx=5, pady=5)


        def on_motion(event):
            self.x = event.x
            self.y = event.y

            x_pos_label.config(text = "X: " + str(int(event.x*self.pixel_scale)))
            y_pos_label.config(text = "Y: " + str(int(event.y*self.pixel_scale)))
            if self.on_canvas:
                canvas.coords(x_line, 0, self.y, 520, self.y)
                canvas.coords(y_line, self.x, 0, self.x, 390)
                canvas.update()

        isle_map.bind('<Motion>', on_motion)

        def reset(event):
            if event.widget != isle_map:
                return
            self.map_opened = False
        isle_map.bind("<Destroy>", reset)

        y_pos_label.pack(side="bottom")
        x_pos_label.pack(side="bottom")
        canvas.pack()

        isle_map.mainloop()











calculator = MortarCalculator()




