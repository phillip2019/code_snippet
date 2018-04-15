# coding=utf-8
"""Base64 encode decode."""


class Base64(object):
    """
     * Utilities for encoding and decoding the Base64 representation of
     * binary data.  See RFCs <a
     * href="http://www.ietf.org/rfc/rfc2045.txt">2045</a> and <a
     * href="http://www.ietf.org/rfc/rfc3548.txt">3548</a>.
    """

    # encoder/decoder 默认标识
    DEFAULT = 0

    # 编码是否省略=号填充
    NO_PADDING = 1

    # 编码是否省略所有的换行符，变成一行
    NO_WRAP = 2

    # 若换行，则换行符是crlf还是lf（若NO_WRAP设置了，则此设置无效)
    CRLF = 4

    # 表明url是否安全
    URL_SAFE = 8

    # 为输出流本身服务
    NO_CLOSE = 16

