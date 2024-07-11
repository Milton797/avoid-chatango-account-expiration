import asyncio
import ssl
from timeit import default_timer
from typing import List, Optional, Tuple, TypedDict

import aiohttp

RESULTS = []
PORT = '8081'
HOST = 'i0.chatango.com'
ORIGIN = 'https://st.chatango.com'
URL = f'wss://{HOST}:{PORT}/'


class LoginResult(TypedDict, total=False):
    """
    Just a typing class.
    """
    account: str
    status: str
    reason: Optional[str]
    msgcount: Optional[int]


async def run() -> None:
    print('-------------------------------------------------------------')
    print('Running script')
    accounts = read_accounts_file()
    total_accounts = len(accounts)
    print(f'Total accounts: {total_accounts}')
    print('-------------------------------------------------------------')
    for login_info in accounts:
        async with asyncio.TaskGroup() as tg:
            RESULTS.append(tg.create_task(login_account(
                login_info[0], login_info[2]
            )))
    logged = 0
    fails = 0
    for data in RESULTS:
        data = data.result()
        if data.get('status', 'ERROR') == 'ERROR':
            fails += 1
        else:
            logged += 1
        print(data)
    print('-------------------------------------------------------------')
    print('|                         STATUS                            |')
    print('-------------------------------------------------------------')
    print(f'Total accounts: {total_accounts}')
    print(f'Logged: {logged}')
    print(f'Failed: {fails}')
    print(f'Final status: {total_accounts - fails}/{total_accounts}')
    print('A LOG FILE HAS BEEN CREATED IN THE ROOT PATH "output.txt".')
    with open('output.txt', 'w') as file:
        file.truncate()
        file.writelines([str(x.result()) + '\n' for x in RESULTS])


def open_and_trim_file(file_path) -> List[str]:
    with open(file_path, 'a+') as file:
        file.seek(0)
        lines = [x.strip() for x in file if x]

        start_index, end_index = None, None

        for i, line in enumerate(lines):
            if line:
                if start_index is None:
                    start_index = i
                end_index = i + 1

        if start_index is not None and end_index is not None:
            return lines[start_index:end_index] + ['']
        return []


def read_accounts_file() -> List[Tuple[str, str, str]]:
    temp = []
    accounts = []
    lines = open_and_trim_file('accounts.txt')
    for line in lines:
        if line != '':
            temp.append(line)
            continue
        username, email, password = ['-UNKNOWN-DATA-'] * 3
        temp_value = len(temp)
        match temp_value:
            case 1:
                username = temp[0]
            case 2:
                username, password = temp[0], temp[1]
            case temp_value if temp_value >= 3:
                username, email, password = temp[0], temp[1], temp[2]
            case _:
                print('Error parsing file.')
                break
        accounts.append((username, email, password))
        temp.clear()
    return accounts


async def login_account(username: str, password: str) -> LoginResult:
    result = {'account': username}
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers('DEFAULT:@SECLEVEL=1')
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(
                URL, origin=ORIGIN, autoping=False, ssl=ssl_context
            ) as ws:

                # Check websocket version
                await ws.send_str('version:4:1\r\n\x00')
                version = await ws.receive_str()
                version = version.replace('\r\n\x00', '')
                if version != 'OK':
                    raise Exception('Bad websocket version')

                # Check login status
                await ws.send_str(f'login:{username}:{password}\r\n\x00')
                login = await ws.receive()
                login = login.data if login.data else ''
                login = login.replace('\r\n\x00', '')
                if login == 'OK':
                    result['status'] = 'OK'
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            text = msg.data.replace('\r\n\x00', '')
                            if 'msgcount' in text:
                                result['msgcount'] = int(text.split(':')[1])
                                await ws.close()
                        elif msg.type in (
                            aiohttp.WSMsgType.CLOSE,
                            aiohttp.WSMsgType.CLOSING,
                            aiohttp.WSMsgType.CLOSED
                        ):
                            result['status'] = 'ERROR'
                            result['reason'] = 'Websocket closed'
                elif login == 'DENIED':
                    result['status'] = 'ERROR'
                    result['reason'] = 'Bad user or password'
                    await ws.close()
                else:
                    result['status'] = 'ERROR'
                    result['reason'] = 'Unknown login error'
                    if len(username) > 20:
                        result['reason'] = 'Username too long > 20 characters'
    except Exception as e:
        result['status'] = 'ERROR'
        result['reason'] = e
    return result

if __name__ == '__main__':
    start_time = default_timer()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run())

    end_time = default_timer()
    elapsed_time = end_time - start_time
    print(f"Finished in: {elapsed_time} seconds.")
    input('PRESS ENTER TO EXIT.')
