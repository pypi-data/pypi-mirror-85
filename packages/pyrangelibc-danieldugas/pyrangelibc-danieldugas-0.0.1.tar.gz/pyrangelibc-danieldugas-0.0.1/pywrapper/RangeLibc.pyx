from libcpp cimport bool
from libcpp.string cimport string
from libcpp.vector cimport vector
import numpy as np
cimport numpy as np
from cython.operator cimport dereference as deref


cdef extern from "includes/RangeLib.h":
    # define flags
    cdef bool _USE_CACHED_TRIG "_USE_CACHED_TRIG"
    cdef bool _USE_ALTERNATE_MOD "_USE_ALTERNATE_MOD"
    cdef bool _USE_CACHED_CONSTANTS "_USE_CACHED_CONSTANTS"
    cdef bool _USE_FAST_ROUND "_USE_FAST_ROUND"
    cdef bool _NO_INLINE "_NO_INLINE"
    cdef bool _USE_LRU_CACHE "_USE_LRU_CACHE"
    cdef int  _LRU_CACHE_SIZE "_LRU_CACHE_SIZE"
    cdef bool _MAKE_TRACE_MAP "_MAKE_TRACE_MAP"
    cdef bool USE_CUDA "USE_CUDA"

cdef extern from "includes/RangeLib.h" namespace "ranges":
    cdef cppclass OMap:
        OMap(int w, int h)
        OMap(string filename)
        OMap(string filename, float threshold)
        unsigned width
        unsigned height
        vector[vector[bool]] grid
        bool save(string filename)
        bool error()
        bool get(int x, int y)


    cdef cppclass BresenhamsLine:
        BresenhamsLine(OMap m, float mr)
        float calc_range(float x, float y, float heading)
        void numpy_calc_range(float * ins, float * outs, int num_casts)
        bool saveTrace(string filename)
        void eval_sensor_model(float * obs, float * ranges, double * outs, int rays_per_particle, int particles)
        void set_sensor_model(double * table, int width)
        void numpy_calc_range_angles(float * ins, float * angles, float * outs, int num_casts, int num_angles)
        void calc_range_repeat_angles_eval_sensor_model(float * ins, float * angles, float * obs, double * weights, int num_particles, int num_angles)
    cdef cppclass RayMarching:
        RayMarching(OMap m, float mr)
        float calc_range(float x, float y, float heading)
        void numpy_calc_range(float * ins, float * outs, int num_casts)
        bool saveTrace(string filename)
        void eval_sensor_model(float * obs, float * ranges, double * outs, int rays_per_particle, int particles)
        void set_sensor_model(double * table, int width)
        void numpy_calc_range_angles(float * ins, float * angles, float * outs, int num_casts, int num_angles)
        void calc_range_repeat_angles_eval_sensor_model(float * ins, float * angles, float * obs, double * weights, int num_particles, int num_angles)
        void get_dist_image(float * outs, int width, int height)
    cdef cppclass CDDTCast:
        CDDTCast(OMap m, float mr, unsigned int td)
        float calc_range(float x, float y, float heading)
        void prune(float max_range)
        void numpy_calc_range(float * ins, float * outs, int num_casts)
        void eval_sensor_model(float * obs, float * ranges, double * outs, int rays_per_particle, int particles)
        void set_sensor_model(double * table, int width)
        void numpy_calc_range_angles(float * ins, float * angles, float * outs, int num_casts, int num_angles)
        void calc_range_repeat_angles_eval_sensor_model(float * ins, float * angles, float * obs, double * weights, int num_particles, int num_angles)
        void calc_range_many_radial_optimized(float * ins, float * outs, int num_particles, int num_rays, float min_angle, float max_angle)
    cdef cppclass GiantLUTCast:
        GiantLUTCast(OMap m, float mr, unsigned int td)
        float calc_range(float x, float y, float heading)
        void numpy_calc_range(float * ins, float * outs, int num_casts)
        void eval_sensor_model(float * obs, float * ranges, double * outs, int rays_per_particle, int particles)
        void set_sensor_model(double * table, int width)
        void numpy_calc_range_angles(float * ins, float * angles, float * outs, int num_casts, int num_angles)
        void calc_range_repeat_angles_eval_sensor_model(float * ins, float * angles, float * obs, double * weights, int num_particles, int num_angles)
    # you can only use this if USE_CUDA is true
    cdef cppclass RayMarchingGPU:
        RayMarchingGPU(OMap m, float mr)
        # this one does not do coordinate space conversion
        void calc_range_many(float * ins, float * outs, int num_casts)
        # these do
        void numpy_calc_range(float * ins, float * outs, int num_casts)
        void numpy_calc_range_angles(float * ins, float * angles, float * outs, int num_casts, int num_angles)
        void eval_sensor_model(float * obs, float * ranges, double * outs, int rays_per_particle, int particles)
        void set_sensor_model(double * table, int width)
        # void numpy_calc_range_angles(float * ins, float * angles, float * outs, int num_casts, int num_angles)
        void calc_range_repeat_angles_eval_sensor_model(float * ins, float * angles, float * obs, double * weights, int num_particles, int num_angles)

