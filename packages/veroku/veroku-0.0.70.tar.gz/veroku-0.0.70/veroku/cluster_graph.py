from IPython.core.display import Image, display
from graphviz import Graph
import networkx as nx
import numpy as np
from tqdm.auto import tqdm
import time
import pandas as pd
from graphviz import Source

from veroku._cg_helpers._cluster import Cluster
import veroku._cg_helpers._animation as cg_animation
from veroku.factors._factor_utils import get_subset_evidence
import matplotlib.pyplot as plt
from veroku.factors.gaussian import Gaussian


# TODO: optimise _pass_message
# TODO: improve sepsets selection for less loopiness
# TODO: Optimisation: messages from clusters that did not receive any new messages in the previous round, do not need
#  new messages calculated.


def _evidence_reduce_factors(factors, evidence):
    """
    Observe relevant evidence for each factor.
    :param factors:
    :param evidence:
    :return:
    """
    reduced_factors = []
    for i, factor in enumerate(factors):
        if evidence is not None:
            vrs, values = get_subset_evidence(all_evidence_dict=evidence,
                                              subset_vars=factor.var_names)
            if len(vrs) > 0:
                factor = factor.reduce(vrs, values)
        reduced_factors.append(factor.copy())
    return reduced_factors


def make_factor_name(factor):
    return str(factor.var_names).replace("'", '')


def _absorb_subset_factors(factors):
    """
    Absorb any factors that has a scope that is a subset of another factor into such a factor.
    :param factors:
    :return:
    """
    factors_absorbtion_dict = {i: [] for i in range(len(factors))}
    final_graph_cluster_factors = []
    # factors: possibly smaller list of factors after factors which have a scope
    # that is a subset of another factor have been absorbed by the larger one.
    # print(f"Info: Absorbing subset factors. (initial number of factors: {len(factors)})")
    factor_processed_mask = [0] * len(factors)
    for i, factor_i in enumerate(factors):
        if not factor_processed_mask[i]:
            factor_product = factor_i.copy()
            for j, factor_j in enumerate(factors):
                if i != j:
                    if not factor_processed_mask[j]:
                        if set(factor_j.var_names) < set(factor_product.var_names):
                            # print(f'Absorbing {factor_j.var_names} into{factor_product.var_names}')
                            # factors_absorbtion_dict[make_factor_name(factors[i])].append(make_factor_name(factors[j]))
                            try:
                                factor_product = factor_product.multiply(factor_j)
                                factors_absorbtion_dict[i].append(j)
                                factor_processed_mask[j] = 1
                                factor_processed_mask[i] = 1
                            except NotImplementedError:
                                print(f'Warning: could not multiply {type(factor_product)} with {type(factor_j)} (Not Implemented)')
            if factor_processed_mask[i]:
                final_graph_cluster_factors.append(factor_product)
    for i, factor_i in enumerate(factors):  # add remaining factors
        if not factor_processed_mask[i]:
            factor_processed_mask[i] = 1
            final_graph_cluster_factors.append(factor_i)
    assert all(factor_processed_mask), 'Error: Some factors where not included during variable subset processing.'
    return final_graph_cluster_factors, _make_subset_factor_df(factors_absorbtion_dict)


def _make_subset_factor_df(subset_dict):
    """
    Make a ...
    :param subset_dict: (dict) A dictionary mapping factors to factors that have subset scopes
    :return:
    """
    keys = list(subset_dict.keys())
    values = list(subset_dict.values())
    assert(len(keys) == len(values))
    # TODO: This raises different list lengths warning (see below). Investigate this.
    #   VisibleDeprecationWarning: Creating an ndarray from ragged nested sequences...
    data = np.array([keys, values]).T
    df = pd.DataFrame(columns=['factor_index', 'subfactor_indices'],
                      data=data)
    df['num_subfactors'] = df['subfactor_indices'].apply(lambda x: len(x))
    df.sort_values(by='num_subfactors', inplace=True, ascending=False)
    return df


