Switch Debouncing
=================

A tool to show the effect of debouncing algorithms on bouncy signals.
Includes a bouncy signal generator along with the debounce logic.

The current debouncer is based on the Counting Algorithm listed [here](http://www.ganssle.com/debouncing-pt2.htm).

The following code instantiates a debouncer that checks the bouncy signal every 5 milliseconds.
Also assumes 15 milliseconds to register a press event and 100 milliseconds a release event.

    db = Debouncer(check_sec=0.005, press_sec=0.015, release_sec=0.1)

The following code generates a bouncy signal with a bouncing time of 20 milliseconds

    analog, digital = generate_bouncy_signal(delay_sec=0.02)

The generated signal can be further parameterized with the below positional arguments:

    pre_sec:       Time that button is released
    delay_sec:     Time of bouncing
    post_sec:      Time that button press is settled
    time_step_sec: Signal resolution
    settled_noise: Noise of the signal

The below code debounces the signal. `new_points` has been calculated to contain the time points of the debouncing signal sampling.

    # Debounce the signal
    dbs = []
    for i in new_points:
        key_changed, key_pressed = db.debounce(digital.signal[i])
        dbs.append(key_pressed)
