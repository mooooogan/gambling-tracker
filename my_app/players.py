class Players(object):
    def __init__(self, name, buy_in):
        self.name = name
        self.buy_in = buy_in

    def __repr__(self):
        return f"Items {self.name}"

    @staticmethod
    def decode_object(o):
        return Players(o["name"], o["buy_in"])

    def win(self, amount):
        self.buy_in = self.buy_in + amount
        return self.buy_in

    def lose(self, amount):
        self.buy_in = self.buy_in - amount
        return self.buy_in

    @property
    def rounded(self):
        return "$" + str(round(self.buy_in, 2))

    @property
    def abs_buyin(self):
        return "$" + str(abs(self.buy_in))


class Game(object):
    def __init__(self, per_tai, shooter):
        self.per_tai = per_tai
        self.shooter = shooter

    @staticmethod
    def decode_object(o):
        return Game(o["per_tai"], o["shooter"])

    @property
    def pretty_shooter(self):
        if self.shooter:
            return "On"
        else:
            return "Off"
