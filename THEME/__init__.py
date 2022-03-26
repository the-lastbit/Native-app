import dearpygui.dearpygui as dpg


with dpg.theme() as table:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding,0)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding,0,0)
        dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
        dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize,0)
        dpg.add_theme_style(dpg.mvStyleVar_CellPadding,-10,-10)
        dpg.add_theme_style(dpg.mvStyleVar_IndentSpacing,0)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing,0,0)
        dpg.add_theme_style(dpg.mvStyleVar_ItemInnerSpacing,0,0)
        dpg.add_theme_color(dpg.mvPlotCol_PlotBorder, (0,0,0,0), category=dpg.mvThemeCat_Plots)
        dpg.add_theme_color(dpg.mvPlotCol_FrameBg, (0,0,0,0), category=dpg.mvThemeCat_Plots)

with dpg.theme() as window:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0,0,0))
        dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize,0)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (250,20,20))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (250,100,100))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (250,150,150))  
        dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, (55,20,25))
        
with dpg.theme() as child:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize,0)
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0,0,0))

with dpg.theme() as principal_window:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (20,20,20))
        dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize,0)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (20,20,20))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (20,20,20))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (100,50,50))
        dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize,20)
        dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding,5)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg,(100,50,50))
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab,(250,50,50))
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered,(250,50,50))
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive,(250,50,50))

with dpg.theme() as in_principal_child:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize,0)
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (20,20,20))

with dpg.theme() as search_window:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0,0,0))
        dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize,0)   
        dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (150,20,60))
        dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (200,20,100))
        dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, (100,20,45))
        dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong, (0,0,0))
        dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight, (50,50,50))
        dpg.add_theme_color(dpg.mvThemeCol_TableRowBg, (30,10,10))
        dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt, (60,20,20))
        dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, (75,20,25))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (250,20,20))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (250,100,100))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (250,150,150))  
        dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize,10)
        dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding,5)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg,(100,50,50))
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab,(250,50,50))
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered,(250,50,50))
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive,(250,50,50))
