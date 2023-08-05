import pysubgroup as ps

from itertools import chain
from heapq import heappop, heappush
import random
import numpy as np
from pysubgroup import defaultdict


def encode_subgroup(decoded_subgroup):

    # score = decodedSubgroup['score']

    conjunction = []
    for cond in decoded_subgroup['conditions'].values():

        attribute_name = cond['attribute_name']
        selector_type = cond['selector_type']

        if selector_type == 'IntervalSelector':
            conjunction.append(ps.subgroup_description.IntervalSelector(attribute_name,
                               lower_bound=cond['lower_bound'],
                               upper_bound=cond['upper_bound']))
        elif selector_type == 'EqualitySelector':
            conjunction.append(ps.subgroup_description.EqualitySelector(attribute_name,
                               attribute_value=cond['attribute_value']))
        else:
            msg = "Unknown pysubgroup Selector type"
            raise ValueError(msg)

    subgroup = ps.subgroup_description.Conjunction(conjunction)

    return subgroup


def decode_subgroup(subgroup):

    decoded_subgroup = {'description': str(subgroup[1]), 'conditions': {}, 'score': subgroup[0]}

    for i in range(len(subgroup[1]._selectors)):

        condition = subgroup[1]._selectors[i]

        decoded_subgroup['conditions'].update({i: {'attribute_name': condition._attribute_name}})

        if issubclass(type(condition), ps.subgroup_description.IntervalSelector):
            decoded_subgroup['conditions'][i].update({'lower_bound': condition._lower_bound,
                                                      'upper_bound': condition._upper_bound})

            selector_type = 'IntervalSelector'
        elif issubclass(type(condition), ps.subgroup_description.EqualitySelector):
            decoded_subgroup['conditions'][i].update({'attribute_value': condition._attribute_value})

            selector_type = 'EqualitySelector'

        decoded_subgroup['conditions'][i].update({'selector_type': selector_type})

    return decoded_subgroup

# Extending the class pysubgroup

# Create a new Numeric QM by cloning the StandardQFNumeric and then define the differences


setattr(ps, 'AbsoluteQFNumeric', ps.StandardQFNumeric)


def standard_qf_numeric(a, _, mean_dataset, instances_subgroup, mean_sg):
    return instances_subgroup ** a * np.abs(mean_sg - mean_dataset)


setattr(ps.AbsoluteQFNumeric, 'standard_qf_numeric', standard_qf_numeric)


class StaticSpecializationOperator2:
    """
        This StaticSpecializationOperator is the same as the original
        but it creates a search space that is more fine grained per attribute
        (for this reason is much slower)
    """
    def __init__(self, selectors):
        search_space_dict = defaultdict(list)
        for selector in selectors:
            search_space_dict[selector.__repr__()].append(selector)
        self.search_space = list(search_space_dict.values())
        self.search_space_index = {key: i for i, key in enumerate(search_space_dict.keys())}

    def refinements(self, subgroup):
        if subgroup.depth > 0:
            index_of_last = self.search_space_index[subgroup._selectors[-1].__repr__()]
            new_selectors = chain.from_iterable(self.search_space[index_of_last + 1:])
        else:
            new_selectors = chain.from_iterable(self.search_space)

        return (subgroup & sel for sel in new_selectors)


setattr(ps, 'StaticSpecializationOperator2', StaticSpecializationOperator2)


