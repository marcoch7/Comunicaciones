import numpy as np

flag_a = 0
flag_b = 0
flag_temp = 0
def moreen(array, f_a, f_b, f_temp):
    if(f_a):
        if(f_b):
            array = [0,0,0,0,0,0]
        for i in range(6):
            if(i == 0):
                if((f_temp > 32 and f_temp < 65)):
                    array[0] = 1
                else:
                    array[0] = 0 
            elif(i==1):
                if((f_temp > 16 and f_temp < 32) or (f_temp > 48 and f_temp < 65)):
                    array[1] = 1
                else:
                    array[1] = 0 
            elif(i==2):
                if((f_temp > 8 and f_temp < 17) or (f_temp > 24 and f_temp < 33) or (f_temp > 40 and f_temp < 49) or (f_temp > 56)):
                    array[2] = 1
                else:
                    array[2] = 0 
            elif(i==3):
                if((f_temp > 3 and f_temp < 9) or (f_temp > 12 and f_temp < 17) or (f_temp > 20 and f_temp < 25) or (f_temp > 28 and f_temp < 33) or (f_temp > 36 and f_temp < 41) or (f_temp > 44 and f_temp < 49) or (f_temp > 52 and f_temp < 57) or (f_temp > 60)):
                    array[3] = 1
                else:
                    array[3] = 0   
            elif(i==4):
                if((f_temp > 2 and f_temp < 5) or (f_temp > 6 and f_temp < 9) or (f_temp > 10 and f_temp < 13) or (f_temp > 14 and f_temp < 17) or (f_temp > 18 and f_temp < 21) or (f_temp > 22 and f_temp < 25) or (f_temp > 26 and f_temp < 29) or (f_temp > 30 and f_temp < 33) or (f_temp > 34 and f_temp < 37) or (f_temp > 38 and f_temp < 41) or (f_temp > 42 and f_temp < 45) or (f_temp > 46 and f_temp < 49) or (f_temp > 50 and f_temp < 53) or (f_temp > 54 and f_temp < 57) or (f_temp > 58 and f_temp < 61) or (f_temp > 62 and f_temp < 65)):
                    array[4] = 1
                else:
                    array[4] = 0  
            elif(i==5):
                if(array[5] == 0):
                    array[5] = 1
                else:
                    array[5] = 0           
        return array 
    else:
        return array   

er = [0,0,0,0,0,0]
moreen(er,1,1,0)
for i in range(64):
    flag_temp += 1
    moreen(er,1,0,flag_temp)
    print(er)
    