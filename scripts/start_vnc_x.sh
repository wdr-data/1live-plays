
# Use this if you want to be able to connect to the framebuffer using vnc
x11vnc -create -env FD_PROG=/usr/bin/fluxbox \
    -env X11VNC_FINDDISPLAY_ALWAYS_FAILS=1 \
        -env X11VNC_CREATE_GEOM=${1:-1600x900x24} \
        -gone 'killall Xvfb' \
        -bg -nopw
