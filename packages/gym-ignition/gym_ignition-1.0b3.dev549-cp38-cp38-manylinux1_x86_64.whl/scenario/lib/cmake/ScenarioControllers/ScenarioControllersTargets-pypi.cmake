#----------------------------------------------------------------
# Generated CMake target import file for configuration "PyPI".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ScenarioControllers::ComputedTorqueFixedBase" for configuration "PyPI"
set_property(TARGET ScenarioControllers::ComputedTorqueFixedBase APPEND PROPERTY IMPORTED_CONFIGURATIONS PYPI)
set_target_properties(ScenarioControllers::ComputedTorqueFixedBase PROPERTIES
  IMPORTED_LOCATION_PYPI "${_IMPORT_PREFIX}/lib/libComputedTorqueFixedBase.so"
  IMPORTED_SONAME_PYPI "libComputedTorqueFixedBase.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS ScenarioControllers::ComputedTorqueFixedBase )
list(APPEND _IMPORT_CHECK_FILES_FOR_ScenarioControllers::ComputedTorqueFixedBase "${_IMPORT_PREFIX}/lib/libComputedTorqueFixedBase.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