# define flags
USE_CACHED_TRIG = _USE_CACHED_TRIG
USE_ALTERNATE_MOD = _USE_ALTERNATE_MOD
USE_CACHED_CONSTANTS = _USE_CACHED_CONSTANTS
USE_FAST_ROUND = _USE_FAST_ROUND
NO_INLINE = _NO_INLINE
USE_LRU_CACHE = _USE_LRU_CACHE
LRU_CACHE_SIZE = _LRU_CACHE_SIZE
SHOULD_USE_CUDA = USE_CUDA

'''
Docs:

PyOMap: wraps OMap class
    constructor: PyOMap(arg1, arg2=None)
        Type options: <type(arg1)> <type(arg2)>
            <int width>, <int height> : empty omap of size width, height
            <string map_path>         : loads map from png image at given path
            <string map_path>, <float>: loads map from png image at given path with given occupancy threshold
            <numpy.ndarray>           : loads map from given numpy boolean array
    methods:
        bool save(string filename)    : saves the occupancy grid to given path in png format. 
                                        white == free, black == occupied
        bool isOccupied(int x, int y) : returns true if the given pixel index is occupied, false otherwise
        bool error()                  : returns true if there was an error loading the map

'''


cdef class PyOMap:
    cdef OMap *thisptr      # hold a C++ instance which we're wrapping
    def __cinit__(self, arg1, arg2=None):
        set_trans_params = False
        if arg1 is not None and arg2 is not None:
            if isinstance(arg1, int) and isinstance(arg1, int):
                self.thisptr = new OMap(<int>arg1,<int>arg2)
            else:
                self.thisptr = new OMap(<string>arg1,<float>arg2)
        elif arg1 is not None:
            if isinstance(arg1, np.ndarray):
                if not arg1.flags.c_contiguous:
                    raise ValueError("ndarray expected to be C contiguous")
                height, width = arg1.shape
                self.thisptr = new OMap(<int>width,<int>height)
                for y in range(height):
                    for x in range(width):
                        self.thisptr.grid[x][y] = <bool>arg1[y,x]
            else:
                self.thisptr = new OMap(arg1)
        else:
            print "Failed to construct PyOMap, check argument types."
            self.thisptr = new OMap(1,1)


    def __dealloc__(self):
        del self.thisptr

    cpdef bool save(self, string fn):
        return self.thisptr.save(fn)

    cpdef bool isOccupied(self, int x, int y):
        return self.thisptr.get(x, y)

    cpdef bool error(self):
        return self.thisptr.error()

    cpdef int width(self):
        return self.thisptr.width

    cpdef int height(self):
        return self.thisptr.height

