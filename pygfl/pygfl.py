#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id:  $
"""
:module: pygfl.py
:synopsis: GFL sdk implementation.
:author: Stéphane JULIEN

** Windows, linux & macosx. Tested on python 2.7 **

"""
from __future__ import print_function, unicode_literals

from itertools import chain
from collections import namedtuple
import sys

import ctypes

if sys.platform == 'win32':
  from ctypes import WINFUNCTYPE as GFLAPI
else:
  from ctypes import CFUNCTYPE as GFLAPI

from ctypes import POINTER
from ctypes import c_ubyte, c_uint32, c_int32, c_uint16, c_int16, c_uint8,\
                   c_char,\
                   c_void_p, c_char_p,\
                   c_float, c_double,\
                   c_size_t,\
                   byref, pointer

if sys.platform == 'win32':
  from ctypes import  c_wchar_p


#  Erreurs :
class GFL_Exception(Exception):
  pass


GFL_UINT8 = c_uint8
GFL_CTYPE = c_uint16

GFL_UINT32 = c_uint32
GFL_INT32 = c_int32

GFL_INT16 = c_int16
GFL_ORIGIN = c_uint16
GFL_UINT16 = c_uint16
GFL_CORDER = c_uint16
GFL_LUT_TYPE = c_uint16
GFL_BITMAP_TYPE = GFL_UINT16
GFL_MODE_PARAMS = GFL_UINT16
GFL_MODE = GFL_UINT16
GFL_COLORMODEL = GFL_UINT16


GFL_TRUE = 1
GFL_FALSE = 0
GFL_BOOL = c_ubyte

# ERROR
GFL_ERROR = c_int16

GFL_NO_ERROR = GFL_ERROR(0)

GFL_ERROR_FILE_OPEN          = GFL_ERROR(1)
GFL_ERROR_FILE_READ          = GFL_ERROR(2)
GFL_ERROR_FILE_CREATE        = GFL_ERROR(3)
GFL_ERROR_FILE_WRITE         = GFL_ERROR(4)
GFL_ERROR_NO_MEMORY          = GFL_ERROR(5)
GFL_ERROR_UNKNOWN_FORMAT     = GFL_ERROR(6)
GFL_ERROR_BAD_BITMAP         = GFL_ERROR(7)
GFL_ERROR_BAD_FORMAT_INDEX   = GFL_ERROR(10)
GFL_ERROR_BAD_PARAMETERS     = GFL_ERROR(50)

GFL_UNKNOWN_ERROR            = GFL_ERROR(255)

#  ORIGIN type
GFL_ORIGIN = GFL_UINT16
GFL_LEFT          = 0x00
GFL_RIGHT         = 0x01
GFL_TOP           = 0x00
GFL_BOTTOM        = 0x10
GFL_TOP_LEFT      = (GFL_TOP | GFL_LEFT)
GFL_BOTTOM_LEFT   = (GFL_BOTTOM | GFL_LEFT)
GFL_TOP_RIGHT     = (GFL_TOP | GFL_RIGHT)
GFL_BOTTOM_RIGHT  = (GFL_BOTTOM | GFL_RIGHT)

# Compression
GFL_COMPRESSION = GFL_UINT16
GFL_NO_COMPRESSION = GFL_COMPRESSION(0)
GFL_RLE = GFL_COMPRESSION(1)
GFL_LZW = GFL_COMPRESSION(2)
GFL_JPEG = GFL_COMPRESSION(3)
GFL_ZIP = GFL_COMPRESSION(4)
GFL_SGI_RLE = GFL_COMPRESSION(5)
GFL_CCITT_RLE = GFL_COMPRESSION(6)
GFL_CCITT_FAX3 = GFL_COMPRESSION(7)
GFL_CCITT_FAX3_2D = GFL_COMPRESSION(8)
GFL_CCITT_FAX4 = GFL_COMPRESSION(9)
GFL_WAVELET = GFL_COMPRESSION(10)
GFL_LZW_PREDICTOR = GFL_COMPRESSION(11)
GFL_UNKNOWN_COMPRESSION = GFL_COMPRESSION(255)

# BITMAP type
GFL_BINARY = 0x0001
GFL_GREY   = 0x0002
GFL_COLORS = 0x0004
GFL_RGB    = 0x0010
GFL_RGBA   = 0x0020
GFL_BGR    = 0x0040
GFL_ABGR   = 0x0080
GFL_BGRA   = 0x0100
GFL_ARGB   = 0x0200
GFL_CMYK   = 0x0400

# OBSOLETE
GFL_24BITS     = (GFL_RGB | GFL_BGR)
GFL_32BITS     = (GFL_RGBA | GFL_ABGR | GFL_BGRA | GFL_ARGB | GFL_CMYK)
GFL_TRUECOLORS = (GFL_24BITS | GFL_32BITS)

def GFL_IS24BITS(_a):     return ((_a) & GFL_24BITS)
def GFL_IS32BITS(_a):     return ((_a) & GFL_32BITS)
#def GFL_ISTRUECOLORS(_a): return ((_a) & GFL_TRUECOLORS)

# ~OBSOLETE
#del GFL_ISTRUECOLORS
del GFL_24BITS
del GFL_32BITS
GFL_24BITS = 0x1000  #Only for gflBitmapTypeIsSupportedByIndex or gflBitmapTypeIsSupportedByName
GFL_32BITS = 0x2000
GFL_48BITS = 0x4000
GFL_64BITS = 0x8000

def GFL_ISTRUECOLORS(_a):
  return (_a & (GFL_RGB | GFL_BGR | GFL_RGBA | GFL_ABGR | GFL_BGRA | GFL_ARGB | GFL_CMYK))

GFL_BITMAP_TYPE = GFL_UINT16


class Structure(ctypes.Structure):
  _pack_ = 8
  def __str__(self):
    return '\n '.join(chain(['** {} **'.format(self.__class__.__name__)],
                            ("{0}:{1} ({2}".format(w[0], getattr(self, w[0]), type(getattr(self, w[0]))) for w in self._fields_)
                           )
                     )


class GFL_COLORMAP(Structure):
  _fields_ = [('Red', GFL_UINT8 * 256),
              ('Green', GFL_UINT8 * 256),
              ('Blue', GFL_UINT8 * 256),
              ('Alpha', GFL_UINT8 * 256),]


class GFL_COLOR(Structure):
  _fields_ = [('Red',GFL_UINT16),
              ('Green', GFL_UINT16),
              ('Blue', GFL_UINT16),
              ('Alpha', GFL_UINT16)]


class GFL_BITMAP(Structure):
  _fields_ = [('Type', GFL_BITMAP_TYPE),
              ('Origin', GFL_ORIGIN),
              ('Width', GFL_INT32),
              ('Height', GFL_INT32),
              ('BytesPerLine', GFL_UINT32),
              ('LinePadding', GFL_INT16),
              ('BitsPerComponent', GFL_UINT16),  #  1, 8, 10, 12, 16
              ('ComponentsPerPixel', GFL_UINT16),  # 1, 3, 4
              ('BytesPerPixel', GFL_UINT16),  # Only valid for 8 or more bits
              ('Xdpi', GFL_UINT16),
              ('Ydpi', GFL_UINT16),
              ('TransparentIndex', GFL_INT16),  # -1 if not used
              ('Reserved', GFL_INT16),
              ('ColorUsed', GFL_INT32),
              ('ColorMap', POINTER(GFL_COLORMAP)),
              ('Data', POINTER(GFL_UINT8)),
              ('Comment', c_char_p),
              ('MetaData', c_void_p),
              ('XOffset', GFL_INT32),
              ('YOffset', GFL_INT32),
              ('Name', c_char_p)]


