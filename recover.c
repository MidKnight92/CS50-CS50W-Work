#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    // Check Quantity of Command-line Arguments
    if (argc != 2)
    {
        printf("Usage: ./recover card.raw\n");
        return 1;
    }

    // Open Memory Card
    FILE *file = fopen(argv[1], "r");

    // Check if file can be opened for reading
    if (file == NULL)
    {
        return 1;
    }

    // Number of new Jpeg files counted
    int i = 0;

    // Declare File pointer
    FILE *img = NULL;

    // Create an Arr for filename: ###.jpg
    char filename[10];

    // Jpeg Found
    bool found = false;

    // Allocate enough memory for 512 Bytes;
    unsigned char bytes[512];


    // Repeat until End of Memory Card
    while (fread(bytes, 512, 1, file) == 1)
    {

        // Check First Four Bytes
        if (bytes[0] == 0xff && bytes[1] == 0xd8 && bytes[2] == 0xff && (bytes[3] & 0xf0) == 0xe0)
        {

            // Check if it is not the first file
            if (i > 0)
            {

                // Close Previous File
                fclose(img);

                // Rename file
                sprintf(filename, "%03i.jpg", i);

                // Open filename to write
                img = fopen(filename, "w");

                if (img == NULL)
                {
                    printf("img ptr returned null");
                    return 2;
                }
                else
                {
                    // Write new file
                    fwrite(bytes, 512, 1, img);

                    // Increment Filename Count
                    i++;

                }
            }
            else
            {

                // Reassign Found to Truthy
                found = true;

                // Rename file
                sprintf(filename, "%03i.jpg", i);

                // Open filename to write
                img = fopen(filename, "w");

                if (img == NULL)
                {
                    printf("img ptr returned null");
                    return 2;
                }
                else
                {
                    // Write new file
                    fwrite(bytes, 512, 1, img);

                    // Increment Filename Count
                    i++;

                }
            }
        }
        else
        {
            if (found)
            {

                // Write new file
                fwrite(bytes, 512, 1, img);

            }

        }
    }

    // Close All Files
    fclose(img);
    fclose(file);

    return 0;
}

