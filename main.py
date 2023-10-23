from asyncio import set_event_loop_policy
import sys
from datetime import datetime, timedelta
import httpx
import asyncio
import platform


class HttpError(Exception):
    pass


if len(sys.argv) != 2 or not sys.argv[1].isdigit() or int(sys.argv[1]) > 10:
    print("Usage: number of days (1-10)")
    sys.exit(1)


async def request(url: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        if r.status_code == 200:
            res = r.json()
            return res
        else:
            raise HttpError(f"Error status: {r.status_code} for {url}")


async def main(index_day):
    d = datetime.today() - timedelta(days=int(index_day))
    shift = d.strftime('%d.%m.%Y')
    try:
        response = await request(f"https://api.privatbank.ua/p24api/exchange_rates?date={shift}")
        return response
    except HttpError as e:
        return None


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        index_day = int(sys.argv[1])
        if index_day > 10:
            raise ValueError("The number of days should be from 1 to 10.")
    except (ValueError, IndexError):
        print("Usage: number of days (1-10)")
        sys.exit(1)
