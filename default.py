#!/usr/bin/env python3

from __future__ import print_function

import os
import sys
from os import path

import macbok as m


def main():
  """
  A fully-functional example of a typical user's OS X configuration.

  """
  # Do not create .DS_Store on network shares
  yield m.Defaults("com.apple.desktopservices",
                   "DSDontWriteNetworkStores", True)

  # Disable autocorrect
  yield m.Defaults("NSGlobalDomain",
                   "NSAutomaticSpellingCorrectionEnabled", False)

  # Disables keyboard press-and-hold for accented character entry
  yield m.Defaults("NSGlobalDomain",
                   "ApplePressAndHoldEnabled", False)

  # Expand the Save panel by default
  yield m.Defaults("NSGlobalDomain",
                   "NSNavPanelExpandedStateForSaveMode", True)

  # Sets the delay before held keys repeat
  # yield m.Defaults("NSGlobalDomain", "InitialKeyRepeat", 15)

  # Sets the repeat rate for held keys
  # yield m.Defaults("NSGlobalDomain", "KeyRepeat", 2)

  # Minimize windows to dock icon
  yield m.Defaults("com.apple.dock", "minimize-to-application", True)

  # Put the dock on the bottom
  yield m.Defaults("com.apple.dock", "orientation", "bottom")

  # Change icon size
  yield m.Defaults("com.apple.dock", "tilesize", 52)

  # Auto-hide the dock
  yield m.Defaults("com.apple.dock", "autohide", 1)

  # Fast updates for Activity Monitor (every second)
  yield m.Defaults("com.apple.ActivityMonitor", "UpdatePeriod", 1)

  # Dark interface
  # yield m.Defaults("Apple Global Domain", "AppleInterfaceStyle", "Dark")

  # Finder show all file extensions
  yield m.Defaults("Apple Global Domain", "AppleShowAllExtensions", 1)

  # Only show scrollbars when scrolling
  yield m.Defaults("Apple Global Domain",
                   "AppleShowScrollBars", "WhenScrolling")

  # Set ask for password delay to 0
  yield m.Defaults("com.apple.screensaver", "askForPasswordDelay", 0)

  # Turn off Apple Airplay status bar icon
  yield m.Defaults("com.apple.airplay", "showInMenuBarIfPresent", 0)

  # Turn off Finder opening when Transmit mounts.
  if path.exists(path.expanduser(
      "~/Library/Preferences/com.panic.Transmit.plist")):
    yield m.Defaults("com.panic.transmit", "OpenMountedFinderWindow", False)

  # On AC Power, keep the display and system on for 3 hours of inactivity.
  yield m.Pmset('displaysleep', '180', 'c')
  yield m.Pmset('sleep', '180', 'c')

  yield m.Link("Library/Application Support/MobileSync",
               path.expanduser("~/MobileSync"))

  if path.exists(path.expanduser("~/C8")):
    # Avoid creating a dead links
    if not path.exists(path.expanduser("~/.atom")):
      os.mkdir(path.expanduser("~/.atom"))
    for atom_path in ["config.cson", "init.coffee", "keymap.cson",
                      "snippets.cson", "styles.less"]:
      yield m.Link("../C8/atom/" + atom_path,
                        path.expanduser("~/.atom/" + atom_path))
    yield m.Link("C8/.bcrc", path.expanduser("~/.bcrc"))
    yield m.Link("C8/.gitconfig", path.expanduser("~/.gitconfig"))
    yield m.Link("C8/.gitignore", path.expanduser("~/.gitignore"))
    yield m.Link("C8/.bash_aliases", path.expanduser("~/.bash_aliases"))
    yield m.Link("C8/.bash_profile", path.expanduser("~/.bash_profile"))
    if not path.exists(path.expanduser("~/.ssh")):
      os.mkdir(path.expanduser("~/.ssh"))
    yield m.Link("../C8/.ssh/known_hosts",
                      path.expanduser("~/.ssh/known_hosts"))
    yield m.Link("../C8/.ssh/config",path.expanduser("~/.ssh/config"))
    if not path.exists(path.expanduser("~/.ssh/ctl")):
      os.mkdir(path.expanduser("~/.ssh/ctl"))

  yield m.Touch(path.expanduser("~/.bash_sessions_disable"))

  # Chrome doesn't respect /etc/hosts if not owned by root (?)
  # yield m.Chown("/etc/hosts", m.Username(), group="staff")

  # Basic packages
  yield m.Homebrew(tap="homebrew/core")
  yield m.Homebrew(tap="caskroom/cask")
  yield m.Homebrew(tap="caskroom/drivers")
  yield m.Homebrew(tap="caskroom/versions")
  yield m.Homebrew(tap="homebrew/fuse")
  yield m.Homebrew(tap="homebrew/x11")
  yield m.Homebrew(tap="homebrew/science")
  yield m.Homebrew(tap="rogerhub/sman")
  yield m.Homebrew(tap="rogerhub/transmit-disk")
  yield m.Homebrew("pstree", force_bottle=True)
  yield m.Homebrew("duplicity", force_bottle=True)
  yield m.Homebrew("mcrypt", force_bottle=True)
  # yield m.Homebrew("iperf")
  yield m.Homebrew("mtr", force_bottle=True)
  yield m.Homebrew("unrar", force_bottle=True)
  yield m.Homebrew("wakeonlan")
  yield m.Homebrew("openssl", force_bottle=True)
  # yield m.Homebrew("imagemagick", force_bottle=True)
  # yield m.Homebrew("gettext", force_bottle=True)
  yield m.Homebrew("python", force_bottle=True)
  yield m.Homebrew("python3", force_bottle=True)
  # yield m.Homebrew("hping")
  # yield m.Homebrew("ffmpeg", force_bottle=True)
  yield m.Homebrew("git", force_bottle=True)
  # yield m.Homebrew("webp", force_bottle=True)
  yield m.Homebrew("nmap", force_bottle=True)
  # yield m.Homebrew("nasm", force_bottle=True)
  yield m.Homebrew("source-highlight", force_bottle=True)
  # yield m.Homebrew("lftp", force_bottle=True)
  yield m.Homebrew("arping", force_bottle=True)
  yield m.Homebrew("socat", force_bottle=True)
  yield m.Homebrew("colordiff", force_bottle=True)

  # Fuse-related packages
  yield m.Homebrew(cask_package="osxfuse")
  yield m.Homebrew("sshfs")
  yield m.Homebrew("fuse-zip", force_bottle=True)

  # Cask packages
  yield m.Homebrew(cask_package="google-chrome")
  yield m.Homebrew(cask_package="gnucash")
  yield m.Homebrew(cask_package="vlc")
  yield m.Homebrew(cask_package="calibre")
  yield m.Homebrew(cask_package="vmware-fusion")
  yield m.Homebrew(cask_package="logitech-options")
  yield m.Homebrew(cask_package="atom")
  # yield m.Homebrew(cask_package="wireshark")
  yield m.Homebrew(cask_package="1password")
  yield m.Homebrew(cask_package="handbrake")
  yield m.Homebrew(cask_package="sman")
  # yield m.Homebrew(cask_package="unetbootin")
  yield m.Homebrew(cask_package="transmit")
  yield m.Homebrew(cask_package="transmit-disk")

  # Mactex is hosted on some remote European web server. It takes forever to
  # download (1-2 hours) regardless of your internet connection, so do it last.
  # yield m.Homebrew(cask_package="mactex")


if __name__ == "__main__":
  m.Execute(main)
