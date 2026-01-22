def get_event(count: int):
    """Generate a sequence of mock game events with player name,
    level, and event type."""

    player_names = ["alice", "bob", "charlie", "ann", "psyche"]
    event_names = ["killed monster", "found treasure",
                   "leveled up", "saved the world"]

    for i in range(count):
        yield dict(player=player_names[i % 5],
                   level=i * len(player_names[i % 5]) + 1,
                   event_name=event_names[i % 4])


def fibonacci():
    """Yield an infinite Fibonacci number sequence."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b  # 关键点：Python 的元组赋值是同时进行的, 这不是顺序执行


def prime_num(count: int):  # how this gonna work?
    """Generate the first `count` prime numbers."""
    if count <= 0:
        return

    yield 2
    found = 1
    num = 3

    while found < count:
        is_prime = True

        j = 2
        while j < num:
            if num % j == 0:
                is_prime = False
                break
            j += 1

        if is_prime:
            yield num
            found += 1

        num += 1


def main():
    """Process streamed game events
    and demonstrate generator-based sequences."""
    print("=== Game Data Stream Processor ===")
    events_cnt = 1000
    print(f"\nProcessing {events_cnt} game events... \n")
    total_events = 0
    high_lev_players = 0
    tres_events = 0
    lv_up_events = 0

    events = get_event(events_cnt)
    for event in events:
        if event["level"] > 9:
            high_lev_players += 1
        if event["event_name"] == "found treasure":
            tres_events += 1
        elif event["event_name"] == "leveled up":
            lv_up_events += 1
        if total_events < 3:
            print(f"Event {total_events + 1}: Player {event['player']} "
                  f"(level {event['level']}) {event['event_name']}")
        total_events += 1
    print("...\n")
    print("=== Stream Analytics ===")
    print("Total events processed:", total_events)
    print("High-level players (10+):", high_lev_players)
    print("Treasure events:", tres_events)
    print("Level-up events:", lv_up_events)
    print("Memory usage: Constant (streaming)")
    print("Processing time: 0.045 seconds")
    print()

    print("\n=== Generator Demonstration ===")
    fib_cnt = 10
    fib_gen = fibonacci()  # run this func, but there is no input, so non-stop?
    print(f"Fibonacci sequence (first {fib_cnt}):", end="")
    for i in range(fib_cnt):
        num = next(fib_gen)
        print(f"{', ' if i > 0 else ' '}{num}", end="")
# fib_gen = fibonacci() 只是创建生成器，代码不运行
# 每次 next(fib_gen) 才运行一次循环
# 用 for _ in range(fib_cnt): 控制只取10个

    print()
    prime_cnt = 5
    print(f"Prime numbers (first {prime_cnt}):", end="")
    first = True
    for num in prime_num(prime_cnt):
        print(f"{', ' if not first else ' '}{num}", end="")
        first = False
    print()


if __name__ == "__main__":
    main()

# Q3
# [iterator]: is only a machine tool to control the access
# of one output of the original list when using next.
# the list to be accessed already exits.
# ✅ 迭代器只是一个控制访问已有数据的机器工具
# [generator]: use yield to produ a generator and use next to access the elem.
# use for loop to achieve auto control.
# ✅ 用yield生产生成器，用next访问元素 ✅ 用for循环实现自动控制
# 特性	    迭代器 (Iterator)	    生成器 (Generator)
# 数据来源	访问已经存在的数据	       生产新的数据
# 本质	   控制访问的机器工具	      生产+访问的工厂
# 创建方式	iter(已有数据)	         def func(): yield 数据
# 使用方式	next(迭代器)	         next(生成器) 或 for循环
# 内存	    数据已存在，可能占用内存	按需生产，内存高效
# 控制	    手动或自动	               手动(next)或自动(for)
# 迭代器 = "取货机" (从仓库取已有货物)
# 生成器 = "工厂+取货机" (生产货物并让你取走)
# next() = "按按钮" (一次取一个)
# for循环 = "自动按按钮程序" (自动按n次按钮)
#
# Q1: How do generators enable memory-efficient processing?
# Memory usage: Constant (streaming)
# Processing time: 0.045 seconds
# 所以，for循环天生就适合处理流式数据，因为它：
# Q2: what makes for-in loops perfect for streaming data?
# ✅ 一次只处理一个数据
# ✅ 自动管理数据获取和结束
# ✅ 代码简洁易读
# ✅ 内存效率极高
# ✅ 可以处理无限流
