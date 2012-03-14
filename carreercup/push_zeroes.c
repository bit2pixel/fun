/*
 * AUTHOR: Renan Cakirerk <public at cakirerk.org>
 * QUESTION: http://www.careercup.com/question?id=12986664
 *           Push all the zero's of a given array to the end of the array. In place only. Ex 1,2,0,4,0,0,8 becomes 1,2,4,8,0,0,0
*/

#include<stdio.h>
#define size 10

int main(int argc, char **argv)
{

    int arr[size] = {0, 0, 1, 2, 0, 4, 0, 0 ,8 ,9};
    int pos = 0, i, count_zero;

    for(i = 0; i <= size-1; i++) {
        if(arr[i] != 0) {
            arr[pos] = arr[i];
            pos++;
        }
    }

    for(i = size; i >= pos; i--)
        arr[i] = 0;


    for(i = 0; i <= size-1; i++)
        printf("%d ", arr[i]);

    printf("\n");

    return 0;
}
