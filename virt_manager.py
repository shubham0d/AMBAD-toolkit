#!/usr/bin/python
import sys
import subprocess
from time import sleep
import os

def cmd(cmd):
    cmd = cmd.split()
    code = os.spawnvpe(os.P_WAIT, cmd[0], cmd, os.environ)
    if code == 127:
        sys.stderr.write('{0}: command not found\n'.format(cmd[0]))
    return code

def installation():
    print()
    if (sys.argv[2] == 'mips'):
        subprocess.getstatusoutput('qemu-img create -f qcow2 data/mips.img 5G')
        sleep(1)
        #subprocess.Popen(["qemu-system-mips -M malta -m 512 -hda data/mips.img -kernel data/mips_vmlinux -initrd data/mips_initrd.gz
        #-append \"console=ttyS0 nokaslr\" -nographic"], shell=True, stderr=subprocess.STDOUT,  stdin=subprocess.PIPE)
        cmd("qemu-system-mips -M malta -m 512 -hda data/mips.img -kernel data/mips_vmlinux -initrd data/mips_initrd.gz -nographic")
    if (sys.argv[2] == 'arm'):
        subprocess.getstatusoutput('qemu-img create -f qcow2 data/arm.img 5G')
        cmd("qemu-system-arm -M malta -m 512 -hda data/arm.img -kernel data/arm_vmlinux -initrd data/arm_initrd.gz -nographic")
    if (sys.argv[2] == 'powerpc'):
        subprocess.getstatusoutput('qemu-img create -f qcow2 data/powerpc.img 5G')
        cmd("qemu-system-ppc -M malta -m 512 -hda data/powerpc.img -kernel data/powerpc_vmlinux -initrd data/powerpc_initrd.gz -nographic")
    if (sys.argv[2] == 'i386'):
        subprocess.getstatusoutput('qemu-img create -f qcow2 data/i386.img 5G')
        cmd("qemu-system-i386 -M malta -m 512 -hda data/i386.img -kernel data/i386_vmlinux -initrd data/i386_initrd.gz -nographic")
    if (sys.argv[2] == 'x86_64'):
        subprocess.getstatusoutput('qemu-img create -f qcow2 data/x86_64.img 5G')
        cmd("qemu-system-x86_64 -M malta -m 512 -hda data/x86_64.img -kernel data/x86_vmlinux -initrd data/x86_64_initrd.gz -nographic")


def vm_start():
    print("bolo taara")
def banner():
    print ("Usage: python", sys.argv[0] , "<setup|start> <mips|arm|powerpc|i386|x86_64>")

def main():
    if (len(sys.argv) != 3):
        banner()
        return
    if (sys.argv[1] not in ['setup', 'start'] or sys.argv[2] not in ['mips','arm','powerpc','i386', 'x86_64']):
        banner()
        return
    if (sys.argv[1] == 'setup'):
        installation()
    if (sys.argv[1] == 'start'):
        vm_start()


main()
