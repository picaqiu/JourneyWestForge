package com.henry.journeywestforge.protocol.proxy;

/**
 * 代理工厂类型枚举 (Type-Safe)
 * @author Qiu Han
 */
public enum ProxyType {
    /**
     * Java 原生动态代理 (只能代理接口)
     */
    JDK,

    /**
     * CGLIB 字节码增强 (可以代理类)
     */
    CGLIB,

    /**
     * Javassist 字节码增强 (Dubbo 首选)
     */
    JAVASSIST
}
