# Support
If you can, I would appreciate your help in contributions to the repo and/or [donations](https://www.paypal.com/paypalme2/JeromieK?st3_text_to_speech_mac)!

You already found me on Github, But, Hey!

Check me out on [StackOverflow.com](https://stackoverflow.com/users/1896134/jayrizzo) OR
Checkout my other Repo ["Random Scripts"](https://github.com/JayRizzo/Random_Scripts)!

# Speak Selected Text for Sublime Text 3

So this is based on the Mac's 'text to speech' function in Sublime Text 3.
Previously from [Scott Martin](https://github.com/scottmartin/speak-selected-text-sublime)

When Sublime Text 3 came out, they changed the way this feature worked with they system, breaking the functionality from the previous versions.

This plug-in has been designed & updated for use with Mac OS X, and it is only needed for OS X 10.14 and higher.


## Installing

Once you have Git installed, just go into Sublime's Packages folder and clone the repo.

```bash
$ cd ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/User/
$ git clone https://github.com/jayrizzo/speak-selected-text-sublime.git "Speak_Selected_Text"
$ mv Speak_Selected_Text/Context.sublime-menu ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/User/Context.sublime-menu
$ mv Speak_Selected_Text/SpeakSelectedText.py ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/User/SpeakSelectedText.py
```

## Usage

From within Sublime Text 3, you can use the plug-in one of three ways.

1. Right-click your selection and choose "Speak Selected Text" from the context menu.
2. Use Sublime's command palette and search for "Speak Selected Text".
3. Create a Sublime Text key-binding mapped to the "speak_selected_text" command

**Note:** The key-binding cannot be the same as the OS shortcut, or the OS shortcut will override it!

**Note:** You can run the command again to stop the speech at any time.
