# Python 异步开发模式学习目录

本目录旨在帮助你系统性学习 Python 的异步开发模式，覆盖核心概念、常用 API、设计模式与实战实践。每个主题都配有说明与实践建议，并附带可运行的示例代码（见 `examples/`）。

## 学习路线概览

1. **基础概念**
   - 事件循环（Event Loop）
   - 协程（Coroutine）与 `await`
   - 任务（Task）与调度
   - Future 与回调

2. **常用语法结构**
   - `async def` / `await`
   - `async with` / `async for`
   - 异步上下文管理器与异步迭代器

3. **并发模式**
   - `asyncio.gather` 与 `asyncio.wait`
   - `asyncio.TaskGroup`（Python 3.11+）
   - 取消与超时（`timeout`、`shield`）

4. **同步原语**
   - `Lock` / `Semaphore` / `Event` / `Condition`
   - `Queue` 与生产者-消费者模式

5. **IO 与网络**
   - `asyncio` 流（Streams）
   - TCP/UDP 服务器
   - 子进程管理（`asyncio.create_subprocess_exec`）

6. **协程与线程/进程协作**
   - `asyncio.to_thread`
   - 线程池与进程池执行器

7. **调试与性能**
   - 结构化日志
   - 阻塞点定位
   - 任务泄漏与取消处理

8. **最佳实践**
   - 明确的超时策略
   - 任务生命周期管理
   - 将阻塞 IO 移出事件循环

---

## 示例代码索引

- `examples/basic_coroutines.py`
  - 协程、`await`、`gather`、并发调度。
- `examples/task_group.py`
  - 使用 `TaskGroup` 管理结构化并发（Python 3.11+）。
- `examples/async_primitives.py`
  - `Lock`、`Semaphore`、`Event` 与 `Queue` 的常见用法。
- `examples/async_server.py`
  - 简单的 TCP 回显服务器与客户端示例。

---

## 关键主题详解

### 1. 事件循环（Event Loop）
事件循环是异步程序的核心调度器。它负责：
- 调度协程执行
- 监听 IO 就绪事件
- 处理定时器与回调

推荐入口：
```python
asyncio.run(main())
```

### 2. 协程与任务
- **协程**：`async def` 定义的函数，执行时返回协程对象。
- **任务**：对协程的封装，用于被事件循环调度执行。

常见模式：
```python
task = asyncio.create_task(worker())
result = await task
```

### 3. 取消与超时
良好的超时与取消策略能避免资源泄漏。

- 取消任务：`task.cancel()`
- 超时等待：`asyncio.wait_for(coro, timeout=2)`

### 4. 结构化并发（TaskGroup）
`TaskGroup` 使任务生命周期与作用域绑定，出错时自动取消其他任务。

```python
async with asyncio.TaskGroup() as tg:
    tg.create_task(worker("A"))
    tg.create_task(worker("B"))
```

### 5. 异步同步原语
异步原语用于协调任务间的访问与顺序：
- `Lock`：互斥
- `Semaphore`：限制并发数
- `Event`：广播信号
- `Queue`：生产者-消费者

---

## 实践建议

- **将阻塞 IO 移出事件循环**：使用 `asyncio.to_thread`。
- **为外部请求设置超时**：避免任务永久挂起。
- **集中管理任务生命周期**：避免孤儿任务。
- **合理选择并发结构**：短小任务用 `gather`，复杂工作流用 `TaskGroup`。

---

## 学习练习建议

1. 编写一个异步爬虫，限制并发为 5。
2. 实现一个异步 TCP 聊天服务器，支持多个客户端。
3. 使用 `asyncio.Queue` 实现生产者-消费者流水线。
4. 模拟一个 API 请求扇出与聚合流程，处理失败与超时。

---

## 运行示例

```bash
python python_async_learning/examples/basic_coroutines.py
python python_async_learning/examples/task_group.py
python python_async_learning/examples/async_primitives.py
python python_async_learning/examples/async_server.py
```
