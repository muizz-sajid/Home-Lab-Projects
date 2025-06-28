#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Error in locating/opening file\n");
        return 1;
    }

    uint8_t buffer[512];
    char filename[8];
    int count = 0;
    FILE *output = NULL;

    while (fread(buffer, 1, 512, card) == 512)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] >= 0xe0 && buffer[3] <= 0xef))
        {
            if (output != NULL)
            {
                fclose(output);
            }

            sprintf(filename, "%03d.jpg", count);
            output = fopen(filename, "w");
            count++;
            fwrite(buffer, 1, 512, output);
        }
        else if (output != NULL)
        {
            fwrite(buffer, 1, 512, output);
        }
    }
    if (output != NULL)
    {
        fclose(output);
    }

    fclose(card);
    return 0;
}
