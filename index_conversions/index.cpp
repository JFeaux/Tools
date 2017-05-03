#include <vector>  
#include <algorithm>  

using namespace std;  

// Set of functions for converting an index {i, j, ..}
// with permutational symmetry aka {i, j} = {j, i}
// to a position in a 1D array with no wasted memory

// Equivalent to upper triangular storage for 2D matrix

// Most common case 2, 3, and 4 index quantities are hardcoded 
// for speed (c2, c3, c4). 
// For general case use cinf

int c2(int i0, int j0, int n)  
{  
    int i = i0; 
    int j = j0;

    if (i0 > j0){
        j = i0;
        i = j0;
    }

    return (-3 * i + 6 * n * i - 3 * i * i) / 6 + j;
}
  
int c3(int i, int j, int k, int n)  
{ 
    vector<int> index {i,j,k};
    sort(index.begin(), index.end());
    i = index[0];
    j = index[1];
    k = index[2];
    return (i * (-1 + 3 * n * n -3 * n * i + i * i)
            -3 * j + 6 * n * j - 3 * j * j) / 6 + k;
}
  
int c4(int i, int j, int k, int l, int n)
{ 
    vector<int> index {i,j,k,l};
    sort(index.begin(), index.end());
    i = index[0];
    j = index[1];
    k = index[2];
    l = index[3];
    return (2 * (1 + 2 * n) * (-1 + n + n * n) * i +
            (1 - 6 * n * (1 + n)) * i * i
            + (2 + 4 * n) * i * i * i - i * i * i * i
            + 4 * (j * (-1 + 3 * n * n - 3 * n * j + j * j)
            + 3 * k + 6 * n * k - 3 * k * k)) / 24 + l - k;
}
 
int factorial(int n)  
{  
    return (n == 1 || n == 0) ? 1: factorial(n - 1) * n;  
}  
 
int combs(int m,int r)  
{ 
    int prod = 1; 
    for (int i = 1; i < r+1; ++i){ 
        prod *= (m + r - i); 
    } 
    return prod / factorial(r); 
} 
  
int cinf(vector<int> index, int n) 
{
    sort(index.begin(),index.end());
    int order = index.size();
    int loc = 0;
    int r = order - 1;
    int count;
    int m;
    for (int i = 0; i < order - 1; ++i){
        if (i > 0){
            count=index[i-1];
            for (int j = 0; j < index[i] - index[i-1]; ++j){
                m = n - count;
                count += 1;
                loc += combs(m, r);
            }
        }
        else {
            count = 0;
            for (int j = 0; j < index[i]; ++j){
                m = n - count;
                count += 1;
                loc += combs(m,r);
            }
        }
        r -= 1;
    }
    return loc + index[order - 1] - index[order - 2];
} 
