#!/usr/bin/python

# COPYRIGHT 2020 by Pietro Mandracci

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy
try:
    from .functions import *
except ImportError:
    from functions import *

def wait():
    return input('Press RETURN to continue...\n')

def main():

    x = numpy.linspace(0, 100, 51)
    a = numpy.linspace(0, 6.3, 64)

    # Open the plot windows, silencing gnuplot output
    p2d = new_plot(plot_type='2D', title='TEST 2D PLOT WINDOW', redirect_output=None)
    p3d = new_plot(plot_type='3D', title='TEST 3D PLOT WINDOW', redirect_output=None)    
    
    print('* -> Plotting a parabola from data')
    plot2d(p2d, x, x*x, 'parabola')
    wait()

    print('* -> Plotting a parabola as a function')
    plot_function(p2d, 'x**2', replot=True)
    wait()

    print('* -> Changing the scale limits')
    plot_set(p2d, xmin=1, xmax=5, ymin=1, ymax=25, replot=True)
    wait()

    print('* -> Set logarithmic x and y axes')
    plot_set(p2d, logx=True, logy=True, replot=True)
    wait()

    print('* -> Adding a label to the plot')
    plot_label(p2d, x=20, y=20, label='THIS IS A LABEL', replot=True)
    wait()

    print('* -> Removing the label')
    plot_label(p2d, label=None, erase=True, replot=True)
    wait()

    print('* -> Plotting a 3D curve from data')
    plot3d(p3d, x, x, 2*x*x, '3D curve')
    wait()

    print('* -> Plotting a 3D surface as a function')
    plot_function(p3d, 'x**2+y**2', replot=True)
    wait()

    print('* -> Setting logarithmic z axis')
    plot_set(p3d, logz=True, replot=True)
    wait()

    print('* -> Listing the plots')
    plot_list()
    wait()

    print('* -> Listing the plots with more details')
    plot_list(expanded=True)
    wait()

    print('* -> Closing the 2d plot, removing data files')
    plot_close(p2d, purge=True)
    wait()

    print('* -> Listing the plots again')
    plot_list()
    wait()    

    print('* -> Closing all the plots, removing data files')
    plot_close_all(purge=True)
    wait()
    
if __name__ == '__main__':
    main()
