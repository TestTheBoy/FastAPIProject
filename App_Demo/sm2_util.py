"""
SM2 国密加密/解密工具类
用于前端登录密码的 SM2 非对称加密传输
"""
import base64

try:
    from gmssl import sm2
    HAS_GMSSL = True
except ImportError:
    HAS_GMSSL = False


class Sm2Util:
    """SM2 国密算法工具"""

    @staticmethod
    def encrypt(public_key: str, plaintext: str, mode: int = 1) -> str:
        """
        SM2 加密（前端使用）

        :param public_key: SM2 公钥（hex 字符串，04开头）
        :param plaintext: 明文
        :param mode: 加密模式 0=C1C3C2, 1=C1C2C3（默认）
        :return: 加密后的 hex 字符串
        """
        # if not HAS_GMSSL:
        #     raise ImportError("请安装 gmssl 库: pip install gmssl")

        sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key="")
        cipher_bytes = sm2_crypt.encrypt(plaintext.encode("utf-8"))
        return base64.b64encode(cipher_bytes).decode("utf-8")

    @staticmethod
    def decrypt(private_key: str, ciphertext: str, mode: int = 1) -> str:
        """
        SM2 解密（后端使用）

        :param private_key: SM2 私钥（hex 字符串）
        :param ciphertext: 密文（base64 或 hex 编码）
        :param mode: 解密模式 0=C1C3C2, 1=C1C2C3（默认）
        :return: 解密后的明文字符串
        """
        # if not HAS_GMSSL:
        #     raise ImportError("请安装 gmssl 库: pip install gmssl")

        # 支持 base64 或 hex 两种编码的密文
        try:
            cipher_bytes = base64.b64decode(ciphertext)
        except Exception:
            cipher_bytes = bytes.fromhex(ciphertext)

        sm2_crypt = sm2.CryptSM2(public_key="", private_key=private_key)
        plaintext_bytes = sm2_crypt.decrypt(cipher_bytes)
        return plaintext_bytes.decode("utf-8")

    @staticmethod
    def generate_key_pair() -> tuple:
        """
        生成 SM2 密钥对

        :return: (private_key, public_key) 均为 hex 字符串
        """
        # if not HAS_GMSSL:
        #     raise ImportError("请安装 gmssl 库: pip install gmssl")

        crypt = sm2.CryptSM2()
        private_key = crypt.private_key
        public_key = crypt.public_key
        return private_key, public_key
