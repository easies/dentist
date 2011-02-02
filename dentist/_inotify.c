/* Generated by Pyrex 0.9.8.5 on Wed Aug 26 20:19:53 2009 */

#define PY_SSIZE_T_CLEAN
#include "Python.h"
#include "structmember.h"
#ifndef PY_LONG_LONG
  #define PY_LONG_LONG LONG_LONG
#endif
#if PY_VERSION_HEX < 0x02050000
  typedef int Py_ssize_t;
  #define PY_SSIZE_T_MAX INT_MAX
  #define PY_SSIZE_T_MIN INT_MIN
  #define PyInt_FromSsize_t(z) PyInt_FromLong(z)
  #define PyInt_AsSsize_t(o)	PyInt_AsLong(o)
#endif
#if !defined(WIN32) && !defined(MS_WINDOWS)
  #ifndef __stdcall
    #define __stdcall
  #endif
  #ifndef __cdecl
    #define __cdecl
  #endif
#endif
#ifdef __cplusplus
#define __PYX_EXTERN_C extern "C"
#else
#define __PYX_EXTERN_C extern
#endif
#include <math.h>
#include "unistd.h"
#include "sys/inotify.h"


typedef struct {PyObject **p; int i; char *s; long n;} __Pyx_StringTabEntry; /*proto*/

static PyObject *__pyx_m;
static PyObject *__pyx_b;
static int __pyx_lineno;
static char *__pyx_filename;
static char **__pyx_f;

static int __Pyx_InitStrings(__Pyx_StringTabEntry *t); /*proto*/

static void __Pyx_AddTraceback(char *funcname); /*proto*/

/* Declarations from dentist._inotify */


/* Declarations from implementation of dentist._inotify */


static char __pyx_k1[] = "IN_ACCESS";
static char __pyx_k2[] = "IN_MODIFY";
static char __pyx_k3[] = "IN_ATTRIB";
static char __pyx_k4[] = "IN_CLOSE_WRITE";
static char __pyx_k5[] = "IN_CLOSE_NOWRITE";
static char __pyx_k6[] = "IN_OPEN";
static char __pyx_k7[] = "IN_MOVED_FROM";
static char __pyx_k8[] = "IN_MOVED_TO";
static char __pyx_k9[] = "IN_CREATE";
static char __pyx_k10[] = "IN_DELETE";
static char __pyx_k11[] = "IN_DELETE_SELF";
static char __pyx_k12[] = "IN_MOVE_SELF";
static char __pyx_k13[] = "IN_UNMOUNT";
static char __pyx_k14[] = "IN_Q_OVERFLOW";
static char __pyx_k15[] = "IN_IGNORED";
static char __pyx_k16[] = "IN_CLOSE";
static char __pyx_k17[] = "IN_MOVE";
static char __pyx_k18[] = "IN_ONLYDIR";
static char __pyx_k19[] = "IN_DONT_FOLLOW";
static char __pyx_k20[] = "IN_MASK_ADD";
static char __pyx_k21[] = "IN_ISDIR";
static char __pyx_k22[] = "IN_ONESHOT";
static char __pyx_k23[] = "IN_ALL_EVENTS";

static PyObject *__pyx_n_IN_ACCESS;
static PyObject *__pyx_n_IN_ALL_EVENTS;
static PyObject *__pyx_n_IN_ATTRIB;
static PyObject *__pyx_n_IN_CLOSE;
static PyObject *__pyx_n_IN_CLOSE_NOWRITE;
static PyObject *__pyx_n_IN_CLOSE_WRITE;
static PyObject *__pyx_n_IN_CREATE;
static PyObject *__pyx_n_IN_DELETE;
static PyObject *__pyx_n_IN_DELETE_SELF;
static PyObject *__pyx_n_IN_DONT_FOLLOW;
static PyObject *__pyx_n_IN_IGNORED;
static PyObject *__pyx_n_IN_ISDIR;
static PyObject *__pyx_n_IN_MASK_ADD;
static PyObject *__pyx_n_IN_MODIFY;
static PyObject *__pyx_n_IN_MOVE;
static PyObject *__pyx_n_IN_MOVED_FROM;
static PyObject *__pyx_n_IN_MOVED_TO;
static PyObject *__pyx_n_IN_MOVE_SELF;
static PyObject *__pyx_n_IN_ONESHOT;
static PyObject *__pyx_n_IN_ONLYDIR;
static PyObject *__pyx_n_IN_OPEN;
static PyObject *__pyx_n_IN_Q_OVERFLOW;
static PyObject *__pyx_n_IN_UNMOUNT;


