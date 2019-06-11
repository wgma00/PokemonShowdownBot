<h1 id="plugins.CommandBase.CommandBase">CommandBase</h1>

```python
CommandBase(self, aliases, can_learn)
```
Wrapper class for all commands written in this Bot.

Defines main behaviour each command should have and also keeps track of
duplicate commands.

Attributes:
    aliases: list of str, keeps track of all the aliases that evoke this command
    can_learn: Bool,  specifying if chat data should be sent to this bot.

