#!/usr/bin/env python

from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
from os import path

import macbok as m


def main():
  """Configures Roger's MacBook Pro."""

  # Open new finder windows in home directory.
  yield m.Plist('NewWindowTarget', 'PfHm', domain='com.apple.finder')

  # Maximum scrolling speed.
  yield m.Plist('com.apple.scrollwheel.scaling', 1)

  # On AC Power, keep the display and system on for 3 hours of inactivity.
  yield m.Pmset('displaysleep', '180', 'c')
  yield m.Pmset('sleep', '180', 'c')

  # Use stable IPv6 addresses. Otherwise, long-lived IPv6 connections are
  # dropped constantly.
  yield m.Sysctl('net.inet6.ip6.use_tempaddr', '0')

  yield m.Text(
      '/private/etc/sudoers.d/alf',
      'roger ALL = NOPASSWD: /usr/libexec/ApplicationFirewall/socketfilterfw',
      sudo=True)

  if path.exists(path.expanduser('~/K')):
    # Avoid creating a dead links
    if not path.exists(path.expanduser('~/.atom')):
      os.mkdir(path.expanduser('~/.atom'))
    for atom_path in ['config.cson', 'init.js', 'keymap.cson', 'snippets.cson',
                      'styles.less']:
      yield m.Link('../K/atom/' + atom_path,
                   path.expanduser('~/.atom/' + atom_path))
    yield m.Link('K/bcrc', path.expanduser('~/.bcrc'))
    yield m.Link('K/colordiffrc', path.expanduser('~/.colordiffrc'))
    yield m.Link('K/editrc', path.expanduser('~/.editrc'))
    yield m.Link('K/gitconfig', path.expanduser('~/.gitconfig'))
    yield m.Link('K/gitignore', path.expanduser('~/.gitignore'))
    if not path.exists(path.expanduser('~/.gnupg')):
      os.mkdir(path.expanduser('~/.gnupg'))
    yield m.Link('../K/gpg-agent.conf', path.expanduser('~/.gnupg/gpg-agent.conf'))
    yield m.Link('K/tmux.conf', path.expanduser('~/.tmux.conf'))
    yield m.Link('K/bash_aliases-mac', path.expanduser('~/.bash_aliases'))
    if not path.exists(path.expanduser('~/.ssh')):
      os.mkdir(path.expanduser('~/.ssh'))
    yield m.Link('../K/ssh/known_hosts', path.expanduser('~/.ssh/known_hosts'))
    yield m.Link('../K/ssh/config', path.expanduser('~/.ssh/config'))
    if not path.exists(path.expanduser('~/.ssh/ctl')):
      os.mkdir(path.expanduser('~/.ssh/ctl'))

    # Set the alert sound to be this empty audio file.
    yield m.Plist('com.apple.sound.beep.sound',
                  path.expanduser('~/K/empty.m4a'))

  yield m.Touch(path.expanduser('~/.bash_sessions_disable'))
  yield m.Touch(path.expanduser('~/.hushlogin'))

  # Basic packages
  yield m.Homebrew(tap='homebrew/core')
  yield m.Homebrew(tap='homebrew/cask')
  yield m.Homebrew('mcrypt', force_bottle=True)
  yield m.Homebrew('iperf')
  yield m.Homebrew('mtr', force_bottle=True)
  yield m.Homebrew('unrar', force_bottle=True)
  yield m.Homebrew('wakeonlan')
  yield m.Homebrew('openssl', force_bottle=True)
  yield m.Homebrew('python', force_bottle=True)
  yield m.Homebrew('libav', force_bottle=True)
  yield m.Homebrew('git', force_bottle=True)
  yield m.Homebrew('nmap', force_bottle=True)
  yield m.Homebrew('source-highlight', force_bottle=True)
  yield m.Homebrew('lftp', force_bottle=True)
  yield m.Homebrew('arping', force_bottle=True)
  yield m.Homebrew('socat', force_bottle=True)
  yield m.Homebrew('colordiff', force_bottle=True)
  yield m.Homebrew('mpv', force_bottle=True)
  # yield m.Homebrew('ykpers', force_bottle=True)
  yield m.Homebrew('gnupg', force_bottle=True)
  yield m.Homebrew('pinentry-mac', force_bottle=True)
  # yield m.Homebrew('libu2f-host', force_bottle=True)
  # yield m.Homebrew('libusb', force_bottle=True)
  yield m.Homebrew('whois', force_bottle=True)
  yield m.Homebrew('gnu-tar', force_bottle=True)
  yield m.Homebrew('the_silver_searcher', force_bottle=True)
  # yield m.Homebrew('go', force_bottle=True)  # Only for gofmt.
  yield m.Homebrew('ctags', force_bottle=True)
  yield m.Homebrew('smartmontools', force_bottle=True)
  yield m.Homebrew('tmux', force_bottle=True)
  # yield m.Homebrew('openssh', force_bottle=True)
  yield m.Homebrew('fping', force_bottle=True)

  # Cask packages
  yield m.Homebrew(cask_package='google-chrome')
  yield m.Homebrew(cask_package='gnucash')
  yield m.Homebrew(cask_package='vmware-fusion')
  yield m.Homebrew(cask_package='atom')


if __name__ == '__main__':
  sys.path.append(path.dirname(__file__))
  m.Execute(main)
