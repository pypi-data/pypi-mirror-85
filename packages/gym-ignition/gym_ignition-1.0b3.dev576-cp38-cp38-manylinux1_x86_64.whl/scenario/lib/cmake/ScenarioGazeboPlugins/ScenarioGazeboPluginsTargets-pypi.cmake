#----------------------------------------------------------------
# Generated CMake target import file for configuration "PyPI".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ScenarioGazeboPlugins::ECMSingleton" for configuration "PyPI"
set_property(TARGET ScenarioGazeboPlugins::ECMSingleton APPEND PROPERTY IMPORTED_CONFIGURATIONS PYPI)
set_target_properties(ScenarioGazeboPlugins::ECMSingleton PROPERTIES
  IMPORTED_LOCATION_PYPI "${_IMPORT_PREFIX}/lib/libECMSingleton.so"
  IMPORTED_SONAME_PYPI "libECMSingleton.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS ScenarioGazeboPlugins::ECMSingleton )
list(APPEND _IMPORT_CHECK_FILES_FOR_ScenarioGazeboPlugins::ECMSingleton "${_IMPORT_PREFIX}/lib/libECMSingleton.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
