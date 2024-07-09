import os
for p in os.environ['PATH'].split(os.pathsep):
    if os.path.isdir(p):
        os.add_dll_directory(p)

import corvus_image

camera = corvus_image.camera_handler()
cascade = corvus_image.cascade_handler("assets/haarcascade_frontalface_alt.xml")

prev_detect_pos = [-1, -1]
detected = False
prev_rect_width = 0
prev_rect_height = 0
detect_width_margin = 50
detect_height_margin = 50

pos = [0, 0]
normalized_pos = [-1, -1]

i = 0

while True:
    img = camera.capture()

    if not detected:
        rects = cascade.get_rect(img)
    else:
        rects = cascade.get_rect(img, prev_detect_pos, prev_rect_width + detect_width_margin, prev_rect_height + detect_height_margin)
    
    if len(rects) > 0:
        prev_detect_pos = [int(rects[0]["x"] + rects[0]["width"] / 2), int(rects[0]["y"] + rects[0]["height"] / 2)]
        prev_rect_width = rects[0]["width"]
        prev_rect_height = rects[0]["height"]
        detected = True
        img.draw_rect([rects[0]])
    else:
        detected = False
    
    if not detected:
        pos_list = cascade.get_target_coordinates(img)
    else:
        pos_list = cascade.get_target_coordinates(img, prev_detect_pos, prev_rect_width + detect_width_margin, prev_rect_height + detect_height_margin)
    
    if len(pos_list) > 0:
        pos = pos_list[0]
        normalized_pos = camera.normalize_position(pos)
    else:
        pos = [0, 0]
        normalized_pos = [-1, -1]

    print(pos, normalized_pos[0], normalized_pos[1])

    i += 1
    if i > 100:
        img.save("hello.png")
        break