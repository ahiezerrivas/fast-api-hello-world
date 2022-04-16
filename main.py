#Python

from typing import Optional
from enum import Enum



#Pydantic
from pydantic import BaseModel, EmailStr
from pydantic import Field

#FastApi
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File


app = FastAPI()

#models

class HairColor(Enum):
    white ="white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"





class Location(BaseModel):
    city: str =Field (
        ...,
        min_length=1,
        max_length=50,
        example="Caracas"
    )
    state: str = Field (
        ...,
        min_length=1,
        max_length=50,
        example="Distrito Capital"
    )
    contry: str = Field (
        ...,
        min_length=1,
        max_length=50,
        example="Venezuela"
    )

class PesonBase(BaseModel):
    first_name: str = Field (
        ...,
        min_length=1,
        max_length=50,
        example="miguel"
    )
    last_name: str = Field (
        ...,
        min_length=1,
        max_length=50,
        example="torres"
    )
    age: int = Field (
        ...,
        gt=0,
        le=115,
        example=25
    )
    hair_color: Optional[HairColor] = Field(default=None, ) 
    is_married: Optional [bool]  = Field(default=None, example=False)
    

class Person(PesonBase):
 
    password: str = Field(
        ...,
        min_length=8,
        example="holasoymiguel"
        )




    # class Config:
    #     schema_extra =  {
    #         "example":{
    #             "first_name":"Facundo",
    #             "last_name":"Garcia",
    #             "age":21,
    #             "hair_color":"blonde",
    #             "is_married":False

    #         }
    #     }


class PersonOut(PesonBase):
   pass
    
class LoginOut(BaseModel):
    username : str = Field(
        ...,
        max_length=20,
        example="miguel2021",
        )
    message: str = Field(default="Login Succesfuly!")


@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
 )
def home():
    return{"Hello": "Backends de TrebolCode"}


@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"]
    )
def create_person(person: Person = Body(...)):
    return person

#Validaciones: Query Parameters
@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]    
    )
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 charactares",
        example="Rocio"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example=25
        )
):
    return {name:age}

persons = [1,2,3,4,5]

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
    )
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example=123,
        title="Person Id",
        description="This is the person Id. It's an integer"
        )
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="!This person doesn't exist"
        ) 
    return {person_id: "It exists!"}

#Validaciones: request Body
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Persons"]
    )
def update_person(


    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is  the person ID",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    # location: Location = Body(...)
    
):
    # results = person.dict()
    # results.update(dict(location))
    # return results
    return person


#Forms

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)

#Cookies and Headers
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK
)
def contact(
    firs_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
        example="ahiezer"
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
        example="rivas"
    ),
    email: EmailStr = Form(..., example="ahiezerrivas@gmail.com"),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
) :
    return user_agent

#Files

@app.post(
    path="/post-image"
)
def post_image(
    image: UploadFile = File(...)

):
    return{
        "Filename":image.filename,
        "Format":image.content_type,
        "Size(kb)":round(len(image.file.read())/1024, ndigits=2)
    }