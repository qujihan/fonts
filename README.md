# 字体
- 中文(仅简体中文)
    - [Fangsong 仿宋](https://github.com/qujihan/font-resource):
    - [SimKai 楷书](https://github.com/qujihan/font-resource):
    - [SimSum 宋体](https://github.com/qujihan/font-resource):
    - [SimHei 黑体](https://github.com/qujihan/font-resource):
    - [Han-serif 思源宋体](https://github.com/adobe-fonts/source-han-serif):
    - [Han-sans 思源黑体](https://github.com/adobe-fonts/source-han-sans):
    - [LxgwWenKai 霞鹜文楷](https://github.com/lxgw/LxgwWenKai):
- 西文(仅英语)
    - [lora](https://github.com/cyrealtype/Lora-Cyrillic):
    - [TimesNewRoman](https://github.com/qujihan/font-resource):
- Codeing
    - [Firacode](https://github.com/ryanoasis/nerd-fonts/releases)
    - [Caskaydia](https://github.com/ryanoasis/nerd-fonts/releases): fork form [Cascadia](https://github.com/microsoft/cascadia-code)

# 使用方式
根据 [fonts-example.json](fonts-example.json) 新建一个文件为 fonts.json , 运行`python download.py`, 根据 fonts.json 的内容会自动下载字体

```shell
git submodule add https://github.com/qujihan/fonts.git

cp fonts/fonts-example.json fonts.json

# 修改 fonts.json文件

python fonts/download.py
```

# 使用typst查看字体名称
```shell
comm <(typst fonts | sort) <(typst fonts --font-path . | sort)
diff <(typst fonts) <(typst fonts --font-path .)
```