cdef class PyBresenhamsLine:
    cdef BresenhamsLine *thisptr      # hold a C++ instance which we're wrapping
    def __cinit__(self, PyOMap Map, float max_range):
        self.thisptr = new BresenhamsLine(deref(Map.thisptr), max_range)
    def __dealloc__(self):
        del self.thisptr
    cpdef float calc_range(self, float x, float y, float heading):
        return self.thisptr.calc_range(x, y, heading)
    cpdef void calc_range_many(self,np.ndarray[float, ndim=2, mode="c"] ins, np.ndarray[float, ndim=1, mode="c"] outs):
        self.thisptr.numpy_calc_range(&ins[0,0], &outs[0], outs.shape[0])
    
    cpdef void calc_range_repeat_angles(self,np.ndarray[float, ndim=2, mode="c"] ins,np.ndarray[float, ndim=1, mode="c"] angles, np.ndarray[float, ndim=1, mode="c"] outs):
        self.thisptr.numpy_calc_range_angles(&ins[0,0], &angles[0], &outs[0], ins.shape[0], angles.shape[0])

    cpdef void calc_range_repeat_angles_eval_sensor_model(self,np.ndarray[float, ndim=2, mode="c"] ins,np.ndarray[float, ndim=1, mode="c"] angles, np.ndarray[float, ndim=1, mode="c"] obs, np.ndarray[double, ndim=1, mode="c"] weights):
        self.thisptr.calc_range_repeat_angles_eval_sensor_model(&ins[0,0], &angles[0], &obs[0],  &weights[0], ins.shape[0], angles.shape[0])

    cpdef float saveTrace(self, string path):
        self.thisptr.saveTrace(path)
    cpdef void eval_sensor_model(self, np.ndarray[float, ndim=1, mode="c"] observation, np.ndarray[float, ndim=1, mode="c"] ranges, np.ndarray[double, ndim=1, mode="c"] outs, int num_rays, int num_particles):
        self.thisptr.eval_sensor_model(&observation[0],&ranges[0], &outs[0], num_rays, num_particles)
    cpdef void set_sensor_model(self, np.ndarray[double, ndim=2, mode="c"] table):
        if not table.shape[0] == table.shape[1]:
            print "Sensor model must have equal matrix dimensions, failing!"
            return
        self.thisptr.set_sensor_model(&table[0,0], table.shape[0])

cdef class PyRayMarching:
    cdef RayMarching *thisptr      # hold a C++ instance which we're wrapping
    def __cinit__(self, PyOMap Map, float max_range):
        self.thisptr = new RayMarching(deref(Map.thisptr), max_range)
    def __dealloc__(self):
        del self.thisptr
    cpdef float calc_range(self, float x, float y, float heading):
        return self.thisptr.calc_range(x, y, heading)
    cpdef void calc_range_many(self,np.ndarray[float, ndim=2, mode="c"] ins, np.ndarray[float, ndim=1, mode="c"] outs):
        if outs.shape[0] != ins.shape[1]:
#            raise ValueError("in and out array must have same first dimension")
            pass
        self.thisptr.numpy_calc_range(&ins[0,0], &outs[0], outs.shape[0])
    cpdef float saveTrace(self, string path):
        self.thisptr.saveTrace(path)
    cpdef void calc_range_repeat_angles(self,np.ndarray[float, ndim=2, mode="c"] ins,np.ndarray[float, ndim=1, mode="c"] angles, np.ndarray[float, ndim=1, mode="c"] outs):
        self.thisptr.numpy_calc_range_angles(&ins[0,0], &angles[0], &outs[0], ins.shape[0], angles.shape[0])

    cpdef void calc_range_repeat_angles_eval_sensor_model(self,np.ndarray[float, ndim=2, mode="c"] ins,np.ndarray[float, ndim=1, mode="c"] angles, np.ndarray[float, ndim=1, mode="c"] obs, np.ndarray[double, ndim=1, mode="c"] weights):
        self.thisptr.calc_range_repeat_angles_eval_sensor_model(&ins[0,0], &angles[0], &obs[0],  &weights[0], ins.shape[0], angles.shape[0])

    cpdef void eval_sensor_model(self, np.ndarray[float, ndim=1, mode="c"] observation, np.ndarray[float, ndim=1, mode="c"] ranges, np.ndarray[double, ndim=1, mode="c"] outs, int num_rays, int num_particles):
        self.thisptr.eval_sensor_model(&observation[0],&ranges[0], &outs[0], num_rays, num_particles)
    cpdef void set_sensor_model(self, np.ndarray[double, ndim=2, mode="c"] table):
        if not table.shape[0] == table.shape[1]:
            print "Sensor model must have equal matrix dimensions, failing!"
            return
        self.thisptr.set_sensor_model(&table[0,0], table.shape[0])

    cpdef void get_dist(self, np.ndarray[float, ndim=2, mode="c"] distImage):
        self.thisptr.get_dist_image(&distImage[0,0], distImage.shape[0], distImage.shape[1])