#  For RAW format, channels Order
GFL_CORDER_INTERLEAVED = 0
GFL_CORDER_SEQUENTIAL = 1
GFL_CORDER_SEPARATE = 2

GFL_ORDER = GFL_UINT16


# Channels Type
GFL_CTYPE_GREYSCALE = 0
GFL_CTYPE_RGB       = 1
GFL_CTYPE_BGR       = 2
GFL_CTYPE_RGBA      = 3
GFL_CTYPE_ABGR      = 4
GFL_CTYPE_CMY       = 5
GFL_CTYPE_CMYK      = 6

GFL_CTYPE = GFL_UINT16

# Lut Type (For DPX/Cineon)
GFL_LUT_TO8BITS  = 1
GFL_LUT_TO10BITS = 2
GFL_LUT_TO12BITS = 3
GFL_LUT_TO16BITS = 4

GFL_LUT_TYPE = GFL_UINT16


# Callbacks
GFL_ALLOC_CALLBACK = GFLAPI(c_void_p, c_size_t, c_void_p)
GFL_REALLOC_CALLBACK = GFLAPI(c_void_p, c_void_p, c_size_t, c_void_p)
GFL_FREE_CALLBACK = GFLAPI(None, c_void_p, c_void_p)

GFL_HANDLE = c_void_p

GFL_READ_CALLBACK = GFLAPI(GFL_UINT32, GFL_HANDLE, c_void_p, GFL_UINT32)
GFL_TELL_CALLBACK = GFLAPI(GFL_UINT32, GFL_HANDLE)
GFL_SEEK_CALLBACK = GFLAPI(GFL_UINT32, GFL_HANDLE, GFL_INT32, GFL_INT32)
GFL_WRITE_CALLBACK = GFLAPI(GFL_UINT32, GFL_HANDLE, c_void_p, GFL_UINT32)

GFL_ALLOCATEBITMAP_CALLBACK = GFLAPI(c_void_p, GFL_INT32, GFL_INT32, GFL_INT32,
                                     GFL_INT32, GFL_INT32, GFL_INT32, c_void_p)

GFL_PROGRESS_CALLBACK = GFLAPI(None, GFL_INT32, c_void_p)
GFL_WANTCANCEL_CALLBACK = GFLAPI(GFL_BOOL, c_void_p)
GFL_VIRTUAL_SAVE_CALLBACK = GFLAPI(GFL_ERROR, POINTER(c_void_p), GFL_INT32, GFL_INT32, c_void_p)

class GFL_LOAD_INFO_CB(Structure):
  _fields_ = [('Type', GFL_BITMAP_TYPE),
              ('Origin', GFL_ORIGIN),
              ('Width', GFL_INT32),
              ('Height', GFL_INT32),
              ('BytesPerLine', GFL_UINT32),
              ('LinePadding', GFL_INT16),
              ('BitsPerComponent', GFL_UINT16),
              ('ComponentsPerPixel', GFL_UINT16),
              ('BytesPerPixel', GFL_UINT16),]

GFL_VIRTUAL_LOAD_CALLBACK = GFLAPI(GFL_ERROR, c_void_p, GFL_INT32, GFL_INT32, POINTER(GFL_LOAD_INFO_CB), c_void_p)

# LOAD_PARAMS Flags
GFL_LOAD_SKIP_ALPHA               = 0x00000001  # Alpha not loaded (32bits only)
GFL_LOAD_IGNORE_READ_ERROR        = 0x00000002
GFL_LOAD_BY_EXTENSION_ONLY        = 0x00000004  # Use only extension to recognize format. Faster
GFL_LOAD_READ_ALL_COMMENT         = 0x00000008  # Read Comment in GFL_FILE_DESCRIPTION
GFL_LOAD_FORCE_COLOR_MODEL        = 0x00000010  # Force to load picture in the ColorModel
GFL_LOAD_PREVIEW_NO_CANVAS_RESIZE = 0x00000020  # With gflLoadPreview, width & height are the maximum box
GFL_LOAD_BINARY_AS_GREY           = 0x00000040  # Load Black&White file in greyscale
GFL_LOAD_ORIGINAL_COLORMODEL      = 0x00000080  # If the colormodel is CMYK, keep it
GFL_LOAD_ONLY_FIRST_FRAME         = 0x00000100  # No search to check if file is multi-frame
GFL_LOAD_ORIGINAL_DEPTH           = 0x00000200  # In the case of 10/16 bits per component
GFL_LOAD_METADATA                 = 0x00000400  # Read all metadata
GFL_LOAD_COMMENT                  = 0x00000800  # Read comment
GFL_LOAD_HIGH_QUALITY_THUMBNAIL   = 0x00001000  # gflLoadThumbnail
GFL_LOAD_EMBEDDED_THUMBNAIL       = 0x00002000  # gflLoadThumbnail
GFL_LOAD_ORIENTED_THUMBNAIL       = 0x00004000  # gflLoadThumbnail
GFL_LOAD_ORIGINAL_EMBEDDED_THUMBNAIL = 0x00008000 # gflLoadThumbnail
GFL_LOAD_ORIENTED                    = 0x00008000


class GFL_LOAD_CALLBACKS(Structure):
  _fields_ = [('Read', GFL_READ_CALLBACK),
              ('Tell', GFL_TELL_CALLBACK),
              ('Seek', GFL_SEEK_CALLBACK),
              ('AllocateBitmap', GFL_ALLOCATEBITMAP_CALLBACK),  # Global or not????
              ('AllocateBitmapParams', c_void_p),
              ('Progress', GFL_PROGRESS_CALLBACK),
              ('ProgressParams', c_void_p),
              ('WantCancel', GFL_WANTCANCEL_CALLBACK),
              ('WantCancelParams', c_void_p),
              ('SetLine', GFL_VIRTUAL_LOAD_CALLBACK),
              ('SetLineParams', c_void_p)]


class GFL_LOAD_PARAMS(Structure):
  _fields_ = [('Flags', GFL_UINT32),
              ('FormatIndex', GFL_INT32),  # -1 for automatic recognition
              ('ImageWanted', GFL_INT32),  # for multi-page or animated file
              ('Origin', GFL_ORIGIN),  # default: GFL_TOP_LEFT
              ('ColorModel', GFL_BITMAP_TYPE),  # Only for 24/32 bits picture, GFL_RGB/GFL_RGBA (default), GFL_BGR/GFL_ABGR, GFL_BGRA, GFL_ARGB
              ('LinePadding', GFL_UINT32),  # 1 (default), 2, 4, ....
              ('DefaultAlpha', GFL_UINT8),  # Used if alpha doesn't exist in original file & ColorModel=RGBA/BGRA/ABGR/ARGB

              ('PsdNoAlphaForNonLayer', GFL_UINT8),
              ('PngComposeWithAlpha', GFL_UINT8),
              ('WMFHighResolution', GFL_UINT8),

              ('Width', GFL_INT32),  # RAW/YUV only
              ('Height', GFL_INT32),  # RAW/YUV only
              ('Offset', GFL_UINT32),  # RAW/YUV only

              ('ChannelOrder', GFL_CORDER),  # RAW only
              ('ChannelType', GFL_CTYPE),  # RAW only

              ('PcdBase', GFL_UINT16), # PCD only, PCD -> 2:768x576, 1:384x288, 0:192x144

              ('EpsDpi', GFL_UINT16),  # EPS/PS/AI/PDF only
              ('EpsWidth', GFL_INT32),  # EPS/PS/AI/PDF only
              ('EpsHeight',GFL_INT32),  # EPS/PS/AI/PDF only

              ('LutType', GFL_LUT_TYPE),  # DPX/Cineon only /* GFL_LUT_TO8BITS, GFL_LUT_TO10BITS, GFL_LUT_TO12BITS, GFL_LUT_TO16BITS */
              ('Reserved3', GFL_UINT16),  # DPX/Cineon only
              ('LutData', POINTER(GFL_UINT16)),  # DPX/Cineon only /* RRRR.../GGGG..../BBBB.....*/
              ('LutFilename', c_char_p),  # DPX/Cineon only

              ('CameraRawUseAutomaticBalance', GFL_UINT8), # Camera RAW only
              ('CameraRawUseCameraBalance', GFL_UINT8), # Camera RAW only
              ('CameraRawHighlight', GFL_UINT8), # Camera RAW only
              ('CameraRawAutoBright', GFL_UINT8), # Camera RAW only
              ('CameraRawGamma', c_float), # Camera RAW only
              ('CameraRawBrightness', c_float), # Camera RAW only
              ('CameraRawRedScaling', c_float), # Camera RAW only
              ('CameraRawBlueScaling', c_float), # Camera RAW only
              ('Callbacks', GFL_LOAD_CALLBACKS),
              ('UserParams', c_void_p),
              ]


