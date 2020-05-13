# STEGANOGRAPHY

[Steganography](https://en.wikipedia.org/wiki/Steganography) is the practice of  concealing a file, message, image, or video within another file, message, image, or video. [Cryptography](https://en.wikipedia.org/wiki/Cryptography) is the practice of protecting the contents of a message alone, steganography is concerned both with concealing the fact that a secret message is being sent and its contents.

## Hiding an image within another image

This is a simple GUI that let's you hide only image inside a image.

## Prerequisites

Python 3.7 is used

You don't need any other modules to run the script.

You can install OpenCV if the given module on ```src``` doesn't work

```
pip install opencv-python
```

## Technique
A [digital image](https://en.wikipedia.org/wiki/Digital_image) is an image composed of picture elements known as pixels. Each pixel has either a single color channel (if it's grayscale) ranging from 0 - 255, or it has 3 color channels (if it's RGB) and each of them has a value between 0 - 255. This numeric values represent intensity of the perticular color. This decimal values are comprised of 8 bits. This method uses the 4 [most significant bits](https://en.wikipedia.org/wiki/Bit_numbering) of each of the hidden image and the dummy image to create a new imgae that resembles the dummy image containing the hidden image within. The way it works is if a pixel of the hidden image has a red value of 174 or in binary 1010 1110 and the in the similar location of the dummy image there is a pixel whose red value is 38 or in binary 0010 0110. Then we take the most significant bits of them , in this case 1010 of the hidden image and 0010 of the dummy image and we make a new pixel whose red value is 0010 1110 or in decimal 46. As the difference between 48 and 38 it's very small the color dosen't change much, hence it is less noticeable. So the resultant image almost looks like the dummay image. To recover the image we just need to extract the least significant 4 bits of the steganographically hidden image and generate a new image with them as most significant bits with 0 padding(4 zeors as least significant bit). We can recover almost the same image as our hidden image.

Here this method has been implemented in a user friendly GUI or graphical user interface. 

## Usage

After downloading or cloning the repository just run the ```main.py``` script , the GUI will open up, then just click on "Choose Image" to navigate to the folder where the images are located and open them. The upper window is for the hidden image and lower window is for the dummy image. Then click on the generate image button on the right window to generate the steganographically hidden image. You can try different images and generate the steganographically hidden image to find the suitable match. Then after you have found the match just click on "Save Image" button to save the image as a '.png' file. You can also decrypt the generated image by navigating to the "Decryption" tab and selecting the appropriate file then click on the generate button to get the hidden image back then you can save the image to your desired folder.

## Example


