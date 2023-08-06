from libc.stdint cimport *
from libc.string cimport *
from cpython.ref cimport PyObject

from pyrobuf_list cimport *
from pyrobuf_util cimport *

import json

cdef class Blob:


    cdef bytes _raw
    cpdef _raw__reset(self)
    cdef int32_t _raw_size
    cpdef _raw_size__reset(self)
    cdef bytes _zlib_data
    cpdef _zlib_data__reset(self)
    cdef bytes _lzma_data
    cpdef _lzma_data__reset(self)
    cdef bytes _OBSOLETE_bzip2_data
    cpdef _OBSOLETE_bzip2_data__reset(self)


    cdef uint64_t __field_bitmap0

    cdef public bint _is_present_in_parent
    cdef bytes _cached_serialization

    cdef object _listener

    cpdef void reset(self)

    cpdef void Clear(self)
    cpdef void ClearField(self, field_name)
    cpdef void CopyFrom(self, Blob other_msg)
    cpdef bint HasField(self, field_name) except -1
    cpdef bint IsInitialized(self)
    cpdef void MergeFrom(self, Blob other_msg)
    cpdef int MergeFromString(self, data, size=*) except -1
    cpdef int ParseFromString(self, data, size=*, bint reset=*, bint cache=*) except -1
    cpdef bytes SerializeToString(self, bint cache=*)
    cpdef bytes SerializePartialToString(self)

    cdef void _clearfield(self, field_name)
    cdef int _protobuf_deserialize(self, const unsigned char *memory, int size, bint cache)

    cdef void _protobuf_serialize(self, bytearray buf, bint cache)

    cpdef void _Modified(self)

cdef class BlobHeader:


    cdef str _type
    cpdef _type__reset(self)
    cdef bytes _indexdata
    cpdef _indexdata__reset(self)
    cdef int32_t _datasize
    cpdef _datasize__reset(self)


    cdef uint64_t __field_bitmap0

    cdef public bint _is_present_in_parent
    cdef bytes _cached_serialization

    cdef object _listener

    cpdef void reset(self)

    cpdef void Clear(self)
    cpdef void ClearField(self, field_name)
    cpdef void CopyFrom(self, BlobHeader other_msg)
    cpdef bint HasField(self, field_name) except -1
    cpdef bint IsInitialized(self)
    cpdef void MergeFrom(self, BlobHeader other_msg)
    cpdef int MergeFromString(self, data, size=*) except -1
    cpdef int ParseFromString(self, data, size=*, bint reset=*, bint cache=*) except -1
    cpdef bytes SerializeToString(self, bint cache=*)
    cpdef bytes SerializePartialToString(self)

    cdef void _clearfield(self, field_name)
    cdef int _protobuf_deserialize(self, const unsigned char *memory, int size, bint cache)

    cdef void _protobuf_serialize(self, bytearray buf, bint cache)

    cpdef void _Modified(self)

cdef class HeaderBlock:


    cdef HeaderBBox _bbox
    cpdef _bbox__reset(self)
    cdef StringList _required_features
    cpdef _required_features__reset(self)
    cdef StringList _optional_features
    cpdef _optional_features__reset(self)
    cdef str _writingprogram
    cpdef _writingprogram__reset(self)
    cdef str _source
    cpdef _source__reset(self)
    cdef int64_t _osmosis_replication_timestamp
    cpdef _osmosis_replication_timestamp__reset(self)
    cdef int64_t _osmosis_replication_sequence_number
    cpdef _osmosis_replication_sequence_number__reset(self)
    cdef str _osmosis_replication_base_url
    cpdef _osmosis_replication_base_url__reset(self)


    cdef uint64_t __field_bitmap0

    cdef public bint _is_present_in_parent
    cdef bytes _cached_serialization

    cdef object _listener

    cpdef void reset(self)

    cpdef void Clear(self)
    cpdef void ClearField(self, field_name)
    cpdef void CopyFrom(self, HeaderBlock other_msg)
    cpdef bint HasField(self, field_name) except -1
    cpdef bint IsInitialized(self)
    cpdef void MergeFrom(self, HeaderBlock other_msg)
    cpdef int MergeFromString(self, data, size=*) except -1
    cpdef int ParseFromString(self, data, size=*, bint reset=*, bint cache=*) except -1
    cpdef bytes SerializeToString(self, bint cache=*)
    cpdef bytes SerializePartialToString(self)

    cdef void _clearfield(self, field_name)
    cdef int _protobuf_deserialize(self, const unsigned char *memory, int size, bint cache)

    cdef void _protobuf_serialize(self, bytearray buf, bint cache)

    cpdef void _Modified(self)

