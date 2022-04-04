import dearpygui.dearpygui as dpg
from pathlib import Path
from os import getcwd, path
from config.conf import tags, groups
import pandas as pd
from time import sleep
from threading import Lock, Thread
from os import getcwd, path
from pathlib import Path

CWD = getcwd()
PATH = Path(CWD)

CURRENT_PATH = Path(getcwd())
CSV_FILE = "app/user/portfolio.csv"
CSV_PATH = CURRENT_PATH / CSV_FILE


def add_logo(logo_name: str, width_: int, height_: int, tag: str):
    logo_path = f"img/icons/{logo_name}.png"
    image = str(PATH / logo_path)
    width, height, _channels, data = dpg.load_image(image)
    with dpg.texture_registry(show=False):
        dpg.add_static_texture(width, height, data, tag=tag)
    with dpg.drawlist(width=width_, height=height_):
        dpg.draw_image(tag, [0, 0], [width_, height_])


def generate_img_button(
    tag: int,
    path: str,
    label: str,
    parent: int,
    group: str,
    callback,
    size=[30, 30],
    show=True,
) -> None:
    """Agrega una imagen a un botón"""
    tags["heatmap"]["btnstage"][str(label)] = dpg.generate_uuid()
    current_path = Path(getcwd())
    image = f"img/icons/{path}.png"
    img_path = current_path / image
    width, height, _channels, data = dpg.load_image(str(img_path))
    with dpg.texture_registry():
        image = dpg.add_static_texture(width, height, data, tag=tag)
    with dpg.stage(tag=tags["heatmap"]["btnstage"][str(label)]):
        dpg.add_image_button(
            texture_tag=image,
            tag=tag,
            label=label,
            show=show,
            width=size[0],
            height=size[1],
            parent=parent,
            user_data=parent,
            callback=lambda: callback(group),
        )

    dpg.push_container_stack(parent)
    dpg.unstage(tags["heatmap"]["btnstage"][str(label)])
    dpg.pop_container_stack()


def calendar_button(
    tag: int,
    path: str,
    label: str,
    parent: int,
    callback,
    size=[30, 30],
) -> None:
    """Agrega una imagen a un botón"""
    current_path = Path(getcwd())
    image = f"img/icons/{path}.png"
    img_path = current_path / image
    width, height, _channels, data = dpg.load_image(str(img_path))
    texture_tag = dpg.generate_uuid()
    with dpg.texture_registry():
        image = dpg.add_static_texture(width, height, data, tag=texture_tag)
        dpg.add_image_button(
            texture_tag=image,
            tag=tag,
            label=label,
            width=size[0],
            height=size[1],
            parent=parent,
            user_data=parent,
            callback=callback,
        )


def reload_table():
    group = tags["miscellaneous"]["activegroup"]
    if tags["miscellaneous"]["state"]:
        show = f"{group}_"
        block = f"{group}__"
    else:
        show = f"{group}__"
        block = f"{group}_"

    dpg.configure_item(item=tags["heatmap"][show], show=True)
    dpg.configure_item(item=tags["heatmap"][block], show=False)


def change_state(sender, app_data, user_data):
    tags["miscellaneous"]["state"] = not tags["miscellaneous"]["state"]
    if tags["miscellaneous"]["state"]:
        path = "today"
    else:
        path = "month"
    dpg.delete_item(item=sender)
    new_tag = dpg.generate_uuid()
    calendar_button(
        tag=new_tag, path=path, label=path, parent=user_data, callback=change_state
    )
    if (
        tags["miscellaneous"]["activegroup"] in groups
        and not tags["miscellaneous"]["updatestate"]
    ):
        reload_table()


def show_update_window():
    dpg.configure_item(item=tags["miscellaneous"]["updating"], show=True)
    for group_ in groups:
        dpg.configure_item(item=tags["heatmap"][f"{group_}_"], show=False)
        dpg.configure_item(item=tags["heatmap"][f"{group_}__"], show=False)
    dpg.configure_item(item=tags["heatmap"]["principalgroup_"], show=False)
    dpg.configure_item(item=tags["heatmap"]["portfoliogroup_"], show=False)


def shift_the_group(group: str):
    try:
        dpg.delete_item(item=tags["main"]["search"])
        tags["main"]["search"] = 0
    except Exception as _:
        pass

    tags["miscellaneous"]["activegroup"] = group

    if tags["miscellaneous"]["updatestate"]:
        show_update_window()
    else:
        if tags["miscellaneous"]["state"]:
            trend = f"{group}_"
            other = f"{group}__"
        else:
            trend = f"{group}__"
            other = f"{group}_"

        for group_ in groups:
            if group == group_:
                dpg.configure_item(item=tags["heatmap"][trend], show=True)
                dpg.configure_item(item=tags["heatmap"][other], show=False)
            else:
                dpg.configure_item(item=tags["heatmap"][f"{group_}_"], show=False)
                dpg.configure_item(item=tags["heatmap"][f"{group_}__"], show=False)

        dpg.configure_item(item=tags["heatmap"]["principalgroup_"], show=False)
        dpg.configure_item(item=tags["heatmap"]["portfoliogroup_"], show=False)


