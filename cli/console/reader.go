package console

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"syscall"

	"golang.org/x/crypto/ssh/terminal"
)

type Reader interface {
	ReadInt(prompt string) (int, error)
	ReadLine(prompt string) (string, error)
	ReadPassword(prompt string) (string, error)
}

type reader struct{}

func NewReader() reader {
	return reader{}
}

func (r reader) ReadInt(prompt string) (int, error) {
	var s string
	var err error
	if s, err = r.ReadLine(prompt); err != nil {
		return -1, err
	}

	var i int
	if i, err = strconv.Atoi(s); err != nil {
		return -1, err
	}

	return i, nil
}

func (r reader) ReadLine(prompt string) (string, error) {
	scanner := bufio.NewScanner(os.Stdin)
	fmt.Fprint(os.Stderr, prompt)
	var s string
	scanner.Scan()
	if scanner.Err() != nil {
		return "", scanner.Err()
	}
	s = scanner.Text()
	return s, nil
}

func (r reader) ReadPassword(prompt string) (string, error) {
	fmt.Fprint(os.Stderr, prompt)
	var pass, err = terminal.ReadPassword(int(syscall.Stdin))

	if err != nil {
		return "", err
	}

	return string(pass[:]), nil
}
