package com.henry.journeywestforge.performance.chapter1;

import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@Warmup(iterations = 5, time = 1, timeUnit = TimeUnit.SECONDS)
@Measurement(iterations = 5, time = 1, timeUnit = TimeUnit.SECONDS)
@Fork(1)
@State(Scope.Thread)
public class DceBenchmark { // (我换了个新名字，以免和你的 FibTest 混淆)

    /**
     * 一个 JIT“能看懂”的简单计算
     * 这是一个简单的循环，JIT 可以轻松分析它
     */
    private double simpleCalculation() {
        double result = Math.PI; // (一个起点)
        for (int i = 0; i < 1000; i++) {
            result += Math.log(result); // (随便做点计算)
        }
        return result;
    }

    // --- 实验 A：“有缺陷”的简单陷阱 ---
    @Benchmark
    public void test_A_Flawed_Simple() {
        // JIT 100% 能看懂：
        // 1. simpleCalculation() 是“纯的”(没有副作用)
        // 2. 它的结果被丢弃了
        // 3. 结论：删除它！
        simpleCalculation();
    }

    // --- 实验 C：“修正”的陷阱 (JMH 黑洞) ---
    @Benchmark
    public void test_C_Fixed_Simple(Blackhole bh) {
        // JIT 看到：
        // 1. 结果被“黑洞”消费了
        // 2. 结论：必须执行！
        bh.consume(simpleCalculation());
    }
}