cdef class PyCDDTCast:
    cdef CDDTCast *thisptr      # hold a C++ instance which we're wrapping
    cdef float max_range
    def __cinit__(self, PyOMap Map, float max_range, unsigned int theta_disc):
        self.max_range = max_range
        self.thisptr = new CDDTCast(deref(Map.thisptr), max_range, theta_disc)
    def __dealloc__(self):
        del self.thisptr
    cpdef void prune(self, float max_range=-1.0):
        if max_range < 0.0:
            self.thisptr.prune(self.max_range)
        else:
            self.thisptr.prune(max_range)
    cpdef float calc_range(self, float x, float y, float heading):
        return self.thisptr.calc_range(x, y, heading)
    cpdef void calc_range_many(self,np.ndarray[float, ndim=2, mode="c"] ins, np.ndarray[float, ndim=1, mode="c"] outs):
        self.thisptr.numpy_calc_range(&ins[0,0], &outs[0], outs.shape[0])

    cpdef void calc_range_repeat_angles_eval_sensor_model(self,np.ndarray[float, ndim=2, mode="c"] ins,np.ndarray[float, ndim=1, mode="c"] angles, np.ndarray[float, ndim=1, mode="c"] obs, np.ndarray[double, ndim=1, mode="c"] weights):
        self.thisptr.calc_range_repeat_angles_eval_sensor_model(&ins[0,0], &angles[0], &obs[0],  &weights[0], ins.shape[0], angles.shape[0])
    
    cpdef void calc_range_many_radial_optimized(self, int num_rays, float min_angle, float max_angle, np.ndarray[float, ndim=2, mode="c"] ins, np.ndarray[float, ndim=1, mode="c"] outs):
        # self.thisptr.calc_range_many_radial_optimized(num_rays, min_angle, max_angle, num_particles, &ins[0,0], &outs[0])
        self.thisptr.calc_range_many_radial_optimized(&ins[0,0], &outs[0], ins.shape[0], num_rays, min_angle, max_angle)

    cpdef void calc_range_repeat_angles(self,np.ndarray[float, ndim=2, mode="c"] ins,np.ndarray[float, ndim=1, mode="c"] angles, np.ndarray[float, ndim=1, mode="c"] outs):
        self.thisptr.numpy_calc_range_angles(&ins[0,0], &angles[0], &outs[0], ins.shape[0], angles.shape[0])
    
    cpdef void eval_sensor_model(self, np.ndarray[float, ndim=1, mode="c"] observation, np.ndarray[float, ndim=1, mode="c"] ranges, np.ndarray[double, ndim=1, mode="c"] outs, int num_rays, int num_particles):
        self.thisptr.eval_sensor_model(&observation[0],&ranges[0], &outs[0], num_rays, num_particles)
    cpdef void set_sensor_model(self, np.ndarray[double, ndim=2, mode="c"] table):
        if not table.shape[0] == table.shape[1]:
            print "Sensor model must have equal matrix dimensions, failing!"
            return
        self.thisptr.set_sensor_model(&table[0,0], table.shape[0])