cdef class HeaderBBox:


    cdef int64_t _left
    cpdef _left__reset(self)
    cdef int64_t _right
    cpdef _right__reset(self)
    cdef int64_t _top
    cpdef _top__reset(self)
    cdef int64_t _bottom
    cpdef _bottom__reset(self)


    cdef uint64_t __field_bitmap0

    cdef public bint _is_present_in_parent
    cdef bytes _cached_serialization

    cdef object _listener

    cpdef void reset(self)

    cpdef void Clear(self)
    cpdef void ClearField(self, field_name)
    cpdef void CopyFrom(self, HeaderBBox other_msg)
    cpdef bint HasField(self, field_name) except -1
    cpdef bint IsInitialized(self)
    cpdef void MergeFrom(self, HeaderBBox other_msg)
    cpdef int MergeFromString(self, data, size=*) except -1
    cpdef int ParseFromString(self, data, size=*, bint reset=*, bint cache=*) except -1
    cpdef bytes SerializeToString(self, bint cache=*)
    cpdef bytes SerializePartialToString(self)

    cdef void _clearfield(self, field_name)
    cdef int _protobuf_deserialize(self, const unsigned char *memory, int size, bint cache)

    cdef void _protobuf_serialize(self, bytearray buf, bint cache)

    cpdef void _Modified(self)

cdef class PrimitiveBlock:


    cdef StringTable _stringtable
    cpdef _stringtable__reset(self)
    cdef TypedList _primitivegroup
    cpdef _primitivegroup__reset(self)
    cdef int32_t _granularity
    cpdef _granularity__reset(self)
    cdef int32_t _date_granularity
    cpdef _date_granularity__reset(self)
    cdef int64_t _lat_offset
    cpdef _lat_offset__reset(self)
    cdef int64_t _lon_offset
    cpdef _lon_offset__reset(self)


    cdef uint64_t __field_bitmap0

    cdef public bint _is_present_in_parent
    cdef bytes _cached_serialization

    cdef object _listener

    cpdef void reset(self)

    cpdef void Clear(self)
    cpdef void ClearField(self, field_name)
    cpdef void CopyFrom(self, PrimitiveBlock other_msg)
    cpdef bint HasField(self, field_name) except -1
    cpdef bint IsInitialized(self)
    cpdef void MergeFrom(self, PrimitiveBlock other_msg)
    cpdef int MergeFromString(self, data, size=*) except -1
    cpdef int ParseFromString(self, data, size=*, bint reset=*, bint cache=*) except -1
    cpdef bytes SerializeToString(self, bint cache=*)
    cpdef bytes SerializePartialToString(self)

    cdef void _clearfield(self, field_name)
    cdef int _protobuf_deserialize(self, const unsigned char *memory, int size, bint cache)

    cdef void _protobuf_serialize(self, bytearray buf, bint cache)

    cpdef void _Modified(self)

