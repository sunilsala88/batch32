#concorrent programming

# import time

# def fun1():
#     print('start fun1')
#     time.sleep(2)
#     print('end fun1')

# def fun2():
#     print('start fun2')
#     time.sleep(2)
#     print('end fun2')


# fun1()
# fun2()



import asyncio

async def fun1():
    print('start fun1')
    await asyncio.sleep(2)
    print('end fun1')

async def fun2():
    print('start fun2')
    await asyncio.sleep(2)
    print('end fun2')

async def main():
    await asyncio.gather(fun1(),fun2())

asyncio.run(main())