package com.henry.journeywestforge.protocol.rpc;

import lombok.Builder;
import lombok.Data;

import java.io.Serializable;

@Data
@Builder
public class RpcRequest implements Serializable {
    private static final long serialVersionUID = 1L; // 确保序列化兼容

    /**
     * 要调用的服务接口的完全限定名
     * e.g., "com.henry.journeywestforge.UserService"
     */
    private String serviceName;

    /**
     * 要调用的方法名
     * e.g., "getUser"
     */
    private String methodName;

    /**
     * 方法参数的类型列表
     * (这对于处理“方法重载”至关重要！)
     * e.g., [java.lang.Long.class]
     */
    private Class<?>[] parameterTypes;

    /**
     * 方法参数的实际值
     * e.g., [123L]
     */
    private Object[] parameters;

    // (未来可扩展)
    // private Map<String, String> attachments; // 隐式传参，如 Dubbo 的 Attachment
}
