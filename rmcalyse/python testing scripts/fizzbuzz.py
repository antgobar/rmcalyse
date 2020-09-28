def fizzbuzz(num1, num2, length):
    for i in range(1, length):
        print("Fizz" * (i % num1 < 1)+(i % num2 < 1) * "Buzz" or i)
