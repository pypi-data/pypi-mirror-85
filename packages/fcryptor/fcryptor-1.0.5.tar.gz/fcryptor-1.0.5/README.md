# File Cryptor

## Install

    pip install fcryptor

## Usage
```fcryptor [-h] (-c | -d) [-si] -i INPUT [-o OUTPUT] [-k KEY] [-gk]```

```
optional arguments:
    [ -h  | --help    ]               show help message and exit

    [ -c  | --crypt   ]               crypting flag
    [ -d  | --decrypt ]               decrypting flag

    [ -si | --stdin   ]               when stdin is true, default=false

    [ -i  | --input   ]    INPUT      Input File/stdin [for stdin pass -si | --stdin]
    [ -o  | --output  ]    OUTPUT     Output crypt/decrypt result to File

    [ -k  | --key     ]    KEY        key of/for file
    [ -gk | --genkey  ]               generate a key and exit
```

# Examples

	fcryptor -c -si -i Hi

    # output
    Key is: szTaqno8sG4K8Gi0z1t4iTzlYb7RIebzhjPFpGPlstg=
    encrypt:
    gAAAAABfqVhMM5dk5HhO7Am3FyFk1qXpobq-JWyF5DbG1PFsRHWH3VzTzhyn8NrcBVfI10_lmqHSm3-YVC4BRYkLTK7T0ldu-Q==
--------------------------------
    fcryptor -d -si -i gAAAAABfqVhMM5dk5HhO7Am3FyFk1qXpobq-JWyF5DbG1PFsRHWH3VzTzhyn8NrcBVfI10_lmqHSm3-YVC4BRYkLTK7T0ldu-Q== -k szTaqno8sG4K8Gi0z1t4iTzlYb7RIebzhjPFpGPlstg=

    # output
    decrypt:
    Hi
---------------------------------
    fcryptor -c -i test.txt -o test.enc
    # output
    Key is: dOmxLC4uEka9vGj8vfwECMHu9MbWo6RCYKDR1hXKGvU=
---------------------------------
    fcryptor -d -i test.enc -o test.txt
    # output
    when pass -d, you have to pass -k [the Key] argument

    #again
    fcryptor -d -i test.enc -o test_d.txt -k dOmxLC4uEka9vGj8vfwECMHu9MbWo6RCYKDR1hXKGvU=
    #output
    [nothing, just create test_d.txt file]
---------------------------------
