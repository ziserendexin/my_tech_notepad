1. 关于某C++的文档，上面说具有其他软件调用，获取信息的可能性：

   > This real-time API does not stand on its own. It is layered on a variety of other packages. In general, these are documented in their own help files. This section discusses how these packages are used by applications in relation to this API.
   >
   > 这个实时API并不是独立的。 它分层在各种其他包装上。 通常，这些都记录在他们自己的帮助文件中。 本节讨论应用程序如何使用这些包与此API相关的包。

   大概这个意思就是可以直接获取实时信息？

   在p21(11)中，说

   ```
   #include "MTSBoxInfo.h"
   #include "MTSBoxSelect.h"
   ```

   就可以获取到`MTSBoxInfo`，然后就能通过C++进行交互？。。。看着应该是这个意思吧。。。吧？！