static __Pyx_StringTabEntry __pyx_string_tab[] = {
  {&__pyx_n_IN_ACCESS, 1, __pyx_k1, sizeof(__pyx_k1)},
  {&__pyx_n_IN_ALL_EVENTS, 1, __pyx_k23, sizeof(__pyx_k23)},
  {&__pyx_n_IN_ATTRIB, 1, __pyx_k3, sizeof(__pyx_k3)},
  {&__pyx_n_IN_CLOSE, 1, __pyx_k16, sizeof(__pyx_k16)},
  {&__pyx_n_IN_CLOSE_NOWRITE, 1, __pyx_k5, sizeof(__pyx_k5)},
  {&__pyx_n_IN_CLOSE_WRITE, 1, __pyx_k4, sizeof(__pyx_k4)},
  {&__pyx_n_IN_CREATE, 1, __pyx_k9, sizeof(__pyx_k9)},
  {&__pyx_n_IN_DELETE, 1, __pyx_k10, sizeof(__pyx_k10)},
  {&__pyx_n_IN_DELETE_SELF, 1, __pyx_k11, sizeof(__pyx_k11)},
  {&__pyx_n_IN_DONT_FOLLOW, 1, __pyx_k19, sizeof(__pyx_k19)},
  {&__pyx_n_IN_IGNORED, 1, __pyx_k15, sizeof(__pyx_k15)},
  {&__pyx_n_IN_ISDIR, 1, __pyx_k21, sizeof(__pyx_k21)},
  {&__pyx_n_IN_MASK_ADD, 1, __pyx_k20, sizeof(__pyx_k20)},
  {&__pyx_n_IN_MODIFY, 1, __pyx_k2, sizeof(__pyx_k2)},
  {&__pyx_n_IN_MOVE, 1, __pyx_k17, sizeof(__pyx_k17)},
  {&__pyx_n_IN_MOVED_FROM, 1, __pyx_k7, sizeof(__pyx_k7)},
  {&__pyx_n_IN_MOVED_TO, 1, __pyx_k8, sizeof(__pyx_k8)},
  {&__pyx_n_IN_MOVE_SELF, 1, __pyx_k12, sizeof(__pyx_k12)},
  {&__pyx_n_IN_ONESHOT, 1, __pyx_k22, sizeof(__pyx_k22)},
  {&__pyx_n_IN_ONLYDIR, 1, __pyx_k18, sizeof(__pyx_k18)},
  {&__pyx_n_IN_OPEN, 1, __pyx_k6, sizeof(__pyx_k6)},
  {&__pyx_n_IN_Q_OVERFLOW, 1, __pyx_k14, sizeof(__pyx_k14)},
  {&__pyx_n_IN_UNMOUNT, 1, __pyx_k13, sizeof(__pyx_k13)},
  {0, 0, 0, 0}
};



/* Implementation of dentist._inotify */

static PyObject *__pyx_f_7dentist_8_inotify_init(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static PyObject *__pyx_f_7dentist_8_inotify_init(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_r;
  PyObject *__pyx_1 = 0;
  static char *__pyx_argnames[] = {0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "", __pyx_argnames)) return 0;
  __pyx_1 = PyInt_FromLong(inotify_init()); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 59; goto __pyx_L1;}
  __pyx_r = __pyx_1;
  __pyx_1 = 0;
  goto __pyx_L0;

  __pyx_r = Py_None; Py_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  __Pyx_AddTraceback("dentist._inotify.init");
  __pyx_r = 0;
  __pyx_L0:;
  return __pyx_r;
}

static PyObject *__pyx_f_7dentist_8_inotify_add_watch(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static PyObject *__pyx_f_7dentist_8_inotify_add_watch(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_v_fd = 0;
  PyObject *__pyx_v_path = 0;
  PyObject *__pyx_v_mask = 0;
  PyObject *__pyx_r;
  int __pyx_1;
  char *__pyx_2;
  uint32_t __pyx_3;
  PyObject *__pyx_4 = 0;
  static char *__pyx_argnames[] = {"fd","path","mask",0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "OOO", __pyx_argnames, &__pyx_v_fd, &__pyx_v_path, &__pyx_v_mask)) return 0;
  Py_INCREF(__pyx_v_fd);
  Py_INCREF(__pyx_v_path);
  Py_INCREF(__pyx_v_mask);
  __pyx_1 = PyInt_AsLong(__pyx_v_fd); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 62; goto __pyx_L1;}
  __pyx_2 = PyString_AsString(__pyx_v_path); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 62; goto __pyx_L1;}
  __pyx_3 = PyInt_AsUnsignedLongMask(__pyx_v_mask); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 62; goto __pyx_L1;}
  __pyx_4 = PyInt_FromLong(inotify_add_watch(__pyx_1,__pyx_2,__pyx_3)); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 62; goto __pyx_L1;}
  __pyx_r = __pyx_4;
  __pyx_4 = 0;
  goto __pyx_L0;

  __pyx_r = Py_None; Py_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_4);
  __Pyx_AddTraceback("dentist._inotify.add_watch");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_fd);
  Py_DECREF(__pyx_v_path);
  Py_DECREF(__pyx_v_mask);
  return __pyx_r;
}