# SAVE_PARAMS Flags
GFL_SAVE_REPLACE_EXTENSION = 0x0001
GFL_SAVE_WANT_FILENAME = 0x0002
GFL_SAVE_ANYWAY = 0x0004
GFL_SAVE_ICC_PROFILE = 0x0008   # Currently only available for jpeg


GFL_BYTE_ORDER_DEFAULT = 0
GFL_BYTE_ORDER_LSBF    = 1
GFL_BYTE_ORDER_MSBF    = 2


class GFL_SAVE_PARAMS_CALLBACKS(Structure):
  _fields_ = [('Write', GFL_WRITE_CALLBACK),
              ('Tell', GFL_TELL_CALLBACK),
              ('Seek', GFL_SEEK_CALLBACK),
              ('GetLine', GFL_VIRTUAL_SAVE_CALLBACK),
              ('GetLineParams', c_void_p), ]


class GFL_SAVE_PARAMS(Structure):
  _fields_ = [('Flags', GFL_UINT32),
              ('FormatIndex', GFL_INT32),
              ('Compression', GFL_COMPRESSION),
              ('Quality', GFL_INT16),
              ('CompressionLevel', GFL_INT16),
              ('Interlaced', GFL_BOOL),
              ('Progressive', GFL_BOOL),
              ('OptimizeHuffmanTable', GFL_BOOL),
              ('InAscii', GFL_BOOL),

              ('LutType', GFL_LUT_TYPE),      # DPX/Cineon only - GFL_LUT_TO8BITS, GFL_LUT_TO10BITS, GFL_LUT_TO12BITS, GFL_LUT_TO16BITS
              ('DpxByteOrder', GFL_UINT8),
              ('CompressRatio', GFL_UINT8),  # JPEG2000
              ('MaxFileSize', GFL_UINT32),   # JPEG2000

              ('LutData', POINTER(GFL_UINT16)),  # RRRR.../GGGG..../BBBB.....
              ('LutFilename', c_char_p),

              ('Offset', GFL_UINT32),
              ('ChannelOrder', GFL_CORDER),
              ('ChannelType', GFL_CTYPE),

              ('Callbacks', GFL_SAVE_PARAMS_CALLBACKS),

              ('UserParams', c_void_p),]


# Color model
GFL_CM_RGB    = 0
GFL_CM_GREY   = 1
GFL_CM_CMY    = 2
GFL_CM_CMYK   = 3
GFL_CM_YCBCR  = 4
GFL_CM_YUV16  = 5
GFL_CM_LAB    = 6
GFL_CM_LOGLUV = 7
GFL_CM_LOGL   = 8

GFL_COLORMODEL = GFL_UINT16


class GFL_FILE_INFORMATION(Structure):
  "FILE_INFORMATION struct"
  _fields_ = [('Type', GFL_BITMAP_TYPE),  # Not used
              ('Origin', GFL_ORIGIN),
              ('Width', GFL_INT32),
              ('Height', GFL_INT32),
              ('FormatIndex', GFL_INT32),
              ('FormatName', c_char *8),
              ('Description', c_char * 64),
              ('Xdpi', GFL_UINT16),
              ('Ydpi', GFL_UINT16),
              ('BitsPerComponent', GFL_UINT16),  # 1, 8, 10, 12, 16 */
              ('ComponentsPerPixel', GFL_UINT16),  # 1, 3, 4  */
              ('NumberOfImages', GFL_INT32),
              ('FileSize', GFL_UINT32),
              ('ColorModel', GFL_COLORMODEL),
              ('Compression', GFL_COMPRESSION),
              ('CompressionDescription', c_char * 64),
              ('XOffset', GFL_INT32),
              ('YOffset', GFL_INT32),
              ('ExtraInfos', c_void_p),]


# GFL_FORMAT_INFORMATION.Status :
GFL_READ = GFL_UINT32(1)
GFL_WRITE = GFL_UINT32(2)

# FORMAT_INFORMATION struct
class GFL_FORMAT_INFORMATION(Structure):
  _fields_ = [('Index', GFL_INT32),
              ('Name', c_char * 8),
              ('Description', c_char * 64),
              ('Status', GFL_UINT32),
              ('NumberOfExtension', GFL_UINT32),
              ('Extension', c_char * 16 * 8),
              ]


# IPTC
class GFL_IPTC_ENTRY(Structure):
  _fields_ = [('Id', GFL_UINT32),
              ('Name', c_char_p),
              ('Value', c_char_p),
             ]


class GFL_IPTC_DATA(Structure):
  _fields_ = [('NumberOfItems', GFL_UINT32),
              ('ItemsList', POINTER(GFL_IPTC_ENTRY)),
              ]

GFL_IPTC_BYLINE              = 0x50
GFL_IPTC_BYLINETITLE         = 0x55
GFL_IPTC_CREDITS             = 0x6e
GFL_IPTC_SOURCE              = 0x73
GFL_IPTC_CAPTIONWRITER       = 0x7a
GFL_IPTC_CAPTION             = 0x78
GFL_IPTC_HEADLINE            = 0x69
GFL_IPTC_SPECIALINSTRUCTIONS = 0x28
GFL_IPTC_OBJECTNAME          = 0x05
GFL_IPTC_DATECREATED         = 0x37
GFL_IPTC_RELEASEDATE         = 0x1e
GFL_IPTC_TIMECREATED         = 0x3c
GFL_IPTC_RELEASETIME         = 0x23
GFL_IPTC_CITY                = 0x5a
GFL_IPTC_STATE               = 0x5f
GFL_IPTC_COUNTRY             = 0x65
GFL_IPTC_COUNTRYCODE         = 0x64
GFL_IPTC_SUBLOCATION         = 0x5c
GFL_IPTC_ORIGINALTRREF       = 0x67
GFL_IPTC_CATEGORY            = 0x0f
GFL_IPTC_COPYRIGHT           = 0x74
GFL_IPTC_EDITSTATUS          = 0x07
GFL_IPTC_PRIORITY            = 0x0a
GFL_IPTC_OBJECTCYCLE         = 0x4b
GFL_IPTC_JOBID               = 0x16
GFL_IPTC_PROGRAM             = 0x41
GFL_IPTC_KEYWORDS            = 0x19
GFL_IPTC_SUPCATEGORIES       = 0x14
GFL_IPTC_CONTENT_LOCATION    = 0x1b
GFL_IPTC_PROGRAM_VERSION     = 0x46
GFL_IPTC_CONTACT             = 0x76


