#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Copyright (C) 2007-2020 Gaetan Delannay

# This file is part of Appy.

# Appy is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# Appy is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# Appy. If not, see <http://www.gnu.org/licenses/>.

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Gridder:
    '''Specification about how to produce search results in grid mode. An
       instance of Gridder can be specified in static attribute
       SomeAppyClass.gridder.'''

    def __init__(self, width='350px', gap='20px', justifyContent='space-evenly',
                 alignContent='space-evenly', cols=None, margin=None):
        # ~~~
        # If a p_width is specified, there will not be a fixed number of
        # columns: this number will depend on available space and this width.
        # If, for example, p_with is defined as being "350px" and the available
        # width is 800 pixels, the grid will have 2 columns.
        # ~~~
        # If p_cols is specified, p_width is ignored. p_cols defines the maximum
        # number of columns for the grid.
        # ~~~
        # The minimum width of every grid element
        self.width = width
        # The gap between grid elements. Will be passed to CSS property
        # "grid-gap".
        self.gap = gap
        # Specify how to align the whole grid horizontally inside the container.
        # Will be passed to CSS property "justify-content".
        self.justifyContent = justifyContent
        # Specify how to align the whole grid vertically inside the container.
        # Will be passed to CSS property "align-content".
        self.alignContent = alignContent
        # The maximum number of columns
        self.cols = cols
        # The gridder's margins
        self.margin = margin

    def getContainerStyle(self):
        '''Returns the CSS styles that must be applied to the grid container
           element.'''
        # Determine columns
        if self.cols:
            columns = 'repeat(%d, 1fr)' % self.cols
        else:
            columns = 'repeat(auto-fill, minmax(%s, 1fr))' % self.width
        # Determine margins
        margin = '; margin:%s' % self.margin if self.margin else None
        
        # Return CSS code
        return 'display:grid; grid-template-columns:%s; ' \
               'grid-gap:%s; justify-content:%s; align-content:%s%s' % \
               (columns, self.gap, self.justifyContent, self.alignContent,
                margin)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
