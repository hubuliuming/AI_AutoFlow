# Cocos 后端协议格式通用说明

本文档总结一种适合 Cocos Creator 项目的前端到后端协议组织方式，基于当前项目已落地的 HTTP + protobuf 方案抽象而来。文档刻意省略具体业务，只保留协议结构、请求封装、编码解码、token、空请求体、错误包和远端配置等关键示例，方便其他同类 Cocos 项目参考。

## 1. 总体约定

推荐把“命令号”和“消息体”分开处理：

- URL 表示命令：`{backendUrl}/{cmd}`
- Body 表示数据：protobuf wire 二进制
- 登录成功前不带 token
- 登录成功后，除登录命令外都在请求头携带 token
- 每个 cmd 对应一组明确的 `Req -> Resp`
- 前端只编码自己要发送的字段，只解码自己实际使用的响应字段

示例：

```text
POST http://example.com/game/1002
Content-Type: application/x-protobuf

<LoginReq protobuf bytes>
```

登录后：

```text
POST http://example.com/game/2100
Content-Type: application/x-protobuf
token: <login token>

<StageStartReq protobuf bytes>
```

## 2. Cocos 中的推荐目录结构

一个简单可维护的结构如下：

```text
assets/script/net/
  BackendHttpClient.ts   # HTTP 传输层，只关心 URL、Header、Body、Timeout
  ProtocolTypes.ts       # cmd 枚举、请求/响应 TypeScript 类型
  ProtoCodec.ts          # protobuf 最小编解码
  LoginService.ts        # 业务服务：构造请求、调用 client、解响应
  XxxService.ts

assets/script/proto/
  ClientCmdConstants.proto
  Common.proto
  Xxx.proto
```

分层原则：

- `BackendHttpClient` 不理解业务字段。
- `ProtoCodec` 不决定什么时候发包，只负责 `object <-> Uint8Array`。
- `XxxService` 才负责把业务数据转成协议请求。
- UI 或游戏逻辑不直接拼 URL、不直接操作 `XMLHttpRequest`。

## 3. HTTP 客户端示例

核心点是统一 `POST`、统一 `arraybuffer`、统一 token 头。

```ts
class BackendHttpClient {
  private token = "";
  private timeout = 1000 * 60;

  setToken(token: string): void {
    this.token = token || "";
  }

  postProtobuf(cmd: number, body: Uint8Array): Promise<Uint8Array> {
    const url = `${backendUrl.replace(/\/+$/, "")}/${cmd}`;

    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.onreadystatechange = () => {
        if (xhr.readyState !== 4) return;

        const bytes = new Uint8Array(xhr.response || new ArrayBuffer(0));
        if (xhr.status >= 200 && xhr.status < 400) {
          resolve(bytes);
          return;
        }

        const error = new Error(`backend protobuf fail ${xhr.status}: ${url}`) as Error & {
          status?: number;
          body?: Uint8Array;
        };
        error.status = xhr.status;
        error.body = bytes;
        reject(error);
      };

      xhr.onerror = () => reject(new Error(`backend protobuf error: ${url}`));
      xhr.ontimeout = () => reject(new Error(`backend protobuf timeout: ${url}`));
      xhr.timeout = this.timeout;
      xhr.responseType = "arraybuffer";
      xhr.open("POST", url, true);
      xhr.setRequestHeader("Content-Type", "application/x-protobuf");

      if (cmd !== ClientCmd.USER_LOGIN && this.token) {
        xhr.setRequestHeader("token", this.token);
      }

      xhr.send(body);
    });
  }
}
```

注意事项：

- `xhr.responseType = "arraybuffer"` 必须在请求前设置。
- 空请求体也建议明确传 `new Uint8Array(0)`。
- 非 2xx 响应也保留二进制 body，便于解码后端错误包。

## 4. cmd 与类型定义示例

命令号建议在 `.proto` 和 TypeScript 中保持一致。

```proto
enum ClientCmd {
  USER_LOGIN = 1002;
  USER_TITLE_LIST = 1122;
  STAGE_START = 2100;
  STAGE_END = 2101;
}
```

```ts
export enum ClientCmd {
  USER_LOGIN = 1002,
  USER_TITLE_LIST = 1122,
  STAGE_START = 2100,
  STAGE_END = 2101,
}

export interface LoginReq {
  account: string;
  password: string;
  channelId: number;
  loginType?: number;
}

export interface LoginResp {
  token?: string;
  uid?: number;
  nickName?: string;
}
```

## 5. protobuf 编码示例

如果项目没有引入完整 protobuf 运行库，也可以手写一个覆盖当前字段类型的最小 codec。常见移动小游戏协议只需要先覆盖：

- `int32/int64`：wire type 0，varint
- `string`：wire type 2，length-delimited
- `message`：wire type 2，length-delimited
- `repeated message`

登录请求编码示例：

```ts
function encodeLoginReq(req: LoginReq): Uint8Array {
  const writer = new ProtoWriter();
  writer.string(1, req.account);
  writer.string(2, req.password);
  writer.int32(3, req.channelId);
  writer.int32(10, req.loginType ?? 1);
  return writer.toUint8Array();
}
```

