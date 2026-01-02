from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Student(BaseModel):
    name: str = "naman" # default argument if nothing is passed then this will be used as default arg
    age: Optional[int] = None
    email: EmailStr
    cgpa: float = Field(gt=0, lt=10, default=5, description="A float value representing the cgpa of the student") # setting constraints "lt= less than equals to" and so on..., u can add RegEx as well 

# Note: Uncomment Chronologically to test it properly
# dicts
# st1 = {"name": "akash"}
# st2 = {"name": 32} # generates error, because pydantic by default validate the vars at runtime not like typedDict
# st3 = {"age": '22'} # Coercing: despite of this mis-typed value pydantic is smart engh to convert it into its original type, so here '32' will be typecasted to int
# st4 = {"name": "akash","age": 22,"email": "abc"} # it will throw err at runtime, because pydantic does validation check
# st4 = {"name": "akash","age": '22',"email": "abc@gmail.com"} # it will throw err at runtime, because pydantic does validation check
st5 = {"age": '22',"email": "abc@gmail.com", "cgpa": 8.9} # try to keep out of the given range it will throw error



# student1 = Student(**st1) # any amount of key-value pairs can be passed using **kwargs, and this format is essential when u are dealing with data extraction
# student2 = Student(**st2) # thows error
# student3 = Student(**st3)
# student4 = Student(**st4)
student5 = Student(**st5)
stud_dict = dict(student5) # converting pydantic object to python dict so we can use python functionalities
stud_json = student5.model_dump_json() # converting pydantic object to json 

# print(student1)
# print(student2)
# print(student3)
# print(student4)
print(student5)
print(stud_dict["name"])
print(stud_dict)
print(stud_json)
