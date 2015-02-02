# coding=utf-8
"""
admin.py - Willie Admin Module
Copyright 2010-2011, Michael Yanovich, Alek Rollyson, and Edward Powell
Copyright © 2012, Elad Alfassa <elad@fedoraproject.org>
Licensed under the Eiffel Forum License 2.

http://willie.dftba.net/

"""

opers = ['NeoMahler','adriaesc','serra_marc1','mikicat']
import re
from willie.module import commands, priority, OP


def setup(bot):
    #Having a db means pref's exists. Later, we can just use `if bot.db`.
    if bot.db and not bot.db.preferences.has_columns('topic_mask'):
        bot.db.preferences.add_columns(['topic_mask'])


@commands('op')
def op(bot, trigger):
    u"""
    Dóna l'estatus d'operador al nick indicat.
    """
    if trigger.nick in opers:
        if not trigger.group(2):
            channel = trigger.sender
            nick = trigger.nick
            bot.msg('ChanServ', 'op ' + trigger.sender + ' ' + nick)
            return
        else:
            channel = trigger.sender
            nick = trigger.group(2)
            bot.msg('ChanServ', 'op ' + trigger.sender + ' ' + nick)
            return
    else:
        return
        

@commands('deop')
def deop(bot, trigger):
    """
    Treu l'estatus d'operador al nick indicat.
    """
    if trigger.nick in opers:
        if not trigger.group(2):
            channel = trigger.sender
            nick = trigger.nick
            bot.msg('ChanServ', 'deop ' + trigger.sender + ' ' + nick)
            return
        else:
            channel = trigger.sender
            nick = trigger.group(2)
            bot.msg('ChanServ', 'deop ' + trigger.sender + ' ' + nick)
            return
    else:
        return


@commands('voice', 'v', 'veu')
def voice(bot, trigger):
    u"""
    Dóna l'estatus veu al nick indicat.
    """
    if trigger.nick in opers:
        if not trigger.group(2):
            channel = trigger.sender
            nick = trigger.nick
            bot.msg('ChanServ', 'voice ' + trigger.sender + ' ' + nick)
            return
        else:
            channel = trigger.sender
            nick = trigger.group(2)
            bot.msg('ChanServ', 'voice ' + trigger.sender + ' ' + nick)
            return
    else:
        return
            


@commands('devoice', 'dv')
def devoice(bot, trigger):
    """
    Treu l'estatus de veu al nick indicat.
    """
    if trigger.nick in opers:
        if not trigger.group(2):
            channel = trigger.sender
            nick = trigger.nick
            bot.msg('ChanServ', 'devoice ' + trigger.sender + ' ' + nick)
            return
        else:
            channel = trigger.sender
            nick = trigger.nick
            bot.msg('ChanServ', 'devoice ' + trigger.sender + ' ' + nick)
            return
    else:
        return


@commands('kick')
@priority('high')
def kick(bot, trigger):
    """
    Fa fora a l'usuari indicat.
    """
    if bot.privileges[trigger.sender][trigger.nick] < OP:
        return
    text = trigger.group().split()
    argc = len(text)
    if argc < 2:
        return
    opt = text[1]
    nick = opt
    channel = trigger.sender
    reasonidx = 2
    if opt.startswith('#'):
        if argc < 3:
            return
        nick = text[2]
        channel = opt
        reasonidx = 3
    reason = ' '.join(text[reasonidx:])
    if nick != bot.config.nick:
        bot.write(['KICK', channel, nick, reason])


def configureHostMask(mask):
    if mask == '*!*@*':
        return mask
    if re.match('^[^.@!/]+$', mask) is not None:
        return '%s!*@*' % mask
    if re.match('^[^@!]+$', mask) is not None:
        return '*!*@%s' % mask

    m = re.match('^([^!@]+)@$', mask)
    if m is not None:
        return '*!%s@*' % m.group(1)

    m = re.match('^([^!@]+)@([^@!]+)$', mask)
    if m is not None:
        return '*!%s@%s' % (m.group(1), m.group(2))

    m = re.match('^([^!@]+)!(^[!@]+)@?$', mask)
    if m is not None:
        return '%s!%s@*' % (m.group(1), m.group(2))
    return ''