class BestFirstSearch2:
    """
    This BestfirstSearch is the same as the original
    but it used StaticSpecializationOperator2() instead of StaticSpecializationOperator()
    """
    def execute(self, task):
        result = []
        queue = [(float("-inf"), ps.Conjunction([]))]
        operator = ps.StaticSpecializationOperator2(task.search_space)
        task.qf.calculate_constant_statistics(task.data, task.target)
        while queue:
            q, old_description = heappop(queue)
            q = -q
            if not q > ps.minimum_required_quality(result, task):
                break
            for candidate_description in operator.refinements(old_description):
                sg = candidate_description
                statistics = task.qf.calculate_statistics(sg, task.target, task.data)
                ps.add_if_required(result, sg, task.qf.evaluate(sg, task.target, task.data, statistics), task, statistics=statistics)
                if len(candidate_description) < task.depth:
                    optimistic_estimate = task.qf.optimistic_estimate(sg, task.target, task.data, statistics)

                    # compute refinements and fill the queue
                    if optimistic_estimate >= ps.minimum_required_quality(result, task):
                        if ps.constraints_satisfied(task.constraints_monotone, candidate_description, statistics, task.data):
                            heappush(queue, (-optimistic_estimate, candidate_description))

        result.sort(key=lambda x: x[0], reverse=True)
        return ps.SubgroupDiscoveryResult(result, task)


setattr(ps, 'BestFirstSearch2', BestFirstSearch2)


class StaticSpecializationOperator3:
    """
        This StaticSpecializationOperator is the same as the original
        but it searches for subsets of the attribute, as given by max_features
    """
    def __init__(self, selectors, max_features=None):
        self.search_space_dict = defaultdict(list)
        self.search_space_attributes = defaultdict(list)
        for i, selector in enumerate(selectors):
            self.search_space_dict[selector.__repr__()].append(selector)
            self.search_space_attributes[selector.attribute_name].append([selector])
        self.search_space = list(self.search_space_dict.values())
        self.search_space_index = {key: i for i, key in enumerate(self.search_space_dict.keys())}
        self.search_space_attributes_index = {key: i for i, key in enumerate(self.search_space_attributes.keys())}
        self.max_features = max_features

    def refinements(self, subgroup):
        search_space = self.search_space

        if self.max_features:
            if self.max_features > 0:
                search_space_ids = random.sample(list(self.search_space_attributes_index), self.max_features)
                search_space = [self.search_space_attributes[i] for i in search_space_ids]
            else:
                msg = "'max_features' must be an int > 0 "
                raise ValueError(msg)

        elif subgroup.depth > 0:
            index_of_last = self.search_space_index[subgroup.__repr__()]
            search_space = search_space[index_of_last + 1:]

        new_selectors = chain.from_iterable(search_space)

        return (subgroup & sel for sel in new_selectors)


setattr(ps, 'StaticSpecializationOperator3', StaticSpecializationOperator3)


class BestFirstSearch3:
    """
    This BestfirstSearch is the same as the original
    but it used StaticSpecializationOperator3() instead of StaticSpecializationOperator()
    """
    def __init__(self,
                 max_features=None):
        self.max_features = max_features

    def execute(self, task):
        result = []
        queue = [(float("-inf"), ps.Conjunction([]))]
        operator = ps.StaticSpecializationOperator3(task.search_space, max_features=self.max_features)
        task.qf.calculate_constant_statistics(task.data, task.target)
        while queue:
            q, old_description = heappop(queue)
            q = -q
            if not q > ps.minimum_required_quality(result, task):
                break
            for candidate_description in operator.refinements(old_description):
                sg = candidate_description
                statistics = task.qf.calculate_statistics(sg, task.target, task.data)
                ps.add_if_required(result, sg, task.qf.evaluate(sg, task.target, task.data, statistics), task,
                                   statistics=statistics)
                if len(candidate_description) < task.depth:
                    optimistic_estimate = task.qf.optimistic_estimate(sg, task.target, task.data, statistics)

                    # compute refinements and fill the queue
                    if optimistic_estimate >= ps.minimum_required_quality(result, task):
                        if ps.constraints_satisfied(task.constraints_monotone, candidate_description, statistics,
                                                    task.data):
                            heappush(queue, (-optimistic_estimate, candidate_description))

        result.sort(key=lambda x: x[0], reverse=True)
        return ps.SubgroupDiscoveryResult(result, task)


setattr(ps, 'BestFirstSearch3', BestFirstSearch3)


