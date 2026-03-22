def ft_count_harvest_recursive():
    harvest = int(input("Days until harvest: "))

    def helper(day):
        if day > harvest:
            print("Harvest time!")
            return
        print("Day", day)
        helper(day + 1)
    helper(1)
#  Python会自动返回 None