cdef class PrimitiveGroup:


    cdef TypedList _nodes
    cpdef _nodes__reset(self)
    cdef DenseNodes _dense
    cpdef _dense__reset(self)
    cdef TypedList _ways
    cpdef _ways__reset(self)
    cdef TypedList _relations
    cpdef _relations__reset(self)
    cdef TypedList _changesets
    cpdef _changesets__reset(self)


    cdef uint64_t __field_bitmap0

    cdef public bint _is_present_in_parent
    cdef bytes _cached_serialization

    cdef object _listener

    cpdef void reset(self)

    cpdef void Clear(self)
    cpdef void ClearField(self, field_name)
    cpdef void CopyFrom(self, PrimitiveGroup other_msg)
    cpdef bint HasField(self, field_name) except -1
    cpdef bint IsInitialized(self)
    cpdef void MergeFrom(self, PrimitiveGroup other_msg)
    cpdef int MergeFromString(self, data, size=*) except -1
    cpdef int ParseFromString(self, data, size=*, bint reset=*, bint cache=*) except -1
    cpdef bytes SerializeToString(self, bint cache=*)
    cpdef bytes SerializePartialToString(self)

    cdef void _clearfield(self, field_name)
    cdef int _protobuf_deserialize(self, const unsigned char *memory, int size, bint cache)

    cdef void _protobuf_serialize(self, bytearray buf, bint cache)

    cpdef void _Modified(self)

cdef class StringTable:


    cdef BytesList _s
    cpdef _s__reset(self)


    cdef uint64_t __field_bitmap0

    cdef public bint _is_present_in_parent
    cdef bytes _cached_serialization

    cdef object _listener

    cpdef void reset(self)

    cpdef void Clear(self)
    cpdef void ClearField(self, field_name)
    cpdef void CopyFrom(self, StringTable other_msg)
    cpdef bint HasField(self, field_name) except -1
    cpdef bint IsInitialized(self)
    cpdef void MergeFrom(self, StringTable other_msg)
    cpdef int MergeFromString(self, data, size=*) except -1
    cpdef int ParseFromString(self, data, size=*, bint reset=*, bint cache=*) except -1
    cpdef bytes SerializeToString(self, bint cache=*)
    cpdef bytes SerializePartialToString(self)

    cdef void _clearfield(self, field_name)
    cdef int _protobuf_deserialize(self, const unsigned char *memory, int size, bint cache)

    cdef void _protobuf_serialize(self, bytearray buf, bint cache)

    cpdef void _Modified(self)

cdef class Info:


    cdef int32_t _version
    cpdef _version__reset(self)
    cdef int64_t _timestamp
    cpdef _timestamp__reset(self)
    cdef int64_t _changeset
    cpdef _changeset__reset(self)
    cdef int32_t _uid
    cpdef _uid__reset(self)
    cdef uint32_t _user_sid
    cpdef _user_sid__reset(self)
    cdef bint _visible
    cpdef _visible__reset(self)


    cdef uint64_t __field_bitmap0

    cdef public bint _is_present_in_parent
    cdef bytes _cached_serialization

    cdef object _listener

    cpdef void reset(self)

    cpdef void Clear(self)
    cpdef void ClearField(self, field_name)
    cpdef void CopyFrom(self, Info other_msg)
    cpdef bint HasField(self, field_name) except -1
    cpdef bint IsInitialized(self)
    cpdef void MergeFrom(self, Info other_msg)
    cpdef int MergeFromString(self, data, size=*) except -1
    cpdef int ParseFromString(self, data, size=*, bint reset=*, bint cache=*) except -1
    cpdef bytes SerializeToString(self, bint cache=*)
    cpdef bytes SerializePartialToString(self)

    cdef void _clearfield(self, field_name)
    cdef int _protobuf_deserialize(self, const unsigned char *memory, int size, bint cache)

    cdef void _protobuf_serialize(self, bytearray buf, bint cache)

    cpdef void _Modified(self)

