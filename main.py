import dearpygui.dearpygui as dpg
from app.login import try_login
from config.conf import tags, groups
from app.miscellaneous import (
    generate_img_button,
    change_state,
    calendar_button,
    show_portfolio,
    shift_the_group,
    shift_other,
    floating_window,
    add_logo,
    display_popup
)


dpg.create_context()


with dpg.window(
    label="Bienvenido",
    tag=tags["main"]["welcomescreen"],
    height=250,
    width=350,
    no_resize=True,
    no_title_bar=True,
    no_close=True,
    no_scrollbar=True,
    no_move=True,
) as welcome_screen:
    from FONTS import default
    with dpg.group():
        add_logo("rosbelogo",width_=350,height_=150,tag="rosbelogo")
        dpg.add_text(
            default_value="                   ",
            tag=tags["main"]["welcometext"],
        )
        with dpg.group(tag=tags["main"]["group"], horizontal=True):
            dpg.add_input_text(
                default_value="http://127.0.0.1:8765/",
                readonly=True,
                tag=tags["main"]["webpage"],
                show=False,
                width=160,
            )
            dpg.add_button(
                label="Entrar", callback=try_login, tag=tags["main"]["welcomebutton"]
            )
            dpg.bind_item_font(tags["main"]["welcomebutton"], default)

with dpg.window(
    tag=tags["main"]["loadingscreen"],
    show=False,
    height=305,
    width=305,
    no_resize=True,
    no_title_bar=True,
    no_close=True,
    no_scrollbar=True,
    no_move=True,
):
    from THEME import child
    with dpg.group(horizontal=True):
        dpg.add_child_window(width=30,tag="spacer")
        dpg.add_loading_indicator(style=1, radius=20, thickness=0.5, color=[250, 0, 0])

    dpg.bind_item_theme(
    item="spacer",
    theme=child,
    )

with dpg.window(
    label="HeatView",
    tag=tags["main"]["heatview"],
    show=False,
    no_title_bar=True,
    no_scrollbar=True,
    menubar=False,
    no_collapse=True,
    no_move=False,
    autosize=True,
    horizontal_scrollbar=False,
) as HeatView:

    with dpg.group(
        tag=tags["main"]["header"],
        horizontal=True,
        parent=tags["main"]["heatview"],
    ):
        add_logo("rosbe",width_=43.3,height_=52,tag="rosbe")
        dpg.add_child_window(width=(550), height=1, tag="horizontal_space")
        calendar_button(
            tag=tags["main"]["calendar"],
            path="today",
            label="today",
            parent=tags["main"]["header"],
            callback=change_state,
        )

        
    with dpg.group(
        tag=tags["heatmap"]["group"],
        horizontal=True,
        parent=tags["main"]["heatview"],
    ):

        with dpg.group(
            tag=tags["heatmap"]["buttongroup"], parent=tags["heatmap"]["group"]
        ):
            from THEME import in_principal_child
            with dpg.child_window(width=40, height=35, tag=tags["main"]["searchcontainer"]):
                pass
            generate_img_button(
                tag=tags["main"]["restore"],
                path="restore",
                label="restore",
                parent=tags["heatmap"]["buttongroup"],
                group="principalgroup",
                callback=shift_other,
            )
            generate_img_button(
                tag=tags["main"]["gainer"],
                path="gainer",
                label="gainer",
                parent=tags["heatmap"]["buttongroup"],
                group="topgrouptable",
                callback=shift_the_group,
            )
            generate_img_button(
                tag=tags["main"]["loser"],
                path="loser",
                label="loser",
                parent=tags["heatmap"]["buttongroup"],
                group="losergrouptable",
                callback=shift_the_group,
            )
            generate_img_button(
                tag=tags["main"]["trendup"],
                path="trendup",
                label="trending",
                parent=tags["heatmap"]["buttongroup"],
                group="trendgrouptable",
                callback=shift_the_group,
            )
            generate_img_button(
                tag=tags["main"]["personal"],
                path="personal",
                label="personal",
                parent=tags["heatmap"]["buttongroup"],
                group=None,
                callback=show_portfolio,
            )
            dpg.add_child_window(
                width=10, height=350,tag="spacer_", parent=tags["heatmap"]["buttongroup"]
            )
            generate_img_button(
                tag=tags["main"]["settings"],
                path="info",
                label="info",
                parent=tags["heatmap"]["buttongroup"],
                group=None,
                callback=display_popup,
            )

        dpg.add_child_window(
            tag=tags["heatmap"]["principalgroup_"],
            parent=tags["heatmap"]["group"],
            no_scrollbar=False,
            horizontal_scrollbar=False,
            show=True,
        )
        dpg.add_child_window(
            tag=tags["heatmap"]["portfoliogroup_"],
            parent=tags["heatmap"]["group"],
            no_scrollbar=False,
            horizontal_scrollbar=False,
            show=False,
        )
        for group in groups:
            dpg.add_child_window(
                tag=tags["heatmap"][f"{group}_"],
                parent=tags["heatmap"]["group"],
                no_scrollbar=False,
                horizontal_scrollbar=False,
                show=False,
            )
            dpg.add_child_window(
                tag=tags["heatmap"][f"{group}__"],
                parent=tags["heatmap"]["group"],
                no_scrollbar=False,
                horizontal_scrollbar=False,
                show=False,
            )
            dpg.bind_item_theme(
            item=tags["heatmap"][f"{group}_"],
            theme=in_principal_child,
            )
            dpg.bind_item_theme(
            item=tags["heatmap"][f"{group}__"],
            theme=in_principal_child,
            )
        with dpg.child_window(
            tag=tags["miscellaneous"]["updating"],
            parent=tags["heatmap"]["group"],
            show=False,
        ):
            add_logo(logo_name="updating", width_=900, height_=600, tag="update")

      
    dpg.bind_item_theme(
    item=tags["heatmap"]["principalgroup_"],
    theme=in_principal_child,
    )
    dpg.bind_item_theme(
    item=tags["heatmap"]["portfoliogroup_"],
    theme=in_principal_child,
    )
    dpg.bind_item_theme(
    item="spacer_",
    theme=in_principal_child,
    )
    dpg.bind_item_theme(
    item=tags["main"]["searchcontainer"],
    theme=in_principal_child,
    )

    dpg.bind_item_theme(
    item="horizontal_space",
    theme=in_principal_child,
    )

    dpg.bind_item_theme(
    item=tags["miscellaneous"]["updating"],
    theme=in_principal_child,
    )


from THEME import window, principal_window

dpg.bind_item_theme(
    item=tags["main"]["welcomescreen"],
    theme=window,
)

dpg.bind_item_theme(
    item=tags["main"]["loadingscreen"],
    theme=window,
)

dpg.bind_item_theme(
    item=tags["main"]["heatview"],
    theme=principal_window,
)

from os import getcwd, path
from pathlib import Path

CWD = getcwd()
PATH = Path(CWD)

CURRENT_PATH = Path(getcwd())
ICON = "img/icons/icon.png"
ICON_PATH = CURRENT_PATH / ICON

dpg.create_viewport(title="HeatView")
floating_window(tags["main"]["welcomescreen"], "Bienvenido")
floating_window(tags["main"]["loadingscreen"], "Bienvenido")
dpg.set_viewport_small_icon(ICON_PATH)
dpg.set_viewport_large_icon(ICON_PATH)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
