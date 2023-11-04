class test:
    def __init__(self, x):
        self.x = x

t1 = test(8)
t2 = t1
t2.x = 10
print(t1.x)
print(t2.x)