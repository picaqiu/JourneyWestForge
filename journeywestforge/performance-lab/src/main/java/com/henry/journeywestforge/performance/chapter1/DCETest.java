package com.henry.journeywestforge.performance.chapter1;

import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
// 提高预热次数，给 JIT 足够的时间思考
@Warmup(iterations = 5, time = 1)
@Measurement(iterations = 5, time = 1)
@Fork(1)
@State(Scope.Thread)
public class DCETest {

    // 我们把循环次数降低到 1000，但每次操作都很“贵”
    private static final int N = 1000;

    // --- 测试 A：有缺陷 (结果未被使用) ---
    @Benchmark
    public void test_A_Flawed() {
        for (int i = 1; i <= N; i++) {
            // Math.log 是一个开销很大的计算。
            // 但 JIT 明确知道它是“纯函数”(无副作用)。
            // 如果结果没人用，JIT 应该 100% 删除它。
            Math.log(i);
        }
    }

    // --- 测试 B：修正 (使用 Blackhole) ---
    @Benchmark
    public void test_B_Fixed(Blackhole bh) {
        for (int i = 1; i <= N; i++) {
            // 强制 JIT 计算
            bh.consume(Math.log(i));
        }
    }
}