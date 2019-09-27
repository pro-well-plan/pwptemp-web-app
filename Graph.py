def create_plot(ax, temp_distribution, well):
    """
    Takes in an axis and plots the temperature data from the timestep
    """
    ax.plot(temp_distribution.tdsi, well.md, c='r', label='Fluid in Drill String')  # Temp. inside Drillpipe vs Depth
    ax.plot(temp_distribution.ta, well.md, 'b', label='Fluid in Annulus')
    if well.riser > 0:
        ax.plot(temp_distribution.tr, well.md, 'g', label='Temp. - Riser')  # Temp. due to gradient vs Depth
    ax.plot(temp_distribution.tcsg, well.md, 'c', label='Casing')  # Temp. due to gradient vs Depth
    ax.plot(temp_distribution.tfm, well.md, 'g', label='Formation')  # Temp. due to gradient vs Depth
    ax.plot(temp_distribution.tsr, well.md, c='k', ls='-', marker='', label='Surrounding Space')  # Temp. due to gradient vs Depth
    return ax


def create_temp_time_plot(ax, stab_data):
    """
    Returns the temperature plot on an axis
    """

    # Plotting Tbottom and Tout through time
    ax.plot(range(stab_data.finaltime), stab_data.tbot, 'b', label='Bottom')  # Temp. inside Annulus vs Time
    ax.plot(range(stab_data.finaltime), stab_data.tout, 'r', label='Outlet (Annular)')  # Temp. inside Annulus vs Time
    ax.axhline(y=stab_data.tfm[-1], color='k', label='Formation')  # Formation Temp. vs Time
    ax.set_xlim(0, stab_data.finaltime - 1)
    ax.set_xlabel('Time, h')
    ax.set_ylabel('Temperature, °C')
    return ax