class ClusterGraph(object):
    
    def __init__(self, factors, evidence=None, special_evidence=dict(), make_animation_gif=False, debug=False,
                 disable_tqdm=False, verbose=False):
        """
        Construct a Cluster graph from a list of factors
        :param factors: (list of factors) The factors to construct the graph from
        :param evidence: (dict) evidence dictionary (mapping variable names to values) that should be used to reduce
            factors before building the cluster graph.
        :param special_evidence: (dict) evidence dictionary (mapping variable names to values) that should be used in
            the calculation of messages, and not to reduce factors. This allows factor approximations - such as the
            non-linear Gaussian to be iteratively refined.
        """

        self.full_mp_iters = 0
        self.debug = debug
        self.debug_passed_message_factors = []
        self.num_messages_passed = 0
        self.make_animation_gif = make_animation_gif
        self.special_evidence = special_evidence
        self.disable_tqdm = disable_tqdm
        self.message_passing_index_strings = []
        self.last_passed_message_factors_dict = dict()
        self.verbose = verbose
        # new
        self.last_sent_message_dict = {}  # {(rec_cluster_id1, rec_cluster_id1): msg1, ...}

        self.sync_message_passing_max_distances = None
        self.sync_message_passing_max_distances = None

        all_evidence_vars = set(self.special_evidence.keys())
        if evidence is not None:
            evidence_vars = set(evidence.keys())
            all_evidence_vars = all_evidence_vars.union(evidence_vars)

        prev_time = time.time()
        all_factors_copy = _evidence_reduce_factors(factors, evidence)
        self._conditional_print(f'Debug: Copy factors and reduce evidence time duration: {time.time() - prev_time}')

        prev_time = time.time()
        final_graph_cluster_factors, absorbtion_df = _absorb_subset_factors(all_factors_copy)

        self._conditional_print(f'Debug: Absorbing subset factors time duration: {time.time() - prev_time}')
        self._conditional_print(f"Info: Factor subset factors. (reduced number of factors: {len(final_graph_cluster_factors)}")

        prev_time = time.time()
        clusters = [Cluster(factor, cluster_name_prefix=f'c{i}#') for i, factor in
                    enumerate(final_graph_cluster_factors)]
        self._non_rip_sepsets = {}

        self._conditional_print('Info: Calculating sepsets')

        for i in tqdm(range(len(clusters)), disable=self.disable_tqdm):
            vars_i = clusters[i].var_names
            for j in range(i + 1, len(clusters)):
                vars_j = clusters[j].var_names
                sepset = set(vars_j).intersection(set(vars_i)) - all_evidence_vars
                self._non_rip_sepsets[(i, j)] = sepset
                self._non_rip_sepsets[(j, i)] = sepset
                if len(sepset) > 0:
                    clusters[i].add_neighbour(clusters[j])
        self._clusters = clusters

        #TODO: copy here?
        self._cluster_id_cluster_dict = {c._cluster_id: c for c in self._clusters}

        self._conditional_print(f'Debug: Calculating sepsets time duration: {time.time() - prev_time}')
        self._conditional_print(f'Debug: number of clusters: {len(self._clusters)} (should be {len(final_graph_cluster_factors)})')

        prev_time = time.time()

        self._conditional_print(f'Debug: building graph')
        self._build_graph()
        self._conditional_print(f'Debug: build graph time duration: {time.time() - prev_time}')

        # TODO: consolodate these two, if possible
        self.message_passing_log_df = None
        self.message_passing_animation_frames = []

    def _build_graph(self, rip_sepsets_dict=None):
        """
        Add the cluster sepsets, graphviz graph and animation graph (for message_passing visualisation).
        """
        # Check for non-unique cluster_ids (This should never be the case)
        cluster_ids = self._get_cluster_ids()
        if len(set(cluster_ids)) != len(cluster_ids):
            raise ValueError(f'Non-unique cluster ids: {cluster_ids}')
        # self.graph_animation = Animation()
        self._conditional_print('Info: Building graph.')
        self._graph = Graph(format='png')
        if rip_sepsets_dict is None:
            rip_sepsets_dict = self._get_running_intersection_sepsets()

        self._conditional_print(f'Debug: number of clusters: {len(self._clusters)}')
        for i in tqdm(range(len(self._clusters)), disable=self.disable_tqdm):
            # TODO: add cleaner solution?
            self._clusters[i].remove_all_neighbours()

        for i in tqdm(range(len(self._clusters)), disable=self.disable_tqdm):

            node_i_name = self._clusters[i]._cluster_id
            self._graph.node(name=node_i_name, label=node_i_name, style='filled', fillcolor='white', color='black')
            for j in range(i + 1, len(self._clusters)):

                if (i, j) in rip_sepsets_dict:
                    sepset = rip_sepsets_dict[(i, j)]
                    assert len(sepset) > 0, 'Error: empty sepset'

                    self._clusters[i].add_neighbour(self._clusters[j], sepset=sepset)
                    self._clusters[j].add_neighbour(self._clusters[i], sepset=sepset)
                    node_j_name = self._clusters[j]._cluster_id
                    sepset_node_label = ','.join(sepset)
                    sepset_node_name = cg_animation.make_sepset_node_name(node_i_name, node_j_name)
                    self._graph.node(name=sepset_node_name, label=sepset_node_label, shape='rectangle')
                    self._graph.edge(node_i_name, sepset_node_name, color='black', penwidth='2.0')
                    self._graph.edge(sepset_node_name, node_j_name, color='black', penwidth='2.0')

    def _conditional_print(self, message):
        if self.verbose:
            print(message)

    def _get_cluster_ids(self):
        """
        Get all the ids for all the clusters.
        :return:
        """
        return [cluster.cluster_id for cluster in self._clusters]

    def plot_message_convergence(self, old=False):
        """
        Plot the the KL-divergence between the messages and their previous instances to indicate the message passing
        convergence.
        :param old: Whether or not to use the older function for synchronous message passing convergence.
        :type old: Bool
        """
        if self.sync_message_passing_max_distances:
            assert self.message_passing_log_df is None, 'Error: it seems bot sync and async message passing was run.'
            plt.plot(self.sync_message_passing_max_distances)
        else:
            if old:
                self._plot_message_convergence_old()
            else:
                self._plot_message_convergence_new()

    def _plot_message_convergence_old(self):
        """
        Plot the message passing convergence over the consecutive iterations.
        """
        # TODO: combine with one below - this one gets messed up by inf values
        message_kld_df = self.message_passing_log_df
        columns_mask = message_kld_df.columns.to_series().str.contains('distance_from_previous')
        message_kld_distances_only_df = message_kld_df[message_kld_df.columns[columns_mask]]
        message_kld_distances_only_df.columns = range(message_kld_distances_only_df.shape[1])

        title = 'KL Divegences between Messages and Previous Iteration Messages'
        ax = message_kld_distances_only_df.plot.box(figsize=[20, 10], title=title)
        ax.title.set_size(20)
        ax.set_ylabel('KLD', fontsize=15)
        ax.set_xlabel('message passing iteration', fontsize=15)

    def _plot_message_convergence_new(self, figsize=[10, 5]):
        # TODO: improve this (inf value workaround is a bit hacky)
        df = self.message_passing_log_df
        kl_cols = [col for col in df.columns if 'distance' in col]
        kl_df = df[kl_cols]

        no_inf_df = kl_df.replace([np.inf], 0) * 2
        max_no_inf = np.max(no_inf_df.values)

        no_inf_df = kl_df.replace([-np.inf], 0) * 2
        min_no_inf = np.min(no_inf_df.values)

        inf_to_max_df = kl_df.replace([np.inf], max_no_inf * 2)
        inf_to_max_min_df = inf_to_max_df.replace([-np.inf], min_no_inf * 2)
        data = inf_to_max_min_df.values
        max_kl_div_per_iteration = np.max(data, axis=0)
        plt.figure(figsize=figsize)
        plt.plot(np.log(max_kl_div_per_iteration))
        plt.title('Message Passing Convergence', fontsize=15)
        plt.ylabel('log max message kld')
        plt.xlabel('message passing iteration')

    def _get_unique_vars(self):
        all_vars = []
        for cluster in self._clusters:
            all_vars += (cluster.var_names)
        unique_vars = list(set(all_vars))
        return unique_vars

    def _get_vars_min_spanning_trees(self):
        all_vars = self._get_unique_vars()
        var_graphs = {var: nx.Graph() for var in all_vars}
        num_clusters = len(self._clusters)
        for i in range(num_clusters):
            for j in range(i + 1, num_clusters):
                sepset = self._non_rip_sepsets[(i, j)]
                for var in sepset:
                    var_graphs[var].add_edge(i, j, weight=1)
        var_spanning_trees = dict()
        for var in all_vars:
            var_spanning_trees[var] = nx.minimum_spanning_tree(var_graphs[var])
        return var_spanning_trees

    def _get_running_intersection_sepsets(self):
        edge_sepset_dict = {}
        unique_vars = self._get_unique_vars()
        min_span_trees = self._get_vars_min_spanning_trees()
        self._conditional_print("Info: Getting unique variable spanning trees.")
        for i in tqdm(range(len(unique_vars)), disable=self.disable_tqdm):
            var = unique_vars[i]
            min_span_tree = min_span_trees[var]
            for edge in min_span_tree.edges():
                if edge in edge_sepset_dict:
                    edge_sepset_dict[edge].append(var)
                else:
                    edge_sepset_dict[edge] = [var]
        return edge_sepset_dict

    def show(self):
        self._graph.render('/tmp/test.gv', view=False)
        image = Image('/tmp/test.gv.png')
        display(image)

    def save_graph_image(self, filename):
        """
        Save image of the graph.
        :param filename: The filename of the file.
        """
        # Source(self._graph, filename="/tmp/test.gv", format="png")
        Source(self._graph, filename=filename, format="png")

    def get_factors(self):
        """
        Get the cluster factor for each cluster in the graph
        :return: A list of cluster factors.
        """
        return [cluster._factor.copy() for cluster in self._clusters]

    def get_marginal(self, vrs):
        """
        Search the graph for a specific variable and get that variables marginal (posterior marginal if process_graph
        has been run previously).
        :return: The marginal
        """
        for cluster in self._clusters:
            if set(vrs) <= set(cluster.var_names):
                factor = cluster._factor.copy()
                evidence_vrs, evidence_values = get_subset_evidence(self.special_evidence, factor.var_names)
                if len(evidence_vrs) > 0:
                    factor = factor.reduce(evidence_vrs, evidence_values)
                marginal = factor.marginalize(vrs, keep=True)
                return marginal
        raise ValueError(f'No cluster with variables containing {vrs}')

    def get_posterior_joint(self):
        """
        Get the posterior joint distribution.
        """
        # TODO: add functionality for efficiently getting a posterior marginal over any subset of variables and replace
        #  the get_marginal function above.
        cluster_product = self._clusters[0]._factor.joint_distribution
        for cluster in self._clusters[1:]:
            cluster_product = cluster_product.multiply(cluster._factor.joint_distribution)
        last_passed_message_factors = list(self.last_passed_message_factors_dict.values())
        if len(last_passed_message_factors) == 0:
            assert self.num_messages_passed == 0
            return cluster_product
        message_product = last_passed_message_factors[0]
        for message_factor in last_passed_message_factors[1:]:
            message_product = message_product.multiply(message_factor)
        joint = cluster_product.cancel(message_product)
        return joint

    def _get_factor(self, cluster_id):
        """
        Get the factor associated with a specific cluster.
        :param cluster_id: The id of the cluster of which the factor will be returned.
        :return: The factor.
        """
        print('number of clusters = ', len(self._clusters))
        for cluster in self._clusters:
            print(f'cluster.cluster_id  {cluster.cluster_id} has type {type(cluster.cluster_id)}')
            if cluster.cluster_id == cluster_id:
                return cluster._factor.copy()
        raise ValueError(f'Could not find cluster with id {cluster_id}')

    def _make_cluster_messages(self, cluster):
        messages = []
        for neighbour_id in cluster.neighbour_ids:
            message = cluster.make_message(neighbour_id, evidence=self.special_evidence)
            messages.append(message)
        return messages

    def _make_all_messages(self):
        """
        Iterate through all clusters and make messages to all the neighbours of a cluster for each of
        the clusters.
        """
        self.full_mp_iters += 1
        all_messages = []

        for cluster in self._clusters:
            cluster_messages = self._make_cluster_messages(cluster)
            all_messages += cluster_messages
        return all_messages

    def _make_clusters_messages_dict(self):
        """
        Iterate through all clusters and make messages to all the neighbours of a cluster for each of
        the clusters.
        :return: A dictionary of cluster_id's mapped to the messages from the respective clusters.
        :rtype: dict
        """
        self.full_mp_iters += 1
        clusters_messages_dict = dict()
        for cluster in self._clusters:
            cluster_messages = self._make_cluster_messages(cluster)
            clusters_messages_dict[cluster.cluster_id] = cluster_messages
        return clusters_messages_dict

    def _get_ranked_message_df(self, previous_message_df=None):
        """
        Get a dataframe containing message objects, their sender and receiver cluster ids, and the distance from their
        previous iterations.
        :param previous_message_df: The message dataframe to use to compute the distances
            (distance from vacuous will be used if this is None)
        :return: The ranked message dataframe sorted by the distance_from_previous column (from high to low)
        """
        messages = self._make_all_messages()
        factors_are_vacuous = [message.factor.is_vacuous for message in messages]
        if all(factors_are_vacuous) and self.verbose:
            print('Warning: All messages are vacuous')
        if len(messages) == 0:
            raise ValueError('no messages to send.')
        message_dict = {'message_object': [], 'message_scope': [], 'sender_id': [], 'receiver_id': [],
                        'distance_from_previous': []}
        for msg in messages:
            message_dict['message_object'].append(msg)
            message_dict['message_scope'].append(msg.var_names)
            message_dict['sender_id'].append(msg.sender_id)
            message_dict['receiver_id'].append(msg.receiver_id)
            if previous_message_df is None:
                # We imagine that vacuous messages were sent at step -1.
                distance = msg.distance_from_vacuous()
            else:
                mask = (previous_message_df['sender_id'] == msg.sender_id) & \
                       (previous_message_df['receiver_id'] == msg.receiver_id)
                previous_msg_list = previous_message_df[mask]['message_object'].values
                assert len(previous_msg_list) == 1, 'Something strange'
                previous_msg = previous_msg_list[0]
                distance = msg.distance_from_other(previous_msg)

            message_dict['distance_from_previous'].append(distance)
        ranked_message_df = pd.DataFrame(message_dict)
        ranked_message_df.sort_values(by='distance_from_previous', ascending=False, inplace=True)

        # debug only
        sorted_index_list = ranked_message_df.sort_values(by='distance_from_previous').index.tolist()

        message_passing_index_string = ''.join([str(i) for i in sorted_index_list])
        self.message_passing_index_strings.append(message_passing_index_string)

        return ranked_message_df

    def _process_graph_async(self, tol, max_iter):
        """
        Perform message passing until convergence (or maximum iterations).
        """
        if len(self._clusters) == 1:
            # The Cluster Graph contains only single cluster. Message passing not possible or necessary.
            self._clusters[0]._factor = self._clusters[0]._factor.reduce(vrs=self.special_evidence.keys(),
                                                                         values=self.special_evidence.values())
            return

        max_message_distance = float('inf')
        previous_message_df = None

        print('Info: Starting iterative message passing.*')
        for iterations in tqdm(range(max_iter), disable=self.disable_tqdm):
            self._conditional_print(f'iteration: {iterations}/{max_iter}')
            if max_message_distance < tol:
                self._conditional_print(f'Info: max_message_distance={max_message_distance} < tol={tol}. Stopping.')
                break

            ranked_message_df = self._get_ranked_message_df(previous_message_df)
            for indx, message_row in ranked_message_df.iterrows():
                message = message_row['message_object']
                distance_from_previous = message_row.iloc[-1]
                if distance_from_previous < 0.0:
                    raise ValueError('Distance from previous message is negative.')
                # TODO: correct this: if the message is not passed, it must not be included in new_message_distances_df
                if distance_from_previous >= tol:
                    if self.debug:
                        print(f'\n {message.sender_id} -> {message.receiver_id}\t\t\t(dfp: {distance_from_previous})')
                        if isinstance(message.factor, Gaussian):
                            message.factor.show(update_covform=False, show_canform=True)
                        else:
                            message.factor.show()
                        self.debug_passed_message_factors.append(message._factor.copy())
                    self._pass_message(message)
                    self.num_messages_passed += 1

            if self.num_messages_passed == 0:
                self._conditional_print('Warning: no messages passed.')
            max_message_distance = ranked_message_df['distance_from_previous'].max()
            previous_message_df = ranked_message_df

            new_message_distances_df = ranked_message_df.loc[:, ranked_message_df.columns != 'message_object']
            if iterations == 0:
                self.message_passing_log_df = new_message_distances_df
            else:
                self.message_passing_log_df = pd.merge(left=self.message_passing_log_df,
                                                       right=new_message_distances_df,
                                                       on=['sender_id', 'receiver_id'],
                                                       suffixes=('', f'_iter_{iterations}'))
        self._conditional_print(f'Info: num_messages_passed = {self.num_messages_passed}')
        if self.make_animation_gif:
            self._make_message_passing_animation_gif()

    def _get_most_informative_message(self, messages):
        """
        Find and remove the most informative message from a list of messages.
        :return: The message with the highest KL between its current and previous iteration (if more than one, only the
         last calculated is returned) and the distance from the previous iteration.
        :rtype: Message, float
        """
        factors_are_vacuous = [message.factor.is_vacuous for message in messages]
        if all(factors_are_vacuous) and self.verbose:
            print('Warning: All messages are vacuous')
        if len(messages) == 0:
            raise ValueError('no messages to send.')

        max_distance = -np.inf
        max_distance_message = None
        distances = []
        for i, msg in enumerate(messages):
            if (msg.sender_id, msg.receiver_id) not in self.last_passed_message_factors_dict:
                # We imagine that vacuous messages were sent at step -1.
                distance = msg.factor.distance_from_vacuous()
            else:
                previous_msg_factor = self.last_passed_message_factors_dict[(msg.sender_id, msg.receiver_id)]
                distance = previous_msg_factor.kl_divergence(msg.factor)
            distances.append(distance)
            if distance > max_distance:
                max_distance_message = msg
                max_distance = distance

        return max_distance_message, max_distance

    def process_graph(self, tol=1e-3, max_iter=50, sync=True):
        """
        Process the graph by performing message passing until convergece.
        :param bool sync: Whether or not to use a synchronous message passing (asynchronous message passing used if False)
        """
        if sync:
            self._process_graph_sync(tol=tol, max_iter=max_iter)
        else:
            self._process_graph_async(tol=tol, max_iter=max_iter)

    # New Synchronous version
    #  TODO: make this more efficient, if no messages have been received by a cluster in the previous round, the next
    #        message iterations from that cluster will be the same.
    def _process_graph_sync(self, tol, max_iter):
        """
        Perform synchronous message passing until convergence (or maximum iterations).
        """
        self.sync_message_passing_max_distances = []
        if len(self._clusters) == 1:
            # The Cluster Graph contains only single cluster. Message passing not possible or necessary.
            self._clusters[0]._factor = self._clusters[0]._factor.reduce(vrs=self.special_evidence.keys(),
                                                                         values=self.special_evidence.values())
            return

        print('Info: Starting iterative message passing.*')
        cluster_messages_dict = self._make_clusters_messages_dict()

        for iterations in tqdm(range(max_iter), disable=self.disable_tqdm):

            self._conditional_print(f'iteration: {iterations}/{max_iter}')
            messages = sum(cluster_messages_dict.values(), [])
            message, distance_from_previous = self._get_most_informative_message(messages)
            self.sync_message_passing_max_distances.append(distance_from_previous)
            if distance_from_previous < tol:
                self._conditional_print(f'Info: distance_from_previous={distance_from_previous} < tol={tol}. Stopping.')
                break
            self._pass_message(message)
            # recompute the messages for the cluster that received the message
            cluster_that_received_msg = self._cluster_id_cluster_dict[message.receiver_id]
            cluster_messages_dict[message.receiver_id] = self._make_cluster_messages(cluster_that_received_msg)
            self.num_messages_passed += 1
            if self.num_messages_passed == 0:
                self._conditional_print('Warning: no messages passed.')

        self._conditional_print(f'Info: num_messages_passed = {self.num_messages_passed}')
        if self.make_animation_gif:
            self._make_message_passing_animation_gif()

    def _pass_message(self, message):
        """
        Pass message to the relevant receiver.
        :param message: The message to pass
        """
        receiver_cluster_id = message.receiver_id
        for cluster in self._clusters:
            if receiver_cluster_id == cluster.cluster_id:
                error_msg = f'Error: {message.var_names} is not a subset of {cluster.var_names}'
                assert set(message.var_names) <= set(cluster.var_names), error_msg
                cluster.receive_message(message)
                self.last_passed_message_factors_dict[(message.sender_id, message.receiver_id)] = message.factor.copy()
                if self.make_animation_gif:
                    cg_animation.add_message_pass_animation_frames(graph=self._graph,
                                                                   frames=self.message_passing_animation_frames,
                                                                   node_a_name=message.sender_id,
                                                                   node_b_name=receiver_cluster_id)

    def _make_message_passing_animation_gif(self):
        print('Making message passing animation.')
        self.message_passing_animation_frames[0].save(fp='./graph_animation.gif',
                                                      format='GIF',
                                                      append_images=self.message_passing_animation_frames[1:],
                                                      save_all=True, duration=400, loop=0)

    @property
    def graph(self):
        return self._graph
