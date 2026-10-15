from fastapi import HTTPException


class CustomException:

    @staticmethod
    def call(message:str,status_code:int=500,exception_type:type[Exception]=HTTPException)->None:
        if issubclass(exception_type,HTTPException):
            raise exception_type(
                status_code=status_code,
                detail=message
            )
        if issubclass(exception_type,ValueError):
            raise HTTPException(
                status_code=status_code,
                detail=message
            )

        raise HTTPException(
            status_code=status_code,
            detail=message
        )
