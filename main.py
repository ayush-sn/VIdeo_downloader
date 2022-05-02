from pytube import *
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
from tkinter.messagebox import *
from threading import *
from tkinter.ttk import Progressbar
import webbrowser

file_size = 0
flag = 0


# YOUTUBE OPEN---------------------------------------------------------------------------------------------
def open_youtube():
    search = search_field.get()
    if search == '':
        showinfo('ERROR', 'Please enter the query in search box')
    else:
        lst = search.split(' ')
        search = '+'.join(lst)
        webbrowser.open('https://www.youtube.com/results?search_query={}'.format(search))


# PROGRESS CHECK-------------------------------------------------------------------------------------------
def progress_check(stream=None, chunk=None, remaining=None):
    file_downloaded = file_size - remaining
    percent = ((file_downloaded * 100) / file_size)
    dBtn.config(text='{:.2f} % downloaded'.format(percent))
    progress['value'] = percent  # PROGRSS BAR VALUE
    main.update_idletasks()  # PROGRESS BAR UPDATE


# STREAM SELECTING-------------------------------------------------------------------------------------------
def get_stream(quality, fpss, obb):
    if quality == 'Mp3 Audio':
        st = obb.streams.filter(only_audio=True).first()
    else:

        lst = quality.split(' ')
        res = lst[1]
        frames = int(fpss)
        st = obb.streams.filter(progressive=True, resolution=res, fps=frames).first()

    return st


# QUALITY SEKECTION
def d_choice():

    global flag
    try:

        u = urlField.get()
        if u == '':

            showinfo('URL FIELD EMPTY', "Please enter the URL to continue")
            return

        elif 'https://www.youtube.com' not in u:

            showinfo('UNSUPPORTED', "Please enter a VALID URL")

        else:

            a_res.config(text='CHECKING...', bg='#EF24C0')
            a_res.config(state=DISABLED)
            status_label.grid(column=1, row=12)

            o = YouTube(u)

            st = o.streams.filter(progressive=True)
            rt = []
            for s in st:
                print(s)
                stream_str = str(s)

                if '1080p' in stream_str:
                    rt.append('Mp4 1080p')
                elif '720p' in stream_str:
                    rt.append('Mp4 720p')
                elif '480p' in stream_str:
                    rt.append('Mp4 480p')
                elif '360p' in stream_str:
                    rt.append('Mp4 360p')
                elif '240p' in stream_str:
                    rt.append('Mp4 240p')
                elif '144p' in stream_str:
                    rt.append('Mp4 144p')
            rt.append('Mp3 Audio')

            # SETTING VALUES TO RESOLUTION COMBO BOX
            down_choices['values'] = tuple(rt)
            # SET RESOLUTION BUTTON
            btn.grid(column=1, row=4, sticky='w', pady=5)
            # SET FPS BUTTON
            f.grid(column=1, row=5, sticky='w')

            # SET BOTH COMBO BOX
            down_choices.grid(column=1, row=4)
            down_choices.current(0)
            fps_ch.grid(column=1, row=5)

            a_res.config(text='AVAILABLE RESOLUTION', bg='#FF4F0E')
            a_res.config(state=NORMAL)
            status_label.config(text='SELECT RESOLUTION AND PRESS ENTER OR(START BUTTON)')
            flag = 1
    except Exception as e:

        print(e)
        showinfo('Some Error Occur..please try again', e)



# FOR ENTER BUTTON-------------------------------------------------------------------------------------------
def start_down_thread(e):
    thread = Thread(target=start_download)
    thread.start()


# FOR MOUSE CLICKED------------------------------------------------------------------------------------------
def start_down_threadd():
    thread = Thread(target=start_download)
    thread.start()


# THREAD FOR RESOLUTION INFO CHECK----------------------------------------------------------------------------
def d_choice_thread():
    thread2 = Thread(target=d_choice())
    thread2.start()


# CLEAR URL FIELD--------------------------------------------------------------------------------------------
def clear():
    urlField.delete(0, END)
    search_field.delete(0, END)


# RESET------------------------------------------------------------------------------------------------------
def reset():
    # RESTORATION
    global flag
    urlField.delete(0, END)  # remove url field null
    search_field.delete(0, END)  # remove youtube search field null
    vsize1.grid_remove()  # remove size (MB) label
    vTitle.grid_remove()  # remove video title label
    vsize.grid_remove()  # remoove video size label
    head.grid_remove()  # remove name label
    progress.grid_remove()  # remove progress bar
    video_l.grid_remove()  # remove length of video (hr min sec) label
    length.grid_remove()  # remove video length name label
    down_choices.grid_remove()  # remove resolution choice combo box
    btn.grid_remove()  # remove resolution label
    fps_ch.grid_remove()  # remove fps combobox
    f.grid_remove()  # remove fps label
    pr_ch.grid_remove()  # remove progress label
    status_label.grid_remove()  # rmove status label
    dBtn.config(text="START", font=('trebuchet ms', 18), bg='green', fg='white', relief='ridge')
    dBtn.config(state=NORMAL)
    a_res.config(text='AVAILABLE RESOLUTION', bg='#FF4F0E')
    a_res.config(state=NORMAL)
    flag = 0


