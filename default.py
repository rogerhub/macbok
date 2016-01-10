#!/usr/bin/env python2.7

import macbok
import sys
from macbok.common.util import get_username
from macbok.modules.chown import Chown
from macbok.modules.defaults import Defaults
from macbok.modules.gem import Gem
from macbok.modules.gitclone import Gitclone
from macbok.modules.homebrew import Homebrew
from macbok.modules.link import Link
from macbok.modules.npm import Npm
from macbok.modules.pypi import Pypi
from os.path import exists, expanduser


def main():
    """
    A fully-functional example of a typical user's OS X configuration.

    """
    # Do not create .DS_Store on network shares
    yield Defaults("com.apple.desktopservices", "DSDontWriteNetworkStores", True)

    # Disable autocorrect
    yield Defaults("NSGlobalDomain", "NSAutomaticSpellingCorrectionEnabled", False)

    # Enables keyboard access for dialog controls
    yield Defaults("NSGlobalDomain", "AppleKeyboardUIMode", 3)

    # Disables keyboard press-and-hold for accented character entry
    yield Defaults("NSGlobalDomain", "ApplePressAndHoldEnabled", False)

    # Expand the Save panel by default
    yield Defaults("NSGlobalDomain", "NSNavPanelExpandedStateForSaveMode", True)

    # Sets the delay before held keys repeat
    yield Defaults("NSGlobalDomain", "InitialKeyRepeat", 15)

    # Sets the repeat rate for held keys
    yield Defaults("NSGlobalDomain", "KeyRepeat", 2)

    # Minimize windows to dock icon
    yield Defaults("com.apple.dock", "minimize-to-application", True)

    # Put the dock on the left
    yield Defaults("com.apple.dock", "orientation", "bottom")

    # Get my vim configuration
    yield Gitclone("https://github.com/rogerhub/vim-config.git", expanduser("~/.vim-config"),
                   recursive=True)
    yield Link(".vim-config/.vim", expanduser("~/.vim"))
    yield Link(".vim-config/.vimrc", expanduser("~/.vimrc"))
    yield Link(".vim-config/.gvimrc", expanduser("~/.gvimrc"))

    yield Link("Development/Configuration", expanduser("~/Configuration"))

    if exists(expanduser("~/Development/Configuration")):
        # Avoid creating a dead links
        yield Link("Configuration/atom", expanduser("~/.atom"))
        yield Link("Configuration/bcrc", expanduser("~/.bcrc"))
        yield Link("Configuration/gitconfig", expanduser("~/.gitconfig"))
        yield Link("Configuration/gitignore", expanduser("~/.gitignore"))
        yield Link("Configuration/ipython", expanduser("~/.ipython"))
        yield Link("Configuration/tmux.conf", expanduser("~/.tmux.conf"))
        yield Link("Configuration/zshconfig", expanduser("~/.zshconfig"))
        yield Link("Configuration/ssh", expanduser("~/.ssh"))

    yield Chown("/etc/hosts", get_username(), group="staff")

    # Basic packages
    yield Homebrew(tap="homebrew/fuse")
    yield Homebrew(tap="homebrew/x11")
    yield Homebrew(tap="homebrew/science")
    yield Homebrew("gcc", force_bottle=True)
    yield Homebrew("rdiff-backup")
    yield Homebrew("awscli")
    yield Homebrew("vim")
    yield Homebrew("fswatch", force_bottle=True)
    yield Homebrew("go", force_bottle=True)
    yield Homebrew("ctags", force_bottle=True)
    yield Homebrew("the_silver_searcher", force_bottle=True)
    yield Homebrew("ant", force_bottle=True)
    yield Homebrew("wget", force_bottle=True)
    yield Homebrew("pstree", force_bottle=True)
    yield Homebrew("duplicity", force_bottle=True)
    yield Homebrew("mcrypt", force_bottle=True)
    yield Homebrew("iperf")
    yield Homebrew("mtr", force_bottle=True)
    yield Homebrew("unrar", force_bottle=True)
    yield Homebrew("htop-osx", force_bottle=True)
    yield Homebrew("wakeonlan")
    yield Homebrew("tmux", force_bottle=True)
    yield Homebrew("openssl", force_bottle=True)
    yield Homebrew("imagemagick", force_bottle=True)
    yield Homebrew("gettext", force_bottle=True)
    yield Homebrew("python", force_bottle=True)
    yield Homebrew("node", force_bottle=True)
    yield Homebrew("hping")
    yield Homebrew("ffmpeg", force_bottle=True)
    yield Homebrew("gradle")
    yield Homebrew("mysql")
    yield Homebrew("clang-format", force_bottle=True)

    # Fuse-related packages
    yield Homebrew(cask_package="osxfuse")
    yield Homebrew(cask_package="sshfs")
    yield Homebrew("fuse-zip", force_bottle=True)

    # Java-related packages
    yield Homebrew(cask_package="java")
    yield Homebrew("maven", force_bottle=True)
    yield Homebrew("scala", force_bottle=True)

    # X11-related packages
    yield Homebrew(cask_package="xquartz")
    yield Homebrew("rdesktop", force_bottle=True)

    # MacVim won't compile until the Xcode is installed
    if exists("/Applications/Xcode.app/"):
        yield Homebrew("macvim")

    # Cask packages
    yield Homebrew(cask_package="google-chrome")
    yield Homebrew(cask_package="keepassx")
    yield Homebrew(cask_package="gnucash")
    yield Homebrew(cask_package="google-hangouts")
    yield Homebrew(cask_package="vlc")
    yield Homebrew(cask_package="calibre")
    yield Homebrew(cask_package="caffeine")
    yield Homebrew(cask_package="tunnelblick")
    yield Homebrew(cask_package="adobe-reader")
    yield Homebrew(cask_package="adobe-creative-cloud")
    yield Homebrew(cask_package="seil")
    yield Homebrew(cask_package="vmware-fusion")
    yield Homebrew(cask_package="vagrant")
    yield Homebrew(cask_package="dropbox")
    yield Homebrew(cask_package="spotify")
    yield Homebrew(cask_package="logitech-options")
    yield Homebrew(cask_package="mactex")
    yield Homebrew(cask_package="atom")
    yield Homebrew(cask_package="intellij-idea")
    yield Homebrew(cask_package="google-cloud-sdk")

    assert sys.executable == "/usr/local/opt/python/bin/python2.7", \
        "Please restart your shell and run this script again, so we install using homebrew's python"

    yield Pypi("boto")
    yield Pypi("dropbox")
    yield Pypi("flake8")
    yield Pypi("gdata")
    yield Pypi("ipdb")
    yield Pypi("ipython")
    yield Pypi("line-profiler")
    yield Pypi("matplotlib", version="1.4.3")
    yield Pypi("numpy")
    yield Pypi("Pillow")
    yield Pypi("psutil")
    yield Pypi("pudb")
    yield Pypi("pycosat")
    yield Pypi("pytest")
    yield Pypi("pyzmq")
    yield Pypi("requests")
    yield Pypi("scipy")
    yield Pypi("scikit-image")
    yield Pypi("scikit-learn")
    yield Pypi("tornado")
    yield Pypi("unittest2")
    yield Pypi("virtualenv")

    yield Gem("tugboat")
    yield Gem("sass")
    yield Gem("uglifier")

    yield Npm("uglify-js")
    yield Npm("coffee-script")
    yield Npm("bower")
    yield Npm("gulp")


if __name__ == "__main__":
    macbok.execute(main)