static PyObject *__pyx_f_7dentist_8_inotify_rm_watch(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static PyObject *__pyx_f_7dentist_8_inotify_rm_watch(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_v_fd = 0;
  PyObject *__pyx_v_wd = 0;
  PyObject *__pyx_r;
  int __pyx_1;
  uint32_t __pyx_2;
  PyObject *__pyx_3 = 0;
  static char *__pyx_argnames[] = {"fd","wd",0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "OO", __pyx_argnames, &__pyx_v_fd, &__pyx_v_wd)) return 0;
  Py_INCREF(__pyx_v_fd);
  Py_INCREF(__pyx_v_wd);
  __pyx_1 = PyInt_AsLong(__pyx_v_fd); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 65; goto __pyx_L1;}
  __pyx_2 = PyInt_AsUnsignedLongMask(__pyx_v_wd); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 65; goto __pyx_L1;}
  __pyx_3 = PyInt_FromLong(inotify_rm_watch(__pyx_1,__pyx_2)); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 65; goto __pyx_L1;}
  __pyx_r = __pyx_3;
  __pyx_3 = 0;
  goto __pyx_L0;

  __pyx_r = Py_None; Py_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_3);
  __Pyx_AddTraceback("dentist._inotify.rm_watch");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_fd);
  Py_DECREF(__pyx_v_wd);
  return __pyx_r;
}

static struct PyMethodDef __pyx_methods[] = {
  {"init", (PyCFunction)__pyx_f_7dentist_8_inotify_init, METH_VARARGS|METH_KEYWORDS, 0},
  {"add_watch", (PyCFunction)__pyx_f_7dentist_8_inotify_add_watch, METH_VARARGS|METH_KEYWORDS, 0},
  {"rm_watch", (PyCFunction)__pyx_f_7dentist_8_inotify_rm_watch, METH_VARARGS|METH_KEYWORDS, 0},
  {0, 0, 0, 0}
};

static void __pyx_init_filenames(void); /*proto*/

PyMODINIT_FUNC init_inotify(void); /*proto*/
PyMODINIT_FUNC init_inotify(void) {
  PyObject *__pyx_1 = 0;
  __pyx_init_filenames();
  __pyx_m = Py_InitModule4("_inotify", __pyx_methods, 0, 0, PYTHON_API_VERSION);
  if (!__pyx_m) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;};
  Py_INCREF(__pyx_m);
  __pyx_b = PyImport_AddModule("__builtin__");
  if (!__pyx_b) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;};
  if (PyObject_SetAttrString(__pyx_m, "__builtins__", __pyx_b) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;};
  if (__Pyx_InitStrings(__pyx_string_tab) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;};

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":34 */
  __pyx_1 = PyInt_FromLong(IN_ACCESS); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 34; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_ACCESS, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 34; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":35 */
  __pyx_1 = PyInt_FromLong(IN_MODIFY); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 35; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_MODIFY, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 35; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":36 */
  __pyx_1 = PyInt_FromLong(IN_ATTRIB); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 36; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_ATTRIB, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 36; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":37 */
  __pyx_1 = PyInt_FromLong(IN_CLOSE_WRITE); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 37; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_CLOSE_WRITE, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 37; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":38 */
  __pyx_1 = PyInt_FromLong(IN_CLOSE_NOWRITE); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 38; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_CLOSE_NOWRITE, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 38; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":39 */
  __pyx_1 = PyInt_FromLong(IN_OPEN); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 39; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_OPEN, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 39; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":40 */
  __pyx_1 = PyInt_FromLong(IN_MOVED_FROM); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 40; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_MOVED_FROM, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 40; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":41 */
  __pyx_1 = PyInt_FromLong(IN_MOVED_TO); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 41; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_MOVED_TO, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 41; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":42 */
  __pyx_1 = PyInt_FromLong(IN_CREATE); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 42; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_CREATE, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 42; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":43 */
  __pyx_1 = PyInt_FromLong(IN_DELETE); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 43; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_DELETE, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 43; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":44 */
  __pyx_1 = PyInt_FromLong(IN_DELETE_SELF); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 44; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_DELETE_SELF, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 44; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":45 */
  __pyx_1 = PyInt_FromLong(IN_MOVE_SELF); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 45; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_MOVE_SELF, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 45; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":46 */
  __pyx_1 = PyInt_FromLong(IN_UNMOUNT); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 46; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_UNMOUNT, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 46; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":47 */
  __pyx_1 = PyInt_FromLong(IN_Q_OVERFLOW); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 47; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_Q_OVERFLOW, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 47; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":48 */
  __pyx_1 = PyInt_FromLong(IN_IGNORED); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 48; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_IGNORED, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 48; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":49 */
  __pyx_1 = PyInt_FromLong(IN_CLOSE); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 49; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_CLOSE, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 49; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":50 */
  __pyx_1 = PyInt_FromLong(IN_MOVE); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 50; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_MOVE, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 50; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":51 */
  __pyx_1 = PyInt_FromLong(IN_ONLYDIR); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 51; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_ONLYDIR, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 51; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":52 */
  __pyx_1 = PyInt_FromLong(IN_DONT_FOLLOW); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 52; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_DONT_FOLLOW, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 52; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":53 */
  __pyx_1 = PyInt_FromLong(IN_MASK_ADD); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 53; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_MASK_ADD, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 53; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":54 */
  __pyx_1 = PyInt_FromLong(IN_ISDIR); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 54; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_ISDIR, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 54; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":55 */
  __pyx_1 = PyInt_FromLong(IN_ONESHOT); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 55; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_ONESHOT, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 55; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":56 */
  __pyx_1 = PyInt_FromLong(IN_ALL_EVENTS); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 56; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_IN_ALL_EVENTS, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 56; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/lee/p/dentist/src/dentist/_inotify.pyx":64 */
  return;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  __Pyx_AddTraceback("dentist._inotify");
}

