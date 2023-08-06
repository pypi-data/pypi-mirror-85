# -*- coding: utf-8 -*-

from elasticsearch.client.indices import IndicesClient
from elasticsearch.client.utils import query_params


class FakeIndicesClient(IndicesClient):

    @query_params('master_timeout', 'timeout')
    def create(self, index, body=None, params=None, headers=None):
        documents_dict = self.__get_documents_dict()
        if index not in documents_dict:
            documents_dict[index] = []

    @query_params('allow_no_indices', 'expand_wildcards', 'ignore_unavailable',
                  'local')
    def exists(self, index, params=None, headers=None):
        return index in self.__get_documents_dict()

    @query_params('allow_no_indices', 'expand_wildcards', 'force',
                  'ignore_unavailable', 'operation_threading')
    def refresh(self, index=None, params=None, headers=None):
        pass

    @query_params('master_timeout', 'timeout')
    def delete(self, index, params=None, headers=None):
        documents_dict = self.__get_documents_dict()
        if index in documents_dict:
            del documents_dict[index]

    def get_alias(self, prefix=None, params=None, headers=None):
        if prefix == "infra-*":
            return {
                        "infra-xyz-13-11-2020" : {
                                "filter" : {
                                    "term" : {
                                        "year" : 2020
                                    }
                            }
                        },
                        "infra-xyz-20-10-2021" : {
                                "filter" : {
                                    "term" : {
                                        "year" : 2021
                                    }
                            }
                        }
                    }

    def stats(self, index, params=None, headers=None):
        return {
                "uuid": "BLuIqmgBQyaWjfWuQUnX7Q",
                "primaries":
                {
                "docs": { "count": 12759052, "deleted": 0 },
                "store": { "size_in_bytes": 7660909325 },
                "indexing":
                    {
                    "index_total": 12759185,
                    "index_time_in_millis": 14299525,
                    "index_current": 0,
                    "index_failed": 0,
                    "delete_total": 0,
                    "delete_time_in_millis": 0,
                    "delete_current": 0,
                    "noop_update_total": 0,
                    "is_throttled": False,
                    "throttle_time_in_millis": 0,
                    },
                "get":
                    {
                    "total": 0,
                    "time_in_millis": 0,
                    "exists_total": 0,
                    "exists_time_in_millis": 0,
                    "missing_total": 0,
                    "missing_time_in_millis": 0,
                    "current": 0,
                    },
                "search":
                    {
                    "open_contexts": 0,
                    "query_total": 0,
                    "query_time_in_millis": 0,
                    "query_current": 0,
                    "fetch_total": 0,
                    "fetch_time_in_millis": 0,
                    "fetch_current": 0,
                    "scroll_total": 0,
                    "scroll_time_in_millis": 0,
                    "scroll_current": 0,
                    "suggest_total": 0,
                    "suggest_time_in_millis": 0,
                    "suggest_current": 0,
                    },
                "merges":
                    {
                    "current": 0,
                    "current_docs": 0,
                    "current_size_in_bytes": 0,
                    "total": 725,
                    "total_time_in_millis": 2568966,
                    "total_docs": 27087860,
                    "total_size_in_bytes": 16955534376,
                    "total_stopped_time_in_millis": 29857,
                    "total_throttled_time_in_millis": 1805866,
                    "total_auto_throttle_in_bytes": 15728640,
                    },
                "refresh": { "total": 6857, "total_time_in_millis": 421864, "listeners": 0 },
                "flush": { "total": 93, "periodic": 93, "total_time_in_millis": 20599 },
                "warmer": { "current": 0, "total": 6753, "total_time_in_millis": 4228 },
                "query_cache":
                    {
                    "memory_size_in_bytes": 0,
                    "total_count": 0,
                    "hit_count": 0,
                    "miss_count": 0,
                    "cache_size": 0,
                    "cache_count": 0,
                    "evictions": 0,
                    },
                "fielddata": { "memory_size_in_bytes": 0, "evictions": 0 },
                "completion": { "size_in_bytes": 0 },
                "segments":
                    {
                    "count": 74,
                    "memory_in_bytes": 14703764,
                    "terms_memory_in_bytes": 10316907,
                    "stored_fields_memory_in_bytes": 3987208,
                    "term_vectors_memory_in_bytes": 0,
                    "norms_memory_in_bytes": 122624,
                    "points_memory_in_bytes": 256145,
                    "doc_values_memory_in_bytes": 20880,
                    "index_writer_memory_in_bytes": 2039828,
                    "version_map_memory_in_bytes": 20083,
                    "fixed_bit_set_memory_in_bytes": 1598168,
                    "max_unsafe_auto_id_timestamp": -1,
                    "file_sizes": {},
                    },
                "translog":
                    {
                    "operations": 862217,
                    "size_in_bytes": 1705567621,
                    "uncommitted_operations": 45429,
                    "uncommitted_size_in_bytes": 89830471,
                    "earliest_last_modified_age": 0,
                    },
                "request_cache":
                    {
                    "memory_size_in_bytes": 0,
                    "evictions": 0,
                    "hit_count": 0,
                    "miss_count": 0,
                    },
                "recovery":
                    {
                    "current_as_source": 0,
                    "current_as_target": 0,
                    "throttle_time_in_millis": 0,
                    },
                },
                "total":
                {
                "docs": { "count": 25507574, "deleted": 0 },
                "store": { "size_in_bytes": 15521849910 },
                "indexing":
                    {
                    "index_total": 25507892,
                    "index_time_in_millis": 28577184,
                    "index_current": 2,
                    "index_failed": 0,
                    "delete_total": 0,
                    "delete_time_in_millis": 0,
                    "delete_current": 0,
                    "noop_update_total": 0,
                    "is_throttled": False,
                    "throttle_time_in_millis": 0,
                    },
                "get":
                    {
                    "total": 0,
                    "time_in_millis": 0,
                    "exists_total": 0,
                    "exists_time_in_millis": 0,
                    "missing_total": 0,
                    "missing_time_in_millis": 0,
                    "current": 0,
                    },
                "search":
                    {
                    "open_contexts": 0,
                    "query_total": 0,
                    "query_time_in_millis": 0,
                    "query_current": 0,
                    "fetch_total": 0,
                    "fetch_time_in_millis": 0,
                    "fetch_current": 0,
                    "scroll_total": 0,
                    "scroll_time_in_millis": 0,
                    "scroll_current": 0,
                    "suggest_total": 0,
                    "suggest_time_in_millis": 0,
                    "suggest_current": 0,
                    },
                "merges":
                    {
                    "current": 1,
                    "current_docs": 547828,
                    "current_size_in_bytes": 332108527,
                    "total": 1453,
                    "total_time_in_millis": 5151344,
                    "total_docs": 54474787,
                    "total_size_in_bytes": 34097980314,
                    "total_stopped_time_in_millis": 51270,
                    "total_throttled_time_in_millis": 3619556,
                    "total_auto_throttle_in_bytes": 31457280,
                    },
                "refresh":
                    { "total": 13740, "total_time_in_millis": 839446, "listeners": 0 },
                "flush": { "total": 187, "periodic": 187, "total_time_in_millis": 39921 },
                "warmer": { "current": 0, "total": 13534, "total_time_in_millis": 8610 },
                "query_cache":
                    {
                    "memory_size_in_bytes": 0,
                    "total_count": 0,
                    "hit_count": 0,
                    "miss_count": 0,
                    "cache_size": 0,
                    "cache_count": 0,
                    "evictions": 0,
                    },
                "fielddata": { "memory_size_in_bytes": 0, "evictions": 0 },
                "completion": { "size_in_bytes": 0 },
                "segments":
                    {
                    "count": 159,
                    "memory_in_bytes": 29491990,
                    "terms_memory_in_bytes": 20699814,
                    "stored_fields_memory_in_bytes": 7976816,
                    "term_vectors_memory_in_bytes": 0,
                    "norms_memory_in_bytes": 251840,
                    "points_memory_in_bytes": 512148,
                    "doc_values_memory_in_bytes": 51372,
                    "index_writer_memory_in_bytes": 6063988,
                    "version_map_memory_in_bytes": 48018,
                    "fixed_bit_set_memory_in_bytes": 3195472,
                    "max_unsafe_auto_id_timestamp": -1,
                    "file_sizes": {},
                    },
                "translog":
                    {
                    "operations": 1707331,
                    "size_in_bytes": 3377273219,
                    "uncommitted_operations": 142315,
                    "uncommitted_size_in_bytes": 281485673,
                    "earliest_last_modified_age": 0,
                    },
                "request_cache":
                    {
                    "memory_size_in_bytes": 0,
                    "evictions": 0,
                    "hit_count": 0,
                    "miss_count": 0,
                    },
                "recovery":
                    {
                    "current_as_source": 0,
                    "current_as_target": 0,
                    "throttle_time_in_millis": 0,
                    },
                },
                }

    def get(self, index, params=None, headers=None):
        return {
            index: {
                "aliases": {},
                "mappings": {},
                "settings": {
                    "index": {
                        "creation_date": "1429308615170",
                        "number_of_replicas": "1",
                        "number_of_shards": "5",
                        "uuid": "C5sqwXClSFyd5uF3MSrVgg",
                        "version": {
                        "created": "1050199"
                        }
                    }
                },
                "warmers": {}
            }
        }

    def __get_documents_dict(self):
        return self.client._FakeElasticsearch__documents_dict
