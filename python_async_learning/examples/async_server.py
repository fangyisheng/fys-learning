import asyncio


async def handle_echo(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    addr = writer.get_extra_info("peername")
    print(f"Client connected: {addr}")
    while True:
        data = await reader.readline()
        if not data:
            break
        message = data.decode().strip()
        print(f"Received: {message}")
        writer.write(f"echo: {message}\n".encode())
        await writer.drain()
    writer.close()
    await writer.wait_closed()
    print(f"Client disconnected: {addr}")


async def main() -> None:
    server = await asyncio.start_server(handle_echo, "127.0.0.1", 8888)
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.")
