
#ifndef HELICS_EXPORT_H
#define HELICS_EXPORT_H

#ifdef HELICS_STATIC_DEFINE
#  define HELICS_EXPORT
#  define HELICS_NO_EXPORT
#else
#  ifndef HELICS_EXPORT
#    ifdef helicsSharedLib_EXPORTS
        /* We are building this library */
#      define HELICS_EXPORT __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define HELICS_EXPORT __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef HELICS_NO_EXPORT
#    define HELICS_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef HELICS_DEPRECATED
#  define HELICS_DEPRECATED __attribute__ ((__deprecated__))
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
