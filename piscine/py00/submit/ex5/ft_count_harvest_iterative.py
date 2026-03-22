def ft_count_harvest_iterative():
    harvest = int(input("Days until harvest: "))
    i = 1
    while i <= harvest:
        print("Day", i)
        i = i + 1
    print("Harvest time!")

# Python automatically creates an int object.
# i += 1
# for i in range(1, days + 1):
#        print("Day", i)
