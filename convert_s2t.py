from ZhConverter.zhhanz_conv import ZhhanzMan

def main():
    zm = ZhhanzMan()

    with open('./NNLM-ZH/assets/tokens.txt', 'r', encoding='UTF-8') as f:
        tokens = [zm.s2t(line) for line in f]

    with open('./tokens.txt', 'w', encoding='UTF-8') as f:
        f.writelines(tokens)

if __name__ == '__main__':
    main()
