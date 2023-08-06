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

""" This module contains functions to plot data on 2D and 3D graphs by means of gnuplot.

Introduction
============

This package allows to plot data or mathematical expressions inside python,
using the gnuplot program, in the form of 2D or 3D plots.

Multiple plot windows can be opened, and a separate gnuplot process 
is started for each of them.  The data to be plotted are saved to files
and the gnuplot program is called to plot them. Mathematical expressions,
instead, are sent directly to gnuplot as strings.
All the package functionalities can be accessed by calling functions,
the list of which is reported at the end of this document.

The most commonly used plot settings, such as applying logarithmic scales
or setting scale limits, can be applied by passing arguments to the functions,
without knowing the specific gnuplot commands.  However, it is also possible
to pass arbitrary commands to gnuplot, using the plot_command() function.


Read the 'README.rst' document for full documentation.


Package structure
=================

This package contains four modules:

*global_variables.py*
    contains the global variables, mainly used to define default values of 
    some parameters;
    
*errors.py*
    contains error messages returned by the package functions;
    
*classes.py*
    contains the *_PlotWindow* class, used to create a structure containing the
    gnuplot process (instance of *subprocess.Popen*) and some information on
    the plot (number of curves, names of datafiles, etc.);

*functions.py*
    contains all the functions used to create plot windows and plot 
    data or mathematical expressions on them.


Importing the package
=====================

How to import
-------------

To import *gnuplot_manager* you can use the *import* directive as usual:

>>> import gnuplot_manager

or 

>>> import gnuplot_manager as gm

or also

>>> from gnuplot_manager import *


Checking gnuplot installation at the module import
--------------------------------------------------

When the module is imported, it checks the availability of the gnuplot program
and sets the global variable *gnuplot_installed* accordingly.
This is achieved by means of a call to the program *which*, that should be
installed in nearly all linux distributions. However, if it is not installed
on your system, the *gnuplot_installed* variable is set to *None*.

*gnuplot_installed=True*
  gnuplot is installed
  
*gnuplot_installed=False*
  gnuplot is not installed
  
*gnuplot_installed=None*
  *which* was not found, so the installation of gnuplot was not checked


Creating a new plot window
==========================

The *new_plot()* function
-------------------------

To open a new plot window, use the *new_plot()* function

>>> myplot = gm.new_plot(plot_type='2D', title='My 2D Plot')

The function returns an instance of the *_PlotWindow* class.

Note that the plot window will not appear on the screen until you plot
something on it.

You can specify 2 types of plot: '2D' and '3D', with '2D' as default.
If you give a title to the window, giving the *title* argument,
it will be printed on the window when something is plotted on it.

All the arguments are optional:

>>> myplot = gm.new_plot()

opens a '2D' plot without a title.

Persistence
-----------

If you give the *persistence=True* argument when opening a new plot, 
the window will remain visible after the gnuplot process has been closed.


Gnuplot output management
-------------------------

When you open a new plot window, you can specify how you like to treat 
the output of the associated gnuplot process, passing the 
*redirect_output* argument:

*redirect_output = False* 
    gnuplot output and errors are sent to */dev/stdout* and */dev/stderr*
    respectively, as it would happen when calling the program from the terminal.
    This can be useful when using gnuplot from the console, to get the output
    immediately;
*redirect_output = True* 
    the output is saved to files, which are stored in the directories
    *gnuplot.out/output/* and *gnuplot.out/errors/*;
*redirect_output = None* 
    the output is suppressed, sending it to */dev/null*.

You can specify a different behavior for each window you open:


Other plot window properties
----------------------------

While opening the plot window, you can specify several other properties,
such as: type of terminal, window dimensions, position on the screen,
axis limits, labels, and so on.

Read the docstring of the *new_plot()* function for a list of all
the available options.


Plotting from data
==================

Plotting 2D curves from data
----------------------------

To plot 2D data, use the *plot2d()* function, passing the *_PlotWindow* 
instance as first argument. The second and third arguments must be 
unidimensional data structures, such as numpy arrays, lists or tuples,
having equal sizes, containing the x-values and y-values of the points to plot.
As an example, if the second and third argument are two arrays *x* and *y*:

    - the first point to plot has coordinates (*x[0]*, *y[0]*)
    - the second point has coordinates (*x[1]*, *y[1]*)
    - and so on...

The third argument (optional) is a string to be used as label in the 
plot legend. If provided, it is also included in the name of 
the data file to which the values to be plotted are saved.
Example:

>>> myplot = gm.new_plot(plot_type='2D', title='My 2D Plot')
>>> x = numpy.linspace(0,100,1001)
>>> y = x * x
>>> gm.plot2d(myplot, x, y, label='y=x^2')
(0, 'Ok')
  

Plotting 3D data
----------------

To plot 3D data, the plot window must have been opened with the option
*plot_type = '3D'* and you have to use the *plot3d()* function.

The x, y and z values to be plotted must be stored in 
unidimensional data structures of equal sizes, and contain the x, y,
and z coordinates of each point to plot. As an example, if you pass
the three arrays *x*, *y* and *z*: 

    - the first point to plot has coordinates (*x[0]*, *y[0]*, *z[0]*)
    - the second point has coordinates (*x[1]*, *y[1]*, *z[1]*)
    - and so on...

Example of 3D curve plot:

>>> my3dplot = gm.new_plot(plot_type='3D', title='My 3D plot')
>>> x = numpy.linspace(0,100,1001)
>>> y = numpy.linspace(0,200,1001)
>>> z = x * y
>>> gm.plot3d(my3dplot, x, y, z, label='3D curve')
(0, 'Ok')


Adding more curves to a plot
----------------------------

To add new data on the same plot, you must pass the *replot=True* argument.


Plotting several curves at the same time
----------------------------------------

The function *plot_curves()* allows to plot several curves at one time,
which is faster than plotting them one at a time using the *replot* option,
since gnuplot is called only once.

Data to be plotted must be recorded in a list, each element of which
is itself a list, made of 3 elements for 2D plots, or 4 elements for 3D ones.

For 2D plots, each list element has the form *[x, y, label]*, while for 3D
plots it has the form *[x, y, z, label]*, where:

    - *x* is the array of x coordinates of the points to plot;
    - *y* is the array of y coordinates of the points to plot;
    - *z* is the array of z coordinates of the points to plot (only for 3D plots);
    - *label* is a string with the label to show in the plot legend,
      or *None* if you do not want a label to be set

Examples:

>>> x1 = numpy.linspace(0, 100, 101)
>>> y1 = 2 * x1
>>> z1 = x1 * y1
>>> x2 = numpy.linspace(0, 100, 201)
>>> y2 = 3 * x2
>>> z2 = x2 * y2 / 10
>>> list2d = [ [x1, y1, 'my first data 2D'], [x2, y2, 'my second data 2D'] ]
>>> list3d = [ [x1, y1, z1, 'my first data 3D'], [x2, y2, z2, 'my second data 3D'] ]

The first argument passed to *plot_curves()* must be the plot on which 
you want to operate, while the second is the list:

>>> my2dplot = gm.new_plot(plot_type = '2D', title='My 2D plot')
>>> gm.plot_curves(my2dplot, list2d)
(0, 'Ok')
>>> my3dplot = gm.new_plot(plot_type = '3D', title='My 3D plot')
>>> gm.plot_curves(my3dplot, list3d)
(0, 'Ok')

Data files
----------

The data to be plotted are written on files, which are saved
in the *gnuplot.out/data/* directory,
which is created in the current working directory.


Plotting mathematical functions
===============================

Plotting a math expression
--------------------------

The function *plot_function()* allows to pass to gnuplot a string, representing
a mathematical function.

>>> my2dplot = gm.new_plot()
>>> gm.plot_function(my2dplot, 'sin(x)', label='sin(x)')
(0, 'Ok')
>>> my3dplot = gm.new_plot(plot_type='3D')
>>> gm.plot_function(my3dplot, 'sin(x)*cos(y)', label='sin(x)*cos(y)')
(0, 'Ok')


If the *label* argument is not given or is set to *None*, gnuplot will automatically
use the function string as a label for the plot legend. If you don't want any label to be shown,
pass the argument *label=""* (empty string).

.. note:: No check is made that the string represents a valid mathematical expression.
   If it is not, gnuplot will print an error message on the console or on the file on 
   which you have redirected */dev/stderr* (unless you have chosen to send it to */dev/null*).

   
Adding a math expression to other curves
----------------------------------------

By default, *plot_function()* removes anything
that was previously plotted on the window. 
You can use the *replot=True* option to plot the function
on top of what was plotted before

>>> myplot = gm.new_plot()
>>> gm.plot_function(myplot, 'x*x',   label='y=x^2')
(0, 'Ok')
>>> gm.plot_function(myplot, '2*x*x', label='y=2x^2', replot=True)
(0, 'Ok')

Plotting several mathematical expression at the same time
---------------------------------------------------------

The function *plot_functions()* allows to plot an arbitrary number of
mathematical expression in a single plot operation. 

The expression to be plotted must be recorded in a list, each element of which
is itself a list of 2 strings: the first one is the math expression, the
second is the label to be shown on the plot legend:

>>> list2d = [ ['x*x', 'y=x^2'],  ['2*x*x', 'y=2x^2'] ]
>>> my2dplot = gm.new_plot()
>>> gm.plot_functions(my2dplot, list2d)
(0, 'Ok')

>>> list3d = [ ['sin(x)*cos(y)', 'z=sin(x)cos(y)'], ['2*sin(x)*cos(y)', 'z=2sin(x)cos(y)'] ]
>>> my3dplot = gm.new_plot(plot_type='3D')
>>> gm.plot_functions(my3dplot, list3d)
(0, 'Ok')

If you don't want to set labels manually, put *None* in their place and gnuplot
will automatically create them, or put "" (empty string) and they will not be set.

You can pass the *replot=True* argument to plot functions without 
deleting anything was plotted before.


Closing plot windows
====================

Closing a single plot window
----------------------------

When you do not need a plot window anymore, you can close it by means of
the *plot_close()* function, which performs the following actions:

    - terminates the gnuplot process associated to the *_PlotWindow* instance
      given as argument, by sending the *quit* gnuplot command to it;
    - sets the *plot_type* attribute of the *_PlotWindow* instance  to *None*;
    - removes the *_PlotWindow* instance from the *window_list* global variable.

.. note:: Closing the window on the screen by clicking on its 
   close button, *does not* close the gnuplot terminal and 
   *does not* remove the *_PlotWindow* instance from the list.


Closing all the open windows at once
------------------------------------

The *plot_close_all()* function closes all the plot windows listed in the *window_list*
global variable, and empties it.

>>> gm.plot_close_all()
(0, 'Ok')


Deleting the output files
-------------------------

By default, the data files associated to the plot window are *not* deleted
when it is closed, but you can ask to delete them giving the *purge=True* argument
to the *plot_close()* or *plot_close_all()* function:

>>> gm.plot_close(myplot, purge=True)
(0, 'Ok')

If the plot was opened passing the *redirect_output=True* argument, then
the files on which the gnuplot output has been redirected will be deleted as well.

The default behavior is stored in the *PURGE_FILES* global variable.

The optional *delay* parameter specifies a time (in seconds) to wait before
deleting the data files, after the *quit* command has been sent to gnuplot.
This can be useful in some circumstances: for example if you want to create
a persistent window, plot something complex on it, and then close the gnuplot
process leaving only the window open:

>>> myplot = gm.new_plot(persistence=True)
>>> x = numpy.linspace(0, 1000, 1000000)
>>> y = x * x
>>> gm.plot2d(myplot, x, y)
(0, 'Ok')
>>> gm.plot_close(myplot, purge=True, delay=1)
(0, 'Ok')

When the *plot_close()* function is called, it immediately sends the
*quit* command to gnuplot, but it is executed only when gnuplot
has completed the plot operation started by the *plot2d()* function.
If the datafiles were deleted immediately after sending the *quit* command,
they could be removed while the plot operation (plotting one million points) is still in progress.


Performing other actions
========================

Refreshing windows
------------------

You can refresh the plot window at any time using the *plot_replot()* function:

>>> gm.plot_replot(myplot)
(0, 'Ok')

If you have closed the window by clicking on its close button, this will cause
it to reappear.

You can refresh all plot windows at once by the *plot_replot_all()* function:

>>> gm.plot_replot_all()
(0, 'Ok')

Changing the window properties
------------------------------

You can change some properties of a plot window, such as logarithmic scale or
range of the axes, using the *plot_set()* function.
Example, to set logarithmic x axis:

>>> myplot = gm.new_plot(logx=False)
>>> gm.plot_set(myplot, logx=True)   # I have changed my mind...
(0, 'Ok')

By default, the new options are applied when a new curve or
function is plotted: if you want to apply them immediately, on
the already plotted items, pass the *replot=True* argument.

Resetting a window
------------------

The *plot_reset()* function allows to reset the window properties:

    - removes all the curves and functions
    - clears the plot area

The *plot_axes* argument, which is *True* by default, tells the function to
plots the axes after having cleared the window.

The *plot_reset_all()* function resets all the plot windows at once.


Checking the window properties
------------------------------

The *plot_check()* function prints information about the plot window
given as argument: 

If the *expanded=True* argument is given, it prints more information,
including the PID of the gnuplot process and the names of the
datafiles:

The *plot_list()* function does the same for all open windows. 

Both functions take two more arguments:

*printout* (default is *True*): 
    if set to *True*, the output is printed on console 
*getstring* (default is *False*): 
    if set to *True*, a string with the output is returned. 
    This can be useful to write the output to a file or inside a GUI window.  
  
Sending arbitrary commands to gnuplot
-------------------------------------

You can send arbitrary commands to the gnuplot process associated to
a plot window using the *plot_command()* function:

>>> myplot=gm.new_plot()
>>> gm.plot_command(myplot,string='<gnuplot-command>')

.. note:: No check is made that the string you provide is a valid
   gnuplot command: if it is not, gnuplot rises an error, which
   can be printed on console, written to file, or discarted, depending
   on the value given to the *redirect_output* parameter
   when the function *new_plot()* was called to create the plot.


List of available functions
===========================

For a complete description of the available functions:

>>> help(gm.functions)

Create and modify plot windows
------------------------------

*new_plot()*
    create a new plot window
*plot_set()*
    modify some properties of a previously created window
*plot_command()*
    send a command to the gnuplot process


Plot data
---------

*plot2d()*
    plot a curve from 2d data
*plot3d()*
    plot a curve from 3d data
*plot_curves()*
    plot several curves at the same time

Plot mathematical functions
---------------------------

*plot_function()*
    plot a mathematical expression
*plot_functions()*
    plot several mathematical expression at once


Reset, clear and refresh plots
------------------------------

*plot_reset()*
    reset a plot: remove all curves and functions
    and the clear the window 
*plot_reset_all()*
    reset all plot windows
*plot_clear()*
    clear the plot area
*plot_clear_all()*
    clear the plot area of all plots
*plot_replot()*
    refresh the plot window
*plot_replot_all()*
    refresh all the plot windows


Utility functions
-----------------

*plot_label()*
    print a string on the plot
*plot_raise()*
    rise the plot window over the other windows on the screen
*plot_lower()*
    lower the plot window under the other windows on the screen
*plot_raise_all()*
    rise all the plot windows    
*plot_lower_all()*
    lower all the plot windows
*plot_check()*
    print the plot properties
*plot_list()*
    print the properties of all plots
*plot_close()*
    close the plot window and terminate the gnuplot process
*plot_close_all()*
    close all the plot windows and terminate all the gnuplot processes 


The *_PlotWindow* class
=======================

Each plot window is an instance of the *_PlotWindow* class, 
which has several attributes:

*self.window_number*:   
    an integer number that identifies the plot window,                               
    mainly used to generate unique names for the data files
*self.gnuplot_process*: 
     gnuplot process (instance of *subprocess.Popen*)    
*self.term_type*:
    the type of gnuplot terminal    
*self.plot_type*:
    a string defining the type of plot : '2D', '3D',
    or *None* if the plot window has been closed
*self.n_axes:*
    number of plot axes (2 for 2D plots, 3 for 3D ones)
*self.xmin*:
    minimum of the x-axis (*None* if not set)
*self.xmax*:
    maximum of the x-axis (*None* if not set)
*self.ymin*:
    minimum of the y-axis (*None* if not set)
*self.ymax*:
    maximum of the y-axis (*None* if not set)
*self.zmin*:
    minimum of the z-axis (*None* if not set)
*self.zmax*:
    maximum of the z-axis (*None* if not set)
*self.persistence*:
    *True* if the plot was opened as persistent
*self.title*:
    the window title (*None* if not given)
*self.filename_out*: 
     name of the file to which gnuplot output is redirected
*self.filename_err*:
     name of the file to which gnuplot errors are redirected     
*self.data_filenames*:
     list containing the names of the datafiles related to the
     curves presently plotted on the window
*self.functions*:
     list containing the function strings [#functions]_
*self.error*:
     if there was an error while opening the plot
     an error message is stored here

.. [#functions] Note that no check is made that function strings given to gnuplot 
   are correct. So even wrong ones (which therefore gnuplot has not plotted)
   are listed here.

.. note:: If you modify the plot by sending commands to gnuplot directly, using
   the *plot_command()* function, some of these attributes, such as the number of curves 
   and the list of data files, may not be updated properly.

The *_PlotWindow* class have some methods also, which are called by the functions
of the *functions.py* module to perform their tasks:

*self._command()*
    method used to send commands to gnuplot
*self._quit_gnuplot()*
    method used to close the gnuplot process and close the window
*self._data_file_2d()*
    method used to write 2D data on datafiles
*self._data_file_3d()*
    method used to write 3D data on datafiles
*self._correct_filename()*
    method used to remove unsuitable chars from filenames
*self._add_functions()*
    method used to add one or more mathematical expression
*self._add_curves()*
    method used to add one or more curves from data

.. note:: Since the package is designed to use the functions in the *functions.py* module,
   these methods are not intended to be called directly.

"""

__version__ = '0.1.0'

from .global_variables import *
from .functions import *




