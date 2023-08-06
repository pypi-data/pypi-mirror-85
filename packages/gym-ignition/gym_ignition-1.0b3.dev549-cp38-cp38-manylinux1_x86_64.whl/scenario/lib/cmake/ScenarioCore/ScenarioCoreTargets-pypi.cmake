#----------------------------------------------------------------
# Generated CMake target import file for configuration "PyPI".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ScenarioCore::CoreUtils" for configuration "PyPI"
set_property(TARGET ScenarioCore::CoreUtils APPEND PROPERTY IMPORTED_CONFIGURATIONS PYPI)
set_target_properties(ScenarioCore::CoreUtils PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_PYPI "CXX"
  IMPORTED_LOCATION_PYPI "${_IMPORT_PREFIX}/lib/libCoreUtils.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS ScenarioCore::CoreUtils )
list(APPEND _IMPORT_CHECK_FILES_FOR_ScenarioCore::CoreUtils "${_IMPORT_PREFIX}/lib/libCoreUtils.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
