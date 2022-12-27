# emoji_mosaic
Python tool to generate a photo mosaic given some set of images and a source to base it on.

I initially created this as a for fun project at work - take all of our slack emojis (over 9000!) and some public images to create cool collages!

All that is required is a source image and a filedir containing photos to be used as tiles.

### Limitations
* Tiles will be resized to square, so anything outside of 1:1 aspect ratio will not look great

### Example

Source Image: ![image](https://user-images.githubusercontent.com/72606788/209713990-72a2269f-1cde-4065-8cda-f1e794b726af.png)


Screencaps of Output Image (scaling factor 2): ![image](https://user-images.githubusercontent.com/72606788/209720264-3c90d20d-972f-4b05-8840-d40906c7fb23.png)
![image](https://user-images.githubusercontent.com/72606788/209720285-a6f8fa05-9973-4b4a-a9fe-a15fbbc511b2.png)


Screencaps of Output Image (scaling factor 6): ![image](https://user-images.githubusercontent.com/72606788/209720385-de269056-ba24-4318-b8e7-f233de3e06af.png)
![image](https://user-images.githubusercontent.com/72606788/209720314-2e5cb1a5-0fbc-4907-a635-22cb67c6240f.png)
