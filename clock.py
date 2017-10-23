import config
from datetime import datetime
from time import sleep

lights = config.aurora()

def get_animdata_to_color_panels(r, g, b, w, t, ids):
    ids = ids or [panel['panelId'] for panel in lights.rotated_panel_positions]
    num_frames = "1"
    panel_frames = [" ".join(map(str, [id, num_frames, r, g, b, w, t])) for id in ids]
    num_panels = str(len(ids))
    return num_panels + " " + " ".join(panel_frames)

def panel_ids_l2r():
    """
    :return: A list of panel ids, sorted left-to-right.
    """
    return [p['panelId'] for p in sorted(lights.rotated_panel_positions, key=lambda k: k['x'])]

def send(animData):
    print(animData)
    effect_data = {
        "command": "display",
        "animType": "static",
        "animData": animData}
    lights.effect_set_raw(effect_data)

def time_to_colors(leaf_time):
    leaf_time = leaf_time or datetime.now()
    scaled_sec = round(leaf_time.second / 60 * 255)
    seconds_color = [0, scaled_sec, 255 - scaled_sec, 0, 0]

    scaled_mins = round(leaf_time.minute / 60 * 255)
    minutes_color = [0, scaled_mins, 255 - scaled_mins, 0, 0]

    scaled_hours = round(leaf_time.hour / 24 * 255)
    hours_color = [0, scaled_hours, 255 - scaled_hours, 0, 0]
    return {'hours': hours_color, 'minutes': minutes_color, 'seconds': seconds_color}


def update_clock():
    colors = time_to_colors(datetime.now())
    ids = panel_ids_l2r()
    #ids = [128,85,159]

    # color hours, mins and seconds
    send(get_animdata_to_color_panels(*colors['hours'], [ids[0]]))
    send(get_animdata_to_color_panels(*colors['minutes'], [ids[1]]))
    send(get_animdata_to_color_panels(*colors['seconds'], [ids[2]]))

    # color other panels white
    send(get_animdata_to_color_panels(0, 0, 0, 0, 1, ids[3:]))

while True:
    update_clock()
    sleep(0.5)