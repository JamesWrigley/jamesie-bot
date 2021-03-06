import pyrc
import pywapi
import pyrc.utils.hooks as hooks

things_dict = {}
weather_locations_dict = {}

class Plaznar(pyrc.Bot):
    @hooks.privmsg("^.tell+\s(?P<recipient>.+)\s+(?P<msg>.+)$")
    def tell(self, target, sender, **kwargs):
        user_messages = {}

        self.message(target, "{0}: Ok, I'll tell {1} that next time I see them.".format(sender, kwargs["recipient"]))
        user_messages[kwargs["recipient"]] = kwargs["msg"]
        self.message(target, "{0}: {1} says \"{2}\"".format(kwargs["recipient"], sender, user_messages[kwargs["recipient"]]))


    @hooks.privmsg("^.let\s+(?P<thing>.+)\s+be\s+(?P<value>.+)$")
    def add_to_library(self, target, sender, **kwargs):        
        things_dict[kwargs["thing"]] = kwargs["value"]
        self.message(target, "{0}: Added to dictionary".format(sender))
        for i,v in things_dict.items(): print(i + " is " + v)

    @hooks.privmsg("^.weather\s+(?P<location>.+)$")
    def get_weather(self, target, sender, **kwargs):
        if kwargs["location"] in weather_locations_dict:
            current_weather = pywapi.get_weather_from_weather_com(weather_locations_dict[kwargs["location"]])
            self.message(target, "Current weather in {0} is {1} and it's {2}°C.".format(kwargs["location"], 
                                                                current_weather['current_conditions']['text'],
                                                                current_weather['current_conditions']['temperature']))
        else:
            self.message(target, "Location not found, run '.loc CITYname', then add the location ID with '.aloc CITYname is LocID' and rerun.")


    @hooks.privmsg("^.loc\s+(?P<search_term>.+)$")
    def search_for_location(self, target, sender, **kwargs):
        if kwargs["search_term"] not in weather_locations_dict:
            self.message(target, pywapi.get_location_ids(kwargs["search_term"]))
        else:
            self.message(target, "{0} already in the weather dictionary.".format(kwargs["search_term"]))
        

    @hooks.privmsg(".aloc\s+(?P<location>.+)\s+is\s+(?P<location_id>.+)$")
    def add_location(self, target, sender, **kwargs):
        if kwargs["location"] not in weather_locations_dict:
            weather_locations_dict[kwargs["location"]] = kwargs["location_id"]
            self.message(target, "Location \"{0}\" added.".format(kwargs["location"]))
        else:
            self.message(target, "Location \"{0}\" already added.".format(kwargs["location"]))

        print(weather_locations_dict)


    @hooks.privmsg("^.wutis\s+(?P<thing>.+)$")
    def wutis(self, target, sender, **kwargs):
        if kwargs["thing"] in things_dict:
            self.message(target, kwargs["thing"] + " is " + things_dict[kwargs["thing"]])
        else:
            self.message(target, "{0}: Item not found".format(sender))


    @hooks.privmsg("^.repeat\s+(?P<msg>.+)$")
    def repeat(self, target, sender, **kwargs):
        if target.startswith("#"):
            self.message(target, kwargs["msg"])
        else:
            self.message(sender, kwargs["msg"])

    @hooks.privmsg("^.five\s+(?P<person>.+)$")
    def highfive(self, target, sender, **kwargs):
        if target.startswith("#"):
            if kwargs["person"] == "Plaznar":
                self.message(target, "\u0001ACTION high-fives himself\u0001")
            else:
                self.message(target, "\u0001ACTION high-fives {0}\u0001".format(kwargs["person"]))

    @hooks.privmsg("^.slap\s+(?P<person>.+)$")
    def slap(self, target, sender, **kwargs):
        if target.startswith("#"):
            if kwargs["person"] == "Plaznar":
                self.message(target, "\u0001ACTION pats himself on the back\u0001")
            else:
                self.message(target, "\u0001ACTION slaps {0} upside the haid\u0001".format(kwargs["person"]))


    @hooks.privmsg("^.tickle\s+(?P<person>.+)$")
    def tickle(self, target, sender, **kwargs):
        if target.startswith("#"):
            if kwargs["person"] == "Plaznar":
                self.message(target, "\u0001ACTION is too mature to tickle himself\u0001")
            else:
                self.message(target, "\u0001ACTION tickles {0}, who giggles like a schoolgirl\u0001".format(kwargs["person"]))

    @hooks.privmsg("^.applaud\s+(?P<person>.+)$")
    def applaud(self, target, sender, **kwargs):
        if target.startswith("#"):
            if kwargs["person"] == "Plaznar":
                self.message(target, "\u0001ACTION gives himself a medal\u0001")
            else:
                self.message(target, "\u0001ACTION slow claps for {0}\u0001".format(kwargs["person"]))


    @hooks.privmsg("^.moar+\s(?P<thing>.+)\s+(?P<person>.+)$")
    def moar(self, target, sender, **kwargs):
        if target.startswith("#"):
            self.message(target, "\u0001ACTION inundates {0} with {1}\u0001".format(kwargs["person"], kwargs["thing"]))


    @hooks.privmsg("(^.fail|^.lamb|^.help|^.success|^.laugh|^.bugz|^.rejoice|^.ram)")
    def runCommand(self, target, sender, *args):
        commands = [".tell", ".fail", ".repeat", ".lamb", ".help", ".laugh", ".success", ".let", ".wutis", ".aloc", ".loc", ".weather", ".bugz", ".tickle", ".applaud", ".slap", ".ram"]

        if target.startswith("#"):
            if args[0] == ".fail":
                self.message(target, "Abject, miserable, despondent, failure.")
            elif args[0] == ".bugz":
                self.message(target, "Bugs. Bugs everywhere. In your code, between your deps, and under your bed O_O")
            elif args[0] == ".lamb":
                self.message(target, "\u0002LAAAYUUMBB\u0002")
            elif args[0] == ".laugh":
                self.message(target, "BAAAAHAHAHAHAH HaHAHAA HA HA HHHHA AH *snort* HA HHA HAHAHA HA HAH HAH HAH HAHAH HAH HAH oh man HAH AH HAAAAAHAAAHHH *cough* *cough* *cough* hah hehhh hehhhhh geez.. *cough*")
            elif args[0] == ".help":
                self.message(target, "{0}: I am a weird chap. Current commands are {1}.".format(sender, ", ".join(commands)))
            elif args[0] == ".success":
                self.message(target, "ZOMG HALLELUJAH IM A GENIUS")
            elif args[0] == ".ram":
                self.message(target, "\u0002RAHHHHUUUUUUUM!!\u0002")
            elif args[0] == ".rejoice":
                self.message(target, "Hell yeah!")
            else:
                self.message(target, "Unrecognised command")



if __name__ == '__main__':
    bot = Plaznar("irc.freenode.net", channels = ["#jamesie", "#coursera-androidapps"])
    bot.connect()
