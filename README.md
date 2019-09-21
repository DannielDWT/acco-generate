# README

#### 基于深度学习的伴奏生成App
    百步梯项目，基于机器学习，通过输入主旋律生成和弦伴奏。

#### 当前版本：
    1.  支持C大调四四拍乐曲的和弦伴奏生成
    2.  支持分解和弦伴奏形式与正常和弦伴奏形式
    3.  支持伴奏的多种乐器选择
    4.  支持midi文件输入
    5.  支持midi文件导出
    6.  支持乐谱导出

#### 下一版本预计：
    1. 支持mp3格式输入
    2. 支持乐曲风格变换
    3. 支持乐曲的平滑处理（对于连续相同和弦进行更改，检测整个乐曲的情感基调）
    4. 支持其它调歌曲的伴奏生成。 

#### 项目使用：
    1.  机器学习相关： sklearn + numpy + pandas
    2.  midi相关:    music21
    3.  IDE: pycharm
    4.  python版本: python3.7
    
#### 项目目录
* ACCO_DATASET：项目数据存放处
   * training（开发过程中训练数据放置处） 
* ACCO_GLOBALDATA:  项目全局数据
   * ACCO_GLOBALDATA_Chord: 和弦相关全局数据
   * ACCO_GLOBALDATA_CNotes: 音符相关全局数据
* ACCO_MODEL: 项目模型
   * ACCO_MODEL_RandomForestModel: 封装的随机森林模型
   * ACCO_MODEL_DescionTree: 同上
   * ACCO_MODEL_SVMModel: 同上
   * ACCO_MODEL_StorageModel: 存储一些废弃的代码（可能会重新使用，开发过程暂时存储处）
* ACCO_PARSER: 解析输入的midi文件
   * ACCO_PARSER_Song:  解析单首歌
   * ACCO_PARSER_ChordDFA: 为了实现常用和弦编配套路用的状态机（当前版本不需使用）
   * ACCO_PARSER_StorageParser: 同上
* ACCO_STYLE: 调整歌曲风格，节奏，乐器等
   * ACCO_STYLE_Instrument: 调整歌曲乐器 

#### 关于模型：
* 模型特征为：
   * 是否是第一个位置
   * 是否是最后一个位置
   * 小节中是否包含和弦内音
   * 小节中重拍所在的音
   * 小节中时值最长的音
   * 小节中出现次数最多的音
   * 每一小节开头的音
* 模型准确率： 测试集约80%，训练集约87%.
* 模型目前只是采用了最为基础的和弦编配理论
* 模型采用每个小节中的信息进行分析判断所配的和弦，因而在歌曲终止符较少，整个歌曲主旋律更为紧凑时表现更为出色，在音较少时会有突兀感。

#### 使用说明：
      1. 在ACCO_DATASET/training放置训练文件，可以使用提供的训练样本，训练样本数目近450个。
      2. 在ACCO_DATASET/predict放置要预测的主旋律文件，也有提供的若干预测音乐文件于predict目录下。
      3. 配制好相应依赖后，运行main.py。（文件顶部有设置相应路径的变量，若1,2中目录不使用项目的目录可以更改为自己制定的目录，同样也可以修改指定的文件名和输出目录，按照1,2设置的可以只修改输出文件名，或者输出默认文件名到ACCO_OUTPUT。）
      4. 在main.py中有设置节奏和乐器的代码，目前尚未提供良好的接口，因而需要自定义节奏和乐器的，需要手动更改几行代码，略微懂一点music21库使用方法。

#### 参考：
      1. music21: <http://web.mit.edu/music21/doc/about/what.html>.
      2. sklearn: <https://scikit-learn.org/stable/>.


