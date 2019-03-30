Title: TrueStudioでJ-Link RTTを使う
Date: 2019-03-30
Category: STM32
Tags: STM32, TrueStudio, J-Link
Slug: TrueStudioWithRTT

# J-Link TrueStudio 始めます
-----------------------------
皆さんはSTM32マイコンを開発するとき, 開発環境は何を使っていますか？
私は以前はVim + Makefile + GDB + ST-Linkみたいな構成で開発していたのですが,

* 最近開発環境がどんどん新しくなってるので取り入れたい.
* デバッガをもっとフルに使いたい.
* J-Linkを使いたい.
* 情けない進化は人の堕落.

などの理由からSTMicroが以前買収したAtollic社から出されているTrueStudioがSTM32をサポートしているのでそれとJ-Linkを使って開発していこうと思いました.
使った感想としては**文明の力すごいな**という感じですが, その中でも特に**J-Link RTT**を気に入ったのでその話を今日はしていきます.

# そもそもJ-Linkとは
-----------------------------
J-LinkはSEGGER社が開発しているマイコン向けのデバッガです.
[SEGGER: J-Link Debug Probes](https://www.segger.com/products/debug-probes/j-link/)
PICマイコンを使うときはPICkit, STM32マイコンを開発するときはLPC-Linkを使うようにJ-Linkもその仲間というイメージです.
このデバッガは様々なマイコンに対応していて,

* Cortex-M0,3,4
* Renesas RX63M
* RV32
* PIC32MX

など様々な種類のマイコンに対応してます. すごい. 詳細はこちら.
[SEGGER: Overview of Supported CPUs and Devices](https://www.segger.com/products/debug-probes/j-link/technology/cpus-and-devices/overview-of-supported-cpus-and-devices/)
他のデバッガとじゃあ何が違うねんとなるわけですが, 今のところ以前使っていたST-Link+GDBと比べた感じ,

* バイナリの転送速度が段違いで速い
* ブレイクポイント間の移動がありえん速い.
* break pointから抜けて次のbreak pointに到達するまでも速い.
* J-Link RTT使えて嬉しい.

などの嬉しい声が届いてます. すごいですね.
詳細は公式HPやidさんのブログ,
[超便利 最強デバッガ J-Link ](http://idken.net/posts/2017-08-31-jlink/ )
に詳しく書いてるのでぜひそちらをご覧ください.
# J-Link RTT って何？
-----------------------------
RTTはReal Time Transferの略で, SWD/JTAGの線上でUART通信みたいにPCと双方向にデータのやり取りができます.
同じようなことができるものとしてsemihostingというものがあると思いますが, RTTはsemihostingより**1万倍速い**ので使わない手はないですね.
下図は168MHzで動くSTM32F407で82文字を送信したときの送信にかかる時間です.
![SEGGER: RTT Performance]({filename}/images/2019-03-30-RTT_SpeedComparison.png)
公式のページより[SEGGER: RTT Performance](https://www.segger.com/products/debug-probes/j-link/technology/about-real-time-transfer/#tab-15668-5)

また, J-Link RTTの特徴として,

* デバッガに繋いでないときはTargetマイコンの内部に送信データがバッファリングされる.
* デバッガが繋げられたときにGDBサーバーを立ち上げずともデータがTargetから送信されてデバッガ側にバッファリングされる.
* GDBサーバーを立ち上げて, Clientを動かすと今までバッファリングされてたデータがPCに送信される.

ということができます.

例えば, ロボットにマイコンを載せて, しばらく動かしたあとにセンサーとかのデータをUARTで送信しようとした場合, 取得して即座に送ると漏れるのでめちゃでか配列を用意してデータを格納して後でまとめて送信するというのが一般的ですが, めんどくさいです.

しかし, RTTを使えば内部で(サイズ制限はあれど)バッファリングしてくれるので, 自分の好きな形式で送信できるし, こちら側で一々めちゃでか配列を用意せずに済みます.

私はマイクロマウスを作っているとき(ホントに作ってるんですか？)に, しばらく走らせたときのセンサーの値の変化を見たいときは

* ロボットを走らせつつ, データをめちゃでか配列に格納していく.
* 走り終わったら形式を整えてUARTで送信

という感じでデータが少ないときはまだしもデータ量が増えたり, 出力形式を変えようとするとそのたびに変更しないといけなくて大変面倒(私がプログラムを書く能力が低いという説は大いにあるが)なのですが, J-Link RTTを使えば

* ロボットを走らせつつ, 欲しい形式でデータを出力してバッファリング
* 走り終えたあとにJ-LinkをさしてまとめてRTTで送信

みたいな感じでずいぶんと楽になります.

便利ですね.
以下でJ-Link RTTを使うためのセットアップの話をしていきます.

# セットアップ
-----------------------------
私のPCの環境はArch Linuxなのでそれをベースに作業していきます.
とりあえず, TrueStudioやSEGGERのツール群, CubeMXをインストールします.
```shell
$ yaourt -S stm32cubemx ozone truestudio
```
私の環境ではtruestudioをビルドするときに/tmp以下が容量不足で爆発したので,
```shell
$ sudo mount -o remount,size=7G,noatime /tmp
```
するとビルドがうまくいきます.
cubemxからTrueStudio向けのプロジェクト生成はいろんなブログで書かれているのでそちらをご参照ください.

以降はcubemxから生成したプロジェクトを読み込んだTrueStudioに対してSEGGER RTTの設定をしていきます.

まずはSEGGER RTTの本体のcファイルやhファイルなどを探します.
私は/opt/SEGGER/SystemView/Target/(SEGGER, Config)以下にありました.

どこにもなかったら
```shell
$ locate RTT
```
って打てば多分見つかると思います.

次にProjectからimportします.
![ImportButton]({filename}/images/2019-03-30-ImportButton.png)


ファイルは2種類あるので両方共importします.
![ImportThem]({filename}/images/2019-03-30-ImportThem.png)


次にProjectを右クリックしてPropertiesからPathとSymbolの設定を行います.
IncludeとSource Locationの箇所に書いてください.
![Include]({filename}/images/2019-03-30-Include.png)
![Source]({filename}/images/2019-03-30-Source.png)


最後に上のボタンからRun→Debug ConfigurationでJ-Linkのためのコンフィギュレーションを行います. 私はSWDを使ってやりました.
![J-LinkConfig]({filename}/images/2019-03-30-JLinkConfig.png)

実際のプログラムは
```C
//include header
#include "SEGGER_RTT.h"
..............
while(1){
    SEGGER_RTT_printf(0, "test\r\n");
    HAL_Delay(100);
}
..............
```
みたいな感じでおkです.
後はコンパイルして書き込み(Debug button)です.
RTTから送信されているデータを見るためには

* JLinkRTTViewer
* JLinkRTTClient
* JLinkRTTLogger

などがありますが,
**Windowsとかでよく見るGUIのJLinkRTTViewerはLinuxの方には実装されていない(キレちゃったねぇ...)**
のでJLinkRTTClientを使います.
Debug Sessionが続いてる間はGDBサーバーが立ち上がっているのでコマンドラインで
```shell
$ JLinkRTTClient
```
を実行するとRTTのデータが見れます. Debug Session中以外は予め
```shell
$ JLinkExe
```
みたいにGDBサーバーを立ち上げておけば大丈夫です.

送信されたデータをファイルに書き込みたい場合は
```shell
$ JLinkRTTLogger
```
を実行すると直接ファイル内に書き出してくれます.

# 終わりに
-----------------------------
いかがでしたか.(これが言いたかった)
私もまだJ-Linkは使いこなせてないのですが, RTTだけでも今までの辛いデバッグ作業で灰色になっていた私の感情が七色に光りだしました.
RTOSのタスクとかも追えたりできるそうなのでそこらへんも今後やっていきたいと思います.
![JLink]({filename}/images/2019-03-30-JLink.jpeg)

最後に
SEGGERさん, Linux版のJLinkRTTViewerください.
