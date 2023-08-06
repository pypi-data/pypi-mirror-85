#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/uint32.hpp>
#include <pythonic/include/types/int.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/types/uint32.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/include/builtins/getattr.hpp>
#include <pythonic/include/builtins/len.hpp>
#include <pythonic/include/builtins/list.hpp>
#include <pythonic/include/builtins/range.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/numpy/ndarray/reshape.hpp>
#include <pythonic/include/numpy/ravel.hpp>
#include <pythonic/include/numpy/square.hpp>
#include <pythonic/include/numpy/stack.hpp>
#include <pythonic/include/numpy/uint32.hpp>
#include <pythonic/include/numpy/zeros.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/iadd.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/operator_/neg.hpp>
#include <pythonic/include/operator_/sub.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/getattr.hpp>
#include <pythonic/builtins/len.hpp>
#include <pythonic/builtins/list.hpp>
#include <pythonic/builtins/range.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/numpy/ndarray/reshape.hpp>
#include <pythonic/numpy/ravel.hpp>
#include <pythonic/numpy/square.hpp>
#include <pythonic/numpy/stack.hpp>
#include <pythonic/numpy/uint32.hpp>
#include <pythonic/numpy/zeros.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/iadd.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/operator_/neg.hpp>
#include <pythonic/operator_/sub.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran_landscape
{
  struct __transonic__
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef pythonic::types::str __type0;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type0>()))>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct compute_adjacency_arr
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::ndarray::functor::reshape{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::stack{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type2;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type4;
      typedef long __type5;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::add(std::declval<__type4>(), std::declval<__type5>()))>::type __type6;
      typedef decltype(std::declval<__type3>()(std::declval<__type6>())) __type7;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::uint32{})>::type>::type __type8;
      typedef typename pythonic::assignable<decltype(std::declval<__type2>()(std::declval<__type7>(), std::declval<__type8>()))>::type __type9;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ravel{})>::type>::type __type10;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type11;
      typedef typename pythonic::assignable<decltype(std::declval<__type10>()(std::declval<__type11>()))>::type __type12;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type13;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type11>())) __type14;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type14>::type>::type>::type __type15;
      typedef decltype(pythonic::operator_::add(std::declval<__type15>(), std::declval<__type5>())) __type16;
      typedef decltype(pythonic::operator_::add(std::declval<__type16>(), std::declval<__type15>())) __type17;
      typedef decltype(pythonic::operator_::add(std::declval<__type17>(), std::declval<__type5>())) __type18;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::len{})>::type>::type __type19;
      typedef decltype(std::declval<__type19>()(std::declval<__type12>())) __type20;
      typedef decltype(pythonic::operator_::sub(std::declval<__type20>(), std::declval<__type16>())) __type21;
      typedef typename pythonic::lazy<__type21>::type __type22;
      typedef decltype(std::declval<__type13>()(std::declval<__type18>(), std::declval<__type22>())) __type23;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type23>::type::iterator>::value_type>::type __type24;
      typedef decltype(std::declval<__type12>()[std::declval<__type24>()]) __type25;
      typedef typename pythonic::lazy<__type25>::type __type26;
      typedef pythonic::types::list<typename std::remove_reference<__type5>::type> __type27;
      typedef typename pythonic::lazy<__type27>::type __type28;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type28>::type::iterator>::value_type>::type __type29;
      typedef decltype(pythonic::operator_::add(std::declval<__type24>(), std::declval<__type29>())) __type30;
      typedef decltype(std::declval<__type12>()[std::declval<__type30>()]) __type31;
      typedef decltype(pythonic::operator_::mul(std::declval<__type6>(), std::declval<__type31>())) __type32;
      typedef decltype(pythonic::operator_::add(std::declval<__type26>(), std::declval<__type32>())) __type33;
      typedef indexable<__type33> __type34;
      typedef typename __combined<__type9,__type34>::type __type35;
      typedef container<typename std::remove_reference<__type5>::type> __type36;
      typedef typename __combined<__type35,__type36>::type __type37;
      typedef pythonic::types::list<typename std::remove_reference<__type15>::type> __type38;
      typedef decltype(pythonic::operator_::neg(std::declval<__type15>())) __type39;
      typedef pythonic::types::list<typename std::remove_reference<__type39>::type> __type40;
      typedef typename __combined<__type38,__type40>::type __type41;
      typedef typename pythonic::lazy<__type41>::type __type42;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type42>::type::iterator>::value_type>::type __type43;
      typedef decltype(pythonic::operator_::add(std::declval<__type24>(), std::declval<__type43>())) __type44;
      typedef decltype(std::declval<__type12>()[std::declval<__type44>()]) __type45;
      typedef decltype(pythonic::operator_::mul(std::declval<__type6>(), std::declval<__type45>())) __type46;
      typedef decltype(pythonic::operator_::add(std::declval<__type26>(), std::declval<__type46>())) __type47;
      typedef indexable<__type47> __type48;
      typedef typename __combined<__type9,__type48>::type __type49;
      typedef typename __combined<__type49,__type36>::type __type50;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type37>(), std::declval<__type50>())) __type51;
      typedef decltype(std::declval<__type1>()(std::declval<__type51>())) __type52;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type5>(), std::declval<__type6>(), std::declval<__type6>())) __type53;
      typedef typename pythonic::returnable<decltype(std::declval<__type0>()(std::declval<__type52>(), std::declval<__type53>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& padded_arr, argument_type1&& num_classes) const
    ;
  }  ;
  typename __transonic__::type::result_type __transonic__::operator()() const
  {
    {
      static typename __transonic__::type::result_type tmp_global = pythonic::types::make_tuple(pythonic::types::str("0.4.5"));
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 >
  typename compute_adjacency_arr::type<argument_type0, argument_type1>::result_type compute_adjacency_arr::operator()(argument_type0&& padded_arr, argument_type1&& num_classes) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type2;
    typedef long __type3;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::add(std::declval<__type2>(), std::declval<__type3>()))>::type __type4;
    typedef decltype(std::declval<__type1>()(std::declval<__type4>())) __type5;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::uint32{})>::type>::type __type6;
    typedef typename pythonic::assignable<decltype(std::declval<__type0>()(std::declval<__type5>(), std::declval<__type6>()))>::type __type7;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ravel{})>::type>::type __type8;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type9;
    typedef typename pythonic::assignable<decltype(std::declval<__type8>()(std::declval<__type9>()))>::type __type10;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type11;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type9>())) __type12;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type12>::type>::type>::type __type13;
    typedef decltype(pythonic::operator_::add(std::declval<__type13>(), std::declval<__type3>())) __type14;
    typedef decltype(pythonic::operator_::add(std::declval<__type14>(), std::declval<__type13>())) __type15;
    typedef decltype(pythonic::operator_::add(std::declval<__type15>(), std::declval<__type3>())) __type16;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::len{})>::type>::type __type17;
    typedef decltype(std::declval<__type17>()(std::declval<__type10>())) __type18;
    typedef decltype(pythonic::operator_::sub(std::declval<__type18>(), std::declval<__type14>())) __type19;
    typedef typename pythonic::lazy<__type19>::type __type20;
    typedef decltype(std::declval<__type11>()(std::declval<__type16>(), std::declval<__type20>())) __type21;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type21>::type::iterator>::value_type>::type __type22;
    typedef decltype(std::declval<__type10>()[std::declval<__type22>()]) __type23;
    typedef typename pythonic::lazy<__type23>::type __type24;
    typedef pythonic::types::list<typename std::remove_reference<__type3>::type> __type25;
    typedef typename pythonic::lazy<__type25>::type __type26;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type26>::type::iterator>::value_type>::type __type27;
    typedef decltype(pythonic::operator_::add(std::declval<__type22>(), std::declval<__type27>())) __type28;
    typedef decltype(std::declval<__type10>()[std::declval<__type28>()]) __type29;
    typedef decltype(pythonic::operator_::mul(std::declval<__type4>(), std::declval<__type29>())) __type30;
    typedef decltype(pythonic::operator_::add(std::declval<__type24>(), std::declval<__type30>())) __type31;
    typedef indexable<__type31> __type32;
    typedef typename __combined<__type7,__type32>::type __type33;
    typedef typename __combined<__type33,__type32>::type __type34;
    typedef container<typename std::remove_reference<__type3>::type> __type35;
    typedef pythonic::types::list<typename std::remove_reference<__type13>::type> __type36;
    typedef decltype(pythonic::operator_::neg(std::declval<__type13>())) __type37;
    typedef pythonic::types::list<typename std::remove_reference<__type37>::type> __type38;
    typedef typename __combined<__type36,__type38>::type __type39;
    typedef typename pythonic::lazy<__type39>::type __type40;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type40>::type::iterator>::value_type>::type __type41;
    typedef decltype(pythonic::operator_::add(std::declval<__type22>(), std::declval<__type41>())) __type42;
    typedef decltype(std::declval<__type10>()[std::declval<__type42>()]) __type43;
    typedef decltype(pythonic::operator_::mul(std::declval<__type4>(), std::declval<__type43>())) __type44;
    typedef decltype(pythonic::operator_::add(std::declval<__type24>(), std::declval<__type44>())) __type45;
    typedef indexable<__type45> __type46;
    typedef typename __combined<__type7,__type46>::type __type47;
    typedef typename __combined<__type47,__type46>::type __type48;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type21>::type::iterator>::value_type>::type>::type i;
    typename pythonic::assignable<decltype(pythonic::operator_::add(num_classes, 1L))>::type num_cols_adjacency = pythonic::operator_::add(num_classes, 1L);
    typename pythonic::assignable<typename __combined<__type34,__type35>::type>::type horizontal_adjacency_arr = pythonic::numpy::functor::zeros{}(pythonic::numpy::functor::square{}(num_cols_adjacency), pythonic::numpy::functor::uint32{});
    typename pythonic::assignable<typename __combined<__type48,__type35>::type>::type vertical_adjacency_arr = pythonic::numpy::functor::zeros{}(pythonic::numpy::functor::square{}(num_cols_adjacency), pythonic::numpy::functor::uint32{});
    typename pythonic::assignable<typename __combined<__type13,__type41>::type>::type num_cols_pixel = std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, padded_arr));
    typename pythonic::assignable<decltype(pythonic::numpy::functor::ravel{}(padded_arr))>::type flat_arr = pythonic::numpy::functor::ravel{}(padded_arr);
    typename pythonic::lazy<decltype(typename pythonic::assignable<typename __combined<pythonic::types::list<typename std::remove_reference<long>::type>,pythonic::types::list<typename std::remove_reference<typename __combined<typename std::remove_cv<typename std::remove_reference<decltype(1L)>::type>::type,typename std::remove_cv<typename std::remove_reference<decltype(-1L)>::type>::type>::type>::type>>::type>::type({1L, -1L}))>::type horizontal_neighbours = typename pythonic::assignable<typename __combined<pythonic::types::list<typename std::remove_reference<long>::type>,pythonic::types::list<typename std::remove_reference<typename __combined<typename std::remove_cv<typename std::remove_reference<decltype(1L)>::type>::type,typename std::remove_cv<typename std::remove_reference<decltype(-1L)>::type>::type>::type>::type>>::type>::type({1L, -1L});
    typename pythonic::lazy<__type40>::type vertical_neighbours = typename pythonic::assignable<typename __combined<typename __combined<pythonic::types::list<typename std::remove_reference<typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>()))>::type>::type>::type>::type>,pythonic::types::list<typename std::remove_reference<decltype(pythonic::operator_::neg(std::declval<typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>()))>::type>::type>::type>()))>::type>>::type,pythonic::types::list<typename std::remove_reference<typename __combined<typename std::remove_cv<typename std::remove_reference<decltype(num_cols_pixel)>::type>::type,typename std::remove_cv<typename std::remove_reference<decltype(pythonic::operator_::neg(num_cols_pixel))>::type>::type>::type>::type>>::type>::type({num_cols_pixel, pythonic::operator_::neg(num_cols_pixel)});
    typename pythonic::lazy<decltype(pythonic::operator_::sub(pythonic::builtins::functor::len{}(flat_arr), pythonic::operator_::add(num_cols_pixel, 1L)))>::type end = pythonic::operator_::sub(pythonic::builtins::functor::len{}(flat_arr), pythonic::operator_::add(num_cols_pixel, 1L));
    {
      long  __target139628544900960 = end;
      for (long  i=pythonic::operator_::add(num_cols_pixel, 1L); i < __target139628544900960; i += 1L)
      {
        typename pythonic::lazy<decltype(flat_arr.fast(i))>::type class_i = flat_arr.fast(i);
        {
          for (auto&& neighbour: horizontal_neighbours)
          {
            horizontal_adjacency_arr[pythonic::operator_::add(class_i, pythonic::operator_::mul(num_cols_adjacency, flat_arr[pythonic::operator_::add(i, neighbour)]))] += 1L;
          }
        }
        {
          for (auto&& neighbour_: vertical_neighbours)
          {
            vertical_adjacency_arr[pythonic::operator_::add(class_i, pythonic::operator_::mul(num_cols_adjacency, flat_arr[pythonic::operator_::add(i, neighbour_)]))] += 1L;
          }
        }
      }
    }
    return pythonic::numpy::ndarray::functor::reshape{}(pythonic::numpy::functor::stack{}(pythonic::types::make_tuple(horizontal_adjacency_arr, vertical_adjacency_arr)), pythonic::types::make_tuple(2L, num_cols_adjacency, num_cols_adjacency));
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
static PyObject* __transonic__ = to_python(__pythran_landscape::__transonic__()());
typename __pythran_landscape::compute_adjacency_arr::type<pythonic::types::ndarray<npy_uint32,pythonic::types::pshape<long,long>>, long>::result_type compute_adjacency_arr0(pythonic::types::ndarray<npy_uint32,pythonic::types::pshape<long,long>>&& padded_arr, long&& num_classes) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_landscape::compute_adjacency_arr()(padded_arr, num_classes);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_landscape::compute_adjacency_arr::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<npy_uint32,pythonic::types::pshape<long,long>>>, long>::result_type compute_adjacency_arr1(pythonic::types::numpy_texpr<pythonic::types::ndarray<npy_uint32,pythonic::types::pshape<long,long>>>&& padded_arr, long&& num_classes) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_landscape::compute_adjacency_arr()(padded_arr, num_classes);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap_compute_adjacency_arr0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"padded_arr", "num_classes",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords , &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<npy_uint32,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]))
        return to_python(compute_adjacency_arr0(from_python<pythonic::types::ndarray<npy_uint32,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<long>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_adjacency_arr1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"padded_arr", "num_classes",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords , &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<npy_uint32,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<long>(args_obj[1]))
        return to_python(compute_adjacency_arr1(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<npy_uint32,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<long>(args_obj[1])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_compute_adjacency_arr(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_compute_adjacency_arr0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_adjacency_arr1(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "compute_adjacency_arr", "\n""    - compute_adjacency_arr(uint32[:,:], int)", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "compute_adjacency_arr",
    (PyCFunction)__pythran_wrapall_compute_adjacency_arr,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n""\n""    - compute_adjacency_arr(uint32[:,:], int)"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "landscape",            /* m_name */
    "",         /* m_doc */
    -1,                  /* m_size */
    Methods,             /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#define PYTHRAN_RETURN return theModule
#define PYTHRAN_MODULE_INIT(s) PyInit_##s
#else
#define PYTHRAN_RETURN return
#define PYTHRAN_MODULE_INIT(s) init##s
#endif
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(landscape)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
__attribute__ ((externally_visible))
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(landscape)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("landscape",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.9.7",
                                      "2020-11-12 19:16:46.012724",
                                      "7a0b9be65c2dac7f4b5e36d8ee98a83ca55f9cacfaacda2971a33d999bba4dba");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);

    PyModule_AddObject(theModule, "__transonic__", __transonic__);
    PYTHRAN_RETURN;
}

#endif