# START DOWNLOAD BUTTON-------------------------------------------------------------------------------------------
def start_download():
    try:
        global file_size, flag
        url = urlField.get()
        if url == '':
            showinfo('ERROR', 'Please enter the url of the video you want to download')
        elif flag == 0:
            showinfo('NO RESOLUTION SELECTED',
                     'Please select required resolution and fps by clicking on CHECK AVAILABLE RESOLUTION button')
        else:
            dBtn.config(text='STARTING....')
            dBtn.config(state=DISABLED)

            status_label.config(text='EXTRACTING THE STREAM....')

            # OBJECT FOR YOUTUBE URL
            ob = YouTube(url, on_progress_callback=progress_check)

            # GETTING REQUIRED STREAM
            choice = down_choices.get()
            fps_c = fps_ch.get()

            strm = get_stream(choice, fps_c, ob)

            print(choice)
            if strm == None:
                showinfo("NOT AVAILABLE", '{} {}fps video is not available'.format(choice, fps_c))
                dBtn.config(text="START", font=('trebuchet ms', 18), bg='green', fg='white', relief='ridge')
                dBtn.config(state=NORMAL)
                reset()
                return
            dBtn.config(text='PLEASE PROVIDE PATH TO STORE VIDEO..')
            status_label.config(text='OPENING DIRECTORY....')
            # DOWNLOADING PATH
            path = askdirectory()
            if path =='':
                return

            print(strm)

            # NAME LABEL
            head.grid(column=0, row=7)
            # SIZE LABEL
            vsize.grid(column=0, row=8)

            # TITLE OF SONG DISPLAY
            try:
                t=ob.title
                title = t[:72]
                vTitle.config(text=title)
            except:
                vTitle.config(text="Not supported encoding", font=('trebuchet ms', 14), bg='#52F6BF')
            vTitle.grid(column=1, row=7, sticky='w')

            # FILE SIZE DISPLAY
            file_size = strm.filesize
            size = (float(strm.filesize)) / (1024 * 1024)
            vsize1.config(text='{:00.2f} MB'.format(size))
            vsize1.grid(column=1, row=8, sticky='w')

            # DOWNLOAD BUTTON CONFIG
            dBtn.config(text='DOWNLOADING..')
            status_label.config(text='STARTING DOWNLOAD PLEASE WAIT!!')

            # PROGRESS
            pr_ch.grid(column=0, row=10)
            progress.grid(column=1, row=10, sticky='w')

            # LENGTH
            length.grid(column=0, row=9)
            l = int(ob.length)
            hr = l / 3600
            m = l % 3600
            min = m / 60
            sec = m % 60

            if int(hr) == 0:
                video_length = '{} Minutes {} Seconds'.format(int(min), int(sec))
            elif int(hr) == 0 and int(min) == 0:
                video_length = '{} Seconds'.format(int(sec))
            else:
                video_length = '{} Hours {} Minutes {} Seconds'.format(int(hr), int(min), int(sec))
            video_l.config(text=video_length)
            video_l.grid(column=1, row=9, sticky='w')

            status_label.config(text='DOWNLOADING VIDEO....')
            # DOWNLOADING START
            strm.download(path)
            status_label.config(text='DOWNLOAD COMPLETED')

            print('done...')

            # DOWNLOADING BUTTON CONFIG
            dBtn.config(text="START", font=('trebuchet ms', 18), bg='green', fg='white', relief='ridge')
            dBtn.config(state=NORMAL)

            # DOWNLOAD COMPLETION MESSAGE
            showinfo('Download finished', 'DOWNLOAD SUCCESSFUL')

            flag = 0


    except Exception as e:
        print(e)
        showinfo('Some Error Occur..please try again', e)
        flag = 1


# MAIN GUI START HERE----------------------------------------------------------------------------------------
main = Tk()
main.configure(bg='#83F8FF')
main.resizable(height=True, width=True)

# WINDOW TITLE
main.title('MY YOUTUBE VIDEO DOWNLOADER')
main.iconbitmap('icon.ico')