# EXIF
GFL_EXIF_IFD_0                = 0x0001
GFL_EXIF_MAIN_IFD             = 0x0002
GFL_EXIF_INTEROPERABILITY_IFD = 0x0004
GFL_EXIF_IFD_THUMBNAIL        = 0x0008
GFL_EXIF_GPS_IFD              = 0x0010
GFL_EXIF_MAKERNOTE_IFD        = 0x0020

GFL_EXIF_MAKER             = 0x010F
GFL_EXIF_MODEL             = 0x0110
GFL_EXIF_ORIENTATION       = 0x0112
GFL_EXIF_EXPOSURETIME      = 0x829A
GFL_EXIF_FNUMBER           = 0x829D
GFL_EXIF_DATETIME_ORIGINAL = 0x9003
GFL_EXIF_SHUTTERSPEED      = 0x9201
GFL_EXIF_APERTURE          = 0x9202
GFL_EXIF_MAXAPERTURE       = 0x9205
GFL_EXIF_FOCALLENGTH       = 0x920A

class GFL_EXIF_ENTRY(Structure):
  _fields_ = [('Flag', GFL_UINT32),  # EXIF_...IFD
               ('Tag', GFL_UINT32),
               ('Name', c_char_p),
               ('Value', c_char_p),
              ]


class GFL_EXIF_DATA(Structure):
  _fields_ = [('NumberOfItems', GFL_UINT32),
              ('ItemsList', POINTER(GFL_EXIF_ENTRY)),
             ]

# For advanced developer only!!!
GFL_EXIF_BYTE      = 1
GFL_EXIF_STRING    = 2
GFL_EXIF_USHORT    = 3
GFL_EXIF_ULONG     = 4
GFL_EXIF_URATIONAL = 5
GFL_EXIF_SBYTE     = 6
GFL_EXIF_UNDEFINED = 7
GFL_EXIF_SSHORT    = 8
GFL_EXIF_SLONG     = 9
GFL_EXIF_SRATIONAL =10
GFL_EXIF_SINGLEF   =11
GFL_EXIF_DOUBLE    =12


class GFL_EXIF_ENTRYEX(Structure):
  _fields_ = [('Tag', GFL_UINT16),
              ('Format', GFL_UINT16),
              ('Ifd', GFL_INT32),
              ('NumberOfComponents', GFL_INT32),
              ('Value', GFL_UINT32),
              ('DataLength', GFL_INT32),
              ('Data', c_char_p),
             ]
GFL_EXIF_ENTRYEX._fields_.append(('Next', POINTER(GFL_EXIF_ENTRYEX)))


class GFL_EXIF_DATAEX(Structure):
  _fields_ = [('Root', POINTER(GFL_EXIF_ENTRYEX)),
              ('UseMsbf', GFL_INT32),
             ]


# SAVE_PARAMS Type
GFL_SAVE_PARAMS_QUALITY           = 0 # 0<=quality<=100
GFL_SAVE_PARAMS_COMPRESSION_LEVEL = 1 # 0<=level<=9
GFL_SAVE_PARAMS_INTERLACED        = 2
GFL_SAVE_PARAMS_PROGRESSIVE       = 3
GFL_SAVE_PARAMS_OPTIMIZE_HUFFMAN  = 4
GFL_SAVE_PARAMS_IN_ASCII          = 5
GFL_SAVE_PARAMS_LUT               = 6

GFL_SAVE_PARAMS_TYPE = GFL_UINT32

#
GFL_RESIZE_QUICK    = 0
GFL_RESIZE_BILINEAR = 1
GFL_RESIZE_HERMITE  = 2
GFL_RESIZE_GAUSSIAN = 3
GFL_RESIZE_BELL     = 4
GFL_RESIZE_BSPLINE  = 5
GFL_RESIZE_MITSHELL = 6
GFL_RESIZE_LANCZOS  = 7


# DOESN'T WORKS YET WITH MORE THAN 8BITS PER COMPONENT!
GFL_MODE_TO_BINARY      = 1
GFL_MODE_TO_4GREY       = 2
GFL_MODE_TO_8GREY       = 3
GFL_MODE_TO_16GREY      = 4
GFL_MODE_TO_32GREY      = 5
GFL_MODE_TO_64GREY      = 6
GFL_MODE_TO_128GREY     = 7
GFL_MODE_TO_216GREY     = 8
GFL_MODE_TO_256GREY     = 9
GFL_MODE_TO_8COLORS     = 12
GFL_MODE_TO_16COLORS    = 13
GFL_MODE_TO_32COLORS    = 14
GFL_MODE_TO_64COLORS    = 15
GFL_MODE_TO_128COLORS   = 16
GFL_MODE_TO_216COLORS   = 17
GFL_MODE_TO_256COLORS   = 18
GFL_MODE_TO_RGB         = 19
GFL_MODE_TO_RGBA        = 20
GFL_MODE_TO_BGR         = 21
GFL_MODE_TO_ABGR        = 22
GFL_MODE_TO_BGRA        = 23
GFL_MODE_TO_ARGB        = 24

GFL_MODE_TO_TRUE_COLORS = GFL_MODE_TO_RGB

GFL_MODE = GFL_UINT16

GFL_MODE_NO_DITHER        = 0
GFL_MODE_PATTERN_DITHER   = 1
GFL_MODE_HALTONE45_DITHER = 2  # Only with GFL_MODE_TO_BINARY
GFL_MODE_HALTONE90_DITHER = 3  # Only with GFL_MODE_TO_BINARY
GFL_MODE_ADAPTIVE         = 4
GFL_MODE_FLOYD_STEINBERG  = 5  # Only with GFL_MODE_TO_BINARY

GFL_MODE_PARAMS = GFL_UINT16


#
def gflGetBitmapPtr(bitmap, y):
  return bitmap.Data + y * bitmap.BytesPerLine
#

class GFL_RECT(Structure):
  _fields_ = [('x', GFL_INT32),
              ('y', GFL_INT32),
              ('w', GFL_INT32),
              ('h', GFL_INT32)]

class GFL_POINT(Structure):
  _fields_ = [('x', GFL_INT32),
              ('y', GFL_INT32),
              ]


#

GFL_CANVASRESIZE_TOPLEFT     = 0
GFL_CANVASRESIZE_TOP         = 1
GFL_CANVASRESIZE_TOPRIGHT    = 2
GFL_CANVASRESIZE_LEFT        = 3
GFL_CANVASRESIZE_CENTER      = 4
GFL_CANVASRESIZE_RIGHT       = 5
GFL_CANVASRESIZE_BOTTOMLEFT  = 6
GFL_CANVASRESIZE_BOTTOM      = 7
GFL_CANVASRESIZE_BOTTOMRIGHT = 8

GFL_CANVASRESIZE = GFL_UINT32

GFL_FILE_HANDLE = c_void_p
GFL_EXIF_WANT_MAKERNOTES = 0x0001


