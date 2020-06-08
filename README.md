# cypher9
Simple file encryptor. You can encrypt, decrypt and edit files with it.

# usage
```
cypher9 [-h] [-e] [-d] [-o] [-k KEY] [FILES [FILES ...]]

Encrypt and decrypt files.

positional arguments:
  FILES              Files to process

optional arguments:<br>
  -h, --help         show this help message and exit <br>
  -e, --encrypt      Encrypt files. (default)<br>
  -d, --decrypt      Decrypt files.<br>
  -o, --open         Decrypt file, open it and encrypt it after closing.<br>
  -k KEY, --key KEY  Use key instead of password<br>
```
