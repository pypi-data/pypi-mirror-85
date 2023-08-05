class Pet(BaseModel):
    id: int
    name: str
    tag: Optional[str] = None


class Pets(BaseModel):
    __root__: List[Pet]


class User(BaseModel):
    class Config:
        extra = Extra.allow

    id: int
    name: str
    tag: Optional[str] = None


class Users(BaseModel):
    __root__: List[User]


class Id(BaseModel):
    __root__: str


class Rules(BaseModel):
    __root__: List[str]


class Error(BaseModel):
    code: int
    message: str


class Event(BaseModel):
    name: Optional[str] = None


class Result(BaseModel):
    event: Optional[Event] = None


class Broken(BaseModel):
    foo: Optional[str] = None
    bar: Optional[int] = None


class Failing(BaseModel):
    pass

    class Config:
        extra = Extra.allow


class Test(BaseModel):
    broken: Optional[Dict[str, Broken]] = None
    failing: Optional[Dict[str, Failing]] = {}


class BrokenArray(BaseModel):
    broken: Optional[Dict[str, List[Broken]]] = None


class Tags(BaseModel):
    __root__: List[str]


class FileSetUpload(BaseModel):
    task_id: Optional[str] = None
    tags: Dict[str, Tags]
