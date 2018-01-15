#!/usr/bin/env python3

from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
from os import path

import macbok as m


def main():
  """Configures Roger's MacBook Pro."""

  # Disable autocorrect
  yield m.Plist('NSAutomaticSpellingCorrectionEnabled', True)

  # Disables keyboard press-and-hold for accented character entry
  yield m.Plist('ApplePressAndHoldEnabled', False)

  # Expand the Save panel by default
  yield m.Plist('NSNavPanelExpandedStateForSaveMode', True)

  # Don't minimize windows to dock
  yield m.Plist('minimize-to-application', False, domain='com.apple.dock')

  # Put the dock on the bottom
  yield m.Plist('orientation', 'bottom', domain='com.apple.dock')

  # Use automatic icon size
  yield m.Plist('tilesize', None, domain='com.apple.dock')

  # Don't auto-hide the dock
  yield m.Plist('autohide', 1, domain='com.apple.dock')

  # Disable magnification
  yield m.Plist('magnification', 0, domain='com.apple.dock')

  if path.exists(path.expanduser(
      '~/Library/Preferences/com.apple.ActivityMonitor.plist')):
    # Fast updates for Activity Monitor (every second)
    yield m.Plist('UpdatePeriod', 1, domain='com.apple.ActivityMonitor')

  # Dark interface
  # yield m.Plist('AppleInterfaceStyle', 'Dark')

  # Finder show all file extensions
  yield m.Plist('AppleShowAllExtensions', 1)

  # Only show scrollbars when scrolling
  yield m.Plist('AppleShowScrollBars', 'WhenScrolling')

  # Enable volume feedback
  yield m.Plist('com.apple.sound.beep.feedback', 1)

  # Mute some system souds
  yield m.Plist('com.apple.sound.uiaudio.enabled', 0)

  # Set ask for password delay to 0
  # TODO: This doesn't work. Fix it.
  # yield m.Plist('askForPasswordDelay', 0, domain='com.apple.screensaver')

  # Tap to click
  yield m.Plist('Clicking', 0,
                domain='com.apple.driver.AppleBluetoothMultitouch.trackpad')
  yield m.Plist('Clicking', 0,
                domain='com.apple.AppleMultitouchTrackpad')

  # Set click threshold to 'light'.
  yield m.Plist('FirstClickThreshold', 0,
                domain='com.apple.AppleMultitouchTrackpad')
  yield m.Plist('SecondClickThreshold', 0,
                domain='com.apple.AppleMultitouchTrackpad')

  # Set tracking speed.
  yield m.Plist('com.apple.trackpad.scaling', 1)

  # # Disable guest account.
  # TODO: This doesn't work. Fix it.
  # yield m.Plist('GuestEnabled', False, domain='com.apple.loginwindow',
  #               sudo=True)

  # Set up gnucash settings.
  if path.exists(path.expanduser(
      '~/Library/Preferences/org.gnucash.Gnucash.plist')):
    # Sliding window for date completion.
    # TODO: This is already the default in gnucash trunk.
    yield m.Plist('/org/gnucash/general/date-backmonths', 10,
                  domain='org.gnucash.Gnucash')
    yield m.Plist('/org/gnucash/general/date-completion-sliding', 1,
                  domain='org.gnucash.Gnucash')
    yield m.Plist('/org/gnucash/general/date-completion-thisyear', 0,
                  domain='org.gnucash.Gnucash')

    # Disable auto-save.
    yield m.Plist('/org/gnucash/general/autosave-interval-minutes', 0,
                  domain='org.gnucash.Gnucash')

    # Disable log files.
    yield m.Plist('/org/gnucash/general/retain-type-never', 1,
                  domain='org.gnucash.Gnucash')
    yield m.Plist('/org/gnucash/general/retain-type-days', 0,
                  domain='org.gnucash.Gnucash')

  # Open new finder windows in home directory.
  yield m.Plist('NewWindowTarget', 'PfHm', domain='com.apple.finder')

  # TODO: Rewrite this with ~/Library/Preferences/com.apple.ServicesMenu.Services.plist
  # # Disable context menus.
  # yield m.Plist(
  #     ('NSServicesStatus',
  #      'com.apple.Stickies - Make Sticky - makeStickyFromTextService'),
  #     {'enabled_context_menu': 0, 'enabled_services_menu': 0},
  #     domain='pbs')
  # yield m.Plist(
  #     ('NSServicesStatus',
  #      'com.apple.services.addToiTunesAsSpokenTrack - '
  #      'Add to iTunes as a Spoken Track - runWorkflowAsService'),
  #     {'enabled_context_menu': 0, 'enabled_services_menu': 0},
  #     domain='pbs')
  # yield m.Plist(
  #     ('NSServicesStatus',
  #      'com.todoist.mac.Todoist - Add to Todoist - addToTodoist'),
  #     {'enabled_context_menu': 0, 'enabled_services_menu': 0},
  #     domain='pbs')

  # On AC Power, keep the display and system on for 3 hours of inactivity.
  yield m.Pmset('displaysleep', '180', 'c')
  yield m.Pmset('sleep', '180', 'c')

  yield m.Link('Library/Application Support/MobileSync',
               path.expanduser('~/MobileSync'))

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
  yield m.Homebrew(tap='caskroom/cask')
  yield m.Homebrew(tap='caskroom/drivers')
  yield m.Homebrew(tap='caskroom/versions')
  yield m.Homebrew(tap='homebrew/x11')
  yield m.Homebrew(tap='homebrew/science')
  yield m.Homebrew(tap='rogerhub/sman')
  yield m.Homebrew('pstree', force_bottle=True)
  yield m.Homebrew('mcrypt', force_bottle=True)
  yield m.Homebrew('iperf')
  yield m.Homebrew('mtr', force_bottle=True)
  yield m.Homebrew('unrar', force_bottle=True)
  yield m.Homebrew('wakeonlan')
  yield m.Homebrew('openssl', force_bottle=True)
  yield m.Homebrew('python', force_bottle=True)
  yield m.Homebrew('python3', force_bottle=True)
  yield m.Homebrew('libav', force_bottle=True)
  yield m.Homebrew('git', force_bottle=True)
  yield m.Homebrew('nmap', force_bottle=True)
  yield m.Homebrew('source-highlight', force_bottle=True)
  yield m.Homebrew('lftp', force_bottle=True)
  yield m.Homebrew('arping', force_bottle=True)
  yield m.Homebrew('socat', force_bottle=True)
  yield m.Homebrew('colordiff', force_bottle=True)
  yield m.Homebrew('mpv', force_bottle=True)
  yield m.Homebrew('ykpers', force_bottle=True)
  yield m.Homebrew('gnupg', force_bottle=True)
  yield m.Homebrew('pinentry-mac', force_bottle=True)
  yield m.Homebrew('libu2f-host', force_bottle=True)
  yield m.Homebrew('libusb', force_bottle=True)
  yield m.Homebrew('whois', force_bottle=True)
  yield m.Homebrew('gnu-tar', force_bottle=True)
  yield m.Homebrew('the_silver_searcher', force_bottle=True)
  yield m.Homebrew('go', force_bottle=True)  # Only for gofmt.
  yield m.Homebrew('ctags', force_bottle=True)
  yield m.Homebrew('smartmontools', force_bottle=True)

  # Cask packages
  yield m.Homebrew(cask_package='google-chrome')
  yield m.Homebrew(cask_package='gnucash')
  yield m.Homebrew(cask_package='vmware-fusion')
  yield m.Homebrew(cask_package='atom')
  yield m.Homebrew(cask_package='1password')
  yield m.Homebrew(cask_package='sman')


if __name__ == '__main__':
  sys.path.append(path.dirname(__file__))
  m.Execute(main)
