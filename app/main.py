"""This module contains entry point & app configuration"""

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def _():
    return "hello"