cdef class DenseInfo:


    cdef Int32List _version
    cpdef _version__reset(self)
    cdef Int64List _timestamp
    cpdef _timestamp__reset(self)
    cdef Int64List _changeset
    cpdef _changeset__reset(self)
    cdef Int32List _uid
    cpdef _uid__reset(self)
    cdef Int32List _user_sid
    cpdef _user_sid__reset(self)
    cdef BintList _visible
    cpdef _visible__reset(self)


    cdef uint64_t __field_bitmap0

    cdef public bint _is_present_in_parent
    cdef bytes _cached_serialization

    cdef object _listener

    cpdef void reset(self)

    cpdef void Clear(self)
    cpdef void ClearField(self, field_name)
    cpdef void CopyFrom(self, DenseInfo other_msg)
    cpdef bint HasField(self, field_name) except -1
    cpdef bint IsInitialized(self)
    cpdef void MergeFrom(self, DenseInfo other_msg)
    cpdef int MergeFromString(self, data, size=*) except -1
    cpdef int ParseFromString(self, data, size=*, bint reset=*, bint cache=*) except -1
    cpdef bytes SerializeToString(self, bint cache=*)
    cpdef bytes SerializePartialToString(self)

    cdef void _clearfield(self, field_name)
    cdef int _protobuf_deserialize(self, const unsigned char *memory, int size, bint cache)

    cdef void _protobuf_serialize(self, bytearray buf, bint cache)

    cpdef void _Modified(self)

cdef class ChangeSet:


    cdef int64_t _id
    cpdef _id__reset(self)


    cdef uint64_t __field_bitmap0

    cdef public bint _is_present_in_parent
    cdef bytes _cached_serialization

    cdef object _listener

    cpdef void reset(self)

    cpdef void Clear(self)
    cpdef void ClearField(self, field_name)
    cpdef void CopyFrom(self, ChangeSet other_msg)
    cpdef bint HasField(self, field_name) except -1
    cpdef bint IsInitialized(self)
    cpdef void MergeFrom(self, ChangeSet other_msg)
    cpdef int MergeFromString(self, data, size=*) except -1
    cpdef int ParseFromString(self, data, size=*, bint reset=*, bint cache=*) except -1
    cpdef bytes SerializeToString(self, bint cache=*)
    cpdef bytes SerializePartialToString(self)

    cdef void _clearfield(self, field_name)
    cdef int _protobuf_deserialize(self, const unsigned char *memory, int size, bint cache)

    cdef void _protobuf_serialize(self, bytearray buf, bint cache)

    cpdef void _Modified(self)

cdef class Node:


    cdef int64_t _id
    cpdef _id__reset(self)
    cdef Uint32List _keys
    cpdef _keys__reset(self)
    cdef Uint32List _vals
    cpdef _vals__reset(self)
    cdef Info _info
    cpdef _info__reset(self)
    cdef int64_t _lat
    cpdef _lat__reset(self)
    cdef int64_t _lon
    cpdef _lon__reset(self)


    cdef uint64_t __field_bitmap0

    cdef public bint _is_present_in_parent
    cdef bytes _cached_serialization

    cdef object _listener

    cpdef void reset(self)

    cpdef void Clear(self)
    cpdef void ClearField(self, field_name)
    cpdef void CopyFrom(self, Node other_msg)
    cpdef bint HasField(self, field_name) except -1
    cpdef bint IsInitialized(self)
    cpdef void MergeFrom(self, Node other_msg)
    cpdef int MergeFromString(self, data, size=*) except -1
    cpdef int ParseFromString(self, data, size=*, bint reset=*, bint cache=*) except -1
    cpdef bytes SerializeToString(self, bint cache=*)
    cpdef bytes SerializePartialToString(self)

    cdef void _clearfield(self, field_name)
    cdef int _protobuf_deserialize(self, const unsigned char *memory, int size, bint cache)

    cdef void _protobuf_serialize(self, bytearray buf, bint cache)

    cpdef void _Modified(self)

