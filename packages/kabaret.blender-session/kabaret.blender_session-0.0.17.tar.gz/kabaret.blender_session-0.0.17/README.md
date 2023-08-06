# kabaret.blender_session

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Kabaret integration into blender GUI**

With kabaret, you design your pipelines/workflows and your users will access them using the standalone GUI provided by the Qt based `KabaretStandaloneGUISession`.

When your workflows use Qt based DCCs like Maya, Nuke, Houdini, ... you can use the `KabaretEmbeddedGUISession` to integrate all or parts of your flow into those DCCs.

Blender GUI isn't Qt based so you need another option, which this package provides: `BlenderEmbeddedSession`.

Here is an example of parameter, groups and actions defined in a flow and usable inside Blender: 

![Example Embedded Flow](https://gitlab.com/kabaretstudio/kabaret.blender_session/-/raw/master/docs/blend_session_example.PNG
)

## Synopsis

When running Blender from your flow, you will set the `BLENDER_USER_SCRIPTS` env var to the result of `kabaret.blender_session.get_blender_startup_dir()`.
This will let `kabaret.blender_session` configure your blender on startup so that it:
    
- Shows a "**Kabaret**" tab on the 3D View UI with a "**Flow Tools**" panel showing the kabaret flow page of the *Object* pointed to by the `KABARET_SESSION_HOME` env var. This Panel will let you navigate the whole Objet tree (but not its parent or sibblings), change *Param* values, and trigger *Action*. Pretty much like the `KabaretEmbeddedGUISession` does (with limited ui configuration support though).
- Add all sites listed in the `BLENDER_EXTRA_SITES` env var (";" separated list). This is usefull to access packages from virtual envs and other site-packages style path where you need to support .pth files for example.
- Consider all paths listed in the `BLENDER_EXTRA_SCRIPTS` env var (";" separated list) as if they were set as `BLENDER_SCRIPT`

With this set up, you will be able to control blender from your flow *Action*.

In order for this to work, your flow code must be accessible from within blender. Depending on your setup, you will need to add one or more paths to the `BLENDER_EXTRA_SITES` and/or to the `BLENDER_EXTRA_SCRIPTS` env var.


We recommend using the [kabaret.subprocess_manager](https://pypi.org/project/kabaret.subprocess-manager/ "See on PyPI") package to run Blender from your flow.

Note that a more complete env vars system and a strategy for addons accessibility/activation is on the roadmap.


## Advanced

### Custom Session

As wiht all kabaret sessions, you can use extensions to add views and actors to the `BlenderEmbeddedSession`. 

If you do so, `kabaret.blender_session` needs to use your session class instead of the default one. The `KABARET_BLENDER_SESSION_TYPE` env var can be used to provide the full qualified class name of you session class (for example `my_studio.blender_session.MyBlenderSession`).

Note that your session constructor **MUST** match the default session constructor. If you need to configure your session creation, we recommend using env vars to do so.

**/!\\ CUSTOM SESSION TYPE IS NOT IMPLEMENTED YET /!\\**

(Tell us on the [kabaret discord](https://discordapp.com/invite/NmJDHsN) if you absolutly need this now.)

### Flow Code Sharing

As for any embedded session, your goal is to share your flow code between the python interpretor used for your standalone session and the one embedded in the DCC. One classic strategy is to have you python interpretor version match the one in your dcc (the "match" here is a loosy define concept ^^).

While this is easy to setup, it has a very limited strength and will limit the list of DCCs supported by your pipelines/workflows.

The pythonic approach is to install your flow and all its dependencies inside a virtual env specific for each interpretor / DCC / release / etc...

This setup sounds complicated but it is not, provided you properly package your code (with a proper setup<span></span>.py for example). How to do so is out of kabaret studio scope, but we strongly encourage doing so and we can help you embrace the python packaging ecosystem. Feel free to ask for help on the [kabaret discord](https://discordapp.com/invite/NmJDHsN) ;)

