import os
import math
import numpy as np

scaling_factor = 0
'''
    Symmetric quantization has slight changes. Now the range of max to min is taken as -2^n-1 to 2^n-1

'''
def symmetric_quantize(arr, bits):
    # max value is referred to the maximum bits available for transformation. An 8 bit number can have a maximum of
    # 2^8-1 = 255 bits 

    lower_end = -(2**(bits-1) -1)
    print("Lower end of symmetry is " , lower_end)
    upper_end = (2**(bits-1) -1) 
    print("Upper end of symmetry is " , upper_end)
    
    # Now we find the scaling factor for the quantization. The scaling factor is obtaoined as |(xmax - xmin)/max_val-min_val|
    # This means the highest and the lowest value in the tensor/array divided by max val - min val
    scaling_factor = max(abs(arr))/upper_end
    print("The scaling factor is: ", scaling_factor)

    # No zero offset needed

    #The new quantized array fpllows the forumla as clamp(x/s;-2^n-1;2^n-1)which means:
    # if the value comes lesser than 0 then clamp to 0 and if the value comes more than max_val clamp it at max_val
    quantized_arr = np.copy(arr)


    counter=0
    for val in arr:
        val_intermediate = int(val/scaling_factor)
        if val_intermediate < lower_end :
            quantized_arr[counter] = lower_end
        elif val_intermediate > upper_end:
            quantized_arr[counter] = upper_end
        else:
            quantized_arr[counter] = val_intermediate
        counter+=1
    
    return quantized_arr



'''
    Assymetric quantization needs a scaling factor and a zero offset as well to ensure that the conversion 
    from floating point 32 bits happens to the requisite bits. Its called assymetric because it includes asymmetric 
    postive and negative integers/ decimals
'''
def asymmetric_quantize(arr, bits):
    # max value is referred to the maximum bits available for transformation. An 8 bit number can have a maximum of
    # 2^8-1 = 255 bits
    max_val = 2**bits -1 
    print("The maximum range of values is:" , max_val)
    
    # Now we find the scaling factor for the quantization. The scaling factor is obtaoined as |(xmax - xmin)/max_val-min_val|
    # This means the highest and the lowest value in the tensor/array divided by max val - min val
    scaling_factor = (max(arr)- min(arr))/max_val
    print("The scaling factor is: ", scaling_factor)

    # The scaling factor now needs to be add with a zero offset .The sero offset formula is given as
    # z = (-1 * B/s) or (-1 * min(arr)/max_val)
    zero_offset = math.ceil(-1 * min(arr)/scaling_factor)
    print("The zero offset  is: ", zero_offset)
    #The new quantized array fpllows the forumla as clamp(x/s + z;0;2^n-1)which means:
    # if the value comes lesser than 0 then clamp to 0 and if the value comes more than max_val clamp it at max_val
    quantized_arr = np.copy(arr)


    counter=0
    for val in arr:
        val_intermediate = int(val/scaling_factor) + zero_offset
        if val_intermediate < 0 :
            quantized_arr[counter] = 0 
        elif val_intermediate > max_val:
            quantized_arr[counter] = max_val
        else:
            quantized_arr[counter] = val_intermediate
        counter+=1
    
    return quantized_arr

def asymmetric_dequantize(arr, quantized_arr,bits):
    dequantized_arr = np.copy(quantized_arr)

    max_val = 2**bits -1 
    scaling_factor = (max(arr)- min(arr))/max_val
    zero_offset = math.ceil(-1 * min(arr)/scaling_factor)

    counter = 0
    for val in quantized_arr:
        dequantized_arr[counter] = scaling_factor * (val-zero_offset)
        counter+=1
    return dequantized_arr
   
def symmetric_dequantize(arr,quantized_arr,bits):
    sym_dequantized_arr = np.copy(arr)
    lower_end = -(2**(bits-1) -1)
    print("Lower end of symmetry is " , lower_end)
    upper_end = (2**(bits-1) -1) 
    print("Upper end of symmetry is " , upper_end)

    scaling_factor = max(abs(arr))/upper_end

    counter = 0
    for val in quantized_arr:
        sym_dequantized_arr[counter] = scaling_factor * val
        counter+=1
    return sym_dequantized_arr
   

if __name__ == "__main__":
    arr = np.array([43.31, -44.93, 0 , 22.99, -43.93, -11.35, 38.48, -20.49, -38.61,-28.02])
    print("The array obtained is:", arr)
    quantized_arr = asymmetric_quantize(arr,8)
    print("Final quantized array is:" , quantized_arr)
    dequantized_arr = asymmetric_dequantize(arr, quantized_arr,8)
    print("Final dequantized array" , dequantized_arr)
    print("As you notice when the array comes out it has slight changes")
    print("##############################################################")

    sym_quantized_arr = symmetric_quantize(arr,8)
    print("Final symmetric quantized array is:" , sym_quantized_arr)
    sym_dequantized_arr = symmetric_dequantize(arr,sym_quantized_arr,8)
    print("Final symmetric dequantized array" , sym_dequantized_arr)

