#include <stdio.h>
#include <cs50.h>
#include <math.h>

int change_owed(void);

int main(void)
{
    int amount = change_owed();
    printf("Amount: %i\n", amount);
    
    //Initialize coin variable to 0 //this will be icremented as coins are being used
    int coins = 0;
    //Initialize diff to amount owed to customer //this will keep track of remaining change owed
    int diff = amount;
    
    //Check if the diff is greater then or equal to respective amounts and not zero
    //increment coin if so and minus the difference    
    while (diff >= 25 && diff > 0)
    {
        coins++;
        diff -= 25;
    }
    while (diff >= 10 && diff > 0)
    {
        coins++;
        diff -= 10;
    }
    while (diff >= 5 && diff > 0)
    {
        coins++;
        diff -= 5;
    }
    while (diff >= 1 && diff > 0)
    {
        coins++;
        diff -= 1;
    }
    printf("%i\n", coins);
}

//Prompt user for change owed
int change_owed(void)
{
    //declare variable
    float change;
    //If the user inputs a non-negative number repromt to comply
    do
    {
        change = get_float("Change Amount:\n");
    }
    while (change < 0);
    
    //Convert Dollars to Cents
    int cents = round(change * 100);
    return cents; 
}


