cmake_minimum_required(VERSION 3.0)

# Create main project.
project(python_gotm LANGUAGES Fortran)

# Specify position-independent code since we will build a shared library.
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if(MSVC)
  add_compile_options("/libs:static")
endif()

# Customize compiler flags
if(${CMAKE_Fortran_COMPILER_ID} STREQUAL "Intel")
  if(MSVC)
    set(CMAKE_Fortran_FLAGS_DEBUG "${CMAKE_Fortran_FLAGS_DEBUG} /Od")
  else()
    # Do not warn about Windows-specific export directives
    set (CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} -diag-disable 7841")
  endif()
endif()

# Include GOTM's CMakeLists.txt.
set(GOTM_EMBED_VERSION ON CACHE BOOL "Embed GOTM version information" FORCE)
find_path(GOTM_BASE src/gotm/gotm.F90 DOC "Path to GOTM source directory.")
add_subdirectory(${GOTM_BASE} gotm EXCLUDE_FROM_ALL)
mark_as_advanced(FORCE GOTM_EMBED_VERSION)

# Add Python-GOTM library
add_library(python_gotm SHARED
            python_gotm.F90
           )
if(MSVC)
  set_property(TARGET python_gotm PROPERTY LINK_FLAGS_DEBUG "/NODEFAULTLIB:\"libcmt\"")
endif()

# Link in GOTM itself
target_link_libraries(python_gotm PRIVATE gotm)

# Set include directories with header files (*.h)
set_property(TARGET python_gotm APPEND PROPERTY INCLUDE_DIRECTORIES "${GOTM_BASE}/include")

install(TARGETS python_gotm
  DESTINATION pygotm)
install(DIRECTORY pygotm.in/
  DESTINATION pygotm)
install(DIRECTORY ${GOTM_BASE}/schemas/
  DESTINATION pygotm/schemas)

