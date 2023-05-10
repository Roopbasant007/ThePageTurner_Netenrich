from pydantic import BaseModel, EmailStr 

#studentSchema
class StudentSchema(BaseModel):
    rollno: str
    name: str
    course: str
    dept: str
    year_of_admission: int
    email: EmailStr

    class Config:
        orm_mode = True
        

#classSchema has been inherited from StudentSchema 
class CreateStudentSchema(StudentSchema):
    
    password: str 

    class Config:
        orm_mode = True
            

# schema for login request 
class LoginRequestSchema(BaseModel):
    rollno: str
    password: str

    class Config:
        orm_mode = True
   


        
