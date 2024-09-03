---
title: "Reviving a 2006 Mac Pro"
date: 2018-01-02
---

Recently I acquired a 2006 Mac Pro (model number 1,1); this was Apple's first Mac Pro but was an incredible powerhouse for its time. For example, the Mac Pro in this article features a dual Xeon configuration as well as 10 gigabytes of RAM located on the motherboard as well as the two sister-boards located in the machine. When I first got hold of the machine, it ran Mac OSX Lion (10.7) and my Father had prepared a partition for me in advance.

My intention was to give this Mac Pro a new life by converting into a cloud server. We eventually achieved this by installing Debian Stretch onto the machine and then installing Nextcloud alongside its required repositories (such as PHP, MySQL, etc.). This article details this process.

## Installing Debian

We started by installing Debian Stretch onto the machine, this was achieved by burning the OSes iso file onto a disk using Disk Utility. This allowed us to boot from the CD, and the Debian Installer GUI soon showed up on the screen. Luckily, the installer recognised the partitions on the hard drive and we were able to install Debian in the desired partition.

## Setting up Dual Booting

We needed to be able to keep both OSes (OS X Lion for troubleshooting and Debian for server stability) and therefore needed a Dual Booting solution. Most resources online suggested a boot-loader by the name of rEFIt. After a while though, it became apparent that the rEFIt menu was not going to show up on boot. Although I had had previous success with rEFIt on my MacBook (on which I had installed Ubuntu), rEFIt refused to work on this Mac Pro. It turned out that rEFIt had long been unsupported and a fork of it, rEFInd had been created. The creator's site featured not only installation instructions but far more detailed troubleshooting documentation. After installing the rEFInd tool and using the troubleshooting hints (which suggested blessing the boot-loader), the rEFInd boot-loader GUI showed up and displayed both Mac OS as well as different versions of the Debian GRUB (a boot-loader in itself).

Thus, the rEFInd boot-loader allowed us to jump between the OSes as necessary. If you also find yourself needing to dual boot between partitions or OSes I would also suggest using rEFInd due to the superior documentation and indeed results. You can find the creator's page [here](http://www.rodsbooks.com/refind/).

## Debian troubleshooting

rEFInd successfully booted into Debian's GRUB, but got stuck trying to switch from the EFI VGA to the Radeon Graphics card. After digging through various forums, it turned out the solution was to change some of the start-up code. Looking through these forums, it seemed this was an issue that persisted with Radeon Graphics cards. If you have a similar issue booting into Debian or even Ubuntu (also based off of Debian) you can check out the solution [here](https://apple.stackexchange.com/questions/211260/grub-2-error-fb-switching-to-radeondrmfb-from-efi-vga#222003).

## Installing Nextcloud

This was the last step of reviving the Mac Pro and turning it into a cloud server. This process seems to be OS specific, although it would be very similar between Linux distros. There are plenty of online guides that are specific to various OSes and even versions of Nextcloud. Although the tutorial you take shouldn't make much of difference, it is a good idea to download the right packages and make sure your cloud server is running correctly.

## What's Next

There are countless ways to make use of cloud servers, such as Web Hosting, Video Streaming and things like Document, Contact and Calendar synchronisation. On top of this, private cloud services like ownCloud and Nextcloud offer many extensions or 'apps' that further the functionality of your cloud service. Furthermore, ownCloud and Nextcloud are notably open source, and many people have created their own code for these services in various GitHub repos. With the large communities around these services, it is likely that you can find a piece of code for your purposes. Moreover, Nextcloud is built on PHP and you could even expand it yourself.

## Conclusion

This article has been an example of how you can revive old hardware and make good use of it, even 32-bit systems like the Mac Pro 1,1. There are limitless possibilities! If you have done or plan to do something similar, feel free to share you experiences with me in the 'About' section of this Blog.

👏 Many thanks to my Dad who made this all possible by giving me his Mac Pro 1,1 and helping me with various troubleshooting issues!