cdef class PyGiantLUTCast:
    cdef GiantLUTCast *thisptr      # hold a C++ instance which we're wrapping
    def __cinit__(self, PyOMap Map, float max_range, unsigned int theta_disc):
        self.thisptr = new GiantLUTCast(deref(Map.thisptr), max_range, theta_disc)
    def __dealloc__(self):
        del self.thisptr
    cpdef float calc_range(self, float x, float y, float heading):
        return self.thisptr.calc_range(x, y, heading)
    cpdef void calc_range_many(self,np.ndarray[float, ndim=2, mode="c"] ins, np.ndarray[float, ndim=1, mode="c"] outs):
        self.thisptr.numpy_calc_range(&ins[0,0], &outs[0], outs.shape[0])
    
    cpdef void calc_range_repeat_angles(self,np.ndarray[float, ndim=2, mode="c"] ins,np.ndarray[float, ndim=1, mode="c"] angles, np.ndarray[float, ndim=1, mode="c"] outs):
        self.thisptr.numpy_calc_range_angles(&ins[0,0], &angles[0], &outs[0], ins.shape[0], angles.shape[0])

    cpdef void calc_range_repeat_angles_eval_sensor_model(self,np.ndarray[float, ndim=2, mode="c"] ins,np.ndarray[float, ndim=1, mode="c"] angles, np.ndarray[float, ndim=1, mode="c"] obs, np.ndarray[double, ndim=1, mode="c"] weights):
        self.thisptr.calc_range_repeat_angles_eval_sensor_model(&ins[0,0], &angles[0], &obs[0],  &weights[0], ins.shape[0], angles.shape[0])

    cpdef void eval_sensor_model(self, np.ndarray[float, ndim=1, mode="c"] observation, np.ndarray[float, ndim=1, mode="c"] ranges, np.ndarray[double, ndim=1, mode="c"] outs, int num_rays, int num_particles):
        self.thisptr.eval_sensor_model(&observation[0],&ranges[0], &outs[0], num_rays, num_particles)
    cpdef void set_sensor_model(self, np.ndarray[double, ndim=2, mode="c"] table):
        if not table.shape[0] == table.shape[1]:
            print "Sensor model must have equal matrix dimensions, failing!"
            return
        self.thisptr.set_sensor_model(&table[0,0], table.shape[0])

cdef class PyRayMarchingGPU:
    cdef RayMarchingGPU *thisptr      # hold a C++ instance which we're wrapping
    cdef float max_range
    def __cinit__(self, PyOMap Map, float max_range):
        if SHOULD_USE_CUDA == False:
            print "CANNOT USE RayMarchingGPU - must compile RangeLib with USE_CUDA=1"
            return
        self.max_range = max_range
        self.thisptr = new RayMarchingGPU(deref(Map.thisptr), max_range)
    def __dealloc__(self):
        del self.thisptr
    cpdef void calc_range_many(self,np.ndarray[float, ndim=2, mode="c"] ins, np.ndarray[float, ndim=1, mode="c"] outs):
#         self.thisptr.numpy_calc_range(&ins[0,0], &outs[0], outs.shape[0])
        self.thisptr.calc_range_many(&ins[0,0], &outs[0], outs.shape[0])

    cpdef void calc_range_repeat_angles(self,np.ndarray[float, ndim=2, mode="c"] ins,np.ndarray[float, ndim=1, mode="c"] angles, np.ndarray[float, ndim=1, mode="c"] outs):
        self.thisptr.numpy_calc_range_angles(&ins[0,0], &angles[0], &outs[0], ins.shape[0], angles.shape[0])

    cpdef void calc_range_repeat_angles_eval_sensor_model(self,np.ndarray[float, ndim=2, mode="c"] ins,np.ndarray[float, ndim=1, mode="c"] angles, np.ndarray[float, ndim=1, mode="c"] obs, np.ndarray[double, ndim=1, mode="c"] weights):
        self.thisptr.calc_range_repeat_angles_eval_sensor_model(&ins[0,0], &angles[0], &obs[0],  &weights[0], ins.shape[0], angles.shape[0])
    
    cpdef void eval_sensor_model(self, np.ndarray[float, ndim=1, mode="c"] observation, np.ndarray[float, ndim=1, mode="c"] ranges, np.ndarray[double, ndim=1, mode="c"] outs, int num_rays, int num_particles):
        self.thisptr.eval_sensor_model(&observation[0],&ranges[0], &outs[0], num_rays, num_particles)
    cpdef void set_sensor_model(self, np.ndarray[double, ndim=2, mode="c"] table):
        if not table.shape[0] == table.shape[1]:
            print "Sensor model must have equal matrix dimensions, failing!"
            return
        self.thisptr.set_sensor_model(&table[0,0], table.shape[0])

cdef class PyNull:
    def __cinit__(self, PyOMap Map, float max_range, unsigned int theta_disc):
        pass
    def __dealloc__(self):
        pass
    cpdef float calc_range(self, float x, float y, float heading):
        return x + y + heading
    cpdef void calc_range_many(self,np.ndarray[float, ndim=2, mode="c"] ins, np.ndarray[float, ndim=1, mode="c"] outs):
        a = ins[0,0]
        b = outs[0]
        c = outs.shape[0]
