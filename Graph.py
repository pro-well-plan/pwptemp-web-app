def create_plot(ax, step, mw_riser, md, riser=1):
    """
    Takes in an axis and plots the temperature data from the timestep
    """
    ax.plot(step['Tdsi'], md, c='r', label='Fluid in Drill String')  # Temp. inside Drillpipe vs Depth
    ax.plot(step['Ta'], md, 'b', label='Fluid in Annulus')
    if riser > 0:
        ax.plot(step['Tr'], md, 'g', label='Temp. - Riser')  # Temp. due to gradient vs Depth
    ax.plot(step['Tcsg'], md, 'c', label='Casing')  # Temp. due to gradient vs Depth
    ax.plot(step['Tfm'], md, 'g', label='Formation')  # Temp. due to gradient vs Depth
    ax.plot(step['Tsr'], md, c='k', ls='-', marker='', label='Surrounding Space')  # Temp. due to gradient vs Depth
    return ax


def create_temp_time_plot(ax, finaltime, Tbot, Tout, Tfm):

    # Plotting Tbottom and Tout through time
    ax.plot(range(finaltime), Tbot, 'b', label='Bottom')  # Temp. inside Annulus vs Time
    ax.plot(range(finaltime), Tout, 'r', label='Outlet (Annular)')  # Temp. inside Annulus vs Time
    ax.axhline(y=Tfm[-1], color='k', label='Formation')  # Formation Temp. vs Time
    ax.set_xlim(0, finaltime - 1)
    ax.set_xlabel('Time, h')
    ax.set_ylabel('Temperature, °C')
    ax.legend()  # applying the legend
    return ax
