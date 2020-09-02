#!/usr/bin/python
import sys
import subprocess
from time import sleep
from shutil import rmtree
from os import stat
from pwd import getpwuid
import os
from os import remove

def cmd(cmd):
    cmd = cmd.split()
    code = os.spawnvpe(os.P_WAIT, cmd[0], cmd, os.environ)
    if code == 127:
        sys.stderr.write('{0}: Error running command\n'.format(cmd[0]))
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

def settingVm():
    # getting the owner and group owner of file to restore later
    defaultOwner = getpwuid(stat("data/"+sys.argv[2]+".img").st_uid).pw_name
    defaultGroup = getpwuid(stat("data/"+sys.argv[2]+".img").st_gid).pw_name
    # copying the boot partition of the image to boot
    subprocess.getstatusoutput('modprobe nbd max_part=63')
    sleep(1)
    if (os.path.isdir("/mnt/"+sys.argv[2]+"/") == False):
        os.mkdir('/mnt/'+sys.argv[2])
    print("Extracing kernel and Filesystem for mips image...")
    subprocess.getstatusoutput('qemu-nbd -c /dev/nbd0 data/'+sys.argv[2]+'.img')
    sleep(2)
    subprocess.getstatusoutput('mount /dev/nbd0p1 /mnt/'+sys.argv[2])
    if (os.path.isdir("data/boot")):
        rmtree('data/boot')
    subprocess.getstatusoutput('cp -r /mnt/'+sys.argv[2]+'/boot data/.')
    #setting back the original  uid and gid to files in data directory
    subprocess.getstatusoutput('chown -R '+defaultOwner+' data')
    subprocess.getstatusoutput('chgrp -R '+defaultGroup+' data')

    subprocess.getstatusoutput('umount /mnt/'+sys.argv[2])
    subprocess.getstatusoutput('qemu-nbd -d /dev/nbd0')
    sleep(1)
    subprocess.getstatusoutput('rmmod nbd')

# command that work
'''
qemu-system-mips -M malta \
  -m 512 -hda hda.img \
  -kernel vmlinux-4.9.0-8-4kc-malta \
  -initrd ./boot/initrd.img-4.9.0-8-4kc-malta \
  -append "root=/dev/sda1 console=ttyS0 nokaslr" \
  -nographic -net user,hostfwd=tcp::2222-:22 -net nic
'''

def poweronVm():
    remove("data/snapshot_"+sys.argv[2])
    subprocess.getstatusoutput('qemu-img create -f qcow2 -b data/'+sys.argv[2]+'.img data/snapshot_'+sys.argv[2]+'.img')
    print("Starting the machine...")
    subprocess.getstatusoutput('qemu-system-mips -M malta  -m 512 -hda data/snapshot_'+sys.argv[2]+'.img kernel data/boot/vmlinux-4.19.0-10-4kc-malta ' \
    '-initrd data/boot/initrd.img-4.9.0-8-4kc-malta -append \"root=/dev/sda1 console=ttyS0 nokaslr\" --nographic -net user,hostfwd=tcp::2222-:22 -net nic')
    print("VM started successfully")

def vm_start():
    check_user = subprocess.getstatusoutput('id -u')
    if int(check_user[1]) != 0:
        print("command: <start> require sudo privilege.")
        exit()
    settingVm()
    poweronVm()


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
