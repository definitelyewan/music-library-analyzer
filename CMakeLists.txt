cmake_minimum_required(VERSION 3.22.1)

project(toCSV VERSION 1.0.0.0)

add_subdirectory("ID3dev")
set(BUILD_SHARED_LIBS ON)
add_compile_options("-Wall")
#add_compile_options("-fsanitize=address")
add_compile_options("-g")
add_executable(toCSV "toCSV.c")
set_target_properties(toCSV PROPERTIES C_STANDARD 99)
target_link_libraries(toCSV PUBLIC Id3dev)



