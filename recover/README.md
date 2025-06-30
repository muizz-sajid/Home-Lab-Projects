# Recover JPEGs from a Forensic Image

This application processes a memory‑card image by sequentially reading every 512‑byte block—eschewing any form of optimization or parallelism—and meticulously scans each block for the characteristic JPEG header signature. Only after this exhaustive, block‑by‑block examination does it aggregate and reconstruct the identified JPEG fragments into complete image files.

## Overview

The process begins with the verification of a memory card's image, opening the file anew, and checking each 512-byte section for JPEG files. Each portion is examined to identify a JPEG header. If there is a match, it creates a new image file in the format ###.jpg, representing a three-digit counter. Each block is then uncorrupted and stored into separate files.

## Usage

```bash
./recover memorycard.raw
```

- `memorycard.raw`: This is the input file containing the raw memory card image.

## How It Works

1. The program checks for correct command-line usage.
2. It opens the input file and reads 512 bytes at a time into a buffer.
3. When it detects a JPEG header (`0xff 0xd8 0xff 0xe0` to `0xff 0xd8 0xff 0xef`), it starts writing to a new JPEG file.
4. If already writing to a file, it closes the previous file before creating a new one.
5. It continues writing until the next header or end of file.

## File Structure

- `recover.c`: The C source code file.
- `###.jpg`: Recovered JPEG files output by the program.

## JPEG Header Signature

A JPEG file starts with the following byte pattern:
- First three bytes: `0xff 0xd8 0xff`
- Fourth byte: `0xe0` to `0xef`

## Example Output

If 50 JPEGs are found, files `000.jpg` through `049.jpg` will be created.

## Requirements

- GCC or any C compiler
- Standard C library

## Compilation

```bash
gcc -o recover recover.c
```

