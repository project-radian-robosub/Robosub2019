import time

targets = [0, 0, 0, 0, 0, 0]  # forward-backward, left-right, up-down, roll, pitch, yaw
motor_strings = ["050", "050", "050", "050", "050", "050"]
current_vals = [0, 0, 0, 0, 0, 0]


def remap(x, b1, b2, v1, v2):
    prop = (x - b1) / (b2 - b1)
    new_prop = prop * (v2 - v1)
    new = v1 + new_prop
    return new


def coroutine(func):
    def start(*args, **kwargs):
        g = func(*args, **kwargs)
        g.__next__()
        return g
    return start


def vals_to_serial(vals):
    for i in range(len(vals)):
        motor_strings[i] = str(int(remap(vals[i], -100, 100, 0, 100)))
        while len(motor_strings[i]) < 3:
            motor_strings[i] = '0' + motor_strings[i]
    write_all = ''
    for i in motor_strings:
        write_all += i
    print(write_all)


def motor_generator():
    try:
        while True:
            for motor_num in range(6):
                if current_vals[motor_num] < targets[motor_num]:

                    current_vals[motor_num] += 5

                if current_vals[motor_num] > targets[motor_num]:

                    current_vals[motor_num] -= 5

            vals_to_serial(current_vals)
            time.sleep(.01)

            yield

    except GeneratorExit:
        print("motor co-routine closed")


motors = motor_generator()

targets = [0, 100, 0, 100, 0, 0]

while time.perf_counter() < .5:
    motors.__next__()
print('change')
targets = [0, -100, -100, -100, 100, 100]

while time.perf_counter() < 1:
    motors.__next__()


