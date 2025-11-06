import os
import tkinter as tk

import matplotlib.pyplot as plt

import input_files.data_read as dw
import output.sus_test as sus_test

PATH = os.getcwd()

file = PATH + "/test_data/01.json"

img_dist_path = PATH + "/input_files/distance.png"
img_time_path = PATH + "/input_files/time.png"
input_values = ()
tested_values = ()


def get_graphics(time, distance):

    # graph for time
    x = [i for i in range(int(dw.MAX_TEST_TIME * 1.1))]
    y = [dw.time_check(i) for i in x]
    plt.scatter(time, dw.time_check(time), color="red", s=100, zorder=5, label="time")
    plt.plot(x, y)
    plt.ylabel("checked_time")
    plt.xlabel("time in minutes")
    plt.savefig(PATH + "/input_files/time.png")
    plt.close()

    # graph for distance
    x = [i for i in range(int(dw.MAX_DIST * 1.1))]
    y = [dw.distance_check(i) for i in x]
    plt.scatter(
        distance,
        dw.distance_check(distance),
        color="red",
        s=100,
        zorder=5,
        label="distance",
    )
    plt.plot(x, y)
    plt.ylabel("checked_distance")
    plt.xlabel("distance in km")
    plt.savefig(PATH + "/input_files/distance.png")
    plt.close()


def new_file(num):
    global input_values, tested_values, file
    file = PATH + f"/test_data/{str(num).zfill(2)}.json"
    input_values = dw.check(file)

    teststelle, PZN, time, distance, original = input_values
    get_graphics(original[2], original[3])

    tested_values = sus_test.estimate_Oliver(distance, teststelle, time, PZN)


def update():
    global file, img_time_path, img_dist_path, input_text, test_text
    new_file(int(entry.get()))
    input_text = f"input values: \nlegit name: {input_values[0]} \nlegit pzn: {input_values[1]} \nlegit time: {input_values[2]} \nlegit distance: {input_values[3]}"
    print(tested_values)
    test_text = f"overall fraud score: {tested_values[0]*100}% \nhigh sus: {tested_values[1][0]} \nmid sus: {tested_values[1][1]} \nlow sus: {tested_values[1][2]}"
    img_time = tk.PhotoImage(file=img_time_path)
    image_time_label.config(image=img_time)
    image_time_label.image = img_time

    img_dist = tk.PhotoImage(file=img_dist_path)
    image_dist_label.config(image=img_dist)
    image_dist_label.image = img_dist

    file_label.config(text="file: "+ file)
    file_label.text = file

    input_value_label.config(text=input_text)
    input_value_label.text = input_text

    test_value_label.config(text=test_text)
    test_value_label.text = test_text


if __name__ == "__main__":
    new_file(1)
    root = tk.Tk()
    root.title("talent_school")
    root.geometry("1340x720")
    file_label = tk.Label(root)
    file_label.pack()

    input_value_label = tk.Label(root)
    input_value_label.pack()
    test_value_label = tk.Label(root)
    test_value_label.pack()
    img_time = tk.PhotoImage(file=img_time_path)
    entry = tk.Spinbox(root, from_=1, to=30)
    entry.pack()
    tk.Button(root, text="update", command=update).pack()
    image_time_label = tk.Label(root, image=img_time)
    image_time_label.pack(side="left", padx=15)

    img_dist = tk.PhotoImage(file=img_dist_path)
    image_dist_label = tk.Label(root, image=img_dist)
    image_dist_label.pack(side="left", padx=15)

    root.mainloop()
