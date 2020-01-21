#include <cs50.h>
#include <stdio.h>

int get_num(void);

int main(void)
{
    int n = get_num();
        
    //rows
    for (int i = 1; i <= n; i++)
    {
        //cols       
        //spaces: total number of rows (n) aka the height minus the actual row number(i)
       for (int j = 1; j <= (n - i); j++)
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


//Prompt user for number if number is less than 1 or greater than 8 reprompt
int get_num(void)
{
    int num;
    do 
    {
        num = get_int("Height: Pick a number 1-8 inclusive: \n");  
    }
    while (num < 1 || num > 8);
    return num;
}