static char *__pyx_filenames[] = {
  "_inotify.pyx",
};

/* Runtime support code */

static void __pyx_init_filenames(void) {
  __pyx_f = __pyx_filenames;
}

static int __Pyx_InitStrings(__Pyx_StringTabEntry *t) {
    while (t->p) {
        *t->p = PyString_FromStringAndSize(t->s, t->n - 1);
        if (!*t->p)
            return -1;
        if (t->i)
            PyString_InternInPlace(t->p);
        ++t;
    }
    return 0;
}

#include "compile.h"
#include "frameobject.h"
#include "traceback.h"

static void __Pyx_AddTraceback(char *funcname) {
    PyObject *py_srcfile = 0;
    PyObject *py_funcname = 0;
    PyObject *py_globals = 0;
    PyObject *empty_tuple = 0;
    PyObject *empty_string = 0;
    PyCodeObject *py_code = 0;
    PyFrameObject *py_frame = 0;
    
    py_srcfile = PyString_FromString(__pyx_filename);
    if (!py_srcfile) goto bad;
    py_funcname = PyString_FromString(funcname);
    if (!py_funcname) goto bad;
    py_globals = PyModule_GetDict(__pyx_m);
    if (!py_globals) goto bad;
    empty_tuple = PyTuple_New(0);
    if (!empty_tuple) goto bad;
    empty_string = PyString_FromString("");
    if (!empty_string) goto bad;
    py_code = PyCode_New(
        0,            /*int argcount,*/
        0,            /*int nlocals,*/
        0,            /*int stacksize,*/
        0,            /*int flags,*/
        empty_string, /*PyObject *code,*/
        empty_tuple,  /*PyObject *consts,*/
        empty_tuple,  /*PyObject *names,*/
        empty_tuple,  /*PyObject *varnames,*/
        empty_tuple,  /*PyObject *freevars,*/
        empty_tuple,  /*PyObject *cellvars,*/
        py_srcfile,   /*PyObject *filename,*/
        py_funcname,  /*PyObject *name,*/
        __pyx_lineno,   /*int firstlineno,*/
        empty_string  /*PyObject *lnotab*/
    );
    if (!py_code) goto bad;
    py_frame = PyFrame_New(
        PyThreadState_Get(), /*PyThreadState *tstate,*/
        py_code,             /*PyCodeObject *code,*/
        py_globals,          /*PyObject *globals,*/
        0                    /*PyObject *locals*/
    );
    if (!py_frame) goto bad;
    py_frame->f_lineno = __pyx_lineno;
    PyTraceBack_Here(py_frame);
bad:
    Py_XDECREF(py_srcfile);
    Py_XDECREF(py_funcname);
    Py_XDECREF(empty_tuple);
    Py_XDECREF(empty_string);
    Py_XDECREF(py_code);
    Py_XDECREF(py_frame);
}