from my_app import app
from flask import render_template, redirect, url_for, flash, request, session
from my_app.forms import mj_form, mj_players, gang
from my_app.functions import gang_calculations, tai_calculation
from my_app.players import Players, Game
import json


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/players", methods=["GET", "POST"])
def players():
    form = mj_form()
    if form.validate_on_submit():
        player1 = json.dumps(
            Players(name=form.name1.data, buy_in=form.buy_in.data).__dict__
        )
        player2 = json.dumps(
            Players(name=form.name2.data, buy_in=form.buy_in.data).__dict__
        )
        player3 = json.dumps(
            Players(name=form.name3.data, buy_in=form.buy_in.data).__dict__
        )
        player4 = json.dumps(
            Players(name=form.name4.data, buy_in=form.buy_in.data).__dict__
        )
        players = [player1, player2, player3, player4]
        session["players"] = players
        session["game_config"] = json.dumps(
            Game(per_tai=float(form.per_tai.data), shooter=form.shooter.data).__dict__
        )
        session["history"] = ["-------Start game-------"]
        session["old_history"] = ["-------Start game-------"]
        session["old_players"] = players
        session["counter"] = 0
        session["old_counter"] = 0

        flash(
            "Success",
            category="success",
        )
        return redirect(url_for("mahjong"))
    if form.errors != {}:  # if no errors from validations
        temp = []
        res = dict()
        for key, val in form.errors.items():
            if val not in temp:
                temp.append(val)
                res[key] = val
        for err_msg in res.values():
            flash(f"ERROR: {err_msg[0]}", category="danger")
    return render_template("players.html", form=form)


@app.route("/mahjong", methods=["GET", "POST"])
def mahjong():
    players = session.get("players")
    player_list = [json.loads(p, object_hook=Players.decode_object) for p in players]
    game_config = session.get("game_config")
    win = mj_players()
    game = json.loads(game_config, object_hook=Game.decode_object)
    price = game.per_tai
    win_gang = gang()
    update_para = session.get("history")
    counter = session.get("counter")
    revered_para = reversed(update_para)
    if request.method == "POST":
        # undo last move
        if "undo" in request.form:
            old_players = session.get("old_players")
            session["players"] = old_players
            old_history = session.get("old_history")
            session["history"] = old_history
            old_counter = session.get("old_counter")
            session["counter"] = old_counter
            return redirect(url_for("mahjong"))
        # normal win
        if "submit_win" in request.form and win.validate_on_submit():
            winner = request.form.get("winner")
            tais = request.form.get("number_tai")
            zi_mo = request.form.get("zimo")
            total, loser_pay = tai_calculation(tais, price, zi_mo)
            update_players = []
            paragraph = []
            shooter = request.form.get("shooter")
            session["old_players"] = [json.dumps(p.__dict__) for p in player_list]
            session["old_history"] = update_para
            session["old_counter"] = counter
            for p in player_list:
                if p.name == winner:
                    p.win(total)
                elif p.name != winner:
                    if game.shooter:
                        if zi_mo is None:
                            if p.name == shooter:
                                p.lose(total)
                                paragraph.append(
                                    f"{shooter} shoots {total} to {winner} for winning {tais} tais"
                                )

                        else:
                            p.lose(loser_pay)
                            paragraph.append(
                                f"{p.name} pays {loser_pay} to {winner} for winning {tais} tai zimo"
                            )

                    else:
                        if zi_mo is None:
                            if p.name == shooter:
                                p.lose(total / 2)
                                paragraph.append(
                                    f"{shooter} shoots {total/2} to {winner} for winning {tais} tais"
                                )
                            else:
                                p.lose(loser_pay)
                                paragraph.append(
                                    f"{p.name} pays {loser_pay} to {winner} for winning {tais} tais"
                                )
                        else:
                            p.lose(loser_pay)
                            paragraph.append(
                                f"{p.name} pay {loser_pay} to {winner} for winning {tais} tai zimo"
                            )
                update_players.append(json.dumps(p.__dict__))
            session["players"] = update_players
            counter += 1
            session["counter"] = counter
            paragraph.append(f"-------Game {counter}-------")
            update_para = update_para + paragraph
            session["history"] = update_para
        # other types of win
        elif "submit_gang" in request.form and win_gang.validate_on_submit():
            winner = request.form.get("winner_gang")
            am_gang = request.form.get("am_gang")
            total = gang_calculations(price, am_gang)
            update_players = []
            paragraph = []
            session["old_players"] = [json.dumps(p.__dict__) for p in player_list]
            session["old_history"] = update_para
            for p in player_list:
                if p.name == winner:
                    p.win(total)
                else:
                    if (game.shooter) and (am_gang is None):
                        shooter = request.form.get("shooter")
                        if p.name == shooter:
                            p.lose(total)
                            paragraph.append(
                                f"{shooter} shoot {round(total,2)} to {winner} for winning gang"
                            )
                    else:
                        p.lose(total / 3)
                        paragraph.append(
                            f"{p.name} pays {round(total / 3,2)} to {winner} for winning {'am gang' if am_gang else 'gang'}"
                        )
                update_players.append(json.dumps(p.__dict__))
            session["players"] = update_players
            update_para = update_para + paragraph
            session["history"] = update_para
        elif "submit_other" in request.form:
            winner = request.form.get("winner_others")
            radio_choice = request.form.get("radio1")
            update_players = []
            paragraph = []
            session["old_players"] = [json.dumps(p.__dict__) for p in player_list]
            session["old_history"] = update_para
            for p in player_list:
                if radio_choice == "split":
                    to_pay = (
                        0
                        if request.form.get("total_amount") == ""
                        else float(request.form.get("total_amount"))
                    )
                    if p.name == winner:
                        p.win(to_pay * 3)
                    else:
                        p.lose(to_pay)
                        paragraph.append(
                            f"{p.name} pay {to_pay} to {winner} for winning new rule"
                        )
                elif radio_choice == "shoot":
                    to_pay = (
                        0
                        if request.form.get("shooter_amount") == ""
                        else float(request.form.get("shooter_amount"))
                    )
                    shooter = request.form.get("shooter")
                    if p.name == winner:
                        p.win(to_pay)
                    elif p.name == shooter:
                        p.lose(to_pay)
                        paragraph.append(
                            f"{shooter} shoot {to_pay} to {winner} for winning new rule"
                        )
                update_players.append(json.dumps(p.__dict__))
            session["players"] = update_players
            update_para = update_para + paragraph
            session["history"] = update_para
        return redirect(url_for("mahjong"))

    return render_template(
        "mahjong.html",
        game=game,
        win=win,
        player_list=player_list,
        win_gang=win_gang,
        revered_para=revered_para,
    )


@app.route("/endgame")
def endgame():
    players = session.get("players")
    player_list = []
    buy_in_list = []
    losers = []
    for p in players:
        player = json.loads(p, object_hook=Players.decode_object)
        player_list.append(player)
        buy_in_list.append(player.buy_in)
    highest_amount = max(buy_in_list)
    initial_buy_in = sum(buy_in_list) / 4
    for player in player_list:
        if player.buy_in == highest_amount:
            winner = player
            player.buy_in = player.buy_in - initial_buy_in
        else:
            player.buy_in = player.buy_in - initial_buy_in
            losers.append(player)
    return render_template("endgame.html", winner=winner, losers=losers)