@commands('ban')
@priority('high')
def ban(bot, trigger):
    """
    Bandeja a un usuari del canal. El bot ha de ser operador.
    """
    if bot.privileges[trigger.sender][trigger.nick] < OP:
        return
    text = trigger.group().split()
    argc = len(text)
    if argc < 2:
        return
    opt = text[1]
    banmask = opt
    channel = trigger.sender
    if opt.startswith('#'):
        if argc < 3:
            return
        channel = opt
        banmask = text[2]
    banmask = configureHostMask(banmask)
    if banmask == '':
        return
    if trigger.sender.startswith('##cafe'):
        bot.write(['mode', '##wowthisban +b ' + banmask])
        bot.reply(trigger.group(2) + ' is banned on ##wowthisban')
    else:
        bot.write(['MODE', channel, '+b', banmask])


@commands('unban')
def unban(bot, trigger):
    """
    Desbandeja a un usuari. El bot ha de ser operador.
    """
    if bot.privileges[trigger.sender][trigger.nick] < OP:
        return
    text = trigger.group().split()
    argc = len(text)
    if argc < 2:
        return
    opt = text[1]
    banmask = opt
    channel = trigger.sender
    if opt.startswith('#'):
        if argc < 3:
            return
        channel = opt
        banmask = text[2]
    banmask = configureHostMask(banmask)
    if banmask == '':
        return
    if trigger.sender.startswith('##cafe'):
        bot.write(['mode', '##wowthisban -b ' + banmask])
        bot.reply(trigger.group(2) + ' is unbanned on ##wowthisban')
    else:
        bot.write(['MODE', channel, '-b', banmask])


@commands('quiet')
def quiet(bot, trigger):
    """
    Impedeix que un usuari parli en el canal. El bot ha de ser operador.
    """
    if bot.privileges[trigger.sender][trigger.nick] < OP:
        return
    text = trigger.group().split()
    argc = len(text)
    if argc < 2:
        return
    opt = text[1]
    quietmask = opt
    channel = trigger.sender
    if opt.startswith('#'):
        if argc < 3:
            return
        quietmask = text[2]
        channel = opt
    quietmask = configureHostMask(quietmask)
    if quietmask == '':
        return
    bot.write(['MODE', channel, '+q', quietmask])


@commands('unquiet')
def unquiet(bot, trigger):
    """
   Treu +q a un usuari. El bot ha de ser operador
   """
    if bot.privileges[trigger.sender][trigger.nick] < OP:
        return
    text = trigger.group().split()
    argc = len(text)
    if argc < 2:
        return
    opt = text[1]
    quietmask = opt
    channel = trigger.sender
    if opt.startswith('#'):
        if argc < 3:
            return
        quietmask = text[2]
        channel = opt
    quietmask = configureHostMask(quietmask)
    if quietmask == '':
        return
    bot.write(['MODE', opt, '-q', quietmask])


@commands('kickban', 'kb')
@priority('high')
def kickban(bot, trigger):
    u"""
    Bandeja i fa fora a un usari. El bot ha de ser operador
    Sintaxi: .kickban [#chan] user1 user!*@* raó
    """
    if bot.privileges[trigger.sender][trigger.nick] < OP:
        return
    text = trigger.group().split()
    argc = len(text)
    if argc < 4:
        return
    opt = text[1]
    nick = opt
    mask = text[2]
    reasonidx = 3
    if opt.startswith('#'):
        if argc < 5:
            return
        channel = opt
        nick = text[2]
        mask = text[3]
        reasonidx = 4
    reason = ' '.join(text[reasonidx:])
    mask = configureHostMask(mask)
    if mask == '':
        return
    bot.write(['MODE', '##wowthisban +b', mask])
    bot.write(['KICK', channel, nick, ' :', reason])

