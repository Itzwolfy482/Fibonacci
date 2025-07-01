from Matrices import MEV4

def main(n):
    #MEV4 stands for Matrix Exponentiation Version 4
    f=MEV4(n)
    with open(f"Fibonacci {n}.txt", "w") as file:
        #File will be located in your repository
        file.write(str(f))


#Feel free to tweak the values
main(10000000)