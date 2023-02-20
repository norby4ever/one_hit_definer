from tkinter import Tk, TOP, LabelFrame, Entry, Button, Label, simpledialog
import requests


def lastfm_get(username, API_KEY, artist):
    # define headers and URL
    headers = {'user-agent': username}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    params = (
        ('method', 'artist.gettoptracks'),
        ('artist', artist),
        ('api_key', API_KEY),
        ('format', 'json'),
    )

    response = requests.get(url, headers=headers, params=params)
    return response


def one_hit_definer(username, API_KEY):
    print(username, API_KEY)
    artist = field.get()

    try:
        res = lastfm_get(username, API_KEY, artist).json()['toptracks']['track']
        for i in range(2):
            hits[i].config(text=str(i + 1) + '. ' + res[i]['name'] + ' (' + res[i]['listeners'] + ' listeners)',
                           font=12, fg='red')

        for i in range(2, 5):
            hits[i].config(text=str(i + 1) + '. ' + res[i]['name'] + ' (' + res[i]['listeners'] + ' listeners)',
                           font=12, fg='black')

        if int(res[0]['listeners']) < 1000:
            hits[-1].config(text='Too few listeners to define.', font=12, fg='magenta')
        elif int(res[0]['listeners']) > int(res[1]['listeners']) * 2:
            hits[-1].config(text='✔ It\'s one hit wonder!', font=20, fg='green')
        else:
            hits[-1].config(text='⊗ It\'s not one hit wonder.', font=20, fg='darkmagenta')

    except KeyError:
        hits[0].config(text='Artist not found ☹', font=15, fg='red')
        hits[0].pack(side=TOP)
        for i in range(1, 6):
            hits[i].config(text='')

    except IndexError:
        hits[0].config(text='There is less than 5 tracks. :(', font=15, fg='red')
        hits[0].pack(side=TOP)
        for i in range(1, 6):
            hits[i].config(text='')


window = Tk()
username = simpledialog.askstring('Username', 'Enter your last.fm username:', parent=window)
API_KEY = simpledialog.askstring('API KEY', 'Enter API key:', parent=window)
window.title('One Hit Wonder Calculator v.0.2')
window.geometry('600x400')
window.resizable(False, False)
f_top = LabelFrame(window, text="Enter artist:", font=15, padx=10, pady=10)
f_top.pack()
f_bot = LabelFrame(window, text="Results:", font=15, padx=10, pady=10)
field = Entry(f_top, font=15)
field.pack(side=TOP)
field.focus()
field.bind('<Return>', one_hit_definer)
Button(window, text='Calculate', font=15, command=lambda: one_hit_definer(username, API_KEY),
       padx=10, pady=10).pack(side=TOP)
f_bot.pack(side=TOP)
hits = [Label(f_bot), Label(f_bot), Label(f_bot), Label(f_bot), Label(f_bot), Label(f_bot)]
for i in range(6):
    hits[i].pack()

window.mainloop()
