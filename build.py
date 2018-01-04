#!/usr/bin/python
import os, glob

PROJECT = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
CC = "arm-none-eabi-gcc"
OC = "arm-none-eabi-objcopy"
LD = "arm-none-eabi-ld"
DEVKITARM = os.environ['DEVKITARM']
ARM_NONE_EABI_VERSION = os.environ.get('ARM_NONE_EABI_VERSION', '7.1.0')

LIBPATH = '-L {0}/lib/gcc/arm-none-eabi/{1}/'.format(
    DEVKITARM, ARM_NONE_EABI_VERSION
)

LIBPATH = '{0} -L {1}/arm-none-eabi/lib/'.format(
    LIBPATH, DEVKITARM
)


def allFile(pattern):
    s = "";
    for file in glob.glob(pattern):
        s += file + " ";
    return s;

def run(cmd):
    print(cmd)
    os.system(cmd)


INCLUDE_C = ' '.join((
    allFile('source/*.c'),
    allFile('source/battle/*.c'),
    allFile('source/rng/*.c'),
))

INCLUDE_S = ' '.join((
    allFile('source/*.s'),
))

INCLUDE_O = ' '.join((
    allFile('lib/*.o'),
))

INCLUDE_A = ' '.join((
    allFile('lib/*.a'),
))

def clean():
    run("rm -rf build")
    run('mkdir build')

def build():
    run('''
    {} -Os -s  -g -I include -I include/libntrplg \
    {} -c -march=armv6 -mlittle-endian
    '''.format(CC, INCLUDE_C))
    run('{} -Os {} -c -s -march=armv6 -mlittle-endian'.\
        format(CC, INCLUDE_S))
    run('''
    {0} {1} -o {2}.elf -pie --print-gc-sections -T 3ds.ld -Map={2}.map \
    {3} {4} {5} -lc --nostdlib
    '''.format(LD, LIBPATH, PROJECT, allFile('*.o'), INCLUDE_O, INCLUDE_A))
    run('{0} -O binary {1}.elf {1}.plg -S'.format(OC, PROJECT))

def move():
    run('mv *.o *.map build')

def main():
    clean()
    build()
    move()

if __name__ == "__main__":
    main()
