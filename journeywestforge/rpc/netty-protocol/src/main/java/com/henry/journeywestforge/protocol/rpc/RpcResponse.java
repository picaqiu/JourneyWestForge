package com.henry.journeywestforge.protocol.rpc;

import lombok.Builder;
import lombok.Data;

import java.io.Serializable;

/**
 * RPC 响应 DTO (数据传输对象)
 * 封装了服务器的执行结果
 * * @author Qiu Han
 */
@Data
@Builder
public class RpcResponse implements Serializable {
    /**
     * 成功时返回的数据
     */
    private Object data;

    /**
     * 失败时返回的异常
     */
    private Throwable error;

    /**
     * 检查是否成功 (约定：error 为 null 即为成功)
     */
    public boolean isSuccess() {
        return this.error == null;
    }
}