def shift_other(group: str):
    # print(group)
    if group != "portfoliogroup":
        try:
            dpg.delete_item(item=tags["main"]["search"])
            tags["main"]["search"] = 0
        except Exception as _:
            pass
    tags["miscellaneous"]["activegroup"] = group
    if group == "principalgroup":
        other = "portfoliogroup_"
    else:
        other = "principalgroup_"

    dpg.configure_item(item=tags["heatmap"][f"{group}_"], show=True)
    dpg.configure_item(item=tags["heatmap"][other], show=False)

    for group_ in groups:
        dpg.configure_item(item=tags["heatmap"][f"{group_}_"], show=False)
        dpg.configure_item(item=tags["heatmap"][f"{group_}__"], show=False)


def show_portfolio(group=None):
    shift_other("portfoliogroup")
    if not tags["main"]["search"]:
        tags["main"]["search"] = dpg.generate_uuid()
        calendar_button(
            tag=tags["main"]["search"],
            path="search",
            label="search",
            parent=tags["main"]["searchcontainer"],
            callback=lambda: search_tab(on_selection)
            if not tags["miscellaneous"]["updatestate"]
            else None,
            size=[28, 28],
        )


def draw_table(staged_item, group, filter: bool):
    from THEME import table

    if filter:
        trend = f"{group}_"
        table_group = group
    else:
        trend = f"{group}__"
        table_group = f"{group}-"
    dpg.push_container_stack(tags["heatmap"][trend])
    dpg.unstage(staged_item)
    dpg.pop_container_stack()
    dpg.bind_item_theme(
        item=tags["heatmap"][table_group]["table"],
        theme=table,
    )
    return tags["heatmap"][table_group]["table"]


def add_to_portfolio(sender, app_data, user_data):
    cusip = user_data[0]
    try:
        csvFile = pd.read_csv(CSV_PATH, header=None)
        portfolio = [stock[0] for stock in csvFile.values.tolist()]
        if cusip not in portfolio:
            df = pd.DataFrame(data=user_data)
            df.to_csv(CSV_PATH, mode="a", index=False, header=False)
    except Exception as _:
        df = pd.DataFrame(data=user_data)
        df.to_csv(CSV_PATH, mode="a", index=False, header=False)


def delete_in_portfolio(sender, app_data, user_data):
    cusip = user_data[0]
    try:
        csvFile = pd.read_csv(CSV_PATH, header=None)
        portfolio = [stock[0] for stock in csvFile.values.tolist()]
        if cusip in portfolio:
            for i, _ in enumerate(portfolio):
                if _ == cusip:
                    portfolio_ = {"cusip": portfolio}
                    df = pd.DataFrame(portfolio_)
                    new_portfolio = df.drop(i)
                    new_portfolio.to_csv(CSV_PATH, index=False, header=False)
                    break
    except Exception as _:
        pass


def load_portfolio():
    from app.heatmap import create_table_

    portfolio = []
    db_data = get_analysis()
    try:
        csvFile = pd.read_csv(CSV_PATH)
        for stock in csvFile.values.tolist():
            for data in db_data:
                if data["id_instrument"] == str(stock[0]):
                    portfolio.append(data)
                    break
        group = "portfoliogroup"
        staged = create_table_(portfolio, group, True)
        table = draw_table(staged, group, True)
        dpg.configure_item(item=table, show=True)
    except Exception as _:
        pass


def get_analysis():
    lock = Lock()
    with lock:
        if tags["miscellaneous"]["state"]:
            return tags["heatmap"]["db_content_daily"]
        else:
            return tags["heatmap"]["db_content_monthly"]


def pandaraizer(filter):
    if filter == True:
        return pd.DataFrame(tags["heatmap"]["db_content_daily"])
    elif filter == False:
        return pd.DataFrame(tags["heatmap"]["db_content_monthly"])
    else:
        return pd.DataFrame(get_analysis())


class Trend:
    def __init__(self, group, sign, key):
        self.group = group
        self.operator_precedence = sign
        self.key = key

    def set_operation(self, filter):
        """Operación que retorna un parámetro para escoger los valores de la lista de tendencia"""
        pass

    def generate_table(self, filter: bool):
        """Retorna la lista de tendencia"""

        from app.heatmap import create_table_

        if filter:
            db_content = tags["heatmap"]["db_content_daily"]
        else:
            db_content = tags["heatmap"]["db_content_monthly"]
        data_list = list()
        quantile = self.set_operation(filter)
        for content in db_content:
            if self.operator_precedence:
                if content[self.key] >= quantile:
                    data_list.append(content)
            else:
                if content[self.key] <= quantile:
                    data_list.append(content)
        staged = create_table_(data_list, self.group, filter)
        table = draw_table(staged, self.group, filter)
        dpg.configure_item(item=table, show=True)


