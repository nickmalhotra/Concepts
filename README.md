# Concepts
This repository is kept to explain concepts in Gen AI and LLM creation

Concepts are simplified for usage of all developers so that they can easily see what happens internally within the LLM code creation. 
QUANTIZATION
Quantization is a technique which enables us to reduce the size of the parameters (weights/biases) so that the model can run better on smaller computes and yet perform with results. The way quantization works and the size on the disk is shown below in a table

let us assume we have a 16 B parameter model with full precision which is normally referred as BF 32 or 32 bit parameters. 32 parameters occupy 8 bytes on a disk as they are represented in a computer as 
                                            |0| 8bits EXPONENT    |  23 bits MANTISSA            |

Firs bit is a sign bit 0 represents positive and 1 represents negative
The next 8 bits represent the exponent , so if a number is 7.23, 7 is the exponent
The remaining 23 bits are kept for mantissa which is post the decimal like .23 above

This 32 bit is brought to a 4 bit or an 8 bit integer based representation whcih reduces size and memnory footprint

A table to showcase the impact is as follows
|  Num Params |  Precision |  Size on Disk calculation 
|      1 B     |    32 bit  |   32x1x10^9/8x10^9 = 4 GB |
|      2 B     |    32 bit  |   32X2X10^9/8x10^9 = 8 GB |
|      8B      |    32 bit  |   32X8X10^9/8x10^9 = 32 GB|
|      8B      |    8 bit   |   8X8X10^9/8x10^9 = 8 GB  |
|      4B      |    8 bit   |   8X4X10^9/8x10^9 = 4 GB  |

The above table shows ap[proximate size on disk as a comparison of parameter size with precision
