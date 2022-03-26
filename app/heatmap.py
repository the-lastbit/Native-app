import dearpygui.dearpygui as dpg
from os import getcwd, path
from pathlib import Path
from API import obtain_range_data, get_sentiment_analysis
from threading import Thread, Event
from config.conf import tags, groups
import asyncio
from PIL import Image, ImageDraw, ImageFont
from time import sleep
from threading import Lock
from app.miscellaneous import shift_the_group, show_update_window, TrendFactory, shift_other


class HeatMap:
    def update(self):
        from app.miscellaneous import get_analysis

        try:
            db_content = get_analysis()
            groups = [
                "portfoliogroup",
                "principalgroup",
            ]
            for group in groups:
                if content_in_group := tags["heatmap"][group]:
                    for content in db_content:
                        if symbol_in_group := tags["heatmap"][group]["textures"].get(
                            content["symbol"]
                        ):
                            dpg.configure_item(
                                item=tags["heatmap"][group]["textures"][
                                    content["symbol"]
                                ][1],
                                tint_color=tint(content["calculation"]),
                            )

        except Exception as _:
            pass


class UpdateHeatmap:
    def __init__(self):
        self.up = True
        self.heatmap = HeatMap()

    def terminate(self):
        self.up = False

    def run(
        self,
    ):
        # from app.miscellaneous import TrendFactory

        while self.up:
            self.heatmap.update()
            if tags["heatmap"]["counter"] > 300:
                tags["heatmap"]["counter"] = 0
                load_monthly_analysis()
                load_daily_analysis
            elif tags["miscellaneous"]["counter"] > 6000:
                tags["miscellaneous"]["updatestate"] = True
                tags["miscellaneous"]["counter"] = 0

                if tags["miscellaneous"]["activegroup"] in groups:
                    shift_the_group(tags["miscellaneous"]["activegroup"])
                else:
                    shift_other(tags["miscellaneous"]["activegroup"])

                for group in groups:
                    trend = TrendFactory(group)
                    function = trend.get_class()
                    function.generate_table(filter=True)

                    trend = TrendFactory(group)
                    function = trend.get_class()
                    function.generate_table(filter=False)

                tags["miscellaneous"]["updatestate"] = False
                dpg.configure_item(item=tags["miscellaneous"]["updating"], show=False)
                if tags["miscellaneous"]["activegroup"] in groups:
                    shift_the_group(tags["miscellaneous"]["activegroup"])
                else:
                    shift_other(tags["miscellaneous"]["activegroup"])

            else:
                tags["heatmap"]["counter"] += 1
                tags["miscellaneous"]["counter"] += 1
                sleep(0.1)


class ImageTicker_:
    """Genera una imagen de cada simbolo representante de un valor bursatil
    con un color que representa el valor sentimental"""

    def __init__(
        self,
        company: str,
        ticker: str,
        sector: str,
        analysis=None,
        plot_id=None,
        group=str,
    ):
        self.company = company
        self.ticker_symbol = ticker
        self.ticker_path = f"img/tmp/{ticker}.png"
        self.sector = sector
        self.content_path = Path(getcwd())
        self.analysis = analysis
        self.group = group

        tags["heatmap"][self.group]["textures"][self.ticker_symbol] = [
            dpg.generate_uuid(),
            dpg.generate_uuid(),
            dpg.generate_uuid(),
        ]
        self.plot = plot_id

    def generate_image_ticker(self):
        """Produce un lienzo para dibujar el nombre de un símbilo"""
        if path.exists(self.content_path / self.ticker_path):
            return None
        font_width = len(self.ticker_symbol) * 16
        image = Image.open(self.content_path / "img/white.png")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(
            str(self.content_path / "FONTS/DosisBook-ZZm3.ttf"), 60
        )
        draw.text((100 - font_width, 60), self.ticker_symbol, font=font, fill=(0, 0, 0))
        image.save(self.content_path / self.ticker_path)

    def generate_static_texture(self):
        """Genera una textura para posteriormente compartir en una tabla gráfica"""
        image = str(self.content_path / self.ticker_path)
        width, height, _channels, data = dpg.load_image(image)
        with dpg.texture_registry(show=False):
            dpg.add_static_texture(
                width,
                height,
                data,
                tag=tags["heatmap"][self.group]["textures"][self.ticker_symbol][0],
            )

    def ticker_dispatcher(self):
        """Método que reúne la textura y el color del análisis sentimental para agragarlo a una tablas gráfica"""
        self.generate_image_ticker()
        self.generate_static_texture()

        origin = [0, 0]
        end = [1, 1]
        dpg.add_image_series(
            texture_tag=tags["heatmap"][self.group]["textures"][self.ticker_symbol][0],
            bounds_min=origin,
            bounds_max=end,
            tag=tags["heatmap"][self.group]["textures"][self.ticker_symbol][1],
            parent=self.plot,
            tint_color=tint(self.analysis),
        )
        with dpg.tooltip(
            parent=dpg.last_item(),
            tag=tags["heatmap"][self.group]["textures"][self.ticker_symbol][2],
        ):
            dpg.add_text(self.ticker_symbol)
            dpg.add_text(self.company)
            dpg.add_text(self.sector)
            # dpg.set_item_theme(
            #     item=config.items_id["textures"][self.ticker_path][2],
            #     theme=config.items_id["registries"]["symbol_tooltip"],
            # )


