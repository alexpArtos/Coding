def scale(n, scale):
    """Returns n with a number of decimal places equal to scale, after rounding.
    """
    return int(n*10**scale + .5) / 10**scale


_ = input()
line = input()
values = line.split()
numbers = [int(i) for i in values]

# mean
average = sum(numbers) / len(numbers)

# median
numbers.sort()
N = len(numbers)
if (N%2 == 0):          
    leftOfCentre = numbers[int (N/2)-1]
    rightOfCentre = numbers[int (N/2)]
    median = (leftOfCentre + rightOfCentre) / 2
else:
    median = numbers[int (N/2)]
    
# mode
count = {}
max = None
for item in numbers:
    if item in count:
        count[item] = count[item] + 1
    else:
        count[item] = 1
    if max is None:
        max = (item, 1)
    else:
        if count[item] > max[1]:
            max = (item, count[item])
mode = max[0]

print (scale(average,1))
print (scale(median,1))
print (mode)
