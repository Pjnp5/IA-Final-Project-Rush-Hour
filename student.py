"""Example client."""
import asyncio
import getpass
import json
import math
import os
import time

# Next 4 lines are not needed for AI agents, please remove them from your code!
import websockets

#from hour_rush_AI import Bot
#from teste2 import Bot
from final_solver import Bot

async def solver(server_address="localhost:8000", agent_name="student"):
    tempo_inicial = time.time()
    async with websockets.connect(f"ws://{server_address}/player") as websocket:
        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        state = json.loads(
            await websocket.recv()
        )  # receive game update, this must be called timely or your game will get out of sync with the server

        retval = True
        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                # Next lines are only for the Human Agent, the key values are nonetheless the correct ones!
                #print(state)
                # Primeira mensagem do server
                if retval:
                    ai = Bot(state['grid'], state["cursor"])
                    retval = False
                else:
                    # Caso o jogo acabe
                    if "highscores" in state:
                        # usamos estas 3 linhas para escrever num ficherio e calcular a media dos 10 jogos
                        """
                        f = open("results.txt", "a")
                        f.write(str(state["score"]))
                        f.write("\n")
                        """
                        print()
                        print(state["score"])
                        print("Demorei: ", (time.time() - tempo_inicial)/60, "minutos")
                        break

                        # buscamos uma jogada
                    #print("State of selection: ", state["selected"])
                    t1 = time.time()
                    key = ai.run(state["grid"], state["cursor"], state["selected"])
                    t2 = time.time() - t1
                    for i in range(round(t2 * state["game_speed"])):
                        #print("DUMPED")
                        await websocket.recv()
                    #print("-> key recebida: ", key)
                    if key is None:
                        continue
                    #print("key: ", key)
                    await websocket.send(
                        json.dumps({"cmd": "key", "key": key})
                    )


            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(solver(f"{SERVER}:{PORT}", NAME))

# problem = asyncio.Queue(loop=loop)
# solution = asyncio.Queue(loop=loop)

# net_task = loop.create_task(agent_loop(f"{SERVER}:{PORT}", NAME))
# solver_task = loop.create_task(solver(problem, solution))


# loop.run_until_complete(asyncio.gather(net_task, solver_task))
# loop.close()