def request_data(month=None, year=None):
    # use pendulum to generate a date
    return asyncio.run(obtain_range_data(data, symbol))


def create_chart(sender, app_data, user_data):
    tags["heatmap"][group]["stagedchart"] = dpg.generate_uuid()
    staged = tags["heatmap"][group]["stagedchart"]
    with dpg.stage(tag=staged):
        with dpg.child_window(tag=tags["heatmap"]["chart"]):
            with dpg.group(parent=tags["heatmap"]["chart"], horizontal=True) as group:
                dpg.add_text(value="Fecha")
                month = dpg.add_input_text(hint="Mes")
                year = dpg.add_input_text(hint="Año")
                dpg.add_button(label="Mostrar", callback=None)


def create_table_(data, group, filter: bool):
    if filter:
        trend = f"{group}_"
        table_group = group
    else:
        trend = f"{group}__"
        table_group = f"{group}-"

    dpg.delete_item(item=tags["heatmap"][trend], children_only=True)
    staged = tags["heatmap"][table_group]["staged"]
    tags["heatmap"][table_group]["table"] = dpg.generate_uuid()
    table = tags["heatmap"][table_group]["table"]
    with dpg.stage(tag=staged):
        dpg.add_table(
            tag=table,
            show=False,
            parent=tags["heatmap"][trend],
            header_row=False,
            row_background=False,
            borders_innerH=False,
            borders_outerH=False,
            borders_innerV=False,
            borders_outerV=False,
            resizable=False,
            scrollX=True,
            scrollY=True,
            no_host_extendX=True,
            policy=dpg.mvTable_SizingFixedFit,
            pad_outerX=False,
        )
        len_data = len(data)
        rows = 25
        for i in range(rows):
            tags["heatmap"][table_group]["rows"][str(i)] = dpg.generate_uuid()
        for stock in data:
            tags["heatmap"][table_group]["portfolio"][stock["id_instrument"]] = [
                dpg.generate_uuid(),
                dpg.generate_uuid(),
            ]
        for column in range(21):
            dpg.add_table_column(parent=table)
        tags["miscellaneous"]["count"] = 0
        tags["miscellaneous"]["stop"] = 21
        tags["miscellaneous"]["start"] = 0

        width = tags["heatmap"]["width"]
        height = tags["heatmap"]["height"]
        for i in range(rows):
            dpg.add_table_row(
                tag=tags["heatmap"][table_group]["rows"][str(i)],
                parent=table,
            )
            for stock in data[
                tags["miscellaneous"]["start"] : tags["miscellaneous"]["stop"]
            ]:
                if tags["miscellaneous"]["count"] < len_data:
                    dpg.add_plot(
                        no_menus=True,
                        no_title=True,
                        no_box_select=True,
                        no_mouse_pos=True,
                        width=width,
                        height=height,
                        equal_aspects=True,
                        tag=tags["heatmap"][table_group]["portfolio"][
                            stock["id_instrument"]
                        ][0],
                        parent=tags["heatmap"][table_group]["rows"][str(i)],
                    )
                    default_x = dpg.add_plot_axis(
                        label="",
                        axis=0,
                        no_gridlines=False,
                        no_tick_marks=True,
                        no_tick_labels=True,
                        lock_min=True,
                        parent=tags["heatmap"][table_group]["portfolio"][
                            stock["id_instrument"]
                        ][0],
                    )
                    dpg.add_plot_axis(
                        label="",
                        tag=tags["heatmap"][table_group]["portfolio"][
                            stock["id_instrument"]
                        ][1],
                        axis=1,
                        no_gridlines=False,
                        no_tick_marks=True,
                        no_tick_labels=True,
                        lock_min=True,
                        parent=tags["heatmap"][table_group]["portfolio"][
                            stock["id_instrument"]
                        ][0],
                    )
                    dpg.set_axis_limits(axis=default_x, ymin=0, ymax=1)
                    dpg.set_axis_limits(
                        axis=tags["heatmap"][table_group]["portfolio"][
                            stock["id_instrument"]
                        ][1],
                        ymin=0,
                        ymax=1,
                    )
                    dpg.add_vline_series(x=[0], parent=default_x)
                    dpg.add_hline_series(
                        x=[0],
                        parent=tags["heatmap"][table_group]["portfolio"][
                            stock["id_instrument"]
                        ][1],
                    )
                    # if group == "portfoliogroup":
                        # some tooltip
                                               
                    img_ticker = ImageTicker_(
                        company=stock["name"],
                        ticker=stock["symbol"],
                        sector=stock["description"],
                        analysis=stock["calculation"],
                        plot_id=tags["heatmap"][table_group]["portfolio"][
                            stock["id_instrument"]
                        ][1],
                        group=table_group,
                    )
                    img_ticker.ticker_dispatcher()
                    tags["miscellaneous"]["count"] += 1
                else:
                    break
            tags["miscellaneous"]["start"] = tags["miscellaneous"]["stop"]
            tags["miscellaneous"]["stop"] += 21

    return staged