class Gainer(Trend):
    def __init__(self, group):
        sign = True
        key = "calculation"
        super().__init__(group, sign, key)

    def set_operation(self, filter):
        return pandaraizer(filter).get("calculation").quantile(0.75)


class Loser(Trend):
    def __init__(self, group):
        sign = False
        key = "calculation"
        super().__init__(group, sign, key)

    def set_operation(self, filter):
        return pandaraizer(filter).get("calculation").quantile(0.10)


class Trending(Trend):
    def __init__(self, group):
        sign = True
        key = "count_analysis"
        super().__init__(group, sign, key)

    def set_operation(self, filter):
        return pandaraizer(filter).get("count_analysis").quantile(0.90)


class TrendFactory:
    def __init__(self, group):
        self.group = group

    def get_class(self):
        if self.group == "trendgrouptable":
            return Trending(self.group)
        elif self.group == "losergrouptable":
            return Loser(self.group)
        elif self.group == "topgrouptable":
            return Gainer(self.group)
        else:
            pass


def search_tab(selection_callback):
    """Ventana flotante de búsqueda"""
    from THEME import search_window
    from FONTS import childs_font

    try:
        tags["miscellaneous"]["portfolioweight"] = len(pd.read_csv(CSV_PATH))
    except Exception as _:
        tags["miscellaneous"]["portfolioweight"] = 0
    with dpg.mutex():
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

        with dpg.window(
            label="", modal=True, no_close=True, no_title_bar=True
        ) as modal_id:
            table_id = dpg.generate_uuid()
            db_content = tags["heatmap"]["db_content_search"]
            filter_tag = dpg.generate_uuid()
            dpg.add_input_text(
                hint="Escribe una acción",
                user_data=filter_tag,
                callback=lambda s, a, u: dpg.set_value(u, dpg.get_value(s)),
            )
            with dpg.table(
                header_row=True,
                no_host_extendX=True,
                delay_search=True,
                borders_innerH=True,
                borders_outerH=True,
                borders_innerV=True,
                borders_outerV=True,
                context_menu_in_body=True,
                row_background=True,
                policy=dpg.mvTable_SizingFixedFit,
                height=300,
                scrollY=True,
                tag=filter_tag,
            ):

                dpg.add_table_column(label="SÍMBOLO")
                dpg.add_table_column(label="NOMBRE")
                dpg.add_table_column(label="DESCRIPCIÓN")
                dpg.add_table_column(label="AGREGAR")
                dpg.add_table_column(label="QUITAR")

                for stock in db_content:
                    try:
                        with dpg.table_row(
                            filter_key=f"{stock['symbol']}{stock['name']}"
                        ):
                            dpg.add_text(f"{stock['symbol']}")
                            dpg.add_text(f"{stock['name']}")
                            dpg.add_text(f"{stock['description']}")
                            dpg.add_button(
                                label="+",
                                user_data=([f"{stock['id_instrument']}"]),
                                callback=add_to_portfolio,
                                small=True,
                            )
                            dpg.add_button(
                                label="-",
                                user_data=([f"{stock['id_instrument']}"]),
                                callback=delete_in_portfolio,
                                small=True,
                            )
                    except Exception as _:
                        dpg.delete_item(modal_id)

            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Cerrar",
                    width=75,
                    user_data=modal_id,
                    callback=selection_callback,
                )

            dpg.bind_item_theme(
                item=modal_id,
                theme=search_window,
            )
            dpg.bind_item_font(modal_id, childs_font)

    dpg.split_frame()
    width = dpg.get_item_width(modal_id)
    height = dpg.get_item_height(modal_id)
    dpg.set_item_pos(
        modal_id, [viewport_width // 2 - width // 2, viewport_height // 2 - height // 2]
    )


def on_selection(sender, unused, user_data):
    """Método para cerrar ventanas flotantes"""
    dpg.delete_item(user_data)
    try:
        if tags["miscellaneous"]["portfolioweight"] != len(pd.read_csv(CSV_PATH)):
            thread = Thread(
                target=load_portfolio,
            )
            thread.start()
    except Exception as _:
        pass


def floating_window(window: int, Title: str):
    if dpg.does_item_exist(window):
        primary_width = dpg.get_viewport_width()
        primary_height = dpg.get_viewport_height()
        secondary_width = dpg.get_item_width(window)
        secondary_height = dpg.get_item_height(window)
        dpg.set_item_pos(
            window,
            [
                int((primary_width / 2 - secondary_width / 2)),
                int((primary_height / 2 - secondary_height / 2)),
            ],
        )
        dpg.set_viewport_title(Title)
