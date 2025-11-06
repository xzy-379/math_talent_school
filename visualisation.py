import os
import tkinter as tk

import matplotlib.pyplot as plt

import input_files.data_read as dw
import output.sus_test as sus_test

PATH = os.getcwd()

file = PATH + "/test_data/22.json"


def get_graphics(time, distance):
    # graph for time
    #dw.n
    x = [i for i in range(int(dw.MAX_TEST_TIME * 1.1))]
    y = [dw.time_check(i) for i in x]
    plt.scatter(3, 1, color="red", s=100, zorder=5, label="")
    plt.plot(x, y)
    plt.ylabel("checked_time")
    plt.xlabel("time in minutes")
    plt.savefig(PATH + "/input_files/time.png")
    plt.close()
    # graph for distance
    x = [i for i in range(int(dw.MAX_DIST * 1.1))]
    y = [dw.distance_check(i) for i in x]
    plt.scatter(3, 1, color="red", s=100, zorder=5, label="")
    plt.plot(x, y)
    plt.ylabel("checked_distance")
    plt.xlabel("distance in km")
    plt.savefig(PATH + "/input_files/distance.png")
    plt.close()


input_values = dw.check(file)

img_dist = PATH + "/input_files/distance.png"
img_time = PATH + "/input_files/time.png"

teststelle, PZN, time, distance, _ = input_values
tested_values = sus_test.evaluate(teststelle, PZN, time, distance)
root = tk.Tk()
root.title("talent_school")
root.geometry("1800x720")

tk.Label(root, text=file).pack()

tk.Label(root, text=f"input values: {input_values}").pack()
tk.Label(root, text=f"tested values {tested_values}").pack()

img_time = tk.PhotoImage(file=img_time)
image_time_label = tk.Label(root, image=img_time)
image_time_label.pack(side="left", padx=15)

img_dist = tk.PhotoImage(file=img_dist)
image_dist = tk.Label(root, image=img_dist)
image_dist.pack(side="left", padx=15)
root.mainloop()
