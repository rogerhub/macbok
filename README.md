# macbok, a provisioner for my MacBook Pro

This project installs packages from Homebrew, Homebrew Cask, PyPI, and Ruby Gems. It also sets up
symbolic links and configures some OS X settings.

## Installation

You probably want to set up an OS X virtual machine, rather than run it live.

1. Install Xcode command line tools with `xcode-select --install` (Or install the full Xcode app
   from the Mac App Store)
2. Download macbok, and run `python2.7 default.py`
3. If it doesn't work, run it a few more times.
4. If that doesn't work, reboot, then go back to step 3.

## Philosophy

This project was born out of frustration with Boxen's complexity, slow performance, and constant
bugs. I personally don't need most of the features that Boxen offers. But on the other hand, I can't
go back to the stone ages of setting up computer manually.

Each module in this project does a single task. Modules can be composed into more complex ideas.
The modules do not support every possible use case. They won't fix version numbers. They won't let
you configure installation paths. That's okay, because I don't need any of those features. They use
simple heuristics to check if the "desired state" has been achieved. From a clean install of OS X,
they do a pretty good job of setting up software the way I want it.

Wherever possible, I try to build in extensibility, so extra features are easier to add in the
future. However, the defaults make very reasonable assumptions. I try to install as much as possible
under the local user, instead of root. Raising an exception is preferred to potentially dangerous
behavior.

Currently, modules are executed in a standard depth-first call stack scheme. However, the modules
are all designed to support a more complex scheduler with cooperative multithreading.

## Performance

My own configuration with 85 tasks (7 settings, 67 software packages, 10 symbolic links, and 1 git
repository) takes 1.13 seconds to finish running in a steady state (when no changes need to be
made) on a virtual machine running on my 13" MacBook Pro 2015.

## Why do I need to install Xcode first?

Well, you can get almost everything working by just installing the Xcode command line tools, which
doesn't require an iCloud account. You can do that by running `xcode-select --install`.

However, some Homebrew apps (like MacVim) require full Xcode.app to compile, so you should probably
download it at some point.

## Doesn't $1 sound too much like $2?

Okay.

## Why are there locks if there's no threading?

Sorry.

## You didn't even synchronize properly. There's a race condition in ...

Yeah I know, it's getting there.

## But muh PEP8

Sorry.

## License

MIT