# =========
# Functions
# =========
class GFL(object):
  def F_GFL_ERROR(self, error, func, arguments):
    "Si le code erreur n'est pas 0, une exception est générée."
    if 0 < error <= 255:
      raise GFL_Exception(error, self.gflGetErrorString(error))
    elif error != 0:
      raise GFL_Exception(error, "Erreur {} inconnue.".format(error))
    return error

  lfn = [
    ('gflMemoryAlloc.argtypes', [GFL_UINT32], c_void_p),
    ('gflMemoryRealloc', [c_void_p, GFL_UINT32], c_void_p),
    ('gflMemoryFree', [c_void_p], None),
    ('gflGetVersion', [], c_char_p),
    ('gflGetVersionOfLibformat', [], c_char_p),
    ('gflLibraryInit', [], GFL_ERROR, F_GFL_ERROR),
    ('gflLibraryInitEx', [GFL_ALLOC_CALLBACK, GFL_REALLOC_CALLBACK, GFL_FREE_CALLBACK, c_void_p], GFL_ERROR, F_GFL_ERROR),
    ('gflLibraryExit', [], None),
    ('gflEnableLZW', [GFL_BOOL], None),
    ('gflSetPluginsPathname', [c_char_p], None),
    ('gflGetNumberOfFormat', [], GFL_INT32),
    ('gflGetFormatIndexByName', [c_char_p], GFL_INT32),
    ('gflGetFormatNameByIndex', [GFL_INT32], c_char_p),
    ('gflFormatIsSupported',[c_char_p], GFL_BOOL),
    ('gflFormatIsWritableByIndex', [GFL_INT32], GFL_BOOL),
    ('gflFormatIsWritableByName', [c_char_p], GFL_BOOL),
    ('gflFormatIsReadableByIndex', [GFL_INT32], GFL_BOOL),
    ('gflFormatIsReadableByName', [c_char_p], GFL_BOOL),
    ('gflGetDefaultFormatSuffixByIndex', [GFL_INT32], c_char_p),
    ('gflGetDefaultFormatSuffixByName', [c_char_p], c_char_p),
    ('gflGetFormatDescriptionByIndex', [GFL_INT32], c_char_p),
    ('gflGetFormatDescriptionByName', [c_char_p], c_char_p),
    ('gflGetFormatInformationByIndex', [GFL_INT32, POINTER(GFL_FORMAT_INFORMATION)], GFL_ERROR, F_GFL_ERROR),
    ('gflGetFormatInformationByName', [c_char_p, POINTER(GFL_FORMAT_INFORMATION)], GFL_ERROR, F_GFL_ERROR),
    ('gflSaveParamsIsSupportedByIndex.argtypes', [GFL_INT32, GFL_SAVE_PARAMS_TYPE], GFL_BOOL),
    ('gflSaveParamsIsSupportedByName', [c_char_p, GFL_SAVE_PARAMS_TYPE], GFL_BOOL),
    ('gflCompressionIsSupportedByIndex', [GFL_INT32, GFL_COMPRESSION], GFL_BOOL),
    ('gflCompressionIsSupportedByName', [c_char_p, GFL_COMPRESSION], GFL_BOOL),
    ('gflBitmapIsSupportedByIndex', [GFL_INT32, POINTER(GFL_BITMAP)], GFL_BOOL),
    ('gflBitmapIsSupportedByName', [c_char_p, POINTER(GFL_BITMAP)], GFL_BOOL),
    ('gflBitmapTypeIsSupportedByIndex', [GFL_INT32, GFL_BITMAP_TYPE, GFL_UINT16], GFL_BOOL),
    ('gflBitmapTypeIsSupportedByName', [c_char_p, GFL_BITMAP_TYPE, GFL_UINT16, ], GFL_BOOL),

    ('gflGetErrorString', [GFL_ERROR], c_char_p),
    ('gflGetLabelForColorModel', [GFL_COLORMODEL], c_char_p),
    ('gflGetFileInformation', [c_char_p, GFL_INT32, POINTER(GFL_FILE_INFORMATION)], GFL_ERROR, F_GFL_ERROR),
    ('gflGetFileInformationEx', [c_char_p, GFL_INT32, POINTER(GFL_FILE_INFORMATION), GFL_UINT32], GFL_ERROR, F_GFL_ERROR),
    ('gflGetFileInformationFromHandle', [GFL_HANDLE, GFL_INT32, POINTER(GFL_LOAD_CALLBACKS), POINTER(GFL_FILE_INFORMATION)], GFL_ERROR, F_GFL_ERROR),
    ('gflGetFileInformationFromMemory', [POINTER(GFL_UINT8), GFL_UINT32, GFL_INT32, POINTER(GFL_FILE_INFORMATION)], GFL_ERROR, F_GFL_ERROR),
    ('gflFreeFileInformation', [POINTER(GFL_FILE_INFORMATION)], None),
    ('gflGetDefaultLoadParams', [POINTER(GFL_LOAD_PARAMS)], None),
    ('gflLoadBitmap', [c_char_p, POINTER(POINTER(GFL_BITMAP)),
                                    POINTER(GFL_LOAD_PARAMS), POINTER(GFL_FILE_INFORMATION)], GFL_ERROR, F_GFL_ERROR),
    ('gflLoadBitmapFromHandle', [GFL_HANDLE, POINTER(POINTER(GFL_BITMAP)),
                                               POINTER(GFL_LOAD_PARAMS),
                                               POINTER(GFL_FILE_INFORMATION)], GFL_ERROR, F_GFL_ERROR),
    ('gflLoadBitmapFromMemory', [POINTER(GFL_UINT8), GFL_UINT32,
                                              POINTER(POINTER(GFL_BITMAP)), POINTER(GFL_LOAD_PARAMS),
                                              POINTER(GFL_FILE_INFORMATION)], GFL_ERROR, F_GFL_ERROR),
    ('gflGetDefaultThumbnailParams', [POINTER(GFL_LOAD_PARAMS)], None),
    ('gflGetDefaultThumbnailParams', [POINTER(GFL_LOAD_PARAMS)], None),
    ('gflLoadThumbnail', [c_char_p, GFL_INT32, GFL_INT32,
                                        POINTER(POINTER(GFL_BITMAP)), POINTER(GFL_LOAD_PARAMS),
                                        POINTER(GFL_FILE_INFORMATION)], GFL_ERROR, F_GFL_ERROR),
    ('gflLoadThumbnailFromHandle', [GFL_HANDLE, GFL_INT32, GFL_INT32,
                                                  POINTER(POINTER(GFL_BITMAP)),
                                                  POINTER(GFL_LOAD_PARAMS),
                                                  POINTER(GFL_FILE_INFORMATION)], GFL_ERROR, F_GFL_ERROR),
    ('gflLoadThumbnailFromMemory', [POINTER(GFL_UINT8), GFL_UINT32, GFL_INT32, GFL_INT32,
                                                  POINTER(POINTER(GFL_BITMAP)),
                                                  POINTER(GFL_LOAD_PARAMS),
                                                  POINTER(GFL_FILE_INFORMATION)], GFL_ERROR, F_GFL_ERROR),
    ('gflGetDefaultSaveParams', [POINTER(GFL_SAVE_PARAMS), ], None),
    ('gflSaveBitmap', [c_char_p, POINTER(GFL_BITMAP), POINTER(GFL_SAVE_PARAMS), ], GFL_ERROR, F_GFL_ERROR),
    ('gflSaveBitmapIntoHandle', [GFL_HANDLE, POINTER(GFL_BITMAP), POINTER(GFL_SAVE_PARAMS)], GFL_ERROR, F_GFL_ERROR),
    ('gflSaveBitmapIntoMemory', [POINTER(POINTER(GFL_UINT8)), POINTER(GFL_UINT32),
                                               POINTER(GFL_BITMAP), POINTER(GFL_SAVE_PARAMS)], GFL_ERROR, F_GFL_ERROR),
    ('gflFileCreate', [POINTER(GFL_FILE_HANDLE), c_char_p, GFL_UINT32, POINTER(GFL_SAVE_PARAMS)], GFL_ERROR, F_GFL_ERROR),
    ('gflFileAddPicture', [GFL_FILE_HANDLE, POINTER(GFL_BITMAP)], GFL_ERROR, F_GFL_ERROR),
    ('gflFileClose', [GFL_FILE_HANDLE], None),
    ('gflAllockBitmap', [GFL_BITMAP_TYPE, GFL_INT32, GFL_UINT32, POINTER(GFL_COLOR)], POINTER(GFL_BITMAP)),
    ('gflAllockBitmapEx', [GFL_BITMAP_TYPE, GFL_INT32, GFL_INT32, GFL_UINT16,
                                         GFL_UINT32, POINTER(GFL_COLOR)], POINTER(GFL_BITMAP)),
    ('gflFreeBitmap', [POINTER(GFL_BITMAP)], None),
    ('gflFreeBitmapData', [POINTER(GFL_BITMAP)], None),
    ('gflCloneBitmap', [POINTER(GFL_BITMAP), ], POINTER(GFL_BITMAP)),
    ('gflBitmapSetName', [POINTER(GFL_BITMAP), c_char_p], None),
    ('gflGetExtraInfosCount', [POINTER(GFL_FILE_INFORMATION)], GFL_INT32),
    ('gflGetExtraInfos', [POINTER(GFL_FILE_INFORMATION), GFL_INT32, POINTER(c_char_p), POINTER(c_char_p)], None),
    ('gflBitmapHasEXIF', [POINTER(GFL_BITMAP)], GFL_BOOL),
    ('gflBitmapHasIPTC', [POINTER(GFL_BITMAP)], GFL_BOOL),
    ('gflBitmapHasICCProfile', [POINTER(GFL_BITMAP)], GFL_BOOL),
    ('gflBitmapRemoveEXIFThumbnail', [POINTER(GFL_BITMAP)],  None),
    ('gflBitmapRemoveICCProfile', [POINTER(GFL_BITMAP)], None),
    ('gflBitmapGetICCProfile', [POINTER(GFL_BITMAP), POINTER(POINTER(GFL_UINT8)),  # pData must be freed by gflFreeMemory
                                              POINTER(GFL_UINT32)], None),
    ('gflBitmapCopyICCProfile', [POINTER(GFL_BITMAP), POINTER(GFL_BITMAP)], None),
    ('gflBitmapRemoveMetaData', [POINTER(GFL_BITMAP)], None),
    ('gflBitmapGetXMP', [POINTER(GFL_BITMAP), POINTER(POINTER(GFL_UINT8)),
                                       POINTER(GFL_UINT32)], GFL_BOOL),
    ('gflBitmapSetEXIFThumbnail', [POINTER(GFL_BITMAP), POINTER(GFL_BITMAP), ], None),
    ('gflGetEXIFDPI', [POINTER(GFL_BITMAP), POINTER(GFL_INT32), POINTER(GFL_INT32)], GFL_BOOL),
    ('gflLoadEXIF', [c_char_p, GFL_UINT32], POINTER(GFL_EXIF_DATA)),
    ('gflHasEXIF', [c_char_p], GFL_BOOL),
    ('gflLoadEXIF2', [c_char_p, GFL_UINT32], POINTER(GFL_EXIF_DATAEX),
    ('gflHasIPTC', [c_char_p], GFL_BOOL),),
    ('gflHasICCProfile', [c_char_p], GFL_BOOL),
    ('gflBitmapGetIPTC', [POINTER(GFL_BITMAP)], POINTER(GFL_IPTC_DATA)),
    ('gflBitmapGetIPTCValue', [POINTER(GFL_BITMAP), GFL_UINT32, c_char_p, GFL_INT32], GFL_ERROR, F_GFL_ERROR),
    ('gflNewIPTC', [], POINTER(GFL_IPTC_DATA)),
    ('gflFreeIPTC', [POINTER(GFL_IPTC_DATA)], None),
    ('gflSetIPTCValue', [POINTER(GFL_IPTC_DATA), GFL_UINT32, c_char_p], GFL_ERROR, F_GFL_ERROR),
    ('gflRemoveIPTCValue', [POINTER(GFL_IPTC_DATA), GFL_UINT32], GFL_ERROR, F_GFL_ERROR),
    ('gflClearIPTCKeywords', [POINTER(GFL_IPTC_DATA)], GFL_ERROR, F_GFL_ERROR),
    ('gflLoadIPTC', [c_char_p], POINTER(GFL_IPTC_DATA)),
    ('gflSaveIPTC', [c_char_p, POINTER(GFL_IPTC_DATA), ], GFL_ERROR, F_GFL_ERROR),
    ('gflBitmapSetIPTC', [POINTER(GFL_BITMAP), POINTER(GFL_IPTC_DATA)], GFL_ERROR, F_GFL_ERROR),
    ('gflBitmapGetEXIF', [POINTER(GFL_BITMAP), GFL_UINT32], POINTER(GFL_EXIF_DATA)),
    ('gflBitmapGetEXIFValue', [POINTER(GFL_BITMAP), GFL_UINT32, c_char_p, GFL_INT32], GFL_ERROR, F_GFL_ERROR),
    ('gflFreeEXIF', [POINTER(GFL_EXIF_DATA)], None),
    ('gflBitmapSetComment', [POINTER(GFL_BITMAP), c_char_p], None),

    ('gflBitmapGetEXIF2', [POINTER(GFL_BITMAP)], POINTER(GFL_EXIF_DATAEX)),
    ('gflFreeEXIF2', [POINTER(GFL_EXIF_DATAEX)], None),
    ('gflBitmapSetEXIF2', [POINTER(GFL_BITMAP), POINTER(GFL_EXIF_DATAEX)], None),
    ('gflBitmapSetEXIFValueString2', [POINTER(GFL_EXIF_DATAEX), GFL_UINT16, GFL_UINT16, c_char_p], None),
    ('gflBitmapSetEXIFValueInt2', [POINTER(GFL_EXIF_DATAEX), GFL_UINT16, GFL_UINT16, GFL_UINT32, GFL_UINT32], None),
    ('gflBitmapSetEXIFValueRational2', [POINTER(GFL_EXIF_DATAEX), GFL_UINT16, GFL_UINT16, GFL_UINT32, GFL_UINT32], None),
    ('gflBitmapSetEXIFValueRationalArray2', [POINTER(GFL_EXIF_DATAEX), GFL_UINT16, GFL_UINT16, POINTER(GFL_UINT32), GFL_INT32], None),

    ('gflJPEGGetComment', [c_char_p, c_char_p, GFL_INT32], GFL_ERROR, F_GFL_ERROR),
    ('gflJPEGSetComment', [c_char_p, c_char_p], GFL_ERROR, F_GFL_ERROR),
    ('gflPNGGetComment', [c_char_p, c_char_p, GFL_INT32], GFL_ERROR, F_GFL_ERROR),
    ('gflPNGSetComment', [c_char_p, c_char_p], GFL_ERROR, F_GFL_ERROR),

    ('gflIsLutFile', [c_char_p], GFL_BOOL),
    ('gflIsCompatibleLutFile', [c_char_p, GFL_INT32, GFL_INT32, POINTER(GFL_LUT_TYPE)], GFL_BOOL),
    ('gflApplyLutFile', [POINTER(GFL_BITMAP), POINTER(POINTER(GFL_BITMAP)), c_char_p, GFL_LUT_TYPE], GFL_ERROR, F_GFL_ERROR),
    ('gflResize', [POINTER(GFL_BITMAP), POINTER(POINTER(GFL_BITMAP)), GFL_INT32, GFL_INT32, GFL_UINT32, GFL_UINT32], GFL_ERROR, F_GFL_ERROR),

    ('gflChangeColorDepth', [POINTER(GFL_BITMAP), POINTER(POINTER(GFL_BITMAP)), GFL_MODE, GFL_MODE_PARAMS], GFL_ERROR, F_GFL_ERROR),
    ('gflGetColorAt', [POINTER(GFL_BITMAP), GFL_INT32, GFL_INT32, POINTER(GFL_COLOR)], GFL_ERROR, F_GFL_ERROR),
    ('gflSetColorAt', [POINTER(GFL_BITMAP), GFL_INT32, GFL_INT32, POINTER(GFL_COLOR)], GFL_ERROR, F_GFL_ERROR),
    ('gflGetColorAtEx', [POINTER(GFL_BITMAP), GFL_UINT8, POINTER(GFL_COLOR)], GFL_ERROR, F_GFL_ERROR),
    ('gflSetColorAtEx', [POINTER(GFL_BITMAP), POINTER(GFL_UINT8), POINTER(GFL_COLOR)], GFL_ERROR, F_GFL_ERROR),
    ('gflFlipVertical', [POINTER(GFL_BITMAP), POINTER(POINTER(GFL_BITMAP))], GFL_ERROR, F_GFL_ERROR),
    ('gflFlipHorizontal', [POINTER(GFL_BITMAP), POINTER(POINTER(GFL_BITMAP))], GFL_ERROR, F_GFL_ERROR),
    ('gflCrop', [POINTER(GFL_BITMAP), POINTER(POINTER(GFL_BITMAP)), POINTER(GFL_RECT)], GFL_ERROR, F_GFL_ERROR),
    ('gflAutoCrop', [POINTER(GFL_BITMAP), POINTER(POINTER(GFL_BITMAP)), POINTER(GFL_COLOR), GFL_INT32], GFL_ERROR, F_GFL_ERROR),
    ('gflAutoCrop2', [POINTER(GFL_BITMAP), POINTER(POINTER(GFL_BITMAP)), POINTER(GFL_COLOR), GFL_INT32], GFL_ERROR, F_GFL_ERROR),
    ('gflResizeCanvas', [POINTER(GFL_BITMAP), POINTER(POINTER(GFL_BITMAP)), GFL_INT32, GFL_INT32, GFL_CANVASRESIZE, POINTER(GFL_COLOR)], GFL_ERROR, F_GFL_ERROR),
    ('gflScaleToGrey', [POINTER(GFL_BITMAP), POINTER(POINTER(GFL_BITMAP)), GFL_INT32, GFL_INT32], GFL_ERROR, F_GFL_ERROR),
    ('gflRotate', [POINTER(GFL_BITMAP), POINTER(POINTER(GFL_BITMAP)), GFL_INT32, POINTER(GFL_COLOR)], GFL_ERROR, F_GFL_ERROR),
    ('gflRotateFine', [POINTER(GFL_BITMAP), POINTER(POINTER(GFL_BITMAP)), c_double, POINTER(GFL_COLOR)], GFL_ERROR, F_GFL_ERROR),
    ('gflReplaceColor', [POINTER(GFL_BITMAP), POINTER(POINTER(GFL_BITMAP)), POINTER(GFL_COLOR), POINTER(GFL_COLOR), GFL_INT32], GFL_ERROR, F_GFL_ERROR),
    ('gflBitblt', [POINTER(GFL_BITMAP), POINTER(GFL_RECT), POINTER(GFL_BITMAP), GFL_INT32, GFL_INT32], GFL_ERROR, F_GFL_ERROR),
    ('gflBitbltEx', [POINTER(GFL_BITMAP), POINTER(GFL_RECT), POINTER(GFL_BITMAP), GFL_INT32, GFL_INT32], GFL_ERROR, F_GFL_ERROR),
    ('gflMerge', [POINTER(POINTER(GFL_BITMAP)), POINTER(GFL_POINT), POINTER(GFL_UINT32), GFL_INT32, POINTER(POINTER(GFL_BITMAP))],  GFL_ERROR, F_GFL_ERROR),
    ('gflCombineAlpha', [POINTER(GFL_BITMAP), POINTER(POINTER(GFL_BITMAP)), POINTER(GFL_COLOR)], GFL_ERROR, F_GFL_ERROR),
    ('gflSetTransparentColor', [POINTER(GFL_BITMAP), POINTER(POINTER(GFL_BITMAP)), POINTER(GFL_COLOR), POINTER(GFL_COLOR)], GFL_ERROR, F_GFL_ERROR),
    ('gflSaveBitmapBegin', [POINTER(c_void_p), c_char_p, POINTER(GFL_BITMAP), POINTER(GFL_SAVE_PARAMS)], GFL_ERROR, F_GFL_ERROR),
    ('gflSaveBitmapEnd', [c_void_p], GFL_ERROR, F_GFL_ERROR),
    ('gflSaveBitmapWriteLine', [c_void_p, POINTER(GFL_UINT8)], GFL_ERROR, F_GFL_ERROR),
    ('gflLoadBitmapBegin', [POINTER(c_void_p), c_char_p, POINTER(POINTER(GFL_BITMAP)), POINTER(GFL_LOAD_PARAMS), POINTER(GFL_FILE_INFORMATION)], GFL_ERROR, F_GFL_ERROR),
    ('gflLoadBitmapEnd', [c_void_p], GFL_ERROR, F_GFL_ERROR),
    ('gflLoadBitmapReadLine', [c_void_p, POINTER(GFL_UINT8)], GFL_ERROR, F_GFL_ERROR),
  ]

  # UNICODE Windows only
  if sys.platform == 'win32':
    lfn.extend([
      ('gflSetPluginsPathnameW', [c_wchar_p], None),
      ('gflGetFileInformationW', [c_wchar_p, GFL_INT32, POINTER(GFL_FILE_INFORMATION)], GFL_ERROR, F_GFL_ERROR),
      ('gflLoadBitmapW', [c_wchar_p, POINTER(POINTER(GFL_BITMAP)), POINTER(GFL_LOAD_PARAMS),
                                          POINTER(GFL_FILE_INFORMATION)], GFL_ERROR, F_GFL_ERROR),
      ('gflLoadThumbnailW', [c_wchar_p, GFL_INT32, GFL_INT32,
                                             POINTER(POINTER(GFL_BITMAP)),
                                             POINTER(GFL_LOAD_PARAMS),
                                             POINTER(GFL_FILE_INFORMATION)], GFL_ERROR, F_GFL_ERROR),
      ('gflSaveBitmapW', [c_wchar_p, POINTER(GFL_BITMAP), POINTER(GFL_SAVE_PARAMS)], GFL_ERROR, F_GFL_ERROR),
      ('gflFileCreateW', [POINTER(GFL_FILE_HANDLE), c_wchar_p, GFL_UINT32, POINTER(GFL_SAVE_PARAMS)],GFL_ERROR, F_GFL_ERROR),
      ('gflLoadEXIFW', [c_wchar_p, GFL_UINT32], POINTER(GFL_EXIF_DATA)),
      ('gflLoadIPTCW', [c_wchar_p], POINTER(GFL_EXIF_DATA)),
      ('gflSaveIPTCW', [c_wchar_p, POINTER(GFL_IPTC_DATA)], GFL_ERROR, F_GFL_ERROR),
      ('gflJPEGGetCommentW', [c_wchar_p, c_char_p, GFL_INT32], GFL_ERROR, F_GFL_ERROR),
      ('gflJPEGSetCommentW', [c_wchar_p, c_char_p], GFL_ERROR, F_GFL_ERROR),
      ('gflPNGGetCommentW', [c_wchar_p, c_char_p, GFL_INT32], GFL_ERROR, F_GFL_ERROR),
      ('gflPNGSetCommentW', [c_wchar_p, c_char_p], GFL_ERROR, F_GFL_ERROR),
    ])

  lalias = [('gflGetDefaultPreviewParams', 'gflGetDefaultThumbnailParams'),
            ('gflLoadPreview', 'gflLoadThumbnail'),
            ('gflLoadPreviewFromHandle', 'gflLoadThumbnailFromHandle'),
           ]

  def __init__(self):
    if sys.platform == 'win32':
      self.libgfl = ctypes.windll.LoadLibrary('libgfl340.dll')
    else:
      self.libgfl = ctypes.cdll.LoadLibrary('libgfl.3.40.dylib')

    for arg in GFL.lfn:
      self.append_libgfl(*arg)

    for alias, f in GFL.lalias:
      setattr(self.libgfl, alias, getattr(self.libgfl, f))

  def append_libgfl(self, fn, argtypes, restype, errcheck=None):
    try:
      f = getattr(self.libgfl, fn)
      f.argtypes = argtypes
      f.restype = restype
      if errcheck:
        f.errcheck = getattr(self, errcheck)
      setattr(self, fn, f)
    except Exception:
      raise

  def close(self):
    "Frees resources"
    self.libgfl.gflLibraryExit()

  def __enter__(self):
    return self

  def __exit__(self, _exc_type, _exc_value, _traceback):
    self.close()


