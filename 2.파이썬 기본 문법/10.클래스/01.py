
class Student:
    def __init__(self,name,age,scores):
        self.name = name
        self.age = age
        self.scores = scores
    def __str__(self):
        return f'이름 : {self.name}, 나이 : {self.age}, 점수 : {self.scores}'
    def get_total(self):
        return sum(self.scores)
    def get_avg(self):
        return self.get_total()/len(self.scores)

s1 = Student('홍길동',20,(95,98,88)  )    
s2 = Student('이순신',30,(100,98,98)  )    
print(s1)
print(s2)