# FRAME CALCULATION
height = 700
width = 990
x = (main.winfo_screenwidth() // 2) - (width // 2)
y = (main.winfo_screenheight() // 2) - (height // 2)

# GEOMETRY OF WINDOW FRAME
main.geometry('{}x{}+{}+{}'.format(width, height, x, y))
# main.geometry('500x600')
file = PhotoImage(file='icon.png')
headingIcon = Label(main, image=file)
headingIcon.grid(column=0, row=0, padx=10)

# TITLE LABEL
title_label = Label(text="YOUTUBE VIDEO DOWNLOADER", font=('Berlin Sans FB', 30), fg='white', bg='#FF0627', padx=5)
title_label.grid(column=1, row=0, padx=30)

# OPEN YT
yt_label = Label(main, text='SEARCH HERE FOR YT', font=('comic sans ms', 14), bg='#783FFC', fg='#FFB2BC')
yt_label.grid(column=0, row=2)

search_field = Entry(main, justify=CENTER, bg='#00FF91', font=('trebuchet ms', 12))
search_field.grid(column=0, row=3)

opn_yt = Button(main, text="SEARCH", font=('comic sans ms', 10), bg='red', fg='white', activebackground='orange',
                command=open_youtube)
opn_yt.grid(column=0, row=4)

# URL
enter_url = Label(main, text='-----------  PASTE THE URL HERE  -----------', font=('Bahnschrift', 16), bg='#83F8FF',
                  bd=10)
enter_url.grid(column=1, row=2, sticky='ew')
urlField = Entry(main, justify=CENTER, bg='#00FF91', font=('trebuchet ms', 12))
"""
urlField.insert("0", placeholder)
urlField.bind("<FocusIn>", urlField.delete("0", "end"))
urlField.bind("<FocusOut>", urlField.insert("0", self.placeholder))
"""
urlField.grid(column=1, row=3, sticky='ew')

# CLEAR URL FIELD
cf = Button(main, text='Clear url', font=('trebuchet ms', 10), bg='#F65DD7', fg='black', relief='ridge', command=clear)
cf.grid(column=1, row=2, sticky='e')

# RESOLUTION LABEL
btn = Label(main, text='RESOLUTION', font=('trebuchet ms', 14), bg='#83F8FF', fg='#360DBA')

# RESOLUTION COMBO BOX
n = StringVar()
down_choices = ttk.Combobox(main, width=27, textvariable=n, state='readonly')
# down_choices['values'] = ("Mp4 1080p", "Mp4 720p", "Mp4 480p", "Mp4 360p", "Mp4 240p", "Mp4 144p", "Mp3 Audio")
# down_choices.grid(column=1, row=4, sticky='e')
# down_choices.current(0)

# FPS LABEL
f = Label(main, text="FPS", font=('trebuchet ms', 14), bg='#83F8FF', fg='#360DBA')

# FPS COMBO BOX
m = StringVar()
fps_ch = ttk.Combobox(main, width=27, textvariable=m, state='readonly')
fps_ch['values'] = ("30", '60')
fps_ch.current(0)

# DOWNLOAD BUTTON
dBtn = Button(main, text="START", font=('trebuchet ms', 16), bg='#00F9A6', fg='black', relief='raised',
              activebackground='red', command=start_down_threadd)
dBtn.grid(column=1, row=6, sticky='ew', pady=5)

# VIDEO TITLE
vTitle = Label(main, text='video title', font=('trebuchet ms', 14), bg='#52F6BF')
# HEADING
head = Label(main, text='NAME :', font=('trebuchet ms', 14), bg='#52F6BF')

# VIDEO SIZE
vsize = Label(main, text='SIZE :', font=('trebuchet ms', 14), bg='#52F6BF')

# LENGTH OF VIDEO
length = Label(main, text='LENGTH :', font=('trebuchet ms', 14), bg='#52F6BF')

# FOCUS OF CURSOR
urlField.focus()

# PROGRESS BAR
progress = Progressbar(main, style="TProgressbar", orient=HORIZONTAL, length=720, mode='determinate')

# PROGRESS CHECK LABEL
pr_ch = Label(main, text='PROGRESS', font=('trebuchet ms', 14), bg='#52F6BF')

# AVAILABLE RRESOLUTION BUTTON
a_res = Button(main, text="AVAILABLE RESOLUTION", width=20, height=1, font=('trebuchet ms', 11), bg='#FF4F0E',
               fg='black', relief='raised', command=d_choice_thread)
a_res.grid(column=1, row=4,  sticky='e')

# STATUS LABEL
status_label = Label(main, text='', font=('trebuchet ms', 18), bg='#FF9CD8', fg='#0055FF')


# RESET BUTTON
reset = Button(main, text="RESET ALL", font=('trebuchet ms', 16), bg='#001787', fg='#ECC190', command=reset)
reset.place(x=700, y=640)

vsize1 = Label(main, text='', font=('trebuchet ms', 14), bg='#52F6BF')
video_l = Label(main, text='', font=('trebuchet ms', 14), bg='#52F6BF')
video_length = Label(main, text='')
# KEY EVENT (ENTER)
main.bind('<Return>', start_down_thread)

mainloop()