class _GFL(object):
  dll_init = False
  formats_lisibles = {}

  def __init__(self):
    if not GFL.dll_init:
      # Load the DLL :
      libgfl.gflLibraryInit()
      libgfl.gflEnableLZW(GFL_TRUE)
      GFL.dll_init = True

      # Options de lecture et de sauvegarde :
      self.load_params = GFL_LOAD_PARAMS()
      libgfl.gflGetDefaultLoadParams(byref(self.load_params))

      self.save_params = GFL_SAVE_PARAMS()
      libgfl.gflGetDefaultSaveParams(byref(self.save_params))


  def print_file_info(self, filename):
    "Imprime des informations sur le fichier (pour debug)."
    file_info = GFL_FILE_INFORMATION()
    libgfl.gflGetFileInformation(filename, -1, byref(file_info))
    print(file_info)
    libgfl.gflFreeFileInformation(byref(file_info))

  def convert2img(self, filenames, target, _type="tiff", compression=GFL_LZW,
                  dpi=None, mode=GFL_MODE_TO_16GREY, comment=""):
    """\
    Concatène des documents dans un seul

    :param filenames: Liste de chemins vers les fichiers à assembler.
    :type  filenames: list(basestring)
    :param basestring target: Chemin du fichier à générer.
    :param basestring _type: Nom du type de fichier à générer.
    :param GFL_COMPRESSION compression: Mode de compression
    :param GFL_UINT16 dpi: Modifie le nombre de dpi avant changement du nombre de couleurs.
    """
    # Calcul du nombre de pages au total :
    nb_pages = []
    file_info = GFL_FILE_INFORMATION()
    for filename in filenames:
      libgfl.gflGetFileInformation(filename, -1, byref(file_info))
      nb_pages.append(file_info.NumberOfImages)
      libgfl.gflFreeFileInformation(byref(file_info))

    # S'il n'y a qu'un seul fichier et qu'il est du type attendu, pas de transcodage.
    if len(nb_pages) == 1:
      # Un seul fichier.
      pass  # :todo..


    sum_nb_pages = sum(nb_pages)  # Nombre total de pages.

    self.save_params.Compression = compression
    self.save_params.FormatIndex = libgfl.gflGetFormatIndexByName(_type)

    handle = GFL_HANDLE()
    p_bitmap = POINTER(GFL_BITMAP)()  # Image avant transformation
    p_bitmap2 = POINTER(GFL_BITMAP)()  # Image après transformation

    libgfl.gflFileCreate(byref(handle), target, sum_nb_pages, byref(self.save_params))
    try:
      for i, filename in enumerate(filenames):
        for page in xrange(nb_pages[i]):
          self.load_params.ImageWanted = page
          # Charge une image :
          libgfl.gflLoadBitmap(filename, byref(p_bitmap), byref(self.load_params), None)

          # Change la résolution:
          if dpi:
            p_bitmap.contents.Xdpi = p_bitmap.contents.Ydpi = dpi

          # Changement de type d'image :
          if compression == GFL_CCITT_FAX4:
            # La compression fax G4 ne fonctionne qu'avec le N&B.
            libgfl.gflChangeColorDepth(p_bitmap, byref(p_bitmap2), GFL_MODE_TO_BINARY, GFL_MODE_NO_DITHER)
          else:
            libgfl.gflChangeColorDepth(p_bitmap, byref(p_bitmap2), mode, GFL_MODE_NO_DITHER)

          # Supprime les commentaires.
          libgfl.gflBitmapSetComment(p_bitmap2, comment)

          # Enregistre l'image :
          libgfl.gflFileAddPicture(handle, p_bitmap2)

          # Libération des ressources :
          libgfl.gflFreeBitmap(p_bitmap)
          libgfl.gflFreeBitmap(p_bitmap2)
    finally:
      libgfl.gflFileClose(handle)

  FMT_INFO = namedtuple('FMT_INFO', ['Description', 'Status', 'Extensions'])
  def get_formats(self):
    """\
    Retourne des informations sur les formats gérés par la bibliothèque.

    :rtype: dict
    :return: {nom_format: namedtuple(description, status, list(Extension))}

    """
    data = {}
    nb_fmts = libgfl.gflGetNumberOfFormat()
    fmt_info = GFL_FORMAT_INFORMATION()

    for i in xrange(nb_fmts):
      libgfl.gflGetFormatInformationByIndex(i, byref(fmt_info))
      l_ext = [ctypes.cast(fmt_info.Extension[j], c_char_p).value for j in xrange(fmt_info.NumberOfExtension)]
      data[fmt_info.Name] = GFL.FMT_INFO(fmt_info.Description, fmt_info.Status, l_ext)
    return data

  def is_ext_supported(self, ext):
    """\
    Détermine si un format, identifié par le suffixe du fichier, est supporté.
    :param basestring ext: extension en minuscule sans le point
    :rtype: bool
    :returs: True si le type de fichier est supporté et False sinon.
    """
    if not GFL.formats_lisibles:
      nb_fmts = libgfl.gflGetNumberOfFormat()
      fmt_info = GFL_FORMAT_INFORMATION()

      for i in xrange(nb_fmts):
        libgfl.gflGetFormatInformationByIndex(i, byref(fmt_info))
        GFL.formats_lisibles.update(ctypes.cast(fmt_info.Extension[j], c_char_p).value.lower()
                                    for j in xrange(fmt_info.NumberOfExtension)
                                    if (fmt_info.Status & GFL_READ))

    return ext.lower() in GFL.formats_lisibles

  def _test(self):
    #filenames = [r'C:\home\scan_hellmann\25-DI-783210\toto.tiff']
    filenames = [r"C:\home\scan_hellmann\25-DI-783210\avis_darrivee-25-DI-783210-U_0.tiff",
                 r"C:\home\scan_hellmann\25-DI-783210\avis_darrivee-25-DI-783210-U_1.tiff",
                 r"C:\home\scan_hellmann\25-DI-783210\profit_share_invoice-25-DI-783210-U_0.tif"]
    #filenames = [r"profit_share_invoice-25-DI-783210-U.pdf"]
    self.convert2img(filenames, 'tutu_g4.tiff', 'tiff', GFL_CCITT_FAX4, 200)
    self.convert2img(filenames, 'tutu_16.tiff', 'tiff', GFL_NO_COMPRESSION, 75, GFL_MODE_TO_16GREY)
    self.convert2img(filenames, 'tutu_8.tiff', 'tiff', GFL_NO_COMPRESSION, 75, GFL_MODE_TO_8GREY)
    self.convert2img(filenames, 'tutu_4.tiff', 'tiff', GFL_NO_COMPRESSION, 75, GFL_MODE_TO_4GREY)
    self.convert2img(filenames, 'tutu_rle16.tiff', 'tiff', GFL_RLE, 75, GFL_MODE_TO_16GREY)


if __name__ == '__main__':
  with GFL() as gfl:
    print(gfl.get_formats())
    gfl._test()

