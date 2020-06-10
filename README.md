# Analysis of Google NNLM-ZH in TF-Hub

## 介紹
+ 這是一份關於 Google NNLM-ZH 的研究範例程式碼，一開始是因為不曉得這份模型的訓練語料庫使用的是簡體中文還是繁體中文 ([#601](https://github.com/tensorflow/hub/issues/601))，隨著 Tensorflow Hub 不斷的更新，這個模型的全貌也逐漸顯現，因此以這兩份 Jupyter Notebook 做紀錄。

## 研究結果
+ 原本的模型中，使用的語料庫與字典基本上是簡體中文。
+ 字典中有特殊符號：`<S>`, `<UNK>`, `</S>`
+ 直接將字典檔翻譯成繁體中文是不能以 `hub.KerasLayer` 的形式讀取的。
  + 推測是 `tf.saved_model` 將字典與權重綁定了
+ 如果要使用繁體中文，目前的方法是將原本的 Embedding 權重視為一般的 Numpy Array 轉存成 `.npy` 檔，並用 `tf.keras.initializers.Constant` 方式放入 Keras Embedding Layer。
  + 這份研究並沒有完整還原出原本模型中如何處理分詞與 OOV 的部分，僅就單個字詞轉換成 Token ID 的方式存取該權重。
  + Sentence Embedding 的方式參考原文件附註的 `tf.nn.embedding_lookup_sparse` 與 sqrtn combiner 方式重現。

## 附註
+ `NNLM-ZH` 資料夾的內容是從 [nnlm-zh-dim128-with-normalization](https://tfhub.dev/google/nnlm-zh-dim128-with-normalization/2) 下載下來的。
+ `convert_s2t.py` 內使用的 [ZhConverter](https://github.com/penut85420/ZhConverter) 套件是使用 MediaWiki 簡單實做出來的簡繁轉換系統。
  + 其準確率並沒有做過評估，理論上任何簡繁轉換系統都可以取代這個部分。

## 尚未完成
+ 尚不理解為何字典大小與模型大小不同：
  + 字典檔有 968,075 個詞，但模型大小為 971,177 x 128，相差 3,102 個詞。
+ 尚不理解原模型的分詞方式：
  + 雖然從使用說明看起來要使用者先自行分詞，但字典中有諸如 `G##` 等詞出現，雖然很有可能是用 `#` 代表數字，但尚未完成這方面的研究。
+ 尚不理解未知詞的處理方式：
  + 有嘗試以 `'<UNK>'` 或 `'<S> <UNK> </S>'` 的方式去還原單個未知詞的情況，但並沒有成功。
+ 在嘗試自行套用 sqrtn 的公式時，尚不理解為何長度的部分需要 +2
+ Tensorflow Hub 上有許多中文模型，目前只用了一個來驗證我的想法，有時間希望可以多拿幾個模型來驗證。

## 授權條款
+ 根據 [tensorflow/hub](https://github.com/tensorflow/hub) 本專案使用 Apache 2.0 授權條款。
