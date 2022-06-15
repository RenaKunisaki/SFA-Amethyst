#!/bin/sh
# build script for my own system
# just moves some directories off a network mount for performance
DISCROOT=/home/rena/projects/sfa/files
ORIGISO=~/projects/sfa/original.iso
PATCHISO=~/projects/sfa/patched.iso
[ -f amethyst.arg ] && mv amethyst.arg $DISCROOT
DISCROOT=$DISCROOT ORIGISO=$ORIGISO PATCHISO=$PATCHISO make $*
[ -f $DISCROOT/amethyst.arg ] && rm $DISCROOT/amethyst.arg
exit 0 # wtf
