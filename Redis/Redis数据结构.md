# Redis数据结构

> 可以通过`debug object key`查看数据所使用的具体的数据结构.

| 类型   | 数据结构                                                     |
| ------ | ------------------------------------------------------------ |
| string | sds                                                          |
| list   | quicklist                                                    |
| hash   | ziplist(元素较少时), dict                                    |
| set    | dict, intset                                                 |
| zset   | ziplist(元素较少时), dist(存储key和score的对应关系), skiplist(跳表, 根据`score`维护有序性) |

## 1.Redis对象结构体

> 所有的Redis对象都会被`RedisObject`包裹.
>
> ```c
> struct RedisObject {
>     int4 type;      // 类型
>     int4 encoding;  // 4bits
>     int24 lru;      // lru信息
>     int32 refcount; // 引用计数
>     void *ptr;      // 数据指针
> } robj;
> ```

## 2.SDS

> `Simple Dynamic String` 源码文件: `sds.h, sds.c`
>
> 针对不同长度字符串, 有`sdshar5, sdshar8, sdshar16, sdshar32, sdshar64`
>
> ```c
> struct __attribute__ ((__packed__)) sdshdr8 {
>     uint8_t len; /* used */
>     uint8_t alloc; /* excluding the header and null terminator */
>     unsigned char flags; /* 3 lsb of type, 5 unused bits */
>     char buf[];
> };
> ```

- 针对不同长度的字符串, 使用不同的`sds`结构体, 以节省空间.
- 长度直接读取`O(1)`, 减少了获取长度的是时间复杂度.
- 字符串内存存储到数组中, 减少修改字符串时的空间申请次数.
- 类似智能数组, 实际分配空间大于等于实际使用空间, 通过预分配空间(*capacity* )长度判断, 减少拼接时溢出可能.
- 内容是`char buf[]`, 可以存放二进制信息.

- `embstr`和`raw`:
    - 字符串长度小于**44**时, 为了节省空间, 
    - ![embstr和raw](./image/embstr_raw.jpg)

## 3.dict

> `hash`结构以及整个`Redis`库的key和value对应.
>
> ```c
> typedef struct dict {
>     dictType *type;
>     void *privdata;
>     dictht ht[2];            // 两个哈希表
>     long rehashidx;          /* 不需要进行 rehash if rehashidx == -1 */
>        
> } dict;
> ```

### 1.渐进式`rehash`

- 扩容: hash表中的元素的**个数等于数组的长度**时, 会开始扩容. 2倍扩容.
- 缩容: 元素变的稀疏时, (个数低于数组长度的10%), 会进行缩容.
- `redis`维护两个哈希表, `rehashidx`指示当需要迁移的索引.
    - 当对字典进行`hset, hget, hdel`等操作期间, 除了执行指定的操作, 还顺带做迁移动作. (分散了迁移代价)
    - 当系统处于空闲时, 会主动迁移.

### 2.hash表结构

```c
struct dictEntry {
    void* key;
    void* val;
    dictEntry* next;   // 拉链法(分桶)解决hash冲突
}

struct dictht {
    dictEntry** table; // 存储链表指针的数组
    long size;         // 数组的长度
    long used;         // hash 表中的元素个数, rehash的判断依据
    ...
}
```



## 4.压缩列表 ziplist

> `zset`和`hash`容器对象在元素个数较少的时候, 采用压缩列表进行存储.
>
> 一块连续存储的内存空间, 元素之间紧挨着存储, 没有冗余空间.
>
> ![压缩列表](./image/压缩列表.png)
>
> ```c
> struct ziplist<T> {
>  int32 zlbytes; // 整个压缩列表占用字节数
>  int32 zltail_offset; // 最后一个元素距离压缩列表起始位置的偏移量，用于快速定位到最后一个节点
>  int16 zllength; // 元素个数
>  T[] entries; // 元素内容列表，挨个挨个紧凑存储
>  int8 zlend; // 标志压缩列表的结束，值恒为 0xFF
> }
> 
> struct entry {
>  int<var> prevlen; // 前一个 entry 的字节长度, 方便向前查找
>  int<var> encoding; // 元素类型编码
>  optional byte[] content; // 元素内容
> }
> ```

- `ziplist`:
    - 支持双向遍历, 通过`ztail_offset`快速定位尾部. 通过元素的`prevlen`找到前一个元素的地址..
    - 通过`zllength`确定元素个数.
- 元素:
    - 通过`prevlen`快速找到前一个元素.
    - 通过`encoding`确定 `content`类型. 可以支持不同类型的数据存储. 所以, 每个`entry`大小不定, 由`encoding`决定.
- 内部紧凑存储, 没有冗余空间, 插入元素需要`realloc`扩展空间. ( 可能需要搬迁原有数据)

## 5.IntSet

> set集合容纳的元素都是整数并且元素个数较少时, Redis会使用`IntSet`存储.
>
> ```c
> struct intset<T> {
>     int32 encoding;  // 决定整数位宽是 16 位、32 位还是 64 位
>     int32 length;    // 元素个数
>     int<T> contents; // 整数数组，可以是 16 位、32 位和 64 位
> }
> ```
>
> ![intset](./image/intset.jpg)

- 当`set`中放入非整数时, 存储会转变为`hashtable`.

## 6.快速列表 quicklist

> list的存储类型. 可以理解为多个压缩列表组成的链表.
>
> ![快速列表](./image/quicklist.png)
>
> ```c
> 
> struct quicklistNode {
>     quicklistNode* prev;
>     quicklistNode* next;
>     ziplist* zl;   // 指向压缩列表
>     int32 size;    // ziplist 的字节总数
>     int16 count;   // ziplist 中的元素数量
>     int2 encoding; // 存储形式 2bit，原生字节数组还是 LZF 压缩存储
>     ...
> }
> struct quicklist {
>     quicklistNode* head;
>     quicklistNode* tail;
>     long count; // 元素总数
>     int nodes; // ziplist 节点的个数
>     int compressDepth; // LZF 算法压缩深度
>     ...
> }
> ```

- 链表的附加空间高(prev, next)指针所占空间高. 且每个节点单独分配内存, 加剧内存的碎片化. 
- 没段数据用`ziplist`紧凑存储, 多个`ziplist`串联成链表.
- 每个`ziplist`的长度由参数`list-max-ziplist-size`确定, 超出限制, 会生成一个新的`ziplist`.
- 

## 7.跳跃列表 skiplist

> 类似B+树的一种结构. 应用于 `zset`. 一方面使用`hash`结构存储`value`和`score`的对应. 一方面按照`score`排序.
>
> ![跳表](./image/跳表.jpg)

- 

## 4.数据的持久化

> 或者称为对象的持久化.

- 主要有两种解决思路:
    - 第一种:
        - 清除原有的存储结构, 只将数据存储到磁盘中.
        - 还原重新将数据组织成原有的数据结构.
        - 弊端: 还原到内存的过程中, 会耗用比较多的时间.
    - 第二种:
        - 保留原先的存储格式. 将数据按照原有格式存储在磁盘中.