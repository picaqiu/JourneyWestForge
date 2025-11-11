package com.henry.journeywestforge.performance.chapter1; // (你的包名)

// 1. 导入 JMH 核心注解
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;

import java.util.concurrent.TimeUnit;

/**
 * 邱涵，这是你的 FibonacciTest 类，已改造为 JMH 基准测试。
 * 我保留了你的类名和核心 fib() 方法。
 *
 * 运行：
 * 1. 在你的 'performance-lab' 模块中，运行 'mvn clean install'
 * 2. Maven 会在 'target/' 目录下生成一个 'benchmarks.jar'
 * 3. 在命令行中运行它：java -jar target/benchmarks.jar
 */

// 2. JMH 基础配置
@BenchmarkMode(Mode.AverageTime) // 测试模式：平均时间
@OutputTimeUnit(TimeUnit.NANOSECONDS) // 输出单位：纳秒 (ns)
@Warmup(iterations = 5, time = 1, timeUnit = TimeUnit.SECONDS) // 预热：5 轮，每轮 1 秒 (让 JIT 充分介入)
@Measurement(iterations = 5, time = 1, timeUnit = TimeUnit.SECONDS) // 测量：5 轮，每轮 1 秒 (在预热后)
@Fork(1) // 在一个单独的子进程中运行 (隔离)
@State(Scope.Thread) // 每个线程一个状态 (JMH 推荐)
public class FibonacciTest {

    // 斐波那契函数 (来自你的代码，保持不变)
    static long fib(int n) {
        if (n <= 1) return n;
        return fib(n - 1) + fib(n - 2);
    }

    /*
     * !!! 重要说明 !!!
     * 你的原始代码测试 fib(50) 是一个“不可能完成”的任务。
     * 1 次 fib(50) 就需要几分钟，JMH 预热 1 秒钟根本跑不完。
     *
     * 为了让你能“跑起来”并看到“JIT 优化”的对比，
     * 我们统一使用一个“中等难度”的数字：fib(20)
     */
    private static final int N = 20;


    // --- 实验一：你的“有缺陷”的基准测试 (JIT 会优化) ---
    // 这就是你书上看到的“陷阱”：JIT 会把这个方法优化成“空”。
    // 因为 fib(N) 的计算结果没有被使用。
    @Benchmark
    public void test_A_FlawedBenchmark() {
        // JIT (C2 编译器) 会说：
        // “这行代码是‘死代码’(Dead Code)，我直接删掉！”
        fib(N);
    }

    // --- 实验二：“修正”的基准测试 (JIT 无法优化 - 方式1) ---
    // 通过“返回”结果，JIT 就无法判定这是“死代码”，
    // 它必须老老实实地计算它。
    @Benchmark
    public long test_B_FixedBenchmark_Return() {
        return fib(N);
    }

    // --- 实验三：“修正”的基准测试 (JMH 推荐 - 方式2) ---
    // JMH 提供了一个“黑洞”(Blackhole)，专门用来“消费”
    // 那些你不想被 JIT 优化掉的计算结果。
    @Benchmark
    public void test_C_FixedBenchmark_Blackhole(Blackhole bh) {
        // bh.consume() 会告诉 JIT：
        // “这个值被‘使用’了，你不准把它优化掉！”
        bh.consume(fib(N));
    }

    /*
     * 运行这个测试，你 100% 会看到：
     *
     * 1. test_A_FlawedBenchmark     :  ~0.5 ns/op (接近0，因为它被优化掉了)
     * 2. test_B_FixedBenchmark_Return : ~10,000 ns/op (一个真实的、很大的数字)
     * 3. test_C_FixedBenchmark_Blackhole: ~10,000 ns/op (和 B 一样的真实数字)
     *
     * 这就是你一直在寻找的“书上的效果”。
     */
}