对应 proto：

```proto
message LoginReq {
  required string account = 1;
  required string password = 2;
  required int32 channelId = 3;
  optional int32 loginType = 10;
}
```

字段号必须严格一致。字段名可以在前端转换成驼峰命名，但 field number 不能变。

## 6. 请求服务示例

业务服务负责构造请求、调用客户端、解码响应。

```ts
class LoginService {
  async login(): Promise<LoginResp> {
    const req: LoginReq = {
      account: "guest_1_xxx",
      password: "123",
      channelId: 1,
      loginType: 1,
    };

    const body = ProtoCodec.encodeLoginReq(req);
    const respBytes = await backendHttpClient.postProtobuf(ClientCmd.USER_LOGIN, body);
    const resp = ProtoCodec.decodeLoginResp(respBytes);

    if (!resp.token) {
      throw new Error("backend login missing token");
    }

    backendHttpClient.setToken(resp.token);
    return resp;
  }
}
```

一个带 token 的普通请求示例：

```ts
class StageService {
  async startStage(id: number): Promise<StageStartResp> {
    const body = ProtoCodec.encodeStageStartReq({ id });
    const respBytes = await backendHttpClient.postProtobuf(ClientCmd.STAGE_START, body);
    return ProtoCodec.decodeStageStartResp(respBytes);
  }
}
```

## 7. 空请求体示例

有些接口只依赖 token，不需要请求字段。这类接口仍然走同一套 `postProtobuf`，body 传空字节数组。

```ts
async function getTitleList(): Promise<number[]> {
  const respBytes = await backendHttpClient.postProtobuf(
    ClientCmd.USER_TITLE_LIST,
    new Uint8Array(0),
  );
  const resp = ProtoCodec.decodeTitleListResp(respBytes);
  return resp.titleIds ?? [];
}
```

这样比传 `null` 或 `{}` 更清晰：当前协议就是“空 protobuf body”。

## 8. 通用小消息示例

很多项目会有只传一个 id、或者传一个键值状态的接口，可以统一定义小消息。

```proto
message PbInt {
  required int32 value = 1;
}

message PbInt2 {
  required int32 k = 1;
  required int32 v = 2;
}
```

示例：

```ts
// 设置某个 id
const body = ProtoCodec.encodePbInt({ value: 1001 });

// 设置某个 id 的状态
const body2 = ProtoCodec.encodePbInt2({ k: 1001, v: 1 });
```

这类小消息适合“设置称号”“装备状态”“领取某项奖励”等轻量接口。

## 9. 错误包处理

建议后端在非 2xx 或业务错误时返回统一错误 protobuf。

```proto
message ErrorMsg {
  optional int32 code = 1;
  optional string msg = 2;
  optional int32 cmd = 3;
}
```

前端捕获错误时，如果 error 上带有二进制 body，就尝试解码：

```ts
function throwProtoError(e: unknown): never {
  const err = e as Error & { body?: Uint8Array };
  if (err?.body && err.body.length > 0) {
    const msg = ProtoCodec.decodeErrorMsg(err.body);
    throw new Error(`backend error ${msg.code}: ${msg.msg || ""}`);
  }
  throw e;
}
```

这样 UI 层可以拿到明确错误原因，而不是只看到 HTTP 状态码。

## 10. 远端配置接口

配置接口可以不走 protobuf，保持普通 JSON 更方便调试。

推荐格式：

```text
GET {configUrl}/loadConf?key=LevelConfig
Accept: application/json
```

一种常见响应：

```json
{
  "key": "LevelConfig",
  "content": "[{\"id\":1,\"name\":\"stage1\"}]"
}
```

前端处理：

```ts
const outer = JSON.parse(responseText);
const rows = JSON.parse(outer.content);
if (!Array.isArray(rows)) {
  throw new Error("config content is not array");
}
```

注意：`content` 是字符串时，需要二次 JSON 解析。

## 11. 接入检查清单

新 Cocos 项目接入类似协议时，建议逐项确认：

- `backendUrl` 是否可被测试参数覆盖。
- 所有后端请求是否集中在一个 HTTP client。
- 登录后 token 是否只由网络层统一添加。
- 每个 cmd 是否有明确的 `Req -> Resp` 类型。
- 空请求是否统一传 `new Uint8Array(0)`。
- 错误响应 body 是否保留并尝试解码。
- `.proto` 字段号与前端 codec 是否一致。
- 远端配置接口是否和主业务协议分层。
- UI 层是否避免直接拼 URL 或直接操作 XHR。

## 12. 适用边界

这种方案适合：

- Cocos Creator 小游戏。
- HTTP 短连接请求。
- 后端以 cmd 区分接口。
- 协议数量不大，或只需要前端解码部分字段。
- 不想在小游戏包体中引入完整 protobuf 运行库的项目。

如果协议规模很大、字段类型复杂、需要 `oneof/map/packed repeated` 等高级能力，建议改用成熟 protobuf 运行库生成代码，而不是继续扩写手写 codec。
