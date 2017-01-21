all: reaction@1x.gif reaction@2x.gif

reaction@1x.gif: 1x/reaction-1@1x.png 1x/reaction-2@1x.png 1x/reaction-3@1x.png
	convert -delay 100 -loop 0 1x/*.png reaction@1x.gif

reaction@2x.gif: 2x/reaction-1@2x.png 2x/reaction-2@2x.png 2x/reaction-3@2x.png
	convert -delay 100 -loop 0 2x/*.png reaction@2x.gif
