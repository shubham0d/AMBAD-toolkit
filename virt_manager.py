#!/usr/bin/python
import sys
import subprocess

def installation():
    print()
    if (sys.argv[2] == 'mips'):
        subprocess.getstatusoutput('qemu-img create -f qcow2 data/mips.img 5G')
        subprocess.getstatusoutput("#qemu-system-mips -M malta -m 512 -hda data/mips.img " \
        "-kernel data/mips_kernel -initrd mips_initrd.gz -nographic")

def banner():
    print ("Usage: python", sys.argv[0] , "<setup|start> <mips|powerpc|x86|x86_64>")

def main():
    if (len(sys.argv) != 3):
        banner()
        return
    if (sys.argv[1] not in ['setup', 'start'] or sys.argv[2] not in ['mips','powerpc','x86', 'x86_64']):
        banner()
        return
    if (sys.argv[1] == 'setup'):
        installation()


main()
