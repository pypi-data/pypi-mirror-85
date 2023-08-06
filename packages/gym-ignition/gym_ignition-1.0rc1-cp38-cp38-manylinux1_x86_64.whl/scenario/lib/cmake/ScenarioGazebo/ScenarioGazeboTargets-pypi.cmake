#----------------------------------------------------------------
# Generated CMake target import file for configuration "PyPI".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ScenarioGazebo::ScenarioGazebo" for configuration "PyPI"
set_property(TARGET ScenarioGazebo::ScenarioGazebo APPEND PROPERTY IMPORTED_CONFIGURATIONS PYPI)
set_target_properties(ScenarioGazebo::ScenarioGazebo PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_PYPI "CXX"
  IMPORTED_LOCATION_PYPI "${_IMPORT_PREFIX}/lib/libScenarioGazebo.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS ScenarioGazebo::ScenarioGazebo )
list(APPEND _IMPORT_CHECK_FILES_FOR_ScenarioGazebo::ScenarioGazebo "${_IMPORT_PREFIX}/lib/libScenarioGazebo.a" )

# Import target "ScenarioGazebo::GazeboSimulator" for configuration "PyPI"
set_property(TARGET ScenarioGazebo::GazeboSimulator APPEND PROPERTY IMPORTED_CONFIGURATIONS PYPI)
set_target_properties(ScenarioGazebo::GazeboSimulator PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_PYPI "CXX"
  IMPORTED_LOCATION_PYPI "${_IMPORT_PREFIX}/lib/libGazeboSimulator.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS ScenarioGazebo::GazeboSimulator )
list(APPEND _IMPORT_CHECK_FILES_FOR_ScenarioGazebo::GazeboSimulator "${_IMPORT_PREFIX}/lib/libGazeboSimulator.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
