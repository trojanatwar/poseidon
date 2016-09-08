/****************************************************
 * Modified by Andrea Pasciuta for Poseidon Browser *
 ****************************************************

https://github.com/aperezdc/webkit2gtk-python-webextension-example

pythonloader.c

The MIT License (MIT)

Copyright (C) 2015-2016 Adrian Perez <aperez@igalia.com>
Copyright (C) 2016 Nathan Hoad <nathan@getoffmalawn.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

********************************************************************************/

#include <webkit2/webkit-web-extension.h>
#include <pygobject.h>

#define py_auto __attribute__((cleanup(py_object_cleanup)))

static void
py_object_cleanup(void *ptr)
{
    PyObject **py_obj_location = ptr;
    if (py_obj_location) {
        Py_DECREF (*py_obj_location);
        *py_obj_location = NULL;
    }
}

G_MODULE_EXPORT void
webkit_web_extension_initialize_with_user_data (WebKitWebExtension *extension,
                                                GVariant           *user_data)
{

    Py_Initialize ();

#if PY_VERSION_HEX < 0x03000000
    const char *argv[] = { "", NULL };
#else
    wchar_t *argv[] = { L"", NULL };
#endif

    PySys_SetArgvEx (1, argv, 0);

    pygobject_init (-1, -1, -1);
    if (PyErr_Occurred ()) {
        g_warning ("Could not initialize PyGObject");
        return;
    }

    pyg_enable_threads ();
    PyEval_InitThreads ();
 
    PyObject *gi, *require_version, *args;

    gi = PyImport_ImportModule ("gi");
    if (!gi) {
      g_critical ("can't find gi");
    return;
    }

    require_version = PyObject_GetAttrString (gi, (char *) "require_version");
    args = PyTuple_Pack (2, PyUnicode_FromString ("WebKit2WebExtension"),
        PyUnicode_FromString ("4.0"));
    PyObject_CallObject (require_version, args);
    Py_DECREF (require_version);
    Py_DECREF (args);
    Py_DECREF (gi);

    PyObject py_auto *web_ext_module =
            PyImport_ImportModule ("gi.repository.WebKit2WebExtension");
    if (!web_ext_module) {
        if (PyErr_Occurred ()) {
            g_printerr ("Could not import gi.repository.WebKit2WebExtension: ");
            PyErr_Print ();
        } else {
            g_printerr ("Could not import gi.repository.WebKit2WebExtension"
                        " (no error given)\n");
        }
        return;
    }

    PyObject py_auto *py_filename = PyUnicode_FromString ("extension");

    PyObject py_auto *py_module = PyImport_Import (py_filename);
    if (!py_module) {
        g_warning ("Could not import '%s'", "extension");
        return;
    }

    PyObject py_auto *py_func = PyObject_GetAttrString (py_module, "initialize");

    if (!py_func) {
        g_warning ("Could not obtain '%s.initialize'", "extension");
        return;
    }

    if (!PyCallable_Check (py_func)) {
        g_warning ("Object '%s.initialize' is not callable", "extension");
        return;
    }

    PyObject py_auto *py_extension = pygobject_new (G_OBJECT (extension));
    PyObject py_auto *py_func_args = PyTuple_New (1);
    PyTuple_SetItem (py_func_args, 0, py_extension);
    PyObject py_auto *py_retval = PyObject_CallObject (py_func, py_func_args);

    if (!py_retval) {
        g_printerr ("Error calling '%s.initialize':\n", "extension");
        PyErr_Print ();
    }

}
