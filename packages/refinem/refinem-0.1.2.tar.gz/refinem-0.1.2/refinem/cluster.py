###############################################################################
#
# binStatistics.py - calculate statistics for each putative genome bin
#
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

import os
import logging

from numpy import (where as np_where,
                   mean as np_mean,
                   reshape as np_reshape,
                   array as np_array,
                   append as np_append,
                   ones as np_ones,
                   zeros as np_zeros,
                   all as np_all)

from biolib.common import remove_extension
from biolib.pca import PCA
import biolib.seq_io as seq_io
from biolib.genomic_signature import GenomicSignature

from scipy.cluster.vq import whiten, kmeans2, ClusterError


class Cluster():
    """Partition genome into distinct clusters."""

    def __init__(self, cpus):
        """Initialization."""

        self.logger = logging.getLogger('timestamp')
        self.reporter = logging.getLogger('no_timestamp')

        self.cpus = cpus

    def pca(self, data_matrix):
        """Perform PCA.

        Principal components are given in self.pca,
        and the variance in self.variance.

        Parameters
        ----------
        data_matrix : list of lists
          List of tetranucleotide signatures
        """

        cols = len(data_matrix[0])
        data_matrix = np_reshape(np_array(data_matrix), (len(data_matrix), cols))

        pca = PCA()
        pc, variance = pca.pca_matrix(data_matrix, 3, bCenter=True, bScale=False)

        # ensure pc matrix has at least 3 dimensions
        if pc.shape[1] == 1:
            pc = np_append(pc, np_zeros((pc.shape[0], 2)), 1)
            variance = np_append(variance[0], np_ones(2))
        elif pc.shape[1] == 2:
            pc = np_append(pc, np_zeros((pc.shape[0], 1)), 1)
            variance = np_append(variance[0:2], np_ones(1))

        return pc, variance

    def kmeans(self, 
                scaffold_stats, 
                num_clusters, 
                num_components, 
                K, 
                no_coverage, 
                no_pca,
                iterations,
                genome_file, 
                output_dir):
        """Cluster genome with k-means.

        Parameters
        ----------
        scaffold_stats : ScaffoldStats
            Statistics for individual scaffolds.
        num_clusters : int
            Number of cluster to form.
        num_components : int
            Number of PCA components to consider.
        K : int
            K-mer size to use for calculating genomic signature
        no_coverage : boolean
            Flag indicating if coverage information should be used during clustering.
        no_pca : boolean
            Flag indicating if PCA of genomic signature should be calculated.
        iterations: int
            iterations to perform during clustering
        genome_file : str
            Sequences being clustered.
        output_dir : str
            Directory to write results.
        """

        # get GC and mean coverage for each scaffold in genome
        self.logger.info('Determining mean coverage and genomic signatures.')
        signatures = GenomicSignature(K)
        genome_stats = []
        signature_matrix = []
        seqs = seq_io.read(genome_file)
        for seq_id, seq in seqs.items():
            stats = scaffold_stats.stats[seq_id]

            if not no_coverage:
                genome_stats.append((np_mean(stats.coverage)))
            else:
                genome_stats.append(())

            if K == 0:
                pass
            elif K == 4:
                signature_matrix.append(stats.signature)
            else:
                sig = signatures.seq_signature(seq)
                total_kmers = sum(sig)
                for i in range(0, len(sig)):
                    sig[i] = float(sig[i]) / total_kmers
                signature_matrix.append(sig)

        # calculate PCA of signatures
        if K != 0:
            if not no_pca:
                self.logger.info('Calculating PCA of genomic signatures.')
                pc, variance = self.pca(signature_matrix)
                self.logger.info('First {:,} PCs capture {:.1f}% of the variance.'.format(num_components, sum(variance[0:num_components]) * 100))
    
                for i, stats in enumerate(genome_stats):
                    genome_stats[i] = np_append(stats, pc[i][0:num_components])
            else:
                self.logger.info('Using complete genomic signature.')
                for i, stats in enumerate(genome_stats):
                    genome_stats[i] = np_append(stats, signature_matrix[i])

        # whiten data if feature matrix contains coverage and genomic signature data
        if not no_coverage and K != 0:
            self.logger.info('Whitening data.')
            genome_stats = whiten(genome_stats)
        else:
            genome_stats = np_array(genome_stats)

        # cluster
        self.logger.info('Partitioning genome into {:,} clusters.'.format(num_clusters))

        bError = True
        while bError:
            try:
                bError = False
                _centroids, labels = kmeans2(genome_stats, num_clusters, iterations, minit='points', missing='raise')
            except ClusterError:
                bError = True

        for k in range(num_clusters):
            self.logger.info('Placed {:,} sequences in cluster {:,}.'.format(sum(labels == k), (k + 1)))

        # write out clusters
        genome_id = remove_extension(genome_file)
        for k in range(num_clusters):
            fout = open(os.path.join(output_dir, genome_id + '_c%d' % (k + 1) + '.fna'), 'w')
            for i in np_where(labels == k)[0]:
                seq_id = seqs.keys()[i]
                fout.write('>' + seq_id + '\n')
                fout.write(seqs[seq_id] + '\n')
            fout.close()
            
    def dbscan(self, scaffold_stats, num_clusters, num_components, K, no_coverage, no_pca, iterations, genome_file, output_dir):
        """Cluster genome with DBSCAN.

        Parameters
        ----------
        scaffold_stats : ScaffoldStats
            Statistics for individual scaffolds.
        num_clusters : int
            Number of cluster to form.
        num_components : int
            Number of PCA components to consider.
        K : int
            K-mer size to use for calculating genomic signature.
        no_coverage : boolean
            Flag indicating if coverage information should be used during clustering.
        no_pca : boolean
            Flag indicating if PCA of genomic signature should be calculated.
        iterations : int
            Iterations of clustering to perform.
        genome_file : str
            Sequences being clustered.
        output_dir : str
            Directory to write results.
        """
        
        pass
        
    def split(self, scaffold_stats, criteria1, criteria2, genome_file, output_dir):
        """Split genome into two based ongenomic feature.

        Parameters
        ----------
        scaffold_stats : ScaffoldStats
            Statistics for individual scaffolds.
        criteria1 : str
            First criteria used for splitting genome.
        criteria2 : str
           Second criteria used for splitting genome.
        genome_file : str
            Sequences being clustered.
        output_dir : str
            Directory to write results.
        """
        
        seqs = seq_io.read(genome_file)
        
        # calculate PCA if necessary
        if 'pc' in criteria1 or 'pc' in criteria2:
            self.logger.info('Performing PCA.')
            signatures = GenomicSignature(K)
            signature_matrix = []
            seqs = seq_io.read(genome_file)
            for seq_id, seq in seqs.items():
                stats = scaffold_stats.stats[seq_id]

                signature_matrix.append(stats.signature)

            pc, _variance = self.pca(signature_matrix)
            for i, seq_id in enumerate(seqs):
                scaffold_stats.stats[seq_id].pc1 = pc[i][0]
                scaffold_stats.stats[seq_id].pc2 = pc[i][1]
                scaffold_stats.stats[seq_id].pc3 = pc[i][2]
                
        # split bin
        genome_id = remove_extension(genome_file)
        fout1 = open(os.path.join(output_dir, genome_id + '_c1.fna'), 'w')
        fout2 = open(os.path.join(output_dir, genome_id + '_c2.fna'), 'w')

        for seq_id, seq in seqs.items():
            stats = scaffold_stats.stats[seq_id]
            
            meet_criteria = True
            for criteria in [criteria1, criteria2]:
                if 'gc' in criteria:
                    v = eval(criteria.replace('gc', str(stats.gc)), {"__builtins__": {}})
                elif 'coverage' in criteria:
                    v = eval(criteria.replace('coverage', str(stats.coverage)), {"__builtins__": {}})
                elif 'pc1' in criteria:
                    v = eval(criteria.replace('pc1', str(stats.pc1)), {"__builtins__": {}})
                elif 'pc2' in criteria:
                    v = eval(criteria.replace('pc2', str(stats.pc2)), {"__builtins__": {}})
                elif 'pc3' in criteria:
                    v = eval(criteria.replace('pc3', str(stats.pc3)), {"__builtins__": {}})
                    
                meet_criteria = meet_criteria and v
            
            if meet_criteria:
                fout1.write('>' + seq_id + '\n')
                fout1.write(seqs[seq_id] + '\n')
            else:
                fout2.write('>' + seq_id + '\n')
                fout2.write(seqs[seq_id] + '\n')
            
        fout1.close()
        fout2.close()        
