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

""" The _PlotWindow class, used to define a plot window. """

from subprocess import Popen, PIPE, DEVNULL, TimeoutExpired
from os import path, mkdir
from time import sleep

from .global_variables import *
from .errors import *


# +---------+
# | Classes |
# +---------+
       
class _PlotWindow:
    """ This class defines a single plot window. """
    
    def __init__(self,
                 gnuplot_default=False,
                 terminal=DEFAULT_TERM,
                 width=DEFAULT_WIDTH,
                 height=DEFAULT_HEIGHT,
                 xpos=DEFAULT_XPOS,
                 ypos=DEFAULT_YPOS,
                 options=None,
                 plot_type=DEFAULT_TYPE,
                 title=None,
                 persistence=PERSISTENCE,
                 redirect_output=REDIRECT_OUT):
        """ An instance of this class contains a plot window.

            Parameters
            ----------
            gnuplot_default: if it is set to True, the terminal 
                             type, window size and position,
                             are not set, leaving the gnuplot defaults 
                             (which are *not* the default values 
                             of the parameters in this method)
            terminal:        terminal type, must be one of
                             the strings in the TERMINALS tuple
            width:           width of the plot window
            height:          height of the plot window
            xpos:            x position of the plot on the screen
            ypos:            y position of the plot on the screen
            plot_type:       a string defining the type of plot
                             must be one of the strings in PLOT_TYPES
            title:           a string used as the title of the plot
            persistence:     if True, the plot window will not close 
                             after the gnuplot process is terminated
            redirect_output: True:  save gnuplot otuput and errors to files
                             False: send then to /dev/stdout and /dev/stderr
                             None:  send them to /dev/null
            options:         a string containing other options for the terminal

            Initialized data attributes
            ---------------------------

            self.window_number:   integer number that identifies the plot window
            self.gnuplot_process: gnuplot process (instance of subprocess.Popen)
            self.term_type:       the type of gnuplot terminal started 
                                  (string, e.g. 'x11' or 'wxt')
            self.persistence:     True if the window is persistent
            self.filename_out:    file to which gnuplot output is redirected 
            self.filename_err:    file to which gnuplot error messages
                                   are redirected
            self.plot_type:       a string defining the type of plot
            self.n_axes:          number of plot axes (2 for 2D plots, 3 for 3D ones)
            self.xmin:            minimum of x-axis range (initialized to None)
            self.xmax:            maximum of x-axis range (initialized to None)
            self.ymin:            minimum of y-axis range (initialized to None)
            self.ymax:            maximum of y-axis range (initialized to None)
            self.zmin:            minimum of z-axis range (initialized to None)
            self.zmax:            maximum of z-axis range (initialized to None)
            self.title:           the window title (None if not given)
            self.data_filenames:  list containing the names of the data files
            self.functions:       list containing the functions plotted
            self.error:           one of the tuples in the errors.py module
        """

        self.error = NOERROR
        
        # Check that terminal and plot type are among the known ones;
        # otherwise, use defaults and store an error message in self.error
        if terminal in TERMINALS:
            self.term_type = terminal
        else:
            self.term_type = DEFAULT_TERM
            (status, message) = ERROR_UNKNOWN_TERM
            message += (' \"' + str(terminal) + '\"'
                        + ', using default  \"'
                        + DEFAULT_TERM + '\"')
            self.error = (status, message)
        if plot_type in PLOT_TYPES: 
            self.plot_type = plot_type
        else:
            self.plot_type = DEFAULT_TYPE
            (status, message) = ERROR_UNKNOWN_TYPE
            message += (' \"' + str(plot_type) + '\"'
                        + ', using default \"'
                        + DEFAULT_TYPE + '\"' )  
            self.error = (status, message)

        # Store the number of axis     
        if (self.plot_type == '3D'): self.n_axes = 3
        else:                        self.n_axes = 2
        
        # Assign a unique number to this plot window
        # to be used to create unique names for datafiles
        self.window_number = None
        for i in range(len(window_list)):
            if (i != window_list[i].window_number):
                self.window_number = i
                break
        if (self.window_number is None): self.window_number = len(window_list)
        
        # Add this plot to the list of the active plots
        window_list.append(self)

        # Store the window title (may be None)
        self.title = title

        # Store the persistence status
        self.persistence = persistence
        
        # Initialize the lists where data filenames 
        # and functon strings will be stored
        self.data_filenames = []
        self.functions      = []

        # Initialize the axis ranges
        self.xmin = None
        self.xmax = None
        self.ymin = None
        self.ymax = None
        self.zmin = None
        self.zmax = None
            
        # Create the data files directory, if it doesn't exist
        if not path.exists(DIRNAME):        mkdir(DIRNAME)
        if not path.exists(DIRNAME_DATA):   mkdir(DIRNAME_DATA)
                
        # Start the gnuplot process to plot on this window
        if persistence: exec_list = ['gnuplot','-p']
        else:           exec_list = ['gnuplot']        
        if redirect_output is True:
            # If redirection of gnuplot output to files is requested
            # create the directories to save gnuplot output and errors
            if not path.exists(DIRNAME_OUT): mkdir(DIRNAME_OUT)
            if not path.exists(DIRNAME_ERR): mkdir(DIRNAME_ERR)
            self.filename_out = path.join( DIRNAME_OUT, FILENAME_OUT
                                           + '_w_' + str(self.window_number) )
            self.filename_err = path.join( DIRNAME_ERR, FILENAME_ERR
                                           + '_w_' + str(self.window_number) )
            if self.title is not None:
                self.filename_out += ( '('
                                       + self._correct_filename(self.title)
                                       + ')' )
                self.filename_err += ( '('
                                       + self._correct_filename(self.title)
                                       + ')' )
            self.gnuplot_process = Popen(exec_list,
                                         stdin=PIPE,
                                         stdout=open(self.filename_out, 'w'),
                                         stderr=open(self.filename_err, 'w'),
                                         universal_newlines=True)
        elif redirect_output is False:
            self.filename_out = '/dev/stdout'
            self.filename_err = '/dev/stderr'               
            self.gnuplot_process = Popen(exec_list,
                                         stdin=PIPE,
                                         universal_newlines=True)            
        else:
            self.filename_out = '/dev/null'
            self.filename_err = '/dev/null'        
            self.gnuplot_process = Popen(exec_list,
                                         stdin=PIPE,
                                         stdout=DEVNULL,
                                         stderr=DEVNULL,
                                         universal_newlines=True)
        if not gnuplot_default:
            command_string = ( 'set terminal ' + str(self.term_type)
                               + ' size '      + str(width) + ',' + str(height)
                               + ' position '  + str(xpos)  + ',' + str(ypos)   )
            if (options is not None):
                command_string += ' ' + str(options)
            self._command(command_string)
        if title is not None:
            self._command('set title \"' + self._correct_filename(self.title)
                          + '\"')
            
            
    def _command(self, command_string):
        """ Send a command to the gnuplot process.

            NOTE: no check is made that the string is a valid gnuplot command

            Parameters
            ----------

            command_string: string containing a gnuplot command
        """

        self.gnuplot_process.stdin.write(command_string + EOL)
        self.gnuplot_process.stdin.flush()

        
    def _quit_gnuplot(self):
        """ Terminate the gnuplot process associated to this window. 

            Returns
            -------

            The last output provided by the gnuplot process
        """

        try:
            gnuplot_last_output = self.gnuplot_process.communicate(input='quit',
                                                                   timeout=TIMEOUT_QUIT)
        except TimeoutExpired:
            self.gnuplot_process.kill()
            gnuplot_last_output = self.gnuplot_process.communicate()

        return gnuplot_last_output                


    def _correct_filename(self, filename):
        """ Remove invalid characters from a filename.

            If the string contains characters in INVALID_CHARS, they are
            substituted with the char in SUBSTITUTE_CHAR.

            Parameters
            ----------

            filename: a string, representive a filename

            Returns
            -------

            The modified string
        """

        for c in INVALID_CHARS:
            filename = filename.replace(c, SUBSTITUTE_CHAR)

        return filename
    
        
    def _data_file_2d(self, x_data, y_data, filename, sep=SEP, eol=EOL):
        """ Create a file and write 2d data to it in csv format.

            The file will contain data in ascii format, in the form:

            x1  y1
            x2  y2
            ..  ..

            Parameters
            ----------

            x_data:   data representing x coordinates of the points to plot
            y_data:   data representing y coordinates of the points to plot
            filename: the name of the data file to be created
            sep:      separator character between colums (vaues in a line)
            eol:      end-of-line character
        """
         
        data_file = open(filename, 'w') 
        for i in range(len(x_data)):
            data_file.write( str(x_data[i])
                             + sep
                             + str(y_data[i])
                             + eol )
        data_file.close()


    def _data_file_3d(self, x_data, y_data, z_data, filename, sep=SEP, eol=EOL):
        """ Create a file and write 3d data to it in csv format.

            The file will contain data in ascii format, in the form:

            x1  y1  z1
            x2  y2  z2
            ..  ..  ..

            Parameters
            ----------

            x_data:   data representing x coordinates of the points to plot
            y_data:   data representing y coordinates of the points to plot
            z_data:   data representing z coordinates of the points to plot
            filename: the name of the data file to be created
            sep:      separator character between colums (vaues in a line)
            eol:      end-of-line character
        """
         
        data_file = open(filename, 'w') 
        for i in range(len(x_data)):
            data_file.write(  str(x_data[i])
                              + sep
                              + str(y_data[i])
                              + sep
                              + str(z_data[i])                                
                              + eol )
        data_file.close()


    def _add_functions(self, function_list, replot=False):
        """ Add one or more functions to a plot window.

            Parameters
            ----------

            function_list: a list in the following form:
                          [ [function1, label1, options1], 
                            [function2, label2, options1], ... ]
                          where:
                          - function1 is a string defining the function 
                            to be plotted
                            e.g. '2*x**2+3*cos(x)' or 'sin(x**2+y**2) 
                          - label1 is a string, that will be used to identify 
                            the plot in the legend, or None
                          - options1 is a string, containing additional options
                            or None 
            replot:       if True, the functions are plotted without erasing 
                          previously plotted ones
            Returns
            -------
            
            One of the tuples defined in the errors.py module
        """

        (status, message) = NOERROR

        if not function_list: return ERROR_NO_FUNCTION 
        if (replot and (not self.data_filenames) and (not self.functions)):
            return ERROR_NO_REPLOT           
        # Check consistency of the whole list
        for i in range(len(function_list)):
            if ( len(function_list[i]) != 3):
                (status, message) = ERROR_PLOT_PARAMETERS
                if len(function_list) > 1:
                    message += ' in list item # ' + str(i)
                message += ( ': 3 items expected, given '
                             + str(len(function_list[i])) )
                return (status, message)
                   
        # Initialize data attributes of this plot window   
        if not replot:
            self.data_filenames.clear()
            self.functions.clear()

        # Beginning of the command string to send to gnuplot
        if replot:                     command_string = 'replot '
        elif (self.plot_type == '3D'): command_string = 'splot '
        else:                          command_string = 'plot '
              
        for i in range(len(function_list)):

            # Add the function to the function list
            self.functions.append(str(function_list[i][0]))
            
            # Read the label, if given
            if (function_list[i][1] is None): label = None
            else:                             label = str(function_list[i][1])
            
            # Add  to the command string the plot command for this function
            command_string += str(function_list[i][0])
            if (label is not None):
                command_string += ' title \"' + str(label) + '\"'
            if (function_list[i][2] is not None):
                command_string += ' ' + str(function_list[i][2])
            if (i < len(function_list) - 1):
                command_string += ', '
                        
        # Send command string to gnuplot   
        self._command(command_string)

        return status, message        
        

    def _add_curves(self, data_list, replot=False):
        """ Add one or more curves from data to the plot window. 

            Parameters
            ----------

            data_list:    a list in one of the following forms:
                          2D data: [ [x1 , y1, label1, options1],     
                                     [x2,  y2, label2, options1]     ... ]
                          3D data: [ [x1,  y1, z1, label1, options1], 
                                     [x2,  y2, z2, label2, options2], ... ] 
                          where:
                          - x1 contains the x-coordinates of the points to plot
                          - y1 contains the y-coordinates of the points to plot 
                          - z1 contains the z-coordinates of the points to plot  
                          - label1 is a string, that will be used to identify the plot 
                            in the legend, or None
                          - options1 is a string, containing additional options
                            or None
                          The form must be consisted with the type of plot 
                          that was defined at the plot window creation, 
                          otherwise an error message is returned
            replot:       if True, the curves are plotted without erasing 
                          previously plotted ones

            Returns
            -------

            One of the tuples defined in the errors.py module
        """

        (status, message) = NOERROR

        if not data_list: return ERROR_NO_DATA
        if (replot and (not self.data_filenames) and (not self.functions)):
            return ERROR_NO_REPLOT
        
        # Check consistency of the whole list
        for i in range(len(data_list)):
            # Transform single numbers to lists
            try:
                len_x = len(data_list[i][0])
            except TypeError:
                data_list[i][0] = [ data_list[i][0] ]
                len_x = 1
            try:
                len_y = len(data_list[i][1])
            except TypeError:
                data_list[i][1] = [ data_list[i][1] ]
                len_y = 1
            if self.n_axes == 3:
                try:
                    len_z = len(data_list[i][2])
                except TypeError:
                    data_list[i][2] = [ data_list[i][2] ]
                    len_z = 1                
            if (len(data_list[i]) != self.n_axes + 2):
                (status, message) = ERROR_PLOT_PARAMETERS
                if len(data_list) > 1: message += ' in list item # ' + str(i)
                message += ( ': ' +  str(self.n_axes + 2)
                             + ' items expected, given '
                             + str(len(data_list[i])) )
                return (status, message)
            elif (len_x != len_y):
                (status, message) = ERROR_PLOT_PARAMETERS
                if len(data_list) > 1:  message += ' in list item # ' + str(i)
                message += ': x and y data have different sizes'
                return status, message
            elif (self.n_axes == 3) and (len_z != len_x):
                (status, message) = ERROR_PLOT_PARAMETERS
                if len(data_list) > 1:  message += ' in list item # ' + str(i)
                message += ': x, y and z data have different sizes'
                return status, message               
            elif (len_x == 0):
                (status, message) = ERROR_PLOT_PARAMETERS
                if len(data_list) > 1: message += ' in list item # ' + str(i)
                message += ': zero size data given'
                return status, message            
                   
        # Initialize data attributes of this plot window   
        if not replot:
            self.data_filenames.clear()
            self.functions.clear()
        
        # Beginning of the command string to send to gnuplot
        if replot:                     command_string = 'replot '
        elif (self.plot_type == '3D'): command_string = 'splot '
        else:                          command_string = 'plot '

        # Number of curves before adding the new ones
        n_curves = len(self.data_filenames)          
        for i in range(len(data_list)):
            
            # This number is used to create a unique filename for each curve
            curve_number = n_curves + i
            
            # Read the curve label, if given
            if (data_list[i][self.n_axes] is None):
                label = None
            else:
                label = str(data_list[i][self.n_axes])

            # Read additional options, if given
            if (data_list[i][self.n_axes+1] is None):
                options = None
            else:
                options = str(data_list[i][self.n_axes+1])
                        
            # Define the unique filename for the data file of this curve
            string = FILENAME_DATA 
            string += '_w' + str(self.window_number)
            if (self.plot_type == '3D'): string += '_3D'
            else:                        string += '_2D'        
            if self.title is not None:
                string += '(' + self._correct_filename(self.title) + ')'
            string += '_c' + str(curve_number)
            if label is not None:
                string += '(' + self._correct_filename(label) + ')' 
            string += FILENAME_DATA_EXT
            filename = path.join( DIRNAME_DATA, string )  
 
            # Add filename to the list
            self.data_filenames.append(filename)

            # Write data to the file
            if self.plot_type == '3D':
                self._data_file_3d( data_list[i][0],
                                    data_list[i][1],
                                    data_list[i][2],
                                    filename )
            else:
                self._data_file_2d( data_list[i][0],
                                    data_list[i][1],
                                    filename )

            # Add plot command to the command string
            command_string += '\"' + filename + '\"'
            if (label is None):
                # If we don't set a title, gnuplot automatically
                # uses the data file name, so we set "" as title
                command_string += ' title \"\"'
            else:
                command_string += ' title \"' + label + '\"'
            if (options is not None):
                command_string += ' ' + options
            if (i < len(data_list) - 1):
                command_string += ', '
                        
        # Send command string to gnuplot   
        self._command(command_string)

        return status, message
    
