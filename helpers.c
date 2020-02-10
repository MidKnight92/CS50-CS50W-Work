#include "helpers.h"
#include <stdio.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop through image 2d array
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Find the average of rgb in indiviual pixel round to the nearest Interger
            float gray = round((image[i][j].rgbtRed + image[i][j].rgbtBlue + image[i][j].rgbtGreen) / 3);
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
    RGBTRIPLE temp;
    // Loop through the full height of the image
    for (int i = 0; i < height; i++)
    {
        // Loop up to the mid-point in the row
        for (int j = 0; j < (width/2); j++)
        {
            // Assign original pixel in a temp var
            temp = image[i][j];
            // Assign the pixels on left to the pixels displayed at the end of array
            image[i][j] = image[i][width - j];
            // Assign the pixels on the right to the original pixel images
            image[i][width - j] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Declare varibales
    int b = 0;
    int g = 0;
    int r = 0;
    float counter = 0.00;
    RGBTRIPLE temp[height][width];

    // Loop through image
    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            // Loop from place to the left to one place to the right to get to the sum
            for (int k = -1; k < 2; k++)
            {
                if (j + k < 0 || j + k > height - 1)
                {
                    continue;
                }

                for (int h = -1; h < 2; h++)
                {
                    if (i + h < 0 || i + h > width - 1)
                    {
                        continue;
                    }
                    b += image[j + k][i + h].rgbtBlue;
                    g += image[j + k][i + h].rgbtGreen;
                    r += image[j + k][i + h].rgbtRed;
                    counter++;
                }
            }
            // Assign the rounded averages
            temp[j][i].rgbtBlue = round(b / counter);
            temp[j][i].rgbtGreen = round(g / counter);
            temp[j][i].rgbtRed = round(r / counter);
        }
    }
    // Loop through image
    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            // Assign temp values to the image
            image[j][i].rgbtBlue = temp[j][i].rgbtBlue;
            image[j][i].rgbtGreen = temp[j][i].rgbtGreen;
            image[j][i].rgbtRed = temp[j][i].rgbtRed;
        }
    }
    return;
}

