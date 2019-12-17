package util

import (
	"crypto/md5"
	"fmt"
	"io"
)

func GenMD5(s string) string {
	h := md5.New()
	io.WriteString(h, s)
	return fmt.Sprintf("%x", h.Sum(nil))
}
