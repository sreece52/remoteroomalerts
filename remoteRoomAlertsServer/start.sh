sudo mjpg_streamer -i 'input_uvc.so' -o 'output_http.so 192.168.0.103:8080' &

sudo python app.py