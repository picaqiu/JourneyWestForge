package com.henry.journeywestforge.protocol.proxy;

/**
 * 动态代理工厂接口
 * 封装了创建代理对象的行为
 */
public interface ProxyFactory {

    /**
     * @param serviceInterface 服务接口的Class
     * @param <T> 服务接口类型
     * @return 代理对象
     */
    <T> T createProxy(Class<T> serviceInterface);
}
