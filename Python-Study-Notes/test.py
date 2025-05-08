v6 = [0x0D, 0x0B, 0xFD, 0x08, 0xFA, 0x15, 0xF7, 0xFB, 0xDF, 0x30, 0x11, 0x43, 0xE0, 0xF0, 0xFB]

def decrypt(v6):
    flag = ""
    for i in range(len(v6)):
        # 将 v6[i] 转换到正数范围
        adjusted_value = (v6[i] + 201) % 256  # 假设 55 的补数是 201
        decrypted_char = (adjusted_value ^ 0xA5)

        # 确保结果在合法范围内
        if decrypted_char < 0:
            decrypted_char += 256

        # 检查是否为有效 ASCII 字符（可打印字符范围：0x20 到 0x7E）
        if 0x20 <= decrypted_char <= 0x7E:
            flag += chr(decrypted_char)
        else:
            # 如果无效，保留原始值的十六进制表示
            flag += f"\\x{decrypted_char:02X}"

    return flag


# 输出解密结果
flag = decrypt(v6)
print("Flag:", flag)