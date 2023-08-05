
#ifndef HELICS_EXPORT_H
#define HELICS_EXPORT_H

#ifdef HELICS_STATIC_DEFINE
#  define HELICS_EXPORT
#  define HELICS_NO_EXPORT
#else
#  ifndef HELICS_EXPORT
#    ifdef helicsSharedLib_EXPORTS
        /* We are building this library */
#      define HELICS_EXPORT __declspec(dllexport)
#    else
        /* We are using this library */
#      define HELICS_EXPORT __declspec(dllimport)
#    endif
#  endif

#  ifndef HELICS_NO_EXPORT
#    define HELICS_NO_EXPORT 
#  endif
#endif

#ifndef HELICS_DEPRECATED
#  define HELICS_DEPRECATED __declspec(deprecated)
#endif

#ifndef HELICS_DEPRECATED_EXPORT
#  define HELICS_DEPRECATED_EXPORT HELICS_EXPORT HELICS_DEPRECATED
#endif

#ifndef HELICS_DEPRECATED_NO_EXPORT
#  define HELICS_DEPRECATED_NO_EXPORT HELICS_NO_EXPORT HELICS_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef HELICS_NO_DEPRECATED
#    define HELICS_NO_DEPRECATED
#  endif
#endif

#endif /* HELICS_EXPORT_H */