cdef class DenseNodes:


    cdef Int64List _id
    cpdef _id__reset(self)
    cdef DenseInfo _denseinfo
    cpdef _denseinfo__reset(self)
    cdef Int64List _lat
    cpdef _lat__reset(self)
    cdef Int64List _lon
    cpdef _lon__reset(self)
    cdef Int32List _keys_vals
    cpdef _keys_vals__reset(self)


    cdef uint64_t __field_bitmap0

    cdef public bint _is_present_in_parent
    cdef bytes _cached_serialization

    cdef object _listener

    cpdef void reset(self)

    cpdef void Clear(self)
    cpdef void ClearField(self, field_name)
    cpdef void CopyFrom(self, DenseNodes other_msg)
    cpdef bint HasField(self, field_name) except -1
    cpdef bint IsInitialized(self)
    cpdef void MergeFrom(self, DenseNodes other_msg)
    cpdef int MergeFromString(self, data, size=*) except -1
    cpdef int ParseFromString(self, data, size=*, bint reset=*, bint cache=*) except -1
    cpdef bytes SerializeToString(self, bint cache=*)
    cpdef bytes SerializePartialToString(self)

    cdef void _clearfield(self, field_name)
    cdef int _protobuf_deserialize(self, const unsigned char *memory, int size, bint cache)

    cdef void _protobuf_serialize(self, bytearray buf, bint cache)

    cpdef void _Modified(self)

cdef class Way:


    cdef int64_t _id
    cpdef _id__reset(self)
    cdef Uint32List _keys
    cpdef _keys__reset(self)
    cdef Uint32List _vals
    cpdef _vals__reset(self)
    cdef Info _info
    cpdef _info__reset(self)
    cdef Int64List _refs
    cpdef _refs__reset(self)


    cdef uint64_t __field_bitmap0

    cdef public bint _is_present_in_parent
    cdef bytes _cached_serialization

    cdef object _listener

    cpdef void reset(self)

    cpdef void Clear(self)
    cpdef void ClearField(self, field_name)
    cpdef void CopyFrom(self, Way other_msg)
    cpdef bint HasField(self, field_name) except -1
    cpdef bint IsInitialized(self)
    cpdef void MergeFrom(self, Way other_msg)
    cpdef int MergeFromString(self, data, size=*) except -1
    cpdef int ParseFromString(self, data, size=*, bint reset=*, bint cache=*) except -1
    cpdef bytes SerializeToString(self, bint cache=*)
    cpdef bytes SerializePartialToString(self)

    cdef void _clearfield(self, field_name)
    cdef int _protobuf_deserialize(self, const unsigned char *memory, int size, bint cache)

    cdef void _protobuf_serialize(self, bytearray buf, bint cache)

    cpdef void _Modified(self)

cdef class Relation:


    cdef int64_t _id
    cpdef _id__reset(self)
    cdef Uint32List _keys
    cpdef _keys__reset(self)
    cdef Uint32List _vals
    cpdef _vals__reset(self)
    cdef Info _info
    cpdef _info__reset(self)
    cdef Int32List _roles_sid
    cpdef _roles_sid__reset(self)
    cdef Int64List _memids
    cpdef _memids__reset(self)
    cdef Int32List _types
    cpdef _types__reset(self)


    cdef uint64_t __field_bitmap0

    cdef public bint _is_present_in_parent
    cdef bytes _cached_serialization

    cdef object _listener

    cpdef void reset(self)

    cpdef void Clear(self)
    cpdef void ClearField(self, field_name)
    cpdef void CopyFrom(self, Relation other_msg)
    cpdef bint HasField(self, field_name) except -1
    cpdef bint IsInitialized(self)
    cpdef void MergeFrom(self, Relation other_msg)
    cpdef int MergeFromString(self, data, size=*) except -1
    cpdef int ParseFromString(self, data, size=*, bint reset=*, bint cache=*) except -1
    cpdef bytes SerializeToString(self, bint cache=*)
    cpdef bytes SerializePartialToString(self)

    cdef void _clearfield(self, field_name)
    cdef int _protobuf_deserialize(self, const unsigned char *memory, int size, bint cache)

    cdef void _protobuf_serialize(self, bytearray buf, bint cache)

    cpdef void _Modified(self)

cdef enum _RelationMemberType:
    _RelationMemberType_NODE = 0
    _RelationMemberType_WAY = 1
    _RelationMemberType_RELATION = 2