# class MyQualityFunction:
#     def calculate_constant_statistics(self, task):
#         """ calculate_constant_statistics
#         This function is called once for every execution,
#         it should do any preparation that is necessary prior to an execution.
#         """
#         pass
#
#     def calculate_statistics(self, subgroup, data=None):
#         """ calculates necessary statistics
#         this statistics object is passed on to the evaluate
#         and optimistic_estimate functions
#         """
#         pass
#
#     def evaluate(self, subgroup, statistics_or_data=None):
#         """ return the quality calculated from the statistics """
#         pass
#
#     def optimistic_estimate(self, subgroup, statistics=None):
#         """ returns optimistic estimate
#         if one is available return it otherwise infinity"""
#         pass

from sklearn.metrics import mutual_info_score
from collections import namedtuple


def kl_divergence(data_target, subgroup_target):
    epsilon = 0.00001

    pk = np.histogram(data_target)[0] + epsilon
    pk = pk / sum(pk)
    qk = np.histogram(subgroup_target)[0] + epsilon
    qk = qk / sum(qk)
    return np.sum(pk * np.log(pk / qk))


class KLDivergenceNumeric(ps.BoundedInterestingnessMeasure):
    tpl = namedtuple('KLDivergenceNumeric_parameters', ('size', 'target', 'estimate'))
    @staticmethod
    def weighted_mutual_info_score(a, _, target_dataset, instances_subgroup, target_subgroup):
        return instances_subgroup ** a * kl_divergence(target_dataset, target_subgroup)
        # return instances_subgroup ** a * (mean_sg - mean_dataset)

    def __init__(self, a, invert=False):
        self.a = a
        self.invert = invert
        self.required_stat_attrs = ('size', 'mean')
        self.dataset_statistics = None
        self.all_target_values = None
        self.has_constant_statistics = False
        # self.estimator = KLDivergenceNumeric.KLEstimator(self)

    def calculate_constant_statistics(self, data, target):
        # data = self.estimator.get_data(data, target)
        self.all_target_values = data[target.target_variable].to_numpy()
        data_size = len(data)
        target_data = self.all_target_values
        self.dataset_statistics = KLDivergenceNumeric.tpl(data_size, target_data, None)
        self.has_constant_statistics = True

    def evaluate(self, subgroup, target, data, statistics=None):
        cover_arr, sg_size = ps.get_cover_array_and_size(subgroup, len(self.all_target_values), data)
        if sg_size > 0:
            sg_target_values = self.all_target_values[cover_arr]
        else:
            sg_target_values = []
        # statistics = self.ensure_statistics(subgroup, target, data, statistics)
        dataset = self.dataset_statistics
        return KLDivergenceNumeric.weighted_mutual_info_score(self.a, dataset.size, dataset.target, sg_size,
                                                     sg_target_values)

    def calculate_statistics(self, subgroup, target, data, statistics=None):
        cover_arr, sg_size = ps.get_cover_array_and_size(subgroup, len(self.all_target_values), data)
        if sg_size > 0:
            sg_target_values = self.all_target_values[cover_arr]
            # sg_mean = np.mean(sg_target_values)
            # estimate = self.estimator.get_estimate(subgroup, sg_size, sg_mean, cover_arr, sg_target_values)
            estimate = float('inf')
        else:
            sg_target_values = []
            estimate = float('-inf')
        return KLDivergenceNumeric.tpl(sg_size, sg_target_values, estimate)

    def optimistic_estimate(self, subgroup, target, data, statistics=None):
        statistics = self.ensure_statistics(subgroup, target, data, statistics)
        return statistics.estimate
        # return float('-inf')


    # class KLEstimator:
    #     def __init__(self, qf):
    #         self.qf = qf
    #         self.indices_greater_mean = None
    #         self.target_values_greater_mean = None

        # def get_data(self, data, target):
        #     return data

        # def calculate_constant_statistics(self, data, target):  # pylint: disable=unused-argument
        #     self.indices_greater_mean = self.qf.all_target_values > self.qf.dataset_statistics.mean
        #     self.target_values_greater_mean = self.qf.all_target_values#[self.indices_greater_mean]

        # def get_estimate(self, subgroup, sg_size, sg_mean, cover_arr, _):  # pylint: disable=unused-argument
            # larger_than_mean = self.target_values_greater_mean[cover_arr][self.indices_greater_mean[cover_arr]]
            # size_greater_mean = len(larger_than_mean)
            # sum_greater_mean = np.sum(larger_than_mean)
            #
            # return sum_greater_mean - size_greater_mean * self.qf.dataset_statistics.mean
            # return float('inf')

