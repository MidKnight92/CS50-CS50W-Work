#include <cs50.h>
#include <stdio.h>


int main(void)
{
    int num;
    do 
    {
         num = get_int("Height: Pick a number between 1 and 8: \n");  
    }
    while (num < 1 || num > 8);
        
       //rows
       for (int i = 1; i <= num; i++)
       {
           //cols
           for (int j = 1; j <= (num - i); j++)
           {
            printf(" ");
           }
           for (int k = 1; k <= i; k++)
           {
               printf("#");
           }
           printf("\n");
       }     
}