@commands('topic')
def topic(bot, trigger):
    """
    Canvia el topic del canal
    """
    purple, green, bold = '\x0306', '\x0310', '\x02'
    if bot.privileges[trigger.sender][trigger.nick] < OP:
        return
    text = trigger.group(2)
    if text == '':
        return
    channel = trigger.sender.lower()

    narg = 1
    mask = None
    if bot.db and channel in bot.db.preferences:
        mask = bot.db.preferences.get(channel, 'topic_mask')
        narg = len(re.findall('%s', mask))
    if not mask or mask == '':
        mask = "Benvinguts a " + channel+  ' || ' + '%s'

    top = trigger.group(2)
    text = tuple()
    if top:
        text = tuple(unicode.split(top, '~', narg))

    if len(text) != narg:
        message = "Not enough arguments. You gave " + str(len(text)) + ', it requires ' + str(narg) + '.'
        return bot.say(message)
    topic = mask % text

    bot.write(['TOPIC', channel + ' :' + topic])


@commands('tmask')
def set_mask(bot, trigger):
    """
    Set the mask to use for .topic in the current channel. %s is used to allow
    substituting in chunks of text.
    """
    if bot.privileges[trigger.sender][trigger.nick] < OP:
        return
    if not bot.db:
        bot.say("I'm afraid I can't do that.")
    else:
        bot.db.preferences.update(trigger.sender.lower(), {'topic_mask': trigger.group(2)})
        bot.say("Gotcha, " + trigger.nick)


@commands('showmask')
def show_mask(bot, trigger):
    """Show the topic mask for the current channel."""
    if bot.privileges[trigger.sender][trigger.nick] < OP:
        return
    if not bot.db:
        bot.say("I'm afraid I can't do that.")
    elif trigger.sender.lower() in bot.db.preferences:
        bot.say(bot.db.preferences.get(trigger.sender.lower(), 'topic_mask'))
    else:
        bot.say("%s")

@commands('m', 'moderat')
def moderat(bot, trigger):
    """Posa el canal en moderat. Només els administradors."""
    if trigger.nick in ops:
        channel = trigger.sender
        bot.write(["MODE", channel, "+m"])
    else:
        bot.say(u"Ho sento, pero no")
        return

@commands('dm', 'nomoderat')
def dmoderat(bot, trigger):
    """Posa el canal en moderat. Només els administradors."""
    if trigger.nick in ops:
        channel = trigger.sender
        bot.write(["MODE", channel + " -m"])
    else:
        bot.say(u"Ho sento, pero no")
        return

@commands('recover', 'recupera')
def recover(bot, trigger):
    u"""
    Recupera el canal: +o al bot, +im al canal i, si es dona al cas, el ChanServ invita el bot al canal.
    """
    if not trigger.admin:
        return
    if trigger.sender.startswith('#'):
        bot.say('En privat')
        return
    if not trigger.group(2):
        return
    if trigger.admin:
        channel = trigger.group(2)
        bot.msg('ChanServ', 'recover ' + channel)
        bot.join(channel)
        bot.write(['INVITE', trigger.nick + ' ' + channel])
        bot.reply(u"Recuperació completada")
        return
    
@commands('i')
def i(bot, trigger):
    u"""Posa el canal en +i."""
    if trigger.nick in opers:
        channel = trigger.sender
        bot.write(['MODE', channel + ' +i'])
        return
    else:
        return

@commands('-i')
def di(bot, trigger):
    u"""Posa el canal en -i."""
    if trigger.nick in opers:
        channel = trigger.sender
        bot.write(['MODE', channel + ' -i'])
        return
    else:
        return

@commands('invite')
def invite(bot, trigger):
    u"""Convida un usuari al canal."""
    if trigger.nick in opers:
        channel = trigger.sender
        bot.write(['INVITE', trigger.group(2)])
        return
    else:
        return

@commands('ops')
def ops(bot, trigger):
    u"""Retorna la llista d'operadors del bot."""
    bot.say(u"Llista d'operadors (No és el mateix que administradors): " + str(opers))
    return