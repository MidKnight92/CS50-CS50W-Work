#include "helpers.h"
#include <stdio.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float gray;
    // Loop through image 2d array
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Find the average of rgb in indiviual pixel round to the nearest Interger
            gray = round((image[i][j].rgbtRed + image[i][j].rgbtBlue + image[i][j].rgbtGreen) / 3.00);
            // Set all the structs to gray
            image[i][j].rgbtRed = gray;
            image[i][j].rgbtBlue = gray;
            image[i][j].rgbtGreen = gray;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Define the highest int
    int max = 255;
    float sepiaRed, sepiaBlue, sepiaGreen;
    int originalRed, originalGreen, originalBlue;

    // Loop through the image 2d array
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
        // Define all indiviual orgininal rbg colors
        originalRed = image[i][j].rgbtRed;
        originalBlue = image[i][j].rgbtBlue;
        originalGreen = image[i][j].rgbtGreen;

        // Define all individual sepia rgb colors
        sepiaRed = round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue);
        sepiaBlue = round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue);
        sepiaGreen = round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue);

        // Check if sepia color is more then max if so assin 2darr color to max else to the sepia value
        image[i][j].rgbtRed = (sepiaRed > max) ? max : sepiaRed;
        image[i][j].rgbtBlue = (sepiaBlue > max) ? max : sepiaBlue;
        image[i][j].rgbtGreen = (sepiaGreen > max) ? max : sepiaGreen;

        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Cretae a temp struct
    RGBTRIPLE temp;
    // Loop through the full height of the image
    for (int i = 0; i < height; i++)
    {
        // Loop up to the mid-point in the row
        for (int j = 0; j < (width/2); j++)
        {
            // Assign original pixel in a temp var
            temp = image[i][j];
            // Assign the pixels on left to the end of array going one more into the middle with each iteration
            image[i][j] = image[i][width - j - 1];
            // Assign the pixels on the right to the original pixel images
            image[i][width - j - 1] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Declare varibales
    int b, g, r, currentColPixel, currentRowPixel;
    int counter;
    RGBTRIPLE temp[height][width];

    // Loop through image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
        // Assign varibales
        b = 0;
        g = 0;
        r = 0;
        counter = 0;

            // Loops elements the position of -1, 0, 1 in a row
            for (int row = -1; row < 2; row++)
            {
                // Loops elements from the position on -1, 0, 1 in a column
                for (int col = -1; col < 2; col++)
                {
                    currentRowPixel = i + row;
                    currentColPixel = j + col;

                    // Check Elements are within the image range
                    if (currentColPixel >= 0 && currentColPixel < (width - 1) && currentRowPixel >= 0 && currentRowPixel < (height - 1))
                    {
                        r += image[currentRowPixel][currentColPixel].rgbtRed;
                        g += image[currentRowPixel][currentColPixel].rgbtGreen;
                        b += image[currentRowPixel][currentColPixel].rgbtBlue;
                        counter++;
                    }
                }
            }

            // Assign the rounded averages
            temp[i][j].rgbtRed = round(r / counter);
            temp[i][j].rgbtGreen = round(g / counter);
            temp[i][j].rgbtBlue = round(b / counter);
        }
    }
    // Loop through image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Assign temp values with new blur averages to the original image
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
        }
    }
    return;
}

