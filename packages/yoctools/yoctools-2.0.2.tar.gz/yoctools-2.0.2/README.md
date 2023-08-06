# flash算法文件的全局更新
    复制CH2201_eFlash_CDK.elf到库目录上一级
    find . -name CH2201_eFlash_CDK.elf | xargs -i  cp ../CH2201_eFlash_CDK.elf {}

# 开启LWIP资源查询
    开启lwipopts.h中的LWIP_STATS LWIP_STATS_DISPLAY MEMP_STATS
    使用free lwip

# WIFI配置
## 无kv配置，默认会用hello,world字符串替代ssid和密码
    kv set wifi_ssid CSKY-T
    kv set wifi_psk test1234

## 启动后，还会初始化如下kv
    aos_kv_setint("gprs_en", 0);
    aos_kv_setint("wifi_en", 1);
    aos_kv_setint("eth_en", 0);

# CLI

## ASII
    esc： 1b
    del:  7f
    bksp: 08
    left: 1b 5b 44
    right:1b 5b 43
    up:   1b 5b 41
    down: 1b 5b 42

## screen
    enter     0d
    backspace 7f
    esc       1b
    del       1b 5b 33 7e

## secureCRT
    enter     0d
    backspace 08
    esc       1b
    del       7e

#媒体文件
## PCM转化（单声道16K）
    ffmpeg -ar 16000 -ac 1 -f s16le -i hello.raw -f wav hello.wav