###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

import mpld3

from scipy.stats import pearsonr
import numpy as np

from refinem.plots.base_plot import BasePlot
from refinem.plots.mpld3_plugins import Tooltip


class CovCorrPlots(BasePlot):
    """Histogram and scatterplot showing coverage profile correlation of scaffolds."""

    def __init__(self, options):
        """Initialize."""
        BasePlot.__init__(self, options)
        
    def _correlation(self, genome_scaffold_stats, mean_coverage):
        """Calculate percent deviant of coverage profiles for each scaffold."""
        
        correlations = []
        for stats in genome_scaffold_stats.values():
            corr_r = 1.0
            if len(mean_coverage) >= 1:
                corr_r, _corr_p = pearsonr(mean_coverage, stats.coverage)
                if np.isnan(corr_r):
                    # both coverage profiles contain identical values,
                    # e.g. pearsonr([1,1,1],[2,2,2]) -> exception
                    corr_r = 1.0

            correlations.append(corr_r)
            
        return correlations
        
    def data_pts(self, genome_scaffold_stats, mean_coverage):
        """Get data points to plot.

        Parameters
        ----------
        genome_scaffold_stats : d[scaffold_id] -> namedtuple of scaffold stats
          Statistics for scaffolds in genome.
          
        Returns
        -------
        dict : d[scaffold_id] -> (x, y)
        """
        
        correlations = self._correlation(genome_scaffold_stats, mean_coverage)
        
        pts = {}
        for i, (scaffold_id, stats) in enumerate(genome_scaffold_stats.items()):
            scaffold_stats[scaffold_id] = (correlations[i], stats.length / 1000.0)
            
        return pts

    def plot(self, genome_scaffold_stats,
             highlight_scaffold_ids, link_scaffold_ids,
             mean_coverage, cov_corrs):
        """Setup figure for plots.

        Parameters
        ----------
        genome_scaffold_stats: d[scaffold_id] -> namedtuple of scaffold stats
          Statistics for scaffolds in genome.
        highlight_scaffold_ids : d[scaffold_id] -> color
            Scaffolds in genome to highlight.
        link_scaffold_ids : list of scaffold pairs
            Pairs of scaffolds to link together.
        mean_coverage : float
          Mean coverage profile of genome.
        cov_corrs : iterable
          Coverage correlation values to mark on plot.
        """

        # Set size of figure
        self.fig.clear()

        mpld3.plugins.clear(self.fig)
        mpld3.plugins.connect(self.fig, mpld3.plugins.Reset(), mpld3.plugins.BoxZoom(), mpld3.plugins.Zoom())
        mpld3.plugins.connect(self.fig, mpld3.plugins.MousePosition(fontsize=12, fmt='.1f'))

        self.fig.set_size_inches(self.options.width, self.options.height)

        axes_hist = self.fig.add_subplot(121)
        axes_scatter = self.fig.add_subplot(122)

        self.plot_on_axes(self.fig, genome_scaffold_stats,
                          highlight_scaffold_ids,
                          link_scaffold_ids,
                          mean_coverage, cov_corrs,
                          axes_hist, axes_scatter, True)

        self.fig.tight_layout(pad=1, w_pad=1)
        self.draw()

    def plot_on_axes(self, figure,
                     genome_scaffold_stats,
                     highlight_scaffold_ids,
                     link_scaffold_ids,
                     mean_coverage, cov_corrs,
                     axes_hist, axes_scatter, tooltip_plugin):
        """Create histogram and scatterplot.

        Parameters
        ----------
        figure : matplotlib.figure
          Figure on which to render axes.
        genome_scaffold_stats: d[scaffold_id] -> namedtuple of scaffold stats
          Statistics for scaffolds in genome.
        highlight_scaffold_ids : d[scaffold_id] -> color
            Scaffolds in genome to highlight.
        link_scaffold_ids : list of scaffold pairs
            Pairs of scaffolds to link together.
        mean_coverage : float
          Mean coverage profile of genome.
        cov_corrs : iterable
          Coverage correlation values to mark on plot.
        """

        # calculate percent deviant of coverage profiles for each scaffold
        correlations = self._correlation(genome_scaffold_stats, mean_coverage)

        # histogram plot
        if axes_hist:
            axes_hist.hist(correlations, bins=20, color=(0.5, 0.5, 0.5))
            axes_hist.set_xlabel("coverage correlation\n(Pearson's $r$)")
            axes_hist.set_ylabel('# scaffolds (out of %d)' % len(correlations))
            self.prettify(axes_hist)

        # scatterplot
        xlabel = "coverage correlation\n(Pearson's $r$)"
        ylabel = 'Scaffold length (kbp)'

        pts = self.data_pts(genome_scaffold_stats, mean_coverage)

        scatter, x, y, plot_labels = self.scatter(axes_scatter,
                                                     pts,
                                                     highlight_scaffold_ids,
                                                     link_scaffold_ids,
                                                     xlabel, 
                                                     ylabel)

        _, ymax = axes_scatter.get_ylim()
        xmin, xmax = axes_scatter.get_xlim()

        # draw vertical line at x=0
        axes_scatter.plot([0, 0], [0, ymax], linestyle='dashed', color=self.axes_colour, lw=1.0, zorder=0)

        # ensure y-axis include zero and covers all sequences
        axes_scatter.set_ylim([0, ymax])

        # ensure x-axis is set appropriately for sequences
        axes_scatter.set_xlim([xmin, max(xmax, max(cov_corrs))])

        # draw vertical line for identifying outliers
        for cov_corr in cov_corrs:
            axes_scatter.plot([cov_corr, cov_corr], [0, ymax], 'r--', lw=1.0, zorder=0)

        # prettify scatterplot
        self.prettify(axes_scatter)

        # tooltips plugin
        if tooltip_plugin:
            tooltip = Tooltip(scatter, labels=plot_labels, hoffset=5, voffset=-15)
            mpld3.plugins.connect(figure, tooltip)

        return scatter, x, y, self.plot_order(plot_labels)