setattr(ps, 'KLDivergenceNumeric', KLDivergenceNumeric)

from pysubgroup import NumericTarget
from abc import ABC, abstractmethod

class OldAbstractInterestingnessMeasure(ABC):
    @abstractmethod
    def supports_weights(self):
        pass

    @abstractmethod
    def is_applicable(self, subgroup):
        pass

    def ensure_statistics(self, subgroup, statistics_or_data):
        if not self.has_constant_statistics:
            self.calculate_constant_statistics(subgroup.data)
        if any(not hasattr(statistics_or_data, attr) for attr in self.required_stat_attrs):
            if getattr(subgroup, 'statistics', False):
                return subgroup.statistics
            else:
                return self.calculate_statistics(subgroup, statistics_or_data)
        return statistics_or_data


setattr(ps, 'OldAbstractInterestingnessMeasure', OldAbstractInterestingnessMeasure)


class OldBoundedInterestingnessMeasure(OldAbstractInterestingnessMeasure):
    pass
    #@abstractmethod
    #def optimistic_estimate_from_dataset(self, data, subgroup, weighting_attribute=None):
    #    pass

setattr(ps, 'OldBoundedInterestingnessMeasure', OldBoundedInterestingnessMeasure)


class OldStandardQFNumeric(ps.OldBoundedInterestingnessMeasure):
    tpl = namedtuple('OldStandardQFNumeric_parameters', ('size', 'mean', 'estimate'))
    @staticmethod
    def standard_qf_numeric(a, _, mean_dataset, instances_subgroup, mean_sg):
        # return instances_subgroup ** a * (mean_sg - mean_dataset)
        return instances_subgroup ** a * np.abs(mean_sg - mean_dataset)

    def __init__(self, a, invert=False, estimator='sum'):
        self.a = a
        self.invert = invert
        self.required_stat_attrs = ('size', 'mean')
        self.dataset_statistics = None
        self.all_target_values = None
        self.has_constant_statistics = False
        if estimator == 'sum':
            self.estimator = OldStandardQFNumeric.Summation_Estimator(self)
        elif estimator == 'average':
            self.estimator = OldStandardQFNumeric.Average_Estimator(self)
        elif estimator == 'order':
            self.estimator = OldStandardQFNumeric.Ordering_Estimator(self)
        else:
            self.estimator = estimator
            warnings.warn('estimator is not one of the following: ' + str(['sum', 'average', 'order']))

    def calculate_constant_statistics(self, task):
        if not self.is_applicable(task):
            raise BaseException("Quality measure cannot be used for this target class")
        data = self.estimator.get_data(task)
        self.all_target_values = data[task.target.target_variable].to_numpy()
        target_mean = np.mean(self.all_target_values)
        data_size = len(data)
        self.dataset_statistics  = OldStandardQFNumeric.tpl(data_size, target_mean, None)
        self.estimator.calculate_constant_statistics(task)
        self.has_constant_statistics = True

    def evaluate(self, subgroup, statistics=None):
        statistics = self.ensure_statistics(subgroup, statistics)
        dataset = self.dataset_statistics
        return OldStandardQFNumeric.standard_qf_numeric(self.a, dataset.size, dataset.mean, statistics.size, statistics.mean)

    def calculate_statistics(self, subgroup, data=None):
        if hasattr(subgroup, "representation"):
            cover_arr = np.array(subgroup)
        else:
            cover_arr = subgroup.covers(data)
        sg_size = np.count_nonzero(cover_arr)
        sg_mean = np.array([0])
        sg_target_values = 0
        if sg_size > 0:
            sg_target_values = self.all_target_values[cover_arr]
            sg_mean = np.mean(sg_target_values)
            estimate = self.estimator.get_estimate(subgroup, sg_size, sg_mean, cover_arr, sg_target_values)
        else:
            estimate = float('-inf')
        return OldStandardQFNumeric.tpl(sg_size, sg_mean, estimate)


    def optimistic_estimate(self, subgroup, statistics=None):
        statistics = self.ensure_statistics(subgroup, statistics)
        return statistics.estimate

    def is_applicable(self, subgroup):
        return isinstance(subgroup.target, NumericTarget)

    def supports_weights(self):
        return False

    class Summation_Estimator:
        def __init__(self, qf):
            self.qf = qf
            self.indices_greater_mean = None
            self.target_values_greater_mean = None

        def get_data(self, task):
            return task.data

        def calculate_constant_statistics(self, task):
            self.indices_greater_mean = np.nonzero(self.qf.all_target_values > self.qf.dataset_statistics.mean)[0]
            self.target_values_greater_mean = self.qf.all_target_values[self.indices_greater_mean]

        def get_estimate(self, subgroup, sg_size, sg_mean, cover_arr, _):
            larger_than_mean = self.target_values_greater_mean[cover_arr[self.indices_greater_mean]]
            size_greater_mean = len(larger_than_mean)
            sum_greater_mean = np.sum(larger_than_mean)

            return sum_greater_mean - size_greater_mean * self.qf.dataset_statistics.mean



    class Average_Estimator:
        def __init__(self, qf):
            self.qf = qf
            self.indices_greater_mean = None
            self.target_values_greater_mean = None

        def get_data(self, task):
            return task.data

        def calculate_constant_statistics(self, task):
            self.indices_greater_mean = np.nonzero(self.qf.all_target_values > self.qf.dataset_statistics.mean)[0]
            self.target_values_greater_mean = self.qf.all_target_values[self.indices_greater_mean]

        def get_estimate(self, subgroup, sg_size, sg_mean, cover_arr, _):
            larger_than_mean = self.target_values_greater_mean[cover_arr[self.indices_greater_mean]]
            size_greater_mean = len(larger_than_mean)
            max_greater_mean = np.sum(larger_than_mean)

            return size_greater_mean ** self.qf.a * (max_greater_mean - self.qf.dataset_statistics.mean)

setattr(ps, 'OldStandardQFNumeric', OldStandardQFNumeric)


class OldBestFirstSearch:
    def execute(self, task):
        result = []
        queue = [(float("-inf"), ps.Conjunction([]))]
        operator = ps.StaticSpecializationOperator(task.search_space)
        task.qf.calculate_constant_statistics(task)
        while queue:
            q, old_description = heappop(queue)
            q = -q
            if not (q > ps.minimum_required_quality(result, task)):
                break
            for candidate_description in operator.refinements(old_description):
                sg = candidate_description
                statistics = task.qf.calculate_statistics(sg, task.data)
                ps.add_if_required(result, sg, task.qf.evaluate(sg, statistics), task)
                optimistic_estimate = task.qf.optimistic_estimate(sg, statistics)

                # compute refinements and fill the queue
                if len(candidate_description) < task.depth and optimistic_estimate >= ps.minimum_required_quality(result, task):
                    heappush(queue, (-optimistic_estimate, candidate_description))

        result.sort(key=lambda x: x[0], reverse=True)
        return ps.SubgroupDiscoveryResult(result, task)

setattr(ps, 'OldBestFirstSearch', OldBestFirstSearch)


