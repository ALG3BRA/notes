from typing import Annotated
from fastapi import Depends
from utils.uow import UOW, AbstractUOW

UOWDep = Annotated[AbstractUOW, Depends(UOW)]