def obtain_data(content: str):
    function = get_sentiment_analysis
    return asyncio.run(function(content))


def load_monthly_analysis():
    db_content = obtain_data(content="market_sentiment_monthly")
    lock = Lock()
    with lock:
        tags["heatmap"]["db_content_monthly"] = db_content


def load_daily_analysis():
    db_content = obtain_data(content="market_sentiment_daily")
    lock = Lock()
    with lock:
        tags["heatmap"]["db_content_daily"] = db_content


def deploy_main_content():
    from app.miscellaneous import (
        draw_table,
        TrendFactory,
        load_portfolio,
    )

    load_daily_analysis()
    load_monthly_analysis()
    tags["heatmap"]["db_content_search"] = tags["heatmap"]["db_content_daily"]
    staged = create_table_(tags["heatmap"]["db_content_daily"], "principalgroup", True)
    table = draw_table(staged, "principalgroup", True)
    dpg.configure_item(item=table, show=True)
    load_portfolio()

    # Builder
    for group in groups:
        # daily
        daily_trend = TrendFactory(group)
        daily_function = daily_trend.get_class()
        daily_function.generate_table(filter=True)
        # monthly
        monthly_trend = TrendFactory(group)
        monthly_function = monthly_trend.get_class()
        monthly_function.generate_table(filter=False)

    dpg.delete_item(item=tags["main"]["loadingscreen"])
    dpg.show_item(item=tags["main"]["heatview"])
    dpg.set_viewport_title("HeatView")
    dpg.set_primary_window(window=tags["main"]["heatview"], value=True)

    global thread, update
    update = UpdateHeatmap()
    thread = Thread(target=update.run)
    thread.start()



def tint(analysis):
    """Método que genera un color producto del valor sentimental para
    posteriormente agragarse a la textura"""
    color = analysis
    if color == None:
        new_color = config.None_color
    elif color > 0.49:
        scale = color * 255
        new_color = [0, scale, 0, 255]
    else:
        scale = color * 255
        new_color = [scale, 0, 0, 255]
    return new_color
