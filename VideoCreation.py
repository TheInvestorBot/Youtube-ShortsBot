# importing libraries
import os
import cv2 
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image 
from moviepy.editor import *
from gtts import gTTS



# Checking the current directory path
print(os.getcwd()) 
  
# Folder which contains all the images
# from which video is to be generated
os.chdir("")  #Directory with images
path = "" # Directory with images
  
mean_height = 0
mean_width = 0
#Pull data of top moving stock
urlpage = 'https://www.tradingview.com/markets/stocks-usa/market-movers-active/' 
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless = True
driver = webdriver.Firefox(options=fireFoxOptions)

#Get web page, with window size set to 1080 x 1080
driver.set_window_size(1080,1080)
driver.get(urlpage)
time.sleep(3)

#Get ticker of top moving stock and navigate to page containing chart
topMover = driver.find_elements_by_xpath('/html/body/div[2]/div[4]/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div/div/div/table/tbody/tr[1]/td[1]/span/a')[0].text
urlpage = "https://www.tradingview.com/symbols/" + str(topMover)
driver.get(urlpage)

#Scroll down for best view of chart
driver.execute_script("window.scrollTo(0, 220)")

#Wait for page to load chart and then screenshot chart.
time.sleep(2)
driver.get_screenshot_as_file("currentTopMover.png")
urlpage = "https://www.tradingview.com/symbols/" + str(topMover) + "/technicals"
driver.get(urlpage)
driver.execute_script("window.scrollTo(0, 410)")
time.sleep(2)
techInd = driver.find_elements(By.XPATH, '/html/body/div[2]/div[4]/div[2]/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[1]/span')[0].text
maInd = driver.find_elements_by_xpath('/html/body/div[2]/div[4]/div[2]/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[3]/span')[0].text
driver.get_screenshot_as_file("indicators.png")


driver.close()  


num_of_images = 1
# print(num_of_images)
text = "The current top moving stock   is " + str(topMover) + ". It's oscillators are indicating " + str(techInd) + " and it's moving averages are indicating " + str(maInd) + "."
language = 'en'
myAudio = gTTS(text=text, lang=language, slow=False)
myAudio.save('audio.mp3')

for file in os.listdir('.'):
    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"):
        im = Image.open(os.path.join(path, file))
        width, height = im.size
        mean_width += width
        mean_height += height
    # im.show()   # uncomment this for displaying the image
  
# Finding the mean height and width of all images.
# This is required because the video frame needs
# to be set with same width and height. Otherwise
# images not equal to that width height will not get 
# embedded into the video
mean_width = int(mean_width / num_of_images)
mean_height = int(mean_height / num_of_images)
  
# print(mean_height)
# print(mean_width)
  
# Resizing of the images to give
# them same width and height 
for file in os.listdir('.'):
    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"):
        # opening image using PIL Image
        im = Image.open(os.path.join(path, file)) 
   
        # im.size includes the height and width of image
        width, height = im.size   
        print(width, height)
  
        # resizing 
        imResize = im.convert('RGB')
        imResize = imResize.resize((mean_width, mean_height), Image.ANTIALIAS) 
        imResize.save( file, 'JPEG', quality = 95) # setting quality
        # printing each resized image name
        print(im.filename.split('\\')[-1], " is resized") 
  
  
# Video Generating function
def generate_video():
    image_folder = '.' # make sure to use your folder
    video_name = 'mygeneratedvideo.mp4'
    os.chdir("") #Image folder
      
    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")]
     
    # Array images should only consider
    # the image files ignoring others if any
    print(images) 
  
    frame = cv2.imread(os.path.join(image_folder, images[0]))
  
    # setting the frame width, height width
    # the width, height of first image
    height, width, layers = frame.shape  
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter(video_name, fourcc, 1, (width, height)) 
  
    # Appending the images to the video one by one
    for image in images:  
        for i in range (0, 4):
            video.write(cv2.imread(os.path.join(image_folder, image))) 
      
    # Deallocating memories taken for window creation
    cv2.destroyAllWindows() 
    video.release()  # releasing the video generated     
  
  
# Calling the generate_video function
generate_video()
  
   
# loading video dsa gfg intro video
clip = VideoFileClip("mygeneratedvideo.mp4")
  
  
clip = clip
  
# loading audio file
audioclip = AudioFileClip("audio.mp3")
  
# adding audio to the video clip
videoclip = clip.set_audio(audioclip)

videoclip.write_videofile('mygeneratedvideo.mp4')  
# showing video clip

