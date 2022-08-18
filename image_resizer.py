import PySimpleGUI as sg
from PIL import Image, ImageOps
from io import BytesIO 
from pathlib import Path

def update_img(original, height, width, flipx, flipy):
    global image
    image = original.resize((height, width))

    if flipx == True:
        image = ImageOps.mirror(image)
    if flipy == True:
        image = ImageOps.flip(image)

    bio = BytesIO()
    image.save(bio, format = 'PNG')

    window['-IMAGE-'].update(data = bio.getvalue())


start_layout = [[sg.Input(key='-FILENAME-'),sg.Button('Browse')]]

window = sg.Window('Image Resizer', start_layout)

while True:
    event, values = window.read(timeout=50)
    if event == sg.WIN_CLOSED:
        break
    if event == 'Browse':
        image_path = sg.popup_get_file('Open', no_window=True)
        window.close()
        original = Image.open(image_path)
        control_col = sg.Column([
            [sg.Text('Height: '), sg.Input(size=(5,1), default_text=original.height, key='-HEIGHT-')],
            [sg.Text('Width: '), sg.Input(size=(5,1), default_text=original.width, key='-WIDTH-')],
            [sg.Checkbox('Flip x', key='-FLIPX-'), sg.Checkbox('Flip y', key='-FLIPY-')],
            [sg.Button('Update', key='-UPDATE-'), sg.Button('Save', key='-SAVE-')]
        ])
        image_col = sg.Column([[sg.Image(image_path, key='-IMAGE-')]])
        resizer_layout = [[
            [sg.VPush()],
            [control_col, sg.Push(), image_col, sg.Push()],
            [sg.VPush()]
            ]]
        window = sg.Window('Image Resizer', resizer_layout, finalize=True, size=(1280,720), element_justification='center')
    
    if event == '-UPDATE-':
        update_img(
            original,
            int(values['-HEIGHT-']),
            int(values['-WIDTH-']),
            values['-FLIPX-'],
            values['-FLIPY-']
            )

    if event == '-SAVE-':
        file_name = sg.popup_get_file('Save as', no_window=True, save_as =True) + '.png'
        if file_name:
            image.save(file_name, 'PNG')


window.close()