from datetime import datetime
import requests
import os
import dotenv

from typing import Union
from bs4 import BeautifulSoup

def get_puzzle_input(day:int=None, year:int=None,*,
                     as_lines:bool=True, example:bool = False) -> Union[list[str],str]:
    now = datetime.now()
    if day is None:
        day = now.day
    if year is None:
        year = now.year
    release = datetime(year,12,day,6)
    if now<release:
        raise ValueError("This puzzle has not been released yet!")
    input_path = f"{year}//input_day_{day:0>2}{'_example'*example}.txt"
    if not os.path.exists(input_path):
        url = f"https://adventofcode.com/{year}/day/{day}"
        if example:
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            elements = iter(soup.body.main.article)
            while (item:=next(elements)):
                if "For example:" in item.text:
                    next(elements)
                    content = next(elements).code.text
                    print(content)
                    break
        else:
            dotenv.load_dotenv()
            r = requests.get(url+"/input", cookies={"session":os.getenv("SESSION")})
            content = r.content.decode()
        with open(input_path, 'w') as file:
            file.write(content)
    with open(input_path,'r') as input_file:
        return input_file.readlines() if as_lines else input_